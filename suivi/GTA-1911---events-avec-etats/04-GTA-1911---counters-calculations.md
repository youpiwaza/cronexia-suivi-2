# GTA-1911 / Calculs des compteurs selon l'état des events

Découpe de [01-GTA-1911---ticket-de-base.md](01-GTA-1911---ticket-de-base.md), lignes « calculs de compteurs » (Annulé / Brouillon / Refusé extraits vers GTA-1915, A valider sans impact, ⏱️ 0,25 j).

Un compteur lit un event seulement s'il n'a pas de workflow, ou si sa demande est à l'état Validé. A valider ne compte pas, y compris dans le prévisionnel. La règle vit dans le moteur de calcul. Une formule qui passe un état en paramètre (`VALEUR_EVENT_ETAT`, `SOMME_ANNEE_ETAT`) continue de lire cet état : c'est le seul moyen de compter autre chose que Validé, et le choix des formules reste de la configuration.

Hors de ce ticket : configuration et base des compteurs ([GTA-1915](https://cronexia.atlassian.net/jira/browse/GTA-1915)), génération des anomalies ([02-GTA-1911---anomaly-generation.md](02-GTA-1911---anomaly-generation.md)), conflits à la saisie ([03-GTA-1911---conflicts-generation-and-management.md](03-GTA-1911---conflicts-generation-and-management.md)), affichage des états dans le front.

Estimation proposée : ⏱️ ~1 j (le 0,25 j du ticket de base ne couvre que « A valider sans impact »). À confirmer après les questions PO en fin de ticket.

À la clôture de ce ticket, poster le commentaire Jira décrit dans « À faire en clôture ». Le prévisionnel change de sens, et les deux sources de soldes divergent jusqu'à GTA-1915.

---

## Règle cible

`WorkflowStateEnum` dans `cronexia-gta-back\app\prisma\schema\workflow.prisma`.

| État | Lecture par défaut du moteur | Solde à date | Solde prévisionnel |
| --- | --- | --- | --- |
| Pas de workflow (`workflowResourceId` null, saisie admin / gestionnaire) | Compte | Compte | Compte |
| `validated` — Validé | Compte | Compte | Compte |
| `pending` — A valider | Ignoré | Ignoré | Ignoré |
| `awaitingAttachements` — En attente de justificatif | Ignoré (hypothèse, à confirmer PO) | Ignoré | Ignoré |
| `draft` — Brouillon | Ignoré | Ignoré | Ignoré |
| `refused` — Refusé | Ignoré | Ignoré | Ignoré |
| `cancelled` — Annulé | Ignoré | Ignoré | Ignoré |

Même règle pour une absence en jours (`EventRangeOnResource`) et une absence en heures (`EventByDay`). Côté heures, l'état est porté par la déclaration (`EventByDay → DeclarationHourly → Declaration → WorkflowResource`), comme dans le ticket 02. Un event en heures sans déclaration compte. Les écarts ADEC / PDEC d'une déclaration ne comptent qu'une fois la déclaration validée.

Le prévisionnel et le solde à date lisent les mêmes états. Ils ne diffèrent plus que par la période : à date s'arrête à aujourd'hui, prévisionnel couvre toute la période demandée (donc les absences Validées futures).

Un second paramètre d'état explicite sur `VALEUR_EVENT_ETAT` / `SOMME_ANNEE_ETAT` reste prioritaire sur cette règle. `null` continue de vouloir dire « saisie directe seulement ».

---

## État des lieux

Le moteur n'a plus de filtre d'état par défaut. `dc261321` (19/05/2026) ne comptait les `EventRangeOnResource` que sans workflow ou `validated`. `c8340d99` (28/05/2026) a commenté ce filtre dans `02-get-resources-with-mixed-events.ts` : le filtrage a été délégué aux paramètres de `VALEUR_EVENT_ETAT` et `SOMME_ANNEE_ETAT`. Les events en heures n'ont jamais eu ce filtre.

Conséquence : un paramètre `Event` nu, ou une `EventsAggregation`, relit tous les états. Brouillon, A valider, Refusé, Annulé et En attente de justificatif comptent. C'est le KO du ticket de base, pour les trois états « à ignorer » comme pour A valider.

Trois lectures, trois règles :

- `getResourcesWithMixedEvents` : aucun filtre. Alimente le paramètre `Event` et les agrégations, jours et heures. La branche « restriction horaire » pose un `OR` sur le `where` des events en heures.
- `SOMME_ANNEE` dans `ct-counters.service.ts` : les jours sont déjà « sans workflow ou `validated` ». Les heures (`eventByDay.findMany`) n'ont pas de filtre d'état.
- `SOMME_ANNEE_ETAT` et `VALEUR_EVENT_ETAT` : sans second paramètre, le préchargement ne filtre rien (tous les états, y compris Refusé). Avec un état, filtre exact. Avec `valueStr: null`, saisie directe. Ces deux préchargements ne lisent que `eventRangeByDay`. Un event en heures est invisible pour elles.

Le helper du ticket 02, `build-counted-workflow-state-where.ts`, est encore une liste noire (`draft`, `refused`, `cancelled`). `pending` et `awaitingAttachements` passent. Ce ticket ne l'appelle pas en l'état. Il s'aligne sur la cible du ticket 02 : sans workflow, ou `validated`.

Somme de quantités, hors formules de compteurs. `buildEventRangeOnResourceWhereForQuantitySum` dans `resources.service.ts` :

- `toDate` (pris à date) : sans workflow, ou `validated`. Déjà conforme.
- `forecast` (pris prévisionnel) : sans workflow, ou `validated` ou `pending`. `draft`, `refused`, `cancelled`, `awaitingAttachements` sont déjà exclus. `pending` est l'exception en dur à retirer.

Cette somme alimente les soldes affichés « sans compteurs » et le contrôle de droits. Le contrôle (`guardWorkflowResourceEventRightsBalance`, `CRO_WR_000000024`) lit `totalQuantity`, donc le prévisionnel. Il est appelé à la création de demande (`workflow-resources.resolver.ts`), à la soumission (`resources-submit-workflow-resource.ts`) et à la mise à jour de la plage (`guard-workflow-resource-event-rights-on-event-range-update.ts`). La validation d'un niveau (`userProfileInstanceUpdateWrlsStatusWithCascade`) ne le rappelle pas. `isWorkflowStateInEventRightsForecast` retire du pris la quantité de la demande en cours quand elle est `pending` ou `validated`, pour ne pas la compter deux fois. Les deux listes (`pending` dans la somme, `pending` dans ce retrait) bougent ensemble.

Recalcul déjà empilé, rien à ajouter pour un passage qui ne franchit pas Validé :

- Entrée dans Validé : validation (`recalculateCountersAfterWrStateChange`, qui sort tout de suite si l'état reste `pending`), soumission sans valideur, création déjà validée.
- Sortie : refus, auto-refus délai de pièces jointes, annulation / suppression (`recalculateCountersAfterWrCancel`).
- Saisie directe sans workflow : `enqueueCounterRecalcForDirectEror`.

Brouillon → A valider n'empile rien. Avec la règle stricte, les deux états sont ignorés : pas d'empilement à ajouter.

Les formules seedées CP / RTT / TT (`counter-conges-CP.seed.ts`, `counter-conges-RTT.seed.ts`, `counter-conges-TT.seed.ts`) n'utilisent pas le paramètre nu. `*PD` (pris à date) somme saisie directe + `validated`. `*PA` (prévisionnel : CPPA, RTTPA, TTPA) ajoute un `SOMME_ANNEE_ETAT(..., pending)`. Ces seeds sont GTA-1915. Tant qu'ils ne bougent pas, les compteurs `*PA` continuent de compter A valider.

Les compteurs qui passent par le moteur sans état explicite, et dont les résultats stockés (`ctResultFlt*`) peuvent changer :

- Recommandé : `PVA`, agrégation `GROUPE_TT` (HS, PNA, PN, DEL, VMED). Events générés pour l'essentiel, peu de demandes workflow.
- Démo : `PVAJ`, agrégation `ABS_JUSTIFIEES` (MAL + CP + RTT). Une demande CP ou RTT non validée compte encore dans ce solde. `cronexia-gta-back\app\prisma\seeds-new\25-demo\counter\counter-presence-jour.demo.seed.ts` (doublon `26-demo-arte`).

Les CPT13 à CPT17 (paramètre `Event` nu ou agrégation) sont commentés dans `seed-po.ts`. Ils ne sont pas en base via ce seed.

---

## Ce qu'il convient de faire

### 1. Une liste blanche partagée, jours et heures

Même cible que le ticket 02. Réutiliser `buildCountedWorkflowStateWhere` et `buildCountedDeclarationEventByDayWhere` une fois qu'ils valent « sans workflow, ou `validated` ».

Si le ticket 02 n'est pas livré : poser cette liste blanche ici, et ne pas appeler le `notIn [draft, refused, cancelled]` actuel, qui laisse passer A valider. Le ticket 02 s'alignera sur la même fonction.

Events en heures : `buildCountedDeclarationEventByDayWhere`. Pas de `workflowResourceId` sur `EventByDay`.

### 2. L'appliquer à la lecture du moteur

Dans `02-get-resources-with-mixed-events.ts`, remettre le filtre sur `eventRangeOnResources` (le bloc commenté par `c8340d99` devient la liste blanche) et le poser sur `eventByDays`.

Point d'attention, branche restriction horaire : le code efface le filtre `eventId` et écrit `where.OR` avec une clause par event. Prisma croise les clés sœurs par ET. Le filtre d'état se pose à côté de ce `OR`, pas à l'intérieur d'une seule branche. Un event en heures sans déclaration (`declarationHourlyId` null) continue de compter.

### 3. `SOMME_ANNEE` et les fonctions `_ETAT` sans état

Dans `ct-counters.service.ts` :

- `SOMME_ANNEE`, requête `eventByDay` : même liste blanche que les jours. Les jours sont déjà conformes.
- `SOMME_ANNEE_ETAT` et `VALEUR_EVENT_ETAT`, quand le second paramètre est absent (`state === undefined`, clé `__all__`) : remplacer le filtre vide par la liste blanche. Un état explicite, et le `null` « saisie directe », ne changent pas.

Mettre à jour les libellés qui disent « sans 2e paramètre : tous les events » :

- `cronexia-gta-back\app\src\_utility\functions\function-definition.ts` (`VALEUR_EVENT_ETAT`, `SOMME_ANNEE_ETAT`)
- les commentaires de `cronexia-gta-back\app\src\ct-counters\functions\manage\function.ts`

Nouveau libellé : sans second paramètre, sans workflow ou Validé. Avec second paramètre, l'état demandé.

Les préchargements `_ETAT` ne lisent toujours pas les events en heures. Limite connue, pas un développement de ce ticket.

### 4. Retirer l'exception A valider du prévisionnel, et laisser un TODO

Commenter le `pending` en dur, ne pas l'effacer, et poser un `// TODO:` : rétablir le choix des états comptés quand les états d'events seront disponibles en paramètres dynamiques (GTA-1915).

Deux endroits, le même commentaire :

- `buildEventRangeOnResourceWhereForQuantitySum`, branche `forecast`, dans `resources.service.ts`. Après coup, `forecast` et `toDate` lisent les mêmes états. Le commentaire au-dessus des agrégats (lignes « prévisionnel : validated, pending ») suit.
- `isWorkflowStateInEventRightsForecast` dans `resolve-workflow-resource-event-rights-guard-context.ts`. Si on retire `pending` de la somme et qu'on le laisse dans ce retrait, une demande A valider en cours d'édition soustrait une quantité que la somme ne contient plus : le solde gonfle.

Aligner les textes qui disent encore « validated ou pending » :

- `cronexia-gta-back\app\src\resources\models\resource-event-quantity-sum-event.model.ts` (`totalQuantity`, `totalDuration`)
- `cronexia-gta-back\app\src\resources\docs\resources-event-quantity-sum-by-period.doc.ts`
- `cronexia-gta-front-v2\app\src\config\events\resources-events-quantity-sum-config.ts`
- `cronexia-gta-front-v2\app\src\routes\functions\cronexia\soldes-conges\build-soldes-conges-from-quantity-sums.ts` (en-tête)
- `cronexia-gta-front-v2\app\src\routes\api\chatbot\_functions\cronexia-gateway.ts` (`readBalances` : le commentaire dit que le chat annonce le même prévisionnel que la page « Mes droits », validés et en attente)

`totalQuantityToDate` ne change pas.

### 5. Résultats déjà stockés

Relancer le calcul des compteurs qui lisent un event ou une agrégation sans état explicite, pour réécrire les `ctResultFlt*`. Cible connue : `PVA`, et `PVAJ` là où le seed démo est chargé. Les compteurs `*PD` / `*PA` / `*SD` / `*SP` ne changent pas par ce filtre : leurs formules portent l'état. `*PA` continue de compter A valider jusqu'à GTA-1915.

---

## Inventaire des impacts

### Fichiers dont le résultat change

- `cronexia-gta-back\app\src\ct-counters\functions\histo\04-events\02-get-resources-with-mixed-events.ts`
- `cronexia-gta-back\app\src\ct-counters\ct-counters.service.ts` (préchargements `SOMME_ANNEE` heures, `_ETAT` sans état)
- `cronexia-gta-back\app\src\resources\resources.service.ts` (`buildEventRangeOnResourceWhereForQuantitySum`, mode `forecast`)
- `cronexia-gta-back\app\src\workflow-resources\functions\resolve-workflow-resource-event-rights-guard-context.ts`

Chaîne qui hérite de la lecture moteur : `resources-values.ts` → `getResourcesWithMixedEvents` → `merge-mixed-events.ts` → déroulé dans `ct-counters.service.ts`. Tout compteur à paramètre `Event` nu ou `EventsAggregation` reçoit moins d'events.

La somme de quantités (`resourcesEventQuantitySumByPeriod`) change sur `totalQuantity` et `totalDuration`. `totalQuantityToDate` reste identique.

### Effets métier attendus

Soldes « sans compteurs », via `build-soldes-conges-from-quantity-sums.ts` et `page.data.resourcesEventsQuantitySums`. Le pris prévisionnel baisse des demandes A valider. Le pris à date ne bouge pas.

Écrans sur cette source (`SoldesCongesSourceLazy` avec `source="quantity-sums"`, ou appel direct) :

- Accueil collaborateur : `HomeEmployee.svelte` (`WidgetMesDroits`, `WidgetSoldesConges`)
- Calendrier annuel : `PersonalCalendarPage.svelte`, `CalendarSidebar.svelte`
- Modale d'absence et fiche de demande : `AbsencesWorkflowModal.svelte`, `WorkflowDemandDetailsCard.svelte`
- Chatbot : `cronexia-gateway.ts` (`readBalances`), puis `chatbot-balance-soldes.ts`
- Discussion IA : `AiPathRightsHowMany.svelte`, `AiPathDemandValidate.svelte`, `resolve-rights-query.ts`, `build-rights-human-string.ts`

Contrôle de droits (`CRO_WR_000000024`), à la création, à la soumission et à la mise à jour de la plage. Une demande A valider déjà posée ne réduit plus le solde prévisionnel. Un collaborateur peut empiler des demandes A valider au-delà de ses droits. La validation ne refait pas ce contrôle : elle ne rattrape pas l'empilement. C'est le comportement demandé (A valider sans impact) ; la question PO dit s'il est acceptable en attendant les paramètres dynamiques.

Compteurs à agrégation : `PVAJ` (démo) ne compte plus un CP / RTT / MAL non validé. `PVA` bouge seulement si un event de `GROUPE_TT` est porté par une demande non validée.

### Déjà conforme, à ne pas retoucher

- `SOMME_ANNEE` sur les events en jours : déjà « sans workflow ou `validated` ».
- Solde à date de la somme de quantités (`toDate`).
- `*PD` (CPPD, RTTPD, TTPD) : `VALEUR_EVENT_ETAT` saisie directe + `validated`.
- Déclencheurs de recalcul listés plus haut. Pas de nouvel empilement pour Brouillon → A valider.
- Appels `_ETAT` avec un état explicite, y compris `pending` dans CPPA / RTTPA / TTPA. Ils restent vrais jusqu'à GTA-1915, et c'est voulu dans ce ticket.

### Hors impact

- Seeds de formules, codes de compteurs en dur (`get-counter-codes-for-event-name.ts`, TT / CP / RTT seulement), écran d'admin des compteurs. GTA-1915.
- Page « Mes droits & soldes » : `vacation-rights\+page.svelte` charge `SoldesCongesSourceLazy` avec `source="counters"` (`/api/counters/soldes-conges`, compteurs CPPA / RTTPA / TTPA). Elle continue de compter A valider. C'est la divergence à signaler en clôture, pas un oubli de ce ticket.
- Générateur d'anomalies et fonction `ANOMALY` des compteurs : ils suivent les events déjà produits, ticket 02. `counter-pva-formula.spec.ts` déroule la formule PVA sur des variables injectées, pas la requête d'events.
- `VALEUR_EVENT_ETAT` / `SOMME_ANNEE_ETAT` ne lisent pas les events en heures. Limite notée, pas corrigée ici.
- Chevauchement à la saisie, affichage planning, reporting absences.

---

## Non-régression

### Specs à mettre à jour

À lancer à la main.

- Nouveau spec du where partagé, ou extension de `build-counted-workflow-state-where.spec.ts` si le ticket 02 l'a déjà basculé en liste blanche : jours « null ou `validated` », heures « sans déclaration, déclaration sans workflow, ou déclaration `validated` ». Cas restriction horaire : le `OR` des plages horaires et le filtre d'état sont vrais ensemble (un event A valider dans la plage horaire sort, un event Validé dans la plage reste, un event Validé hors plage sort).
- `evaluate-workflow-resource-event-rights-balance.spec.ts` : une demande A valider déjà en base ne réduit plus `soldePrevisionnel`. Une demande Validée le réduit encore.
- `is-event-rights-balance-exceeded.spec.ts` : la soustraction de `currentWrForecastQuantity` ne change pas de formule. Le commentaire « pending WR already in pris » ne décrit plus la somme. Ajuster le commentaire, relancer le spec.
- Relecture, le comportement d'empilement ne change pas : `resources-cancel-workflow-resource.spec.ts`, `user-profile-instance-update-wrls-status-with-cascade.spec.ts`.
- `counter-pva-formula.spec.ts` : relance seule. La formule PVA n'est pas réécrite.

### Recette

Pour chaque état : un compteur à paramètre `Event` nu (ou l'agrégation `ABS_JUSTIFIEES` / `PVAJ`), `SOMME_ANNEE`, `VALEUR_EVENT_ETAT` sans second paramètre, `VALEUR_EVENT_ETAT` avec l'état explicite, le solde à date, le solde prévisionnel (somme de quantités). Rejouer en jours et en heures pour les deux premières colonnes. Les fonctions `_ETAT` restent en jours seulement.

| État de la demande | Moteur par défaut (`Event`, agrégation, `SOMME_ANNEE`, `_ETAT` sans param) | `_ETAT` avec cet état en paramètre | Solde à date | Solde prévisionnel (somme de quantités) |
| --- | --- | --- | --- | --- |
| Pas de workflow | Compte | Compte via le param `null` (saisie directe) | Compte | Compte |
| Validé | Compte | Compte | Compte | Compte |
| A valider | Ignoré | Compte | Ignoré | Ignoré |
| En attente de justificatif | Ignoré | Compte | Ignoré | Ignoré |
| Brouillon | Ignoré | Compte | Ignoré | Ignoré |
| Refusé | Ignoré | Compte | Ignoré | Ignoré |
| Annulé | Ignoré | Compte | Ignoré | Ignoré |

Transitions, sur un compteur à paramètre nu et sur le prévisionnel de la somme de quantités :

- A valider → Validé : l'event entre dans le calcul (empilement déjà en place).
- Validé → Refusé, ou suppression d'une demande validée sans valideur : l'event sort.
- Brouillon → A valider : rien ne change, les deux sont ignorés, pas de nouvel empilement.
- Validation d'un niveau intermédiaire (la demande reste A valider) : rien ne change. `recalculateCountersAfterWrStateChange` retourne déjà sans empiler.

Contrôle de droits, après le retrait de `pending` :

- Une seule demande A valider dans la limite des droits : acceptée, comme aujourd'hui.
- Une deuxième demande A valider qui, ajoutée à la première, dépasse les droits : acceptée. C'est le point à faire valider par le PO.
- Une demande qui dépasse les droits déjà consommés par des Validés (ou des saisies directes) : refusée, `CRO_WR_000000024`.
- Édition d'une demande A valider : sa quantité n'est pas soustraite du pris (elle n'y est plus).

Comportements inchangés à rejouer :

- Saisie directe sans workflow.
- Solde à date : une demande A valider future ou passée ne le bouge pas, avant comme après.
- Page « Mes droits & soldes » (`source="counters"`) : CPPA compte encore A valider. Le chiffre diffère du widget d'accueil. Attendu jusqu'à GTA-1915.
- Refus, annulation, auto-refus pièces jointes : le recalcul part encore.

### Jeux de données

Les seeds de workflow décrivent des modèles, pas une instance par état. Recette : faire vivre la demande. L'état Annulé n'est posé par aucun code applicatif ; la recette Annulé part des seeds dev (liste dans le ticket 03).

- Compteurs recommandés : `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-CP.seed.ts` (même schéma RTT et TT). CPPA porte le `SOMME_ANNEE_ETAT(..., pending)` qui reste hors de ce ticket.
- Agrégation qui voit les demandes : `ABS_JUSTIFIEES` dans `cronexia-gta-back\app\prisma\seeds-new\02-recommended\event\events-aggregation.recommanded.seed.ts`, consommée par `PVAJ`.
- Télétravail sans valideur (soumission → Validé) : template `WORKFLOW_EVENT_TT_NO_VALIDATOR` dans `workflow.seed.md`.
- En attente de justificatif : template `SICK_CHILD_ATTACHMENT_REQUIRED_DEFERRED`.

---

## À faire en clôture

Quand le ticket est terminé, poster un commentaire sur GTA-1911, en mentionnant GTA-1915. Texte à reprendre :

> Calculs des compteurs (sous-ticket, fichier `04-GTA-1911---counters-calculations.md`).
>
> Le prévisionnel ne compte plus les demandes A valider. L'exception en dur (`pending` dans la somme de quantités, et dans `isWorkflowStateInEventRightsForecast`) est commentée, avec un `TODO:` pour la rétablir quand les états d'events seront des paramètres dynamiques.
>
> Le solde prévisionnel devient « Validé sur toute la période ». Il ne diffère du solde à date que par les absences Validées futures.
>
> Le contrôle de droits à la création, à la soumission et à la mise à jour lit ce même prévisionnel. Il ne voit plus les demandes A valider : un collaborateur peut empiler des demandes A valider au-delà de ses droits. La validation d'un niveau ne refait pas ce contrôle.
>
> Jusqu'à GTA-1915, les compteurs seedés CPPA / RTTPA / TTPA comptent encore A valider (paramètre `SOMME_ANNEE_ETAT` explicite). La page « Mes droits & soldes » (`source="counters"`) aussi. Les soldes issus de la somme de quantités (accueil, calendrier, chatbot, discussion IA) ne le comptent plus. Les deux sources divergent. GTA-1915 aligne les formules.

---

## Questions PO

1. `awaitingAttachements` est ignoré, comme A valider. À confirmer. Même hypothèse que les tickets 02 et 03, côté calcul cette fois.
2. Le contrôle de droits ne bloque plus l'empilement de demandes A valider au-delà des droits, jusqu'à ce que les états soient des paramètres dynamiques. Est-ce acceptable ?
3. Une fois A valider sorti, le prévisionnel est « Validé sur toute la période », et le solde à date « Validé jusqu'à aujourd'hui ». Ce sens convient-il ?

---

## Dev

### Emplacements des fichiers

- Règle d'état, partagée avec le ticket 02
  - `cronexia-gta-back\app\src\resources\functions\events\times\build-counted-workflow-state-where.ts`
  - spec : `build-counted-workflow-state-where.spec.ts` (même dossier)
- Lecture moteur
  - `cronexia-gta-back\app\src\ct-counters\functions\histo\04-events\02-get-resources-with-mixed-events.ts`
  - appelé par `cronexia-gta-back\app\src\ct-counters\functions\histo\resources-values.ts`
  - fusion : `cronexia-gta-back\app\src\ct-counters\functions\histo\04-events\03-merge-mixed-events.ts`
- Préchargements et libellés
  - `cronexia-gta-back\app\src\ct-counters\ct-counters.service.ts`
  - `cronexia-gta-back\app\src\ct-counters\functions\manage\function.ts`
  - `cronexia-gta-back\app\src\_utility\functions\function-definition.ts`
- Prévisionnel, exception à commenter
  - `cronexia-gta-back\app\src\resources\resources.service.ts` (`buildEventRangeOnResourceWhereForQuantitySum`)
  - description GraphQL : `cronexia-gta-back\app\src\resources\models\resource-event-quantity-sum-event.model.ts`
  - doc : `cronexia-gta-back\app\src\resources\docs\resources-event-quantity-sum-by-period.doc.ts`
  - retrait du pris de la demande en cours : `cronexia-gta-back\app\src\workflow-resources\functions\resolve-workflow-resource-event-rights-guard-context.ts`
  - garde : `cronexia-gta-back\app\src\workflow-resources\functions\guard-workflow-resource-event-rights-balance.ts`
- Empilements déjà en place, à ne pas étendre pour A valider
  - `cronexia-gta-back\app\src\workflows\functions\counter\enqueue-counter-recalc-for-wr-event-range.ts`
  - validation : `cronexia-gta-back\app\src\user-profile-instances\functions\workflow-resource\functions\recalculate-counters-after-wr-state-change.ts`
  - annulation : `cronexia-gta-back\app\src\resources\functions\workflow-resource\recalculate-counters-after-wr-cancel.ts`
- Formules qui restent sur un état explicite (GTA-1915)
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-CP.seed.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-RTT.seed.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\counter\counter-conges-TT.seed.ts`
- Front, soldes qui liront le nouveau prévisionnel
  - `cronexia-gta-front-v2\app\src\routes\functions\cronexia\soldes-conges\build-soldes-conges-from-quantity-sums.ts`
  - config : `cronexia-gta-front-v2\app\src\config\events\resources-events-quantity-sum-config.ts`
  - accueil : `cronexia-gta-front-v2\app\src\routes\components\common\home\HomeEmployee.svelte`
  - page qui reste sur les compteurs : `cronexia-gta-front-v2\app\src\routes\(app)\(without-filters)\vacation-rights\+page.svelte`
- Enum
  - `cronexia-gta-back\app\prisma\schema\workflow.prisma` (`enum WorkflowStateEnum`)
