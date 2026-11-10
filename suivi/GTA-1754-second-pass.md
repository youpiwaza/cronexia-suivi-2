# GTA-1754 / Conflits d'anomalies — détection et affichage / 2eme passe

Repasse finale sur les pages anomalies et synthèse, et sur la génération côté back (`feat-1754-fix-summary-error`, back : 12 commits / 45 fichiers, front : 2 commits / 20 fichiers). Les problèmes 9 et 10 sont corrigés dans le code. Les problèmes 11 à 13 restent à traiter, un plan par problème. Aucun test lancé (les tests se lancent à la main).

## Verdict sur les problèmes 1 à 8

- P1 (fin de conflit / hash) : correct. `conflictMultipleUnicityHash` utilise l'id de la ligne (`idEventByDay` / `idEventRangeByDay`), car `addManualEventToPile` n'écrase plus avec `eventId`. L'override `originalTimeEnd` a disparu : `closeAnomalyInstanceToGenerate` donne `min(fin pré-remplie, instant courant)`. Retirer puis ré-ajouter change le hash, le conflit est donc refermé.
- P2 (2+ saisies manuelles) : correct. `resolvingManualEventCoverage` prend l'union des saisies de même attendance dans la pile. Les neutres sont dans une autre pile. Un mélange absence / présence ne résout que par le bon type. `instanceof Date` est sûr : `convertToUnifiedTime` normalise en amont.
- P3 (morceaux partiels `treated`) : correct. La résolution complète écrit aussi sa ligne `treated` hors logs (problème 10, helper `buildResolvedAnomalyInstance`). Vérification manuelle pas lancée.
- P4 (une ligne par jour) : correct. `uniqueId` finit par le code d'anomalie : ABSINJ et chaque code de conflit ont leur propre ligne. `timelineAnomalyForDay` ne réunit que les lignes de chevauchement.
- P5 (régénération au changement de schedule) : surcharge validée OK. Changement de cycle corrigé dans le code (problème 9) : de l'`effectDate` la plus ancienne jusqu'à hier. Vérification manuelle pas lancée.
- P6 (résolues périmées) : logique correcte (`resolvedAnomalyInstanceIdsToDelete` : clé absente ou réémise ouverte = suppression, clé réémise `treated` / `acquitted` = conservée). Seule la génération crée des instances `counterId = null`, aucun autre producteur n'est touché.
- P7 : skipped, hors scope.
- P8 (théorique / réel par jour) : correct et cohérent des deux côtés. Le chargeur (`resources-theoretical-clockings-by-period-grouped-by-date.ts`) et le moteur (`isDayTheoreticalClockings`) lisent le même `resolveManagementModeByDate`. Retirer les dates vides est sans risque (`resource-merge-times-by-day.ts` retombe sur les plages de l'horaire).
- Identité de l'event (`is-overlap.ts` + `+server.ts` front) : cohérent. `idEvent`, puis `id`, puis `name`. Toute connexion par `code`, `labelShort` ou `labelLong` lève maintenant CRO_EROR_000000002. Plus aucun appelant front d'event-range-on-resource n'utilise `code` (seuls déclaratif et favoris, autres modèles). Côté back (`deferredErorCreate` des workflows, sync calendrier, resolver), les données viennent du front ou passent par des ids.

## Vérification de la gestion des conflits

- Ouverture / clôture : `CONFLIMLTP` se referme à l'instant courant quand la composition change. Quand la pile retombe à 0 ou 1, la clôture prend `min(instant, fin de la saisie restante)`. La clôture de fin de journée garde la fin pré-remplie. OK.
- `CONFLIEXCL` : évalué selon le mode du jour. Jour théorique avec pile homogène : jamais ouvert. Jour réel : comparé à la présence basculée par les pointages. OK.
- `CONFLIOVRL`, `CONFLIMLTP`, `CONFLIMLTPNEUTRE` : inchangés hors correctifs génériques. `isDayManagedByDays` ne coupe toujours que les sections horaires.
- Lignes résolues : P6 supprime les clés absentes ou rouvertes, garde les clés réémises `treated`, le dédoublonnage évite les doubles. Les morceaux partiels d'avant correctif, stockés `toBeTreated`, sont nettoyés à la prochaine génération (même clé, remplacés par le morceau `treated`).

## Problème 9 — un changement de cycle ne régénère qu'UN jour / ✅ Corrigé (code), tests manuels pas lancés

Fichiers :

- @cronexia-gta-back/app/src/resources/resources.service.ts vers 2216-2229
- @cronexia-gta-back/app/src/resources/functions/events/generate/cycle-generation-period.ts
- @cronexia-gta-back/app/src/resources/functions/events/generate/clamp-period-to-yesterday.ts
- @cronexia-gta-back/app/src/resources/functions/events/generate/queue/enqueue-event-generation-for-past-period.ts
- @cronexia-gta-back/app/src/resources/functions/events/generate/earliest-cycle-effect-date.ts

Avant correctif, `resources.service.ts` appelait `enqueueEventGenerationForPastPeriod` sans `dateEnd`. `clampPeriodToYesterday` retombait alors sur `dateEnd = dateStart`. Un cycle s'applique à partir de son `effectDate` et jusqu'au cycle suivant : seul le premier jour était régénéré. C'est le cas cycle du P5.

Correctif :

- `cycleGenerationPeriod` renvoie `{ dateStart: effectDate la plus ancienne, dateEnd: maintenant }`, ou `null` s'il n'y a pas d'`effectDate`.
- Après commit, `resources.service.ts` passe ces deux dates à `enqueueEventGenerationForPastPeriod`. Le clamp ramène la fin à hier. Une `effectDate` aujourd'hui ou dans le futur n'empile rien.
- Pas de plafond : un seul job, même si l'`effectDate` remonte à plusieurs années. `TODO(GTA-1754)` dans le helper : découper en jobs d'environ 31 jours pour ne pas bloquer un des 2 workers.
- Spec : `cycle-generation-period.spec.ts` (null, date passée, aujourd'hui ou futur). Pas lancée. Le clamp, `createJob` et `verifyPeriod` acceptent la période longue (pas de durée maximale).

## Problème 10 — la résolution complète n'écrit jamais sa ligne `treated` en production / ✅ Corrigé (code), tests manuels pas lancés

Fichiers :

- @cronexia-gta-back/app/src/resources/functions/events/generate/resources-generate-events-query-by-period.ts vers 2616
- @cronexia-gta-back/app/src/resources/functions/events/generate/functions/build-resolved-anomaly-instance.ts

Avant correctif, tout le bloc de résolution complète était sous `if (isFullyResolvedFromStart && isFullyResolvedToFinish && displayLogs)`. Le `&& displayLogs` vient d'un commit de lint (`d094674f`, 11 juin 2025) qui ne portait alors qu'un `console.log`. Le commit `b648653d` (24 juin 2025) a ajouté la création de la ligne `treated` dans ce même bloc : elle n'existait que si les logs étaient activés. Les morceaux partiels, eux, étaient toujours émis.

Décision : l'historique « Traité » des résolutions complètes est voulu, c'était l'intention de `b648653d`.

Correctif :

- Nouveau helper `buildResolvedAnomalyInstance` : clone de l'événement, `idEventByDay` vidé, heures reconverties, criticité lue dans la map, puis `createAnomalyInstanceToGenerate` et `markAnomalyInstanceResolved`. La source n'est pas modifiée.
- Les deux blocs partiels (début et fin) passent par ce helper, `partial: true`, avec les mêmes bornes qu'avant.
- Le bloc complet passe par le même helper, `partial: false`, sous `if (isFullyResolvedFromStart && isFullyResolvedToFinish)`. Le `console.log` reste sous `displayLogs`.
- Avec P6, la ligne a la même clé à chaque régénération : le dédoublonnage évite le doublon, et elle est supprimée si la saisie résolvante disparaît.
- Spec : `build-resolved-anomaly-instance.spec.ts` (complète, partielle, ids, heures en chaîne, source intacte, clé stable). Pas lancée.
- Reste le problème 11 : `treated` est posé sans validation de criticité. Les seeds sont en `error`, donc le cas ne se produit pas aujourd'hui.

## Problème 11 — le statut `treated` explicite ne respecte pas la criticité / 🟡 Moyen à bas

Fichiers :

- @cronexia-gta-back/app/src/anomaly-instances/functions/service/validate-or-set-anomaly-instance-status.ts
- @cronexia-gta-back/app/src/resources/functions/events/generate/functions/mark-anomaly-instance-resolved.ts
- @cronexia-gta-back/app/src/resources/functions/events/generate/resources-generate-events-by-period.ts vers 462-470

`validateOrSetAnomalyInstanceStatus` refuse `treated` sauf pour une criticité `error` (`warning` n'accepte que `toWatch`, `info` accepte `info` / `acquitted`). Les morceaux partiels portent désormais toujours `treated`, et l'étape 3 le faisait déjà pour les lignes disparues. Si un client baisse la criticité d'ABSINJ, de PNA ou d'un conflit, `createMany` lève une erreur. Elle tombe après la suppression des événements générés et des non résolues, sans transaction : la journée reste vidée.

Les seeds sont toutes en `error`, le risque dépend donc de la configuration.

Correctif proposé : choisir le statut selon la criticité dans `markAnomalyInstanceResolved` et à l'étape 3 (erreur : `treated`, info : `acquitted`, alerte : statut par défaut), ou englober suppression et création dans une seule transaction.

## Problème 12 — la page synthèse garde sa propre copie de l'agrégation / 🟠 Moyen

Fichiers :

- @cronexia-gta-front-v2/app/src/routes/(app)/(with-filters)/summary/population/[[population]]/resource/[[resource]]/dateStart/[[dateStart]]/dateEnd/[[dateEnd]]/+page.svelte vers 260-322
- @cronexia-gta-front-v2/app/src/routes/functions/cronexia/anomaly/aggregate-anomalies.ts
- @cronexia-gta-front-v2/app/src/routes/functions/cronexia/anomaly/aggregate-anomalies.spec.ts

La synthèse recopie `aggregateAnomalies` et a dérivé :

- Quand un « À traiter » existe le même jour, elle ne garde que les « À traiter ». Le helper partagé masque uniquement les « Traité ».
- `startNeutral` / `endNeutral` sont remplis même pour un conflit neutre traité. Le helper partagé les laisse vides.

La synthèse ne profite du changement d'`uniqueId` que parce que `transformAnomalies` est partagé. Un futur correctif d'affichage peut donc diverger à nouveau.

Correctif proposé :

- Confirmer avec le PO la règle de masquage voulue.
- Remplacer le bloc par `aggregateAnomalies(transformAnomalies(...))`.
- Étendre `aggregate-anomalies.spec.ts` aux cas de masquage.

## Problème 13 — points mineurs et suites / 🟢 Bas

À regrouper dans un seul plan, ou à traiter au cas par cas.

- Concurrence : la génération supprime puis crée sans transaction, et la file lance 2 jobs en parallèle sans sérialisation par ressource. Les nouveaux empilements automatiques (édition de cycle, surcharge validée) augmentent le risque de deux exécutions sur la même ressource (doublons). Piste : verrou par ressource ou `jobId` par ressource (@cronexia-gta-back/app/src/resources/functions/events/generate/queue/event-generation-queue.service.ts, processor).
- Un changement antidaté du mode de gestion (`resourceTimeManagementMethod`) ou de `inDate` via `resource.update` ne relance pas la génération, alors que P8 dépend désormais de cet historique. `collectTouchedHistorisedFields` existe déjà et pourrait servir de déclencheur (@cronexia-gta-back/app/src/resources/resources.service.ts vers 2182-2200).
- Conflit neutre (`CONFLIMLTPNEUTRE`) avec 3 événements ou plus du même code : corrigé (code), vérification manuelle pas lancée. Un conflit par composition, clôturé à l'instant du changement. La fin pré-remplie est la plus tôt des fins de ce code (`reconcileNeutralConflicts`). Spec `reconcile-neutral-conflicts.spec.ts` : 8 tests, passés. Seeds à rejouer sur 777777C : 16/04 escalier (conflits 14h-15h, 15h-16h, 16h-17h) et 17/04 adjacents (14h-15h, 15h-16h), dans @cronexia-gta-back/app/src/resources/functions/tests/add-neutral-events.ts. Le 15/04, `AUTR_NEUTRE` passe de 15h00 à 15h30.
- UX : `CONFLIEXCL`, `CONFLIOVRL` et `CONFLIMLTP` ont le même libellé « Conflit chevauchement ». Avec les lignes par code, deux lignes d'allure identique peuvent apparaître le même jour (seule la description diffère).
- Commentaires périmés : TODO(GTA-1451) dans @cronexia-gta-back/app/src/resources/functions/events/times/resource-merge-times-by-day.ts vers 424, et ids de fixtures sans suffixe de code dans `updated-anomalies-override.test.ts` (sans effet).
- Rien à faire : le chargeur de pointages réels a le même préfiltre `some` que l'ancien chargeur théorique, mais les pointages réels ne s'écrivent pas hors d'un jour en mode réel (contraintes d'écriture des pointages).

## Problème 14 — synthèse : clé `uniqueID` dupliquée, page blanche / 🔴 Haut

✅ Corrigé (code), test manuel pas lancé.

Symptôme : erreur Svelte `each_key_duplicate` dans `SummaryArray.svelte` (clé `idResource-date` en double), la synthèse ne s'affiche plus dès qu'un jour sans pointage compte plusieurs lignes d'anomalies (ex. ABSINJ + conflit).

Cause : dans la page synthèse, le bloc « anomalies sans ligne » filtrait sur `existingKeys` avant d'y ajouter les clés. Chaque ligne d'anomalie agrégée du même jour (une par code / statut / criticité) passait le filtre et créait une ligne de synthèse. Bug ancien (commit 69b6d72fa), révélé par les lignes multiples par jour.

Correctif : helper pur `rowsForAnomaliesWithoutRow` (@cronexia-gta-front-v2/app/src/routes/functions/cronexia/anomaly/rows-for-anomalies-without-row.ts), qui ajoute la clé au fil de l'eau comme le fait déjà le bloc des plannings. Spec : `rows-for-anomalies-without-row.spec.ts`.

## Ordre conseillé

0. P14 : fait dans le code. Reste la vérification manuelle (priorité, la synthèse plante).
1. P9 : fait dans le code. Reste la vérification manuelle.
2. P10 : fait dans le code. Reste la vérification manuelle.
3. P12 : après décision PO sur la règle de masquage.
4. P11 : dépend de la configuration des criticités.
5. P13 : au fil de l'eau.

## Vérification manuelle

À lancer à la main.

1. Tests back touchés par la branche : is-overlap, resources-theoretical-clockings-by-period-grouped-by-date, clamp-period-to-yesterday, earliest-cycle-effect-date, cycle-generation-period, add-manual-event-to-pile, close-anomaly-instance-to-generate, conflict-multiple-unicity-hash, mark-anomaly-instance-resolved, build-resolved-anomaly-instance, resolve-anomaly-against-coverage, resolved-anomaly-instance-ids-to-delete, resolving-manual-event-coverage, enqueue-event-generation-for-past-period, schedule-overload-generation-period, user-profile-instance-update-wrls-status-with-cascade, et le test du mode de gestion théorique. Front : aggregate-anomalies, rows-for-anomalies-without-row, check-timeline-event-conflicts, scan-planning-draft-conflicts.
2. Démarrer le back une fois : le câblage `forwardRef` de `EventGenerationQueueModule` dans `ResourcesModule` et `UserProfileInstancesModule` est nouveau.
3. Scénarios. Le moteur de 3000 lignes n'a pas de test d'intégration, seulement des tests sur les helpers.
   - a. Deux absences qui se chevauchent, puis une troisième ajoutée, retirée, ré-ajoutée.
   - b. ABSINJ 14:00-16:30 avec VMED 15:00-15:30 et une seconde absence qui chevauche.
   - c. Ressource qui passe de théorique à réel en cours de période, avec une saisie de chaque côté.
   - d. Surcharge d'horaire sur un jour passé, puis changement de cycle antidaté de plusieurs jours (vérifie P9).
   - e. Synthèse et anomalies affichent les mêmes lignes pour les mêmes données (vérifie P12).
