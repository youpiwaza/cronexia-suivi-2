# GTA-1744 - Workflows des events en heures - Backend

Contexte des workflow : `cronexia-suivi-2\suivi\________________workflow-context.md`

Branche : `feat-1744-wf-events-hourly`

Deux grandes étapes :

1. Fonctions complexes NestJS / GraphQL du workflow pour le type `eventByDay` (étapes 1 à 8).
2. Seeds des droits d'absence DRC (étapes 2.1 à 2.4, tout en bas du fichier). Indépendante de la grande étape 1 : peut se faire avant, pendant ou après.

Objectif de la grande étape 1 : étendre les fonctions NestJS / GraphQL du workflow au type `eventByDay` (events en heures, workflows DEP et RC), en prenant `eventRangeOnResource` (ERoR, events en jours) comme référence. Les relations, le CRUD et les seeds sont déjà faits.

Les tests (Jest, tsc, seeds) sont lancés par l'équipe, pas par l'agent. Chaque étape liste les specs à écrire, puis une vérification à faire à la main.

L'étape 0 du plan front (`GTA-1744-wf-events-hourly-frontend.md`) est terminée : les payloads qui renvoient des EbD portent `workflowResource { idWorkflowResource state workflow { type } }` pour une demande directe. Les docs le décrivent déjà (demande directe `eventByDay` ou déclaration `declarationHours`, clé directe prioritaire, aucun filtre d'état) : `src/resources/docs/resources-event-by-days-by-period.doc.ts`, `resources-all-events-by-days-by-period.doc.ts`, `resources-planning-datas.doc.ts`, `resources-declaration-hourly-grouped-by-resource-by-date.doc.ts`.

## Conventions

- Tous les chemins sont relatifs à `cronexia-gta-back/app/`.
- Abréviations : WR = `WorkflowResource`, WRLS = `WorkflowResourceLevelState`, ERoR = `EventRangeOnResource`, EbD = `EventByDay`.
- Une étape = un lot de travail autonome (une conversation, un commit). Ordre à respecter : chaque étape dépend des précédentes.
- Commentaires : pas de JSDoc, lignes `// * ...` / `// ! ...`. Imports groupés avec bandeaux, comme les fichiers voisins.
- Ne jamais modifier à la main les fichiers générés (Prisma, GraphQL).

## Constat de départ

- Lire ou lister une demande `eventByDay` (collaborateur ou valideur) lève `CRO_WR_000000009` : `src/resources/functions/workflow-resource/build-workflow-resource-typed-blocks.ts`, branche `default`.
- Créer ou soumettre une demande `eventByDay` lève `CRO_WR_000000018` : `src/workflow-resources/functions/guard-duplicates-workflow-resource.ts`, pas de cas `eventByDay`.
- Les notifications ignorent le type : `src/notifications/functions/workflow-notification-message-templates.ts`, `src/workflow-resources/functions/build-workflow-notification-period-for-wr.ts`.
- Le filtre de période ignore `eventByDays` : `src/resources/functions/workflow-resource/period-to-workflow-resource-date-where.ts` (7 branches OR aujourd'hui).
- Annulation : `src/resources/functions/workflow-resource/delete-workflow-resource-cascade.ts` ne supprime que les EbD rattachés à une déclaration. Les EbD rattachés directement à la demande restent orphelins (`onDelete: SetNull`).
- Aucun compteur RC n'existe (seeds `prisma/seeds-new/02-recommended/counter/` : CP, RTT, TT, PVA, PTO, PRE). Les plafonds de droits sont codés en dur dans `src/workflow-resources/functions/event-rights-balance-config.ts`.
- Le résolveur WR appelle uniquement `findUniqueWithTargetEventForTypeEventRangeOnResource` (`src/workflows/workflows.service.ts`).

## Décisions

- Droits RC : plafond temporaire en dur, en minutes, année civile, constante unique (défaut 35 h = 2100 min, à ajuster). DEP : aucun droit.
- Recalcul des compteurs : branche `eventByDay` branchée, sans effet tant qu'aucun compteur ne correspond à l'event (`getCounterCodesForEventName` renvoie `null`).
- Doublons à la création : entre demandes non refusées et non annulées, et chevauchement avec les EbD déjà saisis (`eventOrigin: Input`) de la ressource. Les lignes d'une demande refusée ou annulée sont exclues du contrôle.
- Création calquée sur l'ERoR : les lignes `eventByDays` sont retirées du `create` Prisma de la demande, puis créées après l'insertion via `EventByDaysService.create` (la validation `generateEventByDay` est conservée) avec `workflowResource.connect`.
- Le serveur injecte l'event cible (`targetEventForTypeEventByDay`), la ressource parente et `eventOrigin: Input` par défaut. `createMany` est refusé sur la demande.
- Un EbD rattaché à une demande ne compte comme event réel que si la demande est validée (règle GTA-1911 déjà appliquée aux ERoR).

## Hors périmètre

- Front (requêtes, familles d'affichage, formulaires).
- Garde de solde RC branchée sur les droits d'absence DRC (`ArResourceBalance`) : la grande étape 1 reste sur un plafond en dur. Les seeds DRC sont, eux, traités dans la grande étape 2.
- Demande d'annulation d'une demande déjà validée (`cancelledWorkflowResource`) : non implémentée non plus pour les ERoR (`CRO_WR_000000008` en TODO dans `resources-cancel-workflow-resource.ts`).
- Le workflow RC reste hors onglet (seul DEP est sur l'onglet `deplacement`).

## Vue d'ensemble

| Étape | Sujet | Dépend de |
|-------|-------|-----------|
| 1 | Fondations : erreurs, DTO, injection | - |
| 2 | Lecture : includes, période, blocs typés | 1 |
| 3 | Aides partagées : période, notifications, génération d'events | 2 |
| 4 | Création et mise à jour dans le résolveur WR | 1, 3 |
| 5 | Droits RC en heures et compteurs | 4 |
| 6 | Collaborateur : soumission, annulation, suppression | 3, 5 |
| 7 | Valideur : cascade de statut | 3, 5 |
| 8 | Documentation et vérification finale | 1 à 7 |
| 9 | Lecture liste : type et drapeaux de la cible heures | 2 |
| 2.1 à 2.4 | Seeds droits d'absence DRC (grande étape 2) | - |

---

## Étape 1 - Fondations : erreurs, DTO, injection / ✅ Terminé

Statut : fait

Objectif : préparer les briques réutilisées par la création (étape 4) sans encore toucher au résolveur.

### Fichiers à modifier

- `src/_utility/error/cronexia-error-dictionnary.ts` : ajouter les codes suivants (le dernier code libre est `CRO_WR_000000042`) :
  - `CRO_WR_000000043` : workflow `eventByDay` sans aucune ligne `eventByDays.create`
  - `CRO_WR_000000044` : workflow sans `targetEventForTypeEventByDay`
  - `CRO_WR_000000045` : demande en doublon (lignes qui se chevauchent)
  - `CRO_WR_000000046` : solde RC insuffisant (heures)
  - `CRO_WR_000000047` : `updateWorkflowResource` avec `eventByDays.create` alors que des lignes existent déjà
  - `CRO_WR_000000048` : `eventByDays.createMany` interdit sur une demande
  - `CRO_WR_000000049` : chevauchement avec un EbD déjà saisi (`Input`)
- `src/workflow-resources/dto/create-workflow-resource.input.ts` : le champ `eventByDays` passe du type `NestedEventByDayManyToOneInput` au nouveau type `NestedEventByDayManyToOneForWrInput`. `UpdateWorkflowResourceInput` (`src/workflow-resources/dto/update-workflow-resource.input.ts`) hérite automatiquement.
- `src/workflows/workflows.service.ts` : ajouter une méthode qui charge le workflow avec les deux events cibles (jours et heures). Garder `findUniqueWithTargetEventForTypeEventRangeOnResource` et `findUniqueWithTargetEventForTypeEventByDay` tels quels.

### Fichiers à créer

- `src/event-by-days/dto/create-event-by-day-for-wr.input.ts` : `CreateEventByDayForWrInput` (`event`, `resource`, `declarationHourly`, `workflowResource`, `eventOrigin` facultatifs ; `date` et heures ou durée à fournir).
  - Modèle : `src/event-range-on-resources/dto/nested/nested-one-to-one-event-range-on-resource-for-wr.input.ts`.
- `src/event-by-days/dto/nested/nested-many-to-one-event-by-day-for-wr.input.ts` : `NestedEventByDayManyToOneForWrInput` (`create` uniquement).
- `src/workflow-resources/functions/inject-target-event-into-nested-event-by-day-creates.ts` : exige au moins une ligne (043), exige l'event cible (044), force `event.connect` sur chaque ligne.
  - Modèle : `src/workflow-resources/functions/inject-target-event-into-nested-event-range-on-resource-create.ts`.
- `src/workflow-resources/functions/inject-parent-resource-into-nested-event-by-day-creates.ts` : reprend le `resource.connect` de la demande si la ligne n'en a pas. Réutilise `clone-resource-connect-for-nested-child.ts`, `remap-event-one-to-many-connect.ts`, `remap-resource-one-to-many-connect.ts` (même dossier).
  - Modèle : `src/workflow-resources/functions/inject-parent-resource-into-nested-event-range-on-resource-create.ts`.
- `src/workflow-resources/functions/map-nested-event-by-day-create-for-wr-to-prisma.ts` : transforme une ligne en `EventByDayCreateInput` avec `workflowResource.connect` et `eventOrigin` par défaut `Input`.
  - Modèle : `src/declaration/functions/map-nested-event-by-day-create-to-prisma.ts`.
- Specs :
  - `src/workflow-resources/functions/inject-target-event-into-nested-event-by-day-creates.spec.ts`
  - `src/workflow-resources/functions/inject-parent-resource-into-nested-event-by-day-creates.spec.ts`

### Vérification

- `bun run type-check` sans nouvelle erreur.
- Specs de l'étape.

---

## Étape 2 - Lecture : includes, filtre de période, blocs typés / ✅ Terminé

Statut : fait

Objectif : plus d'erreur `CRO_WR_000000009` quand un collaborateur ou un valideur liste une demande `eventByDay`, avec les lignes d'heures dans la réponse.

### Includes (ajouter `eventByDays` et `workflow.targetEventForTypeEventByDay`)

- `src/resources/functions/workflow-resource/workflow-resource-resources-get-include.ts` : `eventByDays` à la racine de la demande (`orderBy: [{ date: 'asc' }, { timeStart: 'asc' }]`, `event` avec `code`, `labelShort`, `labelLong`, `type`, `name`) ; `targetEventForTypeEventByDay` avec les mêmes champs que la cible ERoR. Ne pas confondre avec les `eventByDays` imbriqués sous `declaration.declarationHourlies`.
- `src/resources/functions/workflow-resource/workflow-resource-resources-cancel-include.ts` : `eventByDays` (select `date`, `orderBy date`) et cible heures.
- `src/user-profile-instances/functions/workflow-resource/type/workflow-resource-for-validator-row.type.ts` : même ajout que le include collaborateur.
- `src/user-profile-instances/functions/workflow-resource/type/wrls-for-upi-update-row.type.ts` : `eventByDays` (date, `event.labelShort`, `event.name`) et cible heures sur le workflow.

### Filtre de période

- `src/resources/functions/workflow-resource/period-to-workflow-resource-date-where.ts` : 8e branche OR `eventByDays: { some: { date: { gte, lte } } }` ; mettre à jour le commentaire d'en-tête.
- `src/resources/functions/workflow-resource/period-to-workflow-resource-date-where.spec.ts` : le nombre de branches passe de 7 à 8, ajouter un cas EbD.

### Bloc typé `typedEventByDay`

- Créer `src/resources/models/workflow-resource/workflow-resource-typed-event-by-day.model.ts` : champs `dateStart`, `dateEnd` (min et max des dates), `calculatedDays` (jours distincts), `eventByDays[]` (`idEventByDay`, `date`, `timeStart`, `timeEnd`, `duration`, `quantity`, `eventOrigin`, `event`).
  - Modèle : `src/resources/models/workflow-resource/workflow-resource-typed-event-range-on-resource.model.ts`.
- Créer `src/resources/functions/workflow-resource/map-prisma-to-workflow-resource-typed-event-by-day.ts`.
  - Modèle : `src/resources/functions/workflow-resource/map-prisma-to-workflow-resource-typed-event-range-on-resource.ts`.
- Modifier :
  - `src/resources/functions/workflow-resource/build-workflow-resource-typed-blocks.ts` : `case WorkflowTypeEnum.eventByDay`.
  - `src/resources/functions/workflow-resource/null-workflow-resource-typed-blocks.ts` : `typedEventByDay: null`.
  - `src/resources/functions/workflow-resource/type/workflow-resource-typed-blocks-pick.type.ts` : ajouter `typedEventByDay`.
  - `src/resources/models/workflow-resource/workflow-resource-row.model.ts` : champ GraphQL `typedEventByDay`.
  - `src/resources/models/workflow-resource/mock/resources-get-workflow-resource-mock.ts` : `typedEventByDay: null`.

### Documentation

- `src/resources/docs/resources-get-workflow-resource.doc.ts` : `typedEventByDay`, filtre de période sur `eventByDays`, exemple `workflowType: eventByDay`.
- `src/user-profile-instances/docs/user-profile-instance-get-workflow-resource.doc.ts` : idem côté valideur.
- `src/resources/functions/workflow-resource/README.md` : exemple de requête et bloc `typedEventByDay`.

### Specs

- `src/resources/functions/workflow-resource/map-prisma-to-workflow-resource-typed-event-by-day.spec.ts` (nouveau)
- `src/resources/functions/workflow-resource/build-workflow-resource-typed-blocks.spec.ts` (nouveau) : `typedEventByDay` renseigné, `typedEventRangeOnResource` à `null`.
  - Modèles : `map-prisma-to-workflow-resource-typed-clocking.spec.ts`, `map-prisma-to-workflow-resource-typed-schedule-overload.spec.ts` (même dossier).

### Vérification

- Playground : `resourcesGetWorkflowResource` et `userProfileInstanceGetWorkflowResource` avec `workflowType: eventByDay` sur les demandes seedées de Céline Lefevre (septembre et octobre 2024).

---

## Étape 3 - Aides partagées : période, notifications, génération d'events / ✅ Terminé

Statut : fait

Objectif : toutes les fonctions utilitaires qui reçoivent un WR savent traiter le type `eventByDay`.

### Fichiers à modifier

- `src/workflow-resources/functions/resolve-workflow-resource-period-dates.ts` : `case eventByDay` (min et max de `EventByDay.date` pour la demande) ; ajouter `eventByDays` au préchargement `WorkflowResourcePeriodPreload`.
- `src/workflow-resources/functions/build-workflow-notification-period-for-wr.ts` : branche `eventByDay`.
- `src/workflow-resources/functions/resolve-event-label-short-for-workflow-resource.ts` : libellé de l'event cible heures (`targetEventForTypeEventByDay`), repli sur la première ligne.
- `src/notifications/functions/workflow-notification-message-templates.ts` : ajouter `eventByDay` aux types supportés, messages heures sur le modèle ERoR (fonction `getEventByDayMessages`).
- `src/notifications/functions/create-workflow-notification.ts` : à vérifier (devrait fonctionner une fois le reste en place).
- `src/resources/functions/events/generate/workflow-resource-generation-period.ts` : `case eventByDay` avec `eventByDayDates`.
- `src/resources/functions/events/generate/queue/enqueue-event-generation-for-workflow-resource.ts` : source `eventByDays: { date }[]`.
- `src/resources/functions/events/generate/queue/enqueue-event-generation-if-workflow-resource-was-validated.ts` : idem.

### Specs

- `src/workflow-resources/functions/resolve-workflow-resource-period-dates.spec.ts`
- `src/workflow-resources/functions/build-workflow-notification-period-for-wr.spec.ts`
- `src/notifications/functions/workflow-notification-message-templates.spec.ts`
- `src/notifications/functions/create-workflow-notification.spec.ts`
- `src/resources/functions/events/generate/workflow-resource-generation-period.spec.ts`
- `src/resources/functions/events/generate/queue/enqueue-event-generation-for-workflow-resource.spec.ts`
- `src/resources/functions/events/generate/queue/enqueue-event-generation-if-workflow-resource-was-validated.spec.ts`

### Vérification

- Specs de l'étape.

---

## Étape 4 - Création et mise à jour dans le résolveur WR / ✅ Terminé

Statut : fait

Objectif : créer une demande DEP ou RC sans envoyer `event` ni `resource` dans les lignes d'heures.

### Fichier principal

`src/workflow-resources/workflow-resources.resolver.ts`, mutation `createWorkflowResource` (blocs à doubler pour `eventByDay`, numéros de lignes avant modification) :

- 639-643 : injection de la ressource parente dans `eventByDays`.
- 673-686 : chargement du workflow (nouvelle méthode de l'étape 1) puis injection de l'event cible (043, 044).
- 730-744 : droit `canInputWithWorkflow` sur l'event cible heures.
- 813-858 : lignes issues de `eventByDays.create` (date, heures, durée) ; garde repos `assertHourliesNotOnRestSchedule` (`src/declaration-hourlies/functions/assert-hourlies-not-on-rest-schedule.ts`, la variante `-by-declaration.ts` est dans le même dossier) sur ces lignes.
- 862-867 : délai de soumission sur la plus petite date (`src/workflow-resources/functions/guard-workflow-resource-submission-delay.ts` reste inchangé).
- 870-885 : garde de doublons avec les lignes.
- 925-930 : retirer `eventByDays` du `create` Prisma et le garder en différé (refus de `createMany`, 048).
- 981-988 : création différée des lignes une par une avec `EventByDaysService.create` + `workflowResource.connect`.
- 1019-1092 : période et libellé de la notification au valideur.

Mutation `updateWorkflowResource` (même fichier, vers 1254-1401) :

- Branche `eventByDays.create` sur brouillon : refus si des lignes existent déjà (047), refus de `createMany` (048), injection, gardes, création différée.
- Garde droits sur les nouvelles lignes : voir étape 5.

### Garde de doublons

- Modifier `src/workflow-resources/functions/guard-duplicates-workflow-resource.ts` : cas `eventByDay` (lignes 94-189), type `DuplicateGuardInput` avec `eventByDayLines?: { date, timeStart?, timeEnd?, duration? }[]`.
- Créer `src/workflow-resources/functions/guard-dedup/guard-dedup-for-event-by-day-wr.ts` :
  - contre les autres demandes non brouillon, non refusées, non annulées de la ressource, même event, même date, créneaux qui se chevauchent (ou même durée sans heures) : erreur 045 ;
  - contre les EbD `Input` de la ressource (même date, créneaux qui se chevauchent), en excluant les lignes dont la demande est refusée ou annulée : erreur 049.
  - Modèles : `guard-dedup/guard-dedup-for-event-range-on-resource.ts`, `guard-dedup/event-range-pair-duplicate-conflict.ts`.
- Créer `src/workflow-resources/functions/guard-dedup/event-by-day-time-overlap.ts` : fonction pure de chevauchement horaire.
- Service concerné : `src/event-by-days/event-by-days.service.ts` (`create`, validation `generateEventByDay` dans `src/event-by-days/functions/service/generate-event-by-day.ts`).

### Documentation

- `src/workflow-resources/docs/create.doc.ts` : remplacer le paragraphe qui dit que le client envoie `event` et `resource` ; décrire l'injection serveur, la création différée, `createMany` interdit.
- `src/workflow-resources/docs/update.doc.ts` : brouillon uniquement, refus 047 et 048.
- `src/workflow-resources/_tests_all_queries` (fichier) : mutation `createWorkflowResource` sur `seed_workflow_event_dep`.

### Specs

- `src/workflow-resources/functions/guard-duplicates-workflow-resource.spec.ts` : nouveau `describe` `eventByDay`.
- `src/workflow-resources/functions/guard-dedup/event-by-day-time-overlap.spec.ts` (nouveau).

### Vérification

- Playground : `createWorkflowResource` en brouillon puis en `pending` sur `seed_workflow_event_dep`, sans `event` ni `resource` dans les lignes. Un deuxième envoi identique doit lever 045 ou 049.

---

## Étape 5 - Droits RC en heures et compteurs / ✅ Terminé

Statut : fait

Objectif : garde de solde RC à la création et à la mise à jour, et hook de recalcul de compteurs prêt pour les heures.

### Fichiers à modifier

- `src/workflow-resources/functions/event-rights-balance-config.ts` : entrée RC (plafond en minutes, constante unique, défaut 2100) ; type `src/workflow-resources/functions/type/event-rights-balance-config.type.ts` si l'unité doit être précisée.
- `src/workflow-resources/functions/evaluate-workflow-resource-event-rights-balance.ts` : branche `eventByDay` (somme des durées demandées, déjà pris ou prévu sur l'année civile). Vérifier si `resourcesEventQuantitySumByPeriod` (`src/resources/resources.service.ts`) couvre les heures, sinon agrégat Prisma dédié sur `EventByDay.duration`, en excluant la demande courante et les demandes refusées ou annulées.
- `src/workflow-resources/functions/guard-workflow-resource-event-rights-balance.ts` : ne plus sortir tôt pour `eventByDay` ; erreur 046.
- `src/workflow-resources/functions/resolve-workflow-resource-event-rights-guard-context.ts` : contexte à partir de `eventByDays` et de l'event cible heures.
- `src/workflows/functions/get-counter-codes-for-event-name.ts` : prévoir RC (retourne `null` tant qu'aucun compteur n'existe).
- `src/workflows/functions/counter/enqueue-counter-recalc-for-wr-event-range.ts` : accepter `eventByDay` (période = année civile de la première date) ; no-op si `null`. Période : `src/workflows/functions/counter/build-period-for-event-range-on-resource.ts`.
- Appelants à brancher pour `eventByDay` :
  - `src/workflow-resources/workflow-resources.resolver.ts` (création validée d'office)
  - `src/resources/functions/workflow-resource/resources-submit-workflow-resource.ts`
  - `src/resources/functions/workflow-resource/recalculate-counters-after-wr-cancel.ts`
  - `src/user-profile-instances/functions/workflow-resource/functions/recalculate-counters-after-wr-state-change.ts`
  - `src/workflow-resources/functions/recalculate-counters-after-deferred-deadline-auto-refuse.ts`
  - `src/workflow-resources/functions/enforce-deferred-attachment-deadline.ts`

### Fichiers à créer

- `src/workflow-resources/functions/compute-event-by-days-requested-quantity.ts` : somme des durées des lignes demandées.
- `src/workflow-resources/functions/guard-workflow-resource-event-rights-on-event-by-days-update.ts` : garde à la mise à jour d'un brouillon.
  - Modèle : `src/workflow-resources/functions/guard-workflow-resource-event-rights-on-event-range-update.ts`.

### Documentation

- `src/workflow-resources/docs/check-event-rights-balance.doc.ts` : préciser que `eventByDay` n'est pas couvert par la requête à blanc (arguments en jours), ou étendre si besoin.

### Specs

- `src/workflow-resources/functions/evaluate-workflow-resource-event-rights-balance.spec.ts` : cas RC (heures).
- `src/workflow-resources/functions/resolve-workflow-resource-event-rights-guard-context.spec.ts` : cas `eventByDay`.
- `src/workflow-resources/functions/guard-workflow-resource-event-rights-on-event-by-days-update.spec.ts` (nouveau).
- `src/workflows/functions/counter/enqueue-counter-recalc-for-wr-event-range.spec.ts` (nouveau) : ERoR inchangé, `eventByDay` sans effet si aucun compteur.

### Vérification

- Playground : une demande RC au-dessus du plafond est refusée (046) ; une demande DEP n'est jamais bloquée par un solde.

---

## Étape 6 - Collaborateur : soumission, annulation, suppression / ✅ Terminé

Statut : fait

Objectif : le collaborateur peut soumettre, ajouter des PJ et annuler une demande `eventByDay` sans erreur ni ligne orpheline.

### Fichiers à modifier

Résolveur (pass-through, aucun changement attendu) : `src/resources/resources.resolver.ts` (`resourceSubmitWorkflowResource`, `addWorkflowResourceAttachments`, `resourceCancelWorkflowResource`).

- `src/resources/functions/workflow-resource/fetch-and-guard-workflow-resource-for-resources-submit.ts` : passer `eventByDayLines` et le nom de l'event cible heures à la garde de doublons.
- `src/resources/functions/workflow-resource/resources-submit-workflow-resource.ts` : date d'effet pour le délai = plus petite date de ligne ; droits ; compteurs ; notification ; génération d'events avec `eventByDays`.
- `src/resources/functions/workflow-resource/resources-cancel-workflow-resource.ts` : date d'effet = plus petite date de ligne ; génération d'events avec `eventByDays` si la demande était validée.
- `src/resources/functions/workflow-resource/guard-workflow-resource-cancellation-delay.ts` : commentaire de type et appelants (date d'effet = plus petite date de ligne).
- `src/resources/functions/workflow-resource/create-resource-cancel-workflow-resource-notification.ts` : libellé et période `eventByDay`.
- `src/resources/functions/workflow-resource/resources-add-workflow-resource-attachments.ts` : période de notification via l'étape 3 (vérifier).
- `src/resources/functions/workflow-resource/delete-workflow-resource-cascade.ts` : supprimer les EbD liés directement à la demande (`workflowResourceId`) avant la demande.
- `src/resources/functions/workflow-resource/delete-workflow-resource-and-level-states.ts` : commentaire d'en-tête.

### Documentation

- `src/resources/docs/resources-cancel-workflow-resource.doc.ts` : cascade, EbD liés directement à la demande supprimés.
- `src/resources/docs/resources-submit-workflow-resource.doc.ts` : exemple `eventByDay`.

### Specs

- `src/resources/functions/workflow-resource/resources-submit-workflow-resource.spec.ts` : cas `eventByDay`.
- `src/resources/functions/workflow-resource/resources-cancel-workflow-resource.spec.ts` : cas `eventByDay`.
- `src/resources/functions/workflow-resource/delete-workflow-resource-cascade.spec.ts` : ajouter `eventByDay.deleteMany({ where: { workflowResourceId } })` (aujourd'hui seul le chemin déclaration est testé).
- `src/resources/functions/workflow-resource/fetch-and-guard-workflow-resource-for-resources-cancel.spec.ts` : mock avec `eventByDays`.
- `src/resources/functions/workflow-resource/resources-add-workflow-resource-attachments.spec.ts` : mock `eventByDay`.

### Vérification

- Playground : soumettre un brouillon DEP, annuler une demande en attente, vérifier en base qu'aucun `EventByDay` n'a `workflowResourceId` d'une demande supprimée.

---

## Étape 7 - Valideur : cascade de statut / ✅ Terminé

Statut : fait

Objectif : valider ou refuser une demande `eventByDay` met à jour les events, les compteurs et les notifications comme pour une ERoR.

### Fichiers à modifier

Résolveur (pass-through) : `src/user-profile-instances/user-profile-instances.resolver.ts` (`userProfileInstanceGetWorkflowResource` autour de la ligne 874, `userProfileInstanceUpdateWrlsStatusWithCascade` autour de 1528-1600).

- `src/user-profile-instances/functions/workflow-resource/user-profile-instance-update-wrls-status-with-cascade.ts` : génération des events passés quand la demande est validée (source avec `eventByDays`), hook compteurs.
- `src/user-profile-instances/functions/workflow-resource/user-profile-instances-get-workflow-resource.ts` : vérifier le filtre de période avec `eventByDays` (include de l'étape 2).
- `src/user-profile-instances/functions/workflow-resource/functions/create-collaborator-notification-after-wrls-update.ts` : libellé et période `eventByDay`.
- `src/user-profile-instances/functions/workflow-resource/functions/create-next-validator-notification-after-wrls-validated.ts` : idem.
- `src/resources/functions/events/times/build-counted-workflow-state-where.ts` : un EbD rattaché directement à une demande ne compte que si la demande est validée (aujourd'hui seul le chemin déclaration est traité).
- `src/resources/functions/events/times/resources-manual-event-by-days-by-period.ts` : utiliser le nouveau comptage.

### Documentation

- `src/user-profile-instances/docs/user-profile-instance-update-wrls-status-validated.doc.ts` : génération d'events passés pour `eventByDay`, recalcul compteurs seulement si un compteur est associé.
- `src/user-profile-instances/docs/user-profile-instance-update-wrls-status-refused.doc.ts` : idem.
- `src/user-profile-instances/functions/workflow-resource/README.md` : types de notification supportés et blocs typés.

### Specs

- `src/user-profile-instances/functions/workflow-resource/user-profile-instance-update-wrls-status-with-cascade.spec.ts` : cas `WorkflowTypeEnum.eventByDay` avec `eventByDays` dans l'include.
- `src/resources/functions/events/times/build-counted-workflow-state-where.spec.ts` : cas EbD lié à une demande.
- `src/user-profile-instances/functions/workflow-resource/functions/recalculate-counters-after-wr-state-change.spec.ts` (nouveau).

### Vérification

- Playground (valideur Murielle) : valider une demande DEP en attente (Céline, 08/10/2024), refuser une demande RC en attente (03/09/2024). Contrôler la notification, la génération d'events, puis que le refus ne compte pas dans les events réels.

---

## Étape 8 - Documentation et vérification finale / ✅ Terminé

Statut : doc faite, vérification par l'équipe en attente

### Fichiers à modifier

- `prisma/seeds-new/02-recommended/workflow/workflow.seed.md` : sections 7 et 8 si le comportement décrit a changé. ✅ Fait (comportement runtime DEP et RC, phrase d'intro corrigée).
- `prisma/seeds-new/02-recommended/workflow-tab/README.md` : si des changements touchent l'onglet. ✅ Relu, aucun changement nécessaire (DEP sur l'onglet `deplacement`, RC hors onglet).
- Fichiers `_tests_all_queries` des modules modifiés : `src/workflow-resources/_tests_all_queries`, `src/event-by-days/_tests_all_queries`, `src/resources/_tests_all_queries`, `src/user-profile-instances/_tests_all_queries`. ✅ Fait (lectures `typedEventByDay`, soumission, annulation, validation, refus, plafond RC 046, mise à jour 047, EbD liés aux demandes).
- `cronexia-suivi-2/suivi/11-novembre/261120-suivi.md` (section Tests GTA-1744) : retirer les points « hors périmètre » devenus faux (création, soumission, validation, annulation, solde RC). ✅ Fait (sections 5 à 10).
- README et docs `src/` (`resources`, `user-profile-instances`, `workflow-resources/docs`) : déjà à jour depuis les étapes 2 à 7.

### Vérification (par l'équipe)

- `bun run type-check`, lint.
- Jest ciblé sur les specs ajoutées, puis suite backend complète avec les exclusions habituelles (voir `261120-suivi.md`).
- Seed dev après reset de la base, puis scénario manuel de bout en bout sur DEP et RC : création, soumission, validation, refus, annulation.
- Redémarrage de l'API (cycle `forwardRef` entre `EventByDaysModule` et `WorkflowResourcesModule`).

---

## Étape 9 - Cible heures des listes : type et drapeaux / ✅ Terminé

Statut : fait

Objectif : `resourcesGetWorkflowResource` et `userProfileInstanceGetWorkflowResource` peuvent sélectionner `workflow.targetEventForTypeEventByDay { labelShort code type isRemoteWork isOnCallDuty isTravelling isRightsCalculationAssociated }` sans erreur. Le résolveur Workflow ne recharge pas un Event déjà préchargé : le select partiel doit contenir `type` (non nullable) et les trois drapeaux.

### Fichiers à modifier

- `src/resources/functions/workflow-resource/workflow-resource-resources-get-include.ts` : `type`, `isRemoteWork`, `isOnCallDuty`, `isTravelling` sur `targetEventForTypeEventByDay` et sur `targetEventForTypeEventRangeOnResource` (les drapeaux jours revenaient `null`). `name` conservé.
- `src/user-profile-instances/functions/workflow-resource/type/workflow-resource-for-validator-row.type.ts` : les quatre mêmes clés sur `targetEventForTypeEventByDay` seulement. La cible jours n'est pas préchargée.
- Docs : `src/resources/docs/resources-get-workflow-resource.doc.ts`, `src/user-profile-instances/docs/user-profile-instance-get-workflow-resource.doc.ts`.
- Pas de changement de schéma ni de types générés. Include d'annulation inchangé.

### Specs

- `src/resources/functions/workflow-resource/workflow-resource-target-event-list-select.spec.ts` : 3 tests passés (clés des trois selects).

### Vérification

- Playground : `workflowType: eventByDay`, demandes seedées de Céline Lefevre (septembre et octobre 2024). `typedEventByDay` rempli, `typedEventRangeOnResource` à `null`, `targetEventForTypeEventByDay.type` à `Absence`. DEP : `isTravelling: true`. RC : `isRightsCalculationAssociated: true`. Redémarrer l'API si elle ne recharge pas le fichier.

---
---

# Grande étape 2 - Seeds des droits d'absence DRC

Objectif : avoir des soldes de repos compensateur (DRC, en heures) dans les trois jeux de seeds.

- Jeu dev : plusieurs ressources, sur le modèle des exemples de droits existants (Maxime, Bob, PO pour DCP et DRTT).
- Jeux demo et demo-arte : Maxime uniquement.

Ces seeds vivent dans l'ancien dossier `prisma/seeds/absence-right/` (pas dans `seeds-new`). Les chemins ci-dessous sont relatifs à `cronexia-gta-back/app/`.

## Ce qui existe déjà

| Élément | Fichier | État |
|---------|---------|------|
| Droit DRC (`absenceRightDRC`) | `prisma/seeds/absence-right/absence-right.seed.ts` (`seedAbsenceRightDRCExample`) | Fait |
| Version DRC V1 : heures, hors exercice, anticipation refusée | `prisma/seeds/absence-right/ar-version.seed.ts` (`seedArVersionDRCExample1`) | Fait |
| Cible : délai de prise 2 mois, délai de report 2 mois, report non automatique, solde minimum 0 | `prisma/seeds/absence-right/ar-population-target.seed.ts` (`drcPopulationTarget`), période `drcDelay` dans `prisma/seeds/absence-right/period.seed.ts` | Fait |
| Priorité de décompte RC | `prisma/seeds/absence-right/ar-priority.seed.ts` | Fait |
| Orchestrateur | `prisma/seeds/absence-right/absence-right.ts` (`seedAbsenceRightExample`) | Fait |
| Codes de mouvements `AJOUT_ACQUIS`, `PRISE_ACQUIS` | `prisma/seeds/absence-right/ar-movement.seed.ts` | Fait |
| Instance Maxime, dev (`123456A`) | `prisma/seeds/absence-right/ar-movement-instance-maxime-drc.seed.ts`, appelée dans `absence-right.ts` (bloc « Exemples ressources (dev uniquement) ») | Fait |
| Instance Maxime, demo (`200010H`) | même fichier, appelée dans `prisma/seed-demo.ts` (autour des lignes 103-106) | Fait |
| Instance Maxime, demo-arte | `prisma/seed-demo-arte.ts` : import ligne 22 et appel (autour des lignes 104-107) en commentaire | **Manquant** |
| Instances Bob (`777777C`) et PO (`987654B`), dev | `prisma/seeds/absence-right/ar-movement-instance-bob.seed.ts`, `ar-movement-instance-po.seed.ts` : en-têtes « Pas de DRC » | **Manquant** |

Données de Maxime (au 12/10/2026) : +7 le 28/08, +3 le 15/09, prise −3,5 le 01/10, restant **6,5**. Un seul pot, sans exercice (`arExerciseId` à `null`).

Cible DRC en dev : populations `…0046` (Maxime et Bob) et `…0047` (PO), via `dcpPopulationIds` dans `absence-right.ts`. Bob et PO sont donc déjà couverts par la cible, il ne leur manque que les mouvements et le solde.

Identifiants déjà pris dans `prisma/seeds/absence-right/` : mouvements `00000000-0000-0000-a532-0000000000NN` jusqu'à `…042`, soldes `00000000-0000-0000-a55b-0000000000NN` jusqu'à `…008`. Aucune collision avec `prisma/seeds-new`. Prochains libres : `a532` à partir de `…043`, `a55b` à partir de `…009`.

Contrainte : l'anticipation est refusée sur DRC, donc pas de solde négatif.

## Vue d'ensemble

| Étape | Sujet | Dépend de |
|-------|-------|-----------|
| 2.1 | Dev : DRC pour Bob et PO | - |
| 2.2 | Demo-arte : DRC de Maxime | - |
| 2.3 | Demo : vérification (déjà en place) | - |
| 2.4 | Documentation et vérification | 2.1 à 2.3 |

---

## Étape 2.1 - Dev : DRC pour Bob et PO

Statut : à faire

Objectif : trois situations DRC différentes en dev, comme les exemples DCP et DRTT qui diffèrent par les prises.

| Ressource | Matricule | Cas | Mouvements | Restant |
|-----------|-----------|-----|------------|---------|
| Maxime (existant) | `123456A` | partiel | +7 (28/08), +3 (15/09), −3,5 (01/10) | 6,5 |
| Bob | `777777C` | épuisé | +8 (02/09), +4 (15/09), −12 (30/09) | 0 |
| PO | `987654B` | non entamé | +4 (15/09) | 4 |

Pour chaque ressource : mouvements `AJOUT_ACQUIS` et `PRISE_ACQUIS`, effet avant la date de calcul du 12/10/2026, type `test`, `arExerciseId` à `null`, un solde sur la version DRC V1 (cumul acquis, pris acquis, restant, `computationEffectDate` et `lastUpdatedAt` au 12/10/2026).

### Fichiers à créer

- `prisma/seeds/absence-right/ar-movement-instance-drc-bob-po.seed.ts` :
  - fonction commune `seedDrcForResource(prisma, { arVersionId, matricule, balanceId, movements, balance })`, même logique que `ar-movement-instance-maxime-drc.seed.ts` (upsert des mouvements par id, upsert du solde par id) ;
  - exports `seedBobDrc(prisma, { arVersionId })` et `seedPoDrc(prisma, { arVersionId })` ;
  - ids : mouvements `a532` à partir de `…043`, soldes `a55b` `…009` (Bob) et `…010` (PO) ;
  - erreur explicite si la ressource ou un code de mouvement est absent (même message que les autres seeds).

### Fichiers à modifier

- `prisma/seeds/absence-right/absence-right.ts` : dans le bloc « Exemples ressources (dev uniquement) », après `seedMaximeDrc`, appeler `seedBobDrc` et `seedPoDrc` avec `arVersionDRC1.idArVersion`. Mettre à jour les commentaires « pas de DRC » de Bob et de PO.
- `prisma/seeds/absence-right/ar-movement-instance-bob.seed.ts` : retirer « Pas de DRC » de l'en-tête (ligne 9).
- `prisma/seeds/absence-right/ar-movement-instance-po.seed.ts` : retirer « Pas de DRC, pas de prise prévisionnelle » de l'en-tête (ligne 11) ou le reformuler.

### Vérification

- Seed dev après reset de la base (commande habituelle de seed dev).
- Requête `arResourceBalances` (voir `src/ar-resource-balances/_tests_all_queries`) filtrée sur la version DRC : trois soldes, restants 6,5 / 0 / 4.

---

## Étape 2.2 - Demo-arte : DRC de Maxime

Statut : à faire

Objectif : Maxime (`200010H`) a son solde DRC dans le jeu demo-arte, comme dans demo. Seul le DRC est rétabli : les blocs DCP et DRTT restent en commentaire.

### Fichiers à modifier

- `prisma/seed-demo-arte.ts` :
  - décommenter l'import de `seedMaximeDrc` (ligne 22) ;
  - décommenter l'appel `seedMaximeDrc(prisma, { arVersionId: absenceRights.arVersionDRC1.idArVersion, matricule: '200010H' })` (autour des lignes 104-107) ;
  - adapter le commentaire d'en-tête du bloc (« Maxime démo ... ») pour dire que seul le DRC est actif.
- Prérequis déjà satisfaits (à vérifier) : la ressource `200010H` existe dans `prisma/seeds-new/26-demo-arte/resource/employee/managed-by-bruno/200010H_Maxime_Chevasson.demo.seed.ts` ; `seedAbsenceRightExample` (appelé avec `populationId` de la population All_Resources) crée déjà le droit, la version et la cible DRC.

### À confirmer avant de faire

- Les blocs de soldes sont tous en commentaire dans demo-arte. Si c'est volontaire (démo Arte sans soldes), la demande actuelle prime : seul le DRC est rétabli.

### Vérification

- Seed demo-arte sur base vide : pas d'erreur, un solde DRC de 6,5 pour `200010H`.

---

## Étape 2.3 - Demo : vérification

Statut : à faire

Objectif : confirmer que le jeu demo donne bien le DRC de Maxime et rien d'autre.

### Fichiers à contrôler (aucune modification attendue)

- `prisma/seed-demo.ts` : `seedMaximeDrc` appelé pour `200010H` avec la version DRC V1 (déjà en place, import ligne 22).
- Bob et PO ne sont pas ajoutés en demo : `seedAbsenceRightExample` est appelé avec `populationId`, ce qui saute le bloc « Exemples ressources (dev uniquement) » de `absence-right.ts`. Les appels `seedBobDrc` et `seedPoDrc` de l'étape 2.1 doivent rester dans ce bloc.

### Vérification

- Seed demo sur base vide : un seul solde DRC, celui de `200010H`.

---

## Étape 2.4 - Documentation et vérification

Statut : à faire

### Fichiers à modifier

- `prisma/seeds/absence-right/_absence-right-new-seeds-10-2026.md` :
  - section « Instances » : ajouter Bob (épuisé, restant 0) et PO (non entamé, restant 4) au DRC ; retirer les mentions « pas de DRC » de leurs sections ;
  - ajouter un court tableau « Jeux de seeds » : dev = Maxime, Bob, PO ; demo et demo-arte = Maxime seul (`200010H`).
- `cronexia-suivi-2/suivi/11-novembre/261120-suivi.md` : si une mention des droits DRC est ajoutée au plan de tests.

### Points d'attention

- Contexte (hors périmètre) : les droits d'absence sont en cours d'implémentation et n'ont pas encore de génération. Les seeds ne servent donc qu'à tester l'affichage, sans calculs complexes : les soldes sont posés à la main via les mouvements, rien n'est recalculé. Le front charge les droits (`ArResourceBalance`) et le système actuel (compteurs + requête dédiée, pour la performance), puis affiche de façon hybride : droits si la ressource en a, système actuel sinon, avec des données mock pour combler les trous sur certaines pages.
- Conséquence pour les seeds : une ressource sans solde DRC n'affiche pas « rien », elle retombe sur le système actuel (ou du mock). Pour tester l'affichage des droits, la ressource doit donc avoir un `ArResourceBalance`, d'où les soldes de Maxime (3 jeux) et de Bob et PO (dev).
- Ces soldes DRC ne sont lus par aucune garde du workflow : la garde de solde RC de la grande étape 1 utilise un plafond en dur (35 h par défaut, étape 5). Ils servent à l'affichage « Mes droits et soldes ». Les brancher sur le workflow serait un chantier à part.
- Les demandes RC de dev du workflow sont à Céline Lefevre (`resource__LefevreC`), qui n'est pas dans les populations de la cible DRC. Si on veut un solde DRC cohérent avec ces demandes, il faudra l'ajouter à une population cible et lui poser un solde : non prévu ici.

### Vérification (par l'équipe)

- Seed dev, demo et demo-arte, chacun sur base vide, sans erreur.
- Contrôle visuel dans « Mes droits et soldes » pour Maxime : DRC à 6,5 h dans les trois jeux.
