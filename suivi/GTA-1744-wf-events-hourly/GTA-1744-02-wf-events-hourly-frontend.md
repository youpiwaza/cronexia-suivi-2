# GTA-1744 - Workflows des events en heures - Frontend

Contexte des workflow : `cronexia-suivi-2/suivi/________________workflow-context.md`

Plan backend (référence) : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/GTA-1744-wf-events-hourly-backend.md`

Branche : `feat-1744-wf-events-hourly` (à confirmer pour le dépôt front)

Objectif : étendre le front aux workflows de type `eventByDay` (events en heures : DEP = déplacement, RC = repos compensateur), en prenant `eventRangeOnResource` (ERoR, events en jours) comme référence. Le backend de la grande étape 1 est terminé (relations, CRUD, lecture `typedEventByDay`, création, soumission, validation, refus, annulation), mais une vérification faite pour ce plan a révélé un manque : l'étape 0 ci-dessous (même ticket) est à faire avant le front.

Le plan est découpé en une étape 0 (backend) et 12 étapes front. Chaque étape fera l'objet de son propre plan détaillé, puis d'une conversation et d'un commit.

Les tests (jest côté backend, vitest, type-check, lint côté front) sont lancés par l'équipe, pas par l'agent. Chaque étape liste les specs à écrire, puis une vérification à faire à la main.

## Conventions

- Chemins front : relatifs à `cronexia-gta-front-v2/app/src/` (sauf mention contraire). Chemins backend (étape 0) : relatifs à `cronexia-gta-back/app/`.
- Abréviations : WR = `WorkflowResource`, WRLS = `WorkflowResourceLevelState`, ERoR = `EventRangeOnResource`, EbD = `EventByDay`, DEP = déplacement, RC = repos compensateur.
- Une étape = un lot de travail autonome. Ordre à respecter : chaque étape dépend des précédentes.
- Commentaires : pas de JSDoc, lignes `// * ...` / `// ! ...`. Imports groupés avec bandeaux, comme les fichiers voisins (règle `import-conventions`).
- Svelte : consulter le MCP Svelte et passer `svelte-autofixer` sur chaque composant écrit ou modifié.
- Ne jamais modifier à la main les fichiers générés (types front `lib/generated/types/graphql/graphql.ts`, `graphql.schema.json`, Prisma et GraphQL côté backend).
- Principe de classement : tout nouveau branchement `eventByDay` se base sur les propriétés de l'event cible (type `Absence` / `Presence` / `Neutral`, drapeaux `isRemoteWork`, `isOnCallDuty`, `isTravelling`...), jamais sur un code ou un nom d'event en dur (`DEP`, `RC`).

## Constat de départ

- Le front ne connaît pas le type workflow `eventByDay` : pas de `typedEventByDay`, de `targetEventForTypeEventByDay` ni de `WorkflowTypeEnum.EventByDay` (le `graphql.ts` commité s'arrête à `scheduleOverload`). Les `eventByDays` déjà présents concernent les déclarations d'heures (`declarationHours`), le planning et l'API EventByDay brute. Ne pas les confondre avec le bloc typé `typedEventByDay`.
- Backend : les résolveurs `resourcesGetWorkflowResource` et `userProfileInstanceGetWorkflowResource` acceptent `workflowType: eventByDay` (argument `WorkflowTypeEnum` facultatif, filtre `workflow.type`). Omis, tous les types reviennent, avec les blocs `typed*` calculés selon `workflow.type`.
- Backend, manque constaté : les payloads qui renvoient des EbD au front (planning `resourcesPlanningDatas`, `resourcesAllEventsByDaysByPeriod`, `resourcesEventByDaysByPeriod`, absences, déclaration horaire) posent `workflowResource` et `workflowState` uniquement via la chaîne déclaration (`src/resources/functions/events/event-by-day-declaration-workflow-resource.ts` : `declarationHourly → declaration → workflowResource`). Un EbD rattaché directement à une demande (`workflowResourceId`) arrive donc avec `workflowResource: null` et `workflowState: null`, et le front le lit comme « sans demande donc validé ». Une demande DEP ou RC en attente, refusée ou annulée apparaîtrait comme un event validé dans le planning, les calendriers, l'accueil, la synthèse, les anomalies et les pages d'absences. Ces payloads n'ont pas de filtre d'état (comme pour les ERoR, c'est le front qui masque). Le résolveur d'entité `EventByDay` (`src/event-by-days/event-by-days.resolver.ts`, ligne 173) gère déjà la clé directe : seul le chemin agrégé est concerné. Traité par l'étape 0.
- Règle de visibilité existante pour les ERoR (en-tête de `routes/functions/cronexia/event-range-on-resource/event-range-on-resource-workflow.helpers.ts`) : tous les statuts sont affichés avec une bordure selon le statut (refusé : bordure rouge) ; brouillon masqué pour les autres viewers si `IS_DISPLAY_DRAFT_REQUESTS` est faux (GTA-1789) ; refusés et annulés masquables par la case « afficher annulés et refusés » (GTA-1911, `routes/functions/cronexia/planning/is-cancelled-or-refused-event.ts`, utilisée par `SummaryArray`, `AnomaliesArray`, `PersonalCalendarPage`, `planning/collective/filter-mapped-planning-cancelled-or-refused.ts`) ; pages de gestion des absences : saisie directe, en attente et validé seulement (GTA-1622, `isAbsenceVisibleOnGestionPages`) ; comptage des events réels : demande validée seulement (backend). Les EbD de demande directe doivent suivre cette même règle, pas une règle nouvelle.
- Tout le front workflow est piloté par des familles d'affichage (`routes/functions/cronexia/workflow-tab/`) : `resolve-display-family.ts` (switch sur le type) puis un pack par famille (`families/*.family.ts`, registre `families/index.ts`). Un type inconnu retombe sur `generic` (colonnes type et période). Pour la période, `getDateRangeFromRawItem` (`routes/functions/cronexia/workflow/employee-demands-page.helpers.ts`) ne lit aujourd'hui que les blocs typés connus, puis se rabat sur la date de soumission.
- Les trois allowlists `WORKFLOW_TYPES` (`routes/api/workflow/resources/+server.ts`, `routes/api/resource/workflow-resources/+server.ts`, `routes/api/user-profile-instance/workflow-resource-to-validate/+server.ts`) ne servent qu'à valider le paramètre facultatif `workflowType` de l'URL. Elles ne filtrent pas les résultats : les appels par défaut ne passent pas ce paramètre. À compléter malgré tout pour les appels qui l'utilisent.
- Les sélections GraphQL de l'event cible ERoR (`resourcesGetWorkflowResource.ts`, lignes 48-55) contiennent `labelShort code isRemoteWork isOnCallDuty isTravelling isRightsCalculationAssociated`, mais pas `type`. Le type d'event (`EventTypeEnum` : `Absence`, `Neutral`, `Presence`) est disponible dans le schéma. DEP et RC sont tous deux de type `Absence` dans les seeds (`prisma/seeds-new/02-recommended/event/events.seed.ts`, DEP : `isTravelling: true`, RC : `isRightsCalculationAssociated: true`).
- Création : `WorkflowNewDemandButton.svelte` charge à la demande 4 modales (absences, télétravail, changement d'horaire, pointages), choisies via `create-modal-target-from-family.ts` (dont la constante `CREATE_MODAL_ITEM_IDS`), `catalog-workflow-create-item-id.ts`, `employee-tab-create-action.ts` et `components/cronexia/workflow/workflow-new-demand-items.ts` (union `WorkflowNewDemandItemId`). Aucune modale pour des demandes en heures. `AbsencesWorkflowModal.svelte` est codée en dur sur `eventRangeOnResource`.
- Popup de consultation `WorkflowDemandConsultModal.svelte` : aucun `switch` sur le type dans la modale. Tout vient du modèle `WorkflowAccordionModel` (`build-workflow-demand-details.ts`, `workflow-demand-consult.helpers.ts`). Deux points dépendent du type : `build-workflow-demand-details.ts` (lignes 39, 68, 196-197) lit uniquement `targetEventForTypeEventRangeOnResource` pour `eventLabel`, `code` et `targetEvent` ; `describeWorkflowValidationCandidate` (partagé avec `ValidatorDemandsTabShell` et `WidgetValidationDemandes`) renvoie un candidat dès que `code` et `dateStart` existent, et lance alors le contrôle de conflits ERoR en jours (`checkWorkflowDemandConflicts`, périodes `Day`), inadapté aux heures.
- Planning (clics et fusion des demandes) : `routes/functions/cronexia/planning/planning-workflow-resolve.helpers.ts`. `resolvePlanningWorkflowForHourAbsence` délègue à `resolvePlanningWorkflowForDayAbsence`, qui ne garde que les workflows `eventRangeOnResource` ou à nom d'absence et compare les dates via `typedEventRangeOnResource` / STO. Un clic sur une ligne d'heures de demande renverrait `null`. La récupération (`fetchPlanningWorkflowResources`) appelle `/api/workflow/resources` sans filtre de type, avec la fenêtre de dates : les demandes `eventByDay` reviendront dès l'étape 2.
- Calendriers : `routes/functions/cronexia/calendrier-annuel/planning-data-to-events.ts`. La pastille « hour-wf » (lignes 876-950) ne traite que les EbD générés avec demande (`isUserInput === false`, déclaration ADEC / PDEC). DEP et RC ont `isUserInput: true` : ils passent par la map `hourlyAbsences` (ligne 1248) avec `status: ebd.workflowState` et `workflowResource: ebd.workflowResource`, donc dépendent de l'étape 0. Le planning collectif (`planning/collective/planning-data.mapper.ts`, lignes 706-712, 784-788, 834-839), `filter-planning-datas-draft-for-viewer.ts` et `is-cancelled-or-refused-event.ts` lisent déjà `ev.workflowResource` / `workflowState` : ils fonctionneront dès que le backend les renseigne.
- Demandes en cours du calendrier : `routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.ts`, `classifyPendingWorkflow` classe aujourd'hui `eventByDay` en `other` et lit uniquement la cible ERoR pour `eventCode`.
- Helpers EbD / déclaration : `getDeclarationWorkflowResourceId` (`event-range-on-resource-workflow.helpers.ts`, ligne 109) renvoie l'id du WR pour tout EbD sans ERoR. Un EbD de demande directe est donc pris pour un EbD de déclaration (ADEC / PDEC, GTA-1771) : `HomeEmployee.svelte` (ligne 280) l'affiche quel que soit son état ; `DayTimelineAccordion.svelte` (`editEvent`, ligne 352) ouvre la consultation de déclaration, et ne fait rien si le WR n'est pas dans le payload de la page. Traité par l'étape 8.
- Pages droits (`rights/[right]/dateStart/[[dateStart]]`) : soldes via `ArResourceBalance` (DCP, DRTT, TT, DRC), repli compteurs (CP, RTT, TT seulement). Prises lues par `components/cronexia/rights-employee/fetch-employee-rights-take-ranges.ts` (route `event-range-on-resource/by-period`, DRC rattaché à l'event RC, durées de `eventRangeByDays`). `employee-rights-takes.ts` compte les prises sans WR, validées ou en attente. Aucun parcours de demande sur cette page.
- RC absent des soldes de demande : `AbsenceWorkflowSoldePanel.svelte` (`onlyKeys: cp|rtt|tt`), `functions/cronexia/vacation-rights/resolve-workflow-right-key.ts`, `VacationRightsDemandsSection.svelte`.
- Pages RH `rights/individual|collective` : aucun usage de WR (Ar pur), rien à faire.
- Il n'y a pas de dépôt `cronexia-gta-front` (v1) à côté de v2 : seul v2 est concerné.

## Décisions

- Même ticket : le backend se termine d'abord (étape 0), le front ensuite.
- Une seule famille d'affichage `hourlyEvent` pour DEP et RC (colonnes : type, date, créneau, durée). Un découpage DEP / RC reste possible plus tard sans casser les étapes.
- Création : une nouvelle modale dédiée aux demandes en heures (date, début et fin ou durée), branchée sur `WorkflowNewDemandButton`. Le serveur injecte l'event cible, la ressource et `eventOrigin` : le client n'envoie que date, heures et durée dans `eventByDays.create`. `createMany` est refusé.
- RC : pas d'onglet côté backend (pool non affecté), donc pas de point d'entrée de création RC dans ce chantier. Le front doit néanmoins lire, afficher, valider et refuser une demande RC (demandes de dev seedées sur Céline Lefevre).
- Classement dans « Demandes en cours » du calendrier : DEP et RC sont des demandes d'absence. Le classement se déduit du type de l'event cible (`type === 'Absence'` donne `absence`, `Presence` ou `Neutral` donne `other`), pas d'un code ou d'un nom en dur. Il faut donc sélectionner `type` sur l'event cible heures (étape 2). Le comportement ERoR existant n'est pas modifié.
- Visibilité : les EbD de demande directe suivent exactement la règle des ERoR (voir constat) : aucune règle nouvelle côté front. Le backend renvoie tous les états (comme pour les ERoR) ; le front masque selon les cases et la configuration existantes.
- Validation : pas de contrôle de conflits à la validation pour la famille `hourlyEvent` (`describeWorkflowValidationCandidate` renvoie `null`, donc la demande est classée « sans conflit »). Les doublons sont contrôlés à la création par le backend (045 et 049). À rouvrir plus tard si besoin métier.
- Les widgets de changement d'état (valider / refuser, WRLS) ne doivent pas changer : vérification seulement.
- Le plafond RC (2100 min, erreur `CRO_WR_000000046`) est en dur côté backend et ignore les soldes DRC (`ArResourceBalance`). Le front affiche l'erreur telle quelle, sans brancher les soldes DRC sur la demande.

## Hors périmètre

- Chatbot / IA (`routes/api/chatbot/**`, `components/common/ai/**`).
- Point d'entrée de création RC (en attente d'un onglet RC ou d'un parcours dédié).
- Demande d'annulation d'une demande déjà validée (non faite non plus pour ERoR).
- Brancher les soldes DRC sur la garde de solde du workflow.
- Pages RH `rights/individual|collective`.
- Contrôle de conflits à la validation pour les EbD (voir décisions).

## Vue d'ensemble

| Étape | Sujet | Dépend de |
|-------|-------|-----------|
| 0 | Backend : demande directe estampillée sur les EbD des payloads | backend terminé |
| 1 | Fondations front : codegen, enum, libellés, couleurs, allowlists API | 0 |
| 2 | Lecture GraphQL : requêtes et parseurs | 1 |
| 3 | Famille d'affichage `hourlyEvent` et mappeurs de lignes | 2 |
| 4 | Page admin : organisation des onglets | 3 |
| 5 | Page collaborateur : `/demands` | 3 |
| 6 | Page valideurs : `/request-management` | 3, 5 |
| 7 | Création : modale heures, `WorkflowNewDemandButton`, API | 5 |
| 8 | Visibilité des EbD de demande : alignement sur la règle ERoR | 0, 2, 3 |
| 9 | Affichage transversal A : popups et widgets | 3, 5, 6, 8 |
| 10 | Affichage transversal B : planning, calendriers, pointages | 0, 8, 9 |
| 11 | Pages droits : prises RC, soldes | 0, 3, 8 |
| 12 | Documentation et vérification finale | 0 à 11 |

---

## Étape 0 - Backend : demande directe estampillée sur les EbD des payloads / ✅ Terminé

Statut : fait

Objectif : tout payload qui renvoie des EbD au front porte `workflowResource { idWorkflowResource state }` et `workflowState` quand l'EbD est rattaché directement à une demande `eventByDay` (DEP, RC), avec de quoi distinguer ce cas d'une demande de déclaration (ADEC / PDEC). Aucun filtre d'état n'est ajouté : tous les états sont renvoyés, comme pour les ERoR.

Chemins relatifs à `cronexia-gta-back/app/`.

### Fichiers à modifier

- `src/resources/functions/events/event-by-day-declaration-workflow-resource.ts` : étendre `EVENT_BY_DAY_DECLARATION_WORKFLOW_RESOURCE_SELECT` avec la relation directe `workflowResource` (id, state, et `workflow { type }` si le champ est exposé sur le modèle) et `mapEventByDayDeclarationWorkflowResource` : clé directe prioritaire, déclaration en repli. Renommer le fichier et les exports en `event-by-day-workflow-resource` si le nom devient faux (à décider dans le plan détaillé).
- Appelants du select et du stamp (même dossier ou voisins) :
  - `src/resources/functions/events/resources-all-events-by-days-by-period.ts`
  - `src/resources/functions/events/times/resources-event-by-days-by-period.ts`
  - `src/resources/functions/events/resources-specific-events-by-names-by-period.ts`
  - `src/resources/functions/events/resources-specific-events-by-days-by-period.ts`
  - `src/resources/functions/events/resources-absences-list-by-period.ts`
  - `src/resources/functions/events/format-and-merge-all-events-by-resources.ts` (pose `workflowState` et `workflowResource` ligne 71)
  - `src/resources/functions/declaration/hourly/resources-declaration-hourly-grouped-by-resource-by-date.ts`
  - `src/event-by-days/event-by-days.resolver.ts` (vérifier la cohérence avec le `ResolveField` `workflowResource`, ligne 173)
- Fusions du planning : `src/resources/functions/planning/merge/merge-hourly-absences.ts` (recopie `workflowState` et `workflowResource`), `merge-daily-absences.ts` (ligne 117), et les autres fusions qui reprennent des EbD (otherEvents) : vérifier que les deux champs passent.
- Modèles : `src/resources/functions/planning/model/hourly-absence-event.model.ts` (description « déclaration horaire » devenue inexacte), `src/resources/functions/planning/interfaces/resources-planning-datas.interface.ts`, modèle des « all events » (`ResourceAllEventsByDaysModel` et lignes).
- Discriminant : confirmer que `workflow { type }` est sélectionnable sur `WorkflowResourceModel` quand l'objet est posé par le stamp (le champ `workflow` doit être résolu depuis l'id). Sinon ajouter un champ explicite sur les modèles d'event (`workflowType`).

### Documentation

- Docs des requêtes concernées (`src/resources/docs/*`) : le `workflowResource` d'un EbD peut venir d'une demande directe ou d'une déclaration.
- Fichiers `_tests_all_queries` de `src/resources` : exemples avec une demande DEP ou RC (en attente, refusée).

### Specs

- `src/resources/functions/events/event-by-day-declaration-workflow-resource.spec.ts` : demande directe, déclaration, aucune demande, priorité de la clé directe.
- Specs des fusions planning si elles existent (cas EbD à demande directe).

### Vérification

- Playground (`resourcesPlanningDatas`, `resourcesAllEventsByDaysByPeriod`, `resourcesEventByDaysByPeriod`) sur les demandes seedées de Céline Lefevre : un DEP en attente renvoie `workflowState: pending` et `workflowResource { state }`, un RC refusé renvoie `refused`. Les EbD de déclaration (ADEC / PDEC) gardent exactement leur comportement.
- Tests Jest ciblés puis suite backend (par l'équipe).

---

## Étape 1 - Fondations front : codegen, enum, libellés, allowlists / ✅ Terminé

Statut : fait

Objectif : le type `eventByDay` existe partout dans les types et constantes, sans comportement visuel nouveau, et le projet compile.

### Prérequis

- Étape 0 terminée. Backend de la branche `feat-1744-wf-events-hourly` lancé en local sur `localhost:3000`.

### Fichiers à modifier

- Régénérer les types : `bun run generate-graphql-schema-from-backend` puis `bun run codegen---generate-graphql-types-from-back` (sorties `lib/generated/types/graphql/graphql.ts`, alias `$typesGraphql`, `app/generated/graphql/schema.graphql`, `app/graphql.schema.json`). Vérifier la présence de : `WorkflowTypeEnum.EventByDay`, `WorkflowResourceTypedEventByDayModel` (et son `...LineModel`), `targetEventForTypeEventByDay`, `NestedEventByDayManyToOneForWrInput` sur `CreateWorkflowResourceInput`.
- `_utility/workflow/function/as-workflow-type-enum.ts`, `_utility/workflow/function/map-workflow-type-from-api.ts` (repli par défaut), `_utility/label/constant/workflow-type-labels.ts`, `_utility/label/function/get-workflow-type-label.ts` : libellé du type `eventByDay` (events en heures).
- `config/color-config.ts` et `routes/components/common/badge/BadgeWorkflowType.svelte` : couleur et badge.
- Les trois allowlists `WORKFLOW_TYPES` (voir constat) : ajouter `eventByDay`. Elles ne bloquent pas la liste par défaut, mais elles sont nécessaires dès qu'un appel passe `workflowType=eventByDay`.
- Corriger les erreurs de compilation dues aux `switch` exhaustifs sur `WorkflowTypeEnum` (type-check). Les adaptations cachées apparaissent ici.

### Specs

- Specs des labels et de `as-workflow-type-enum` si elles existent.

### Vérification

- `bun run type-check` sans nouvelle erreur.
- Appel `/api/workflow/resources?...&workflowType=eventByDay` accepté (pas d'erreur de validation du paramètre).

---

## Étape 2 - Lecture GraphQL : requêtes et parseurs / ✅ Terminé

Statut : fait

Prérequis : backend étape 9 (`GTA-1744-wf-events-hourly-backend.md`) — les includes de liste préchargent déjà `type`, `isRemoteWork`, `isOnCallDuty` et `isTravelling` sur `targetEventForTypeEventByDay`.

Objectif : toutes les requêtes de liste renvoient `typedEventByDay`, `eventByDays` et la cible heures (avec son `type`), et les parseurs les exposent.

### Fichiers à modifier

- `lib/graphql/resources/queries/resourcesGetWorkflowResource.ts` (et variante `resourcesGetWorkflowResourceRemoteWorkEmployee.ts` à évaluer) : bloc `typedEventByDay { dateStart dateEnd calculatedDays eventByDays { idEventByDay date timeStart timeEnd duration quantity eventOrigin event { ... } } }` et `workflow.targetEventForTypeEventByDay { labelShort code type isRemoteWork isOnCallDuty isTravelling isRightsCalculationAssociated }`. Le champ `type` est nouveau (il sert au classement, voir décisions).
- `lib/graphql/user-profile-instance/queries/userProfileInstanceGetWorkflowResource.ts` : idem côté valideur.
- `lib/graphql/workflow/queries/Workflows.ts`, `lib/graphql/workflow-tab/queries/workflowTabsForNavigation.ts`, `lib/graphql/workflow-on-workflow-tab/queries/workflowsNotAffectedToTabs.ts` : `targetEventForTypeEventByDay` (avec `type`).
- `lib/graphql/workflow-resource/mutations/createWorkflowResources.ts` : sélection de retour avec `eventByDays` (voir étape 7).
- Parseurs et types :
  - `routes/functions/cronexia/workflow-tab/parse-workflow-tabs-for-navigation.ts`
  - `routes/functions/cronexia/workflow-tab/organize/parse-organize-workflows.ts`
  - `routes/functions/cronexia/workflow/workflow-demand-details.types.ts`
  - `routes/functions/cronexia/workflow-tab/load-validator-tab-page.server.ts` (cible heures)

### Specs

- `parse-workflow-tabs-for-navigation.spec.ts` et specs du parseur organize : fixtures avec un workflow de type `eventByDay`.

### Vérification

- Playground GraphQL : `resourcesGetWorkflowResource` et `userProfileInstanceGetWorkflowResource` avec `workflowType: eventByDay` sur les demandes seedées de Céline Lefevre (septembre et octobre 2024) : `typedEventByDay` rempli, `typedEventRangeOnResource` à `null`, `targetEventForTypeEventByDay.type` à `Absence`.

---

## Étape 3 - Famille d'affichage `hourlyEvent` et mappeurs de lignes / ✅ Terminé

Statut : fait

Objectif : un workflow `eventByDay` n'est plus rendu en `generic` (période de repli = date de soumission) mais avec ses colonnes propres, sur les pages employé et valideur.

### Fichiers à modifier

- `routes/functions/cronexia/workflow-tab/display-family.types.ts` : ajouter `hourlyEvent` à `DisplayFamily` (et à la famille d'accordéon si besoin, `displayFamilyToAccordionFamily`).
- `routes/functions/cronexia/workflow-tab/resolve-display-family.ts` : `case 'eventByDay'` renvoie `hourlyEvent`, sans dépendre du nom du workflow.
- `routes/functions/cronexia/workflow-tab/families/index.ts` : enregistrer le pack dans `FAMILY_PACK_BY_ID`.
- `routes/functions/cronexia/workflow-tab/workflows-for-display-family.ts` et `families-on-tab.ts` : prendre en compte la nouvelle famille.
- Période : `routes/functions/cronexia/workflow/employee-demands-page.helpers.ts` (`RawWorkflowItem` : ajouter `typedEventByDay`, `getDateRangeFromRawItem` : branche `typedEventByDay`), `routes/functions/cronexia/workflow/workflow-resource-row-display.helpers.ts` (ordre des types, `getDateRangeFromWorkflowResourceRow`).
- Event cible : `routes/functions/cronexia/workflow/build-workflow-demand-details.ts` (lignes 39, 68, 196-197) : lire aussi `targetEventForTypeEventByDay` pour `eventLabel`, `code` et `targetEvent` quand la cible ERoR est absente.
- `routes/functions/cronexia/workflow/demand-type-visual.ts` : icône et couleur par famille.
- Routage des lignes :
  - `routes/functions/cronexia/workflow-tab/map-employee-catalog-tab-rows.ts` (branche `hourlyEvent`)
  - `routes/functions/cronexia/workflow-tab/map-validator-catalog-tab-rows.ts`
  - `routes/functions/cronexia/workflow-tab/load-validator-tab-page.server.ts` (`mapItemsByFamily`)
  - `routes/functions/cronexia/workflow-tab/build-tab-table-spec.ts` (colonnes en union, vérifier le mélange avec d'autres familles sur un même onglet)

### Fichiers à créer

- `routes/functions/cronexia/workflow-tab/families/hourly-event.family.ts` : pack `EmployeeFamilyPack` (`mapEmployeeRow`, `mapValidatorRow`, `familyColumnDefs`, `validatorFamilyColumnDefs`, `searchKeys`).
  - Modèle : `families/absence-event.family.ts`.
- `routes/functions/cronexia/workflow/hourly-event-workflow-display.helpers.ts` : période (date ou plage de dates), créneaux `HH:mm - HH:mm`, durée en h min, nombre de jours distincts.
  - Modèle : `workflow/absence-workflow-display.helpers.ts`.
- `routes/functions/cronexia/workflow/map-employee-hourly-event-from-api.ts` et `map-validator-hourly-event-from-api.ts`.
  - Modèles : `map-employee-remote-work-from-api.ts` et `map-validator-remote-work-from-api.ts` (même dossier).

### Specs

- `resolve-display-family.spec.ts`, `build-tab-table-spec.spec.ts`, specs des mappeurs et des helpers d'affichage, spec de `build-workflow-demand-details` (cible heures).

### Vérification

- Un workflow DEP affecté à l'onglet `deplacement` affiche date, créneau et durée côté collaborateur et côté valideur.

---

## Étape 4 - Page admin : organisation des onglets / ✅ Terminé

Statut : fait

Objectif : DEP et RC apparaissent correctement dans le catalogue de l'organisation et peuvent être (ré)affectés sans erreur.

Route : `routes/(app)/(without-filters)/admin/workflow/organize` (`+page.server.ts`, `+page.svelte`). Elle charge `workflowTabsForNavigation` et `workflows`, sans modale de demande. Le travail est dans les modules partagés.

### Fichiers à modifier

- `routes/functions/cronexia/workflow-tab/organize/organize-catalog-group-key.ts` et `organize-catalog-workflow-groups.ts` : groupe d'affichage `hourlyEvent` (libellé, icône).
- `routes/functions/cronexia/workflow-tab/parse-workflow-tabs-for-navigation.ts` : `iconFromDisplayFamily` pour la famille heures.
- `routes/functions/cronexia/workflow-tab/organize/organize-workflow-is-missing-target-event.ts` : alerte « cible manquante » aussi pour `eventByDay` (`targetEventForTypeEventByDay`).
- À vérifier visuellement : `OrganizeWorkflowRow.svelte`, `OrganizeWorkflowCatalogBar.svelte`, `OrganizeWorkflowTabCard.svelte` (dossier `routes/components/cronexia/workflow-tab/organize/`).

### Points d'attention

- RC est dans le pool non affecté. L'affecter à un onglet doit afficher ses demandes (étapes 5 et 6), mais la création reste indisponible (hors périmètre).

### Specs

- `organize-catalog-group-key.spec.ts`, `organize-workflow-is-missing-target-event.spec.ts`.

### Vérification

- Onglet `deplacement` visible, DEP affecté, RC déplaçable depuis le pool vers un onglet, puis retour au pool.

---

## Étape 5 - Page collaborateur : `/demands` / ✅ Terminé

Statut : fait

Objectif : le collaborateur voit, consulte, soumet (brouillon vers en attente) et annule ses demandes DEP et RC.

### Fichiers à modifier

- Chargement : `routes/(app)/(without-filters)/demands/+layout.server.ts` (route `/api/workflow/resources`) et `demands/[tab]/+layout.server.ts`. Vérifier que les demandes `eventByDay` arrivent bien dans `workflowResourcesData` (période, `ignorePeriod`).
- Onglet synthèse (`summary`) : `buildAllSynthesisRows` et colonne période pour les demandes heures (`employee-demands-page.helpers.ts`, voir étape 3).
- Détail :
  - `routes/functions/cronexia/workflow/build-workflow-demand-details.ts` (`switch (family)` ; cible heures vue à l'étape 3)
  - `routes/components/cronexia/workflow/demand-details/WorkflowDemandDetailsCard.svelte`
  - `routes/functions/cronexia/workflow/workflow-demand-consult.helpers.ts` (titre et icône : `switch (details.family)` lignes 47 et 72, conditions lignes 147, 170, 191)
  - `routes/functions/cronexia/workflow/workflow-demand-details-format.ts`
  - Afficher les lignes d'heures (date, créneau, durée), l'event cible et les PJ.
- Actions : `_utility/workflow/function/use-workflow-collab-demand-actions.svelte.ts` (soumettre, annuler) : vérifier que rien n'est conditionné au type.
- Messages d'erreur backend à traduire : `CRO_WR_000000045` et `049` (doublon, chevauchement), `046` (solde RC), `047`, `048`.
- `routes/functions/cronexia/workflow-tab/filter-employee-catalog-tabs-for-modality.ts` : famille non concernée par la modalité (heures ou jours), à confirmer.

### Specs

- `map-employee-catalog-tab-rows.spec.ts`, `workflow-demand-consult.helpers.spec.ts`, specs des détails.

### Vérification

- Employé Patrick ou Céline : liste, détail, soumission et annulation d'un brouillon DEP.

---

## Étape 6 - Page valideurs : `/request-management` / ✅ Terminé

Statut : fait

Objectif : le valideur liste, consulte, valide et refuse une demande `eventByDay`, avec des compteurs de badge corrects.

### Fichiers à modifier

- `routes/(app)/(with-filters)/request-management/+layout.server.ts` : compteurs via `workflow-resource-to-validate` (période, filtre des types).
- `routes/functions/cronexia/workflow-tab/load-validator-tab-page.server.ts` : liste par onglet (noms de workflows de l'onglet), branche `hourlyEvent` dans `mapItemsByFamily`.
- `routes/components/cronexia/workflow/ValidatorDemandsTabContent.svelte` et `ValidatorDemandsTabShell.svelte` : colonnes de la famille, liens de détail, commentaires.
- Validation et refus : `WorkflowRefuseModal`, `userProfileInstanceUpdateWrlsStatusWithCascade` (aucun changement attendu). Vérifier `_utility/workflow/function/extract-wrls-cascade-warnings.ts` pour les avertissements liés aux heures.
- Conflits à la validation (décision prise, voir « Décisions ») : `routes/functions/cronexia/workflow/describe-workflow-validation-candidate.ts` renvoie `null` pour la famille `hourlyEvent` (la demande est classée « sans conflit »). Cette fonction est partagée avec la popup de consultation et `WidgetValidationDemandes.svelte` : un seul changement couvre les trois.

### Specs

- `map-validator-catalog-tab-rows`, `build-workflow-to-validate-summary.spec.ts`, spec de `describe-workflow-validation-candidate` (cas `hourlyEvent`).

### Vérification

- Murielle valide la demande DEP du 08/10/2024 de Céline (sans fenêtre de conflit) et refuse la demande RC du 03/09/2024 ; les compteurs de badge se mettent à jour.

---

## Étape 7 - Création : modale heures et API / ✅ Terminé

Statut : fait

Objectif : un collaborateur crée et soumet une demande DEP depuis `/demands` (et depuis les points d'entrée existants de `WorkflowNewDemandButton`).

### Fichiers à créer

- `routes/components/cronexia/workflow/HourlyEventWorkflowModal.svelte` : formulaire (date, début et fin ou durée, commentaire, PJ si le modèle le prévoit), event cible affiché en lecture seule. MCP Svelte et autofixer.
- `routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.ts` : construction de `eventByDays.create` sans `event` ni `resource` ; validations côté client (heure de fin après le début). Garde repos côté backend : `assertHourliesNotOnRestSchedule`.

### Fichiers à modifier

- Branchement de la modale :
  - `routes/functions/cronexia/workflow-tab/create-modal-target-from-family.ts` : `hourlyEvent` vers `hourlyEvents`, et ajouter `hourlyEvents` à la constante `CREATE_MODAL_ITEM_IDS`.
  - `routes/components/cronexia/workflow/workflow-new-demand-items.ts` : ajouter `hourlyEvents` à l'union `WorkflowNewDemandItemId`.
  - `routes/functions/cronexia/workflow-tab/catalog-workflow-create-item-id.ts` : droit `canInputWithWorkflow` sur l'event cible heures.
  - `routes/functions/cronexia/workflow-tab/employee-tab-create-action.ts` : 0 / 1 / N choix.
  - `routes/components/cronexia/workflow/WorkflowNewDemandButton.svelte` : import dynamique.
- API : `routes/api/workflow-resource/create/+server.ts` et `update/+server.ts` (transmission de `eventByDays`), mutation `lib/graphql/workflow-resource/mutations/createWorkflowResources.ts`.
- Flux : création en brouillon puis soumission (`resourceSubmitWorkflowResource`), comme les autres modales.
- Erreurs : codes `CRO_WR_000000043` à `049` traduits en messages utilisateur.

### Décision

- Création seule : une ligne, brouillon puis soumission. Pas d'édition des lignes d'un brouillon (le backend refuse `eventByDays.create` si des lignes existent déjà, 047).

### Specs

- Helpers de création (construction du payload, validations).

### Vérification

- Création en brouillon puis passage en `pending` d'un DEP. Un deuxième envoi identique affiche l'erreur de doublon (045 ou 049).

---

## Étape 8 - Visibilité des EbD de demande : alignement sur la règle ERoR / ✅ Terminé

Statut : fait

Objectif : un EbD rattaché directement à une demande `eventByDay` (DEP, RC) est traité comme un ERoR (même règle de visibilité, mêmes cases, même bordure) et n'est plus confondu avec un EbD de déclaration (ADEC / PDEC). Cette étape ne change aucune page : elle fournit les helpers et sélections que les étapes 9 et 10 consomment. Aucune règle nouvelle : voir « Constat de départ ».

### Prérequis

- Étape 0 (le payload porte la demande directe), étapes 2 et 3.

### Sélections GraphQL

- Ajouter le discriminant choisi à l'étape 0 (`workflowResource { idWorkflowResource state workflow { type } }` ou champ dédié) dans les requêtes qui renvoient des EbD : `lib/graphql/planning/queries/resourcesPlanningDatas.ts`, `lib/graphql/events/queries/resourcesAllEventsByDaysByPeriod.ts`, `resourcesEventByDaysByPeriod.ts`, `resourcesManualEventByDaysByPeriod.ts` (à évaluer), et les requêtes d'absences en heures.

### Helpers

- `routes/functions/cronexia/event-range-on-resource/event-range-on-resource-workflow.helpers.ts` :
  - étendre `RawEventByDayWithWorkflow` (type du workflow) ;
  - ajouter une fonction de nature d'EbD : aucun workflow, via ERoR, via déclaration, via demande directe `eventByDay` ;
  - restreindre `getDeclarationWorkflowResourceId` aux EbD de déclaration ;
  - ajouter l'équivalent pour la demande directe (id de la demande) ;
  - vérifier `getEventByDayWorkflowFields` pour une demande directe : visible avec bordure selon l'état, brouillon masqué via `hideDrafts` (aucune règle de plus à ajouter) ;
  - mettre à jour le commentaire d'en-tête (« EventByDay sans EROR : toujours visible (pas de workflow) » n'est plus vrai pour une demande directe).

### Règles à confirmer sur les EbD de demande (par surface, comme les ERoR)

- Planning, calendriers, accueil : tous états affichés avec bordure ; brouillon masqué pour les autres viewers selon `IS_DISPLAY_DRAFT_REQUESTS` ; refusés et annulés masquables par la case « afficher annulés et refusés ».
- Pages de gestion des absences : saisie directe, en attente et validé seulement (`isAbsenceVisibleOnGestionPages`).
- Conflits entre events : `isConflictingWorkflowState` (un EbD en attente occupe la période ; brouillon, refusé, annulé non) : à vérifier dans `routes/functions/cronexia/event/check-timeline-event-conflicts.ts` et `planning/collective/scan-planning-draft-conflicts.ts`.
- Events réels : demande validée seulement (déjà fait côté backend).

### Consommateurs à vérifier (sans changement attendu une fois l'étape 0 faite)

- `planning/is-cancelled-or-refused-event.ts`, `planning/filter-planning-datas-draft-for-viewer.ts` (couvre déjà `hourlyAbsences`, `hourAbs`, `otherEvents`), `planning/filter-planning-workflow-resources-for-viewer.ts`, `planning/collective/planning-data.mapper.ts`, `planning/collective/filter-mapped-planning-cancelled-or-refused.ts`, `anomaly/transform-events.ts`.

Les consommateurs à corriger (affichage et clics) sont traités aux étapes 9 et 10 : `HomeEmployee.svelte` (ligne 280), `DayTimelineAccordion.svelte` (ligne 352), `summary/.../+page.svelte` (ligne 128).

### Décision

- Discriminant : `workflowResource.workflow.type` (`eventByDay` = demande directe, `declarationHours` = déclaration). Sans type, un id de demande reste une déclaration.
- Sélection dans un fragment dédié aux `eventByDays`. Le fragment partagé des absences en jours n'est pas modifié. `resourcesManualEventByDaysByPeriod` est laissé : le back n'y estampille pas la demande.
- Aucune page modifiée. Le planning collectif, les filtres et les anomalies suivent déjà l'état. Calendrier personnel, accueil et synthèse restent aux étapes 9 et 10.

### Specs

- `event-range-on-resource-workflow.helpers.spec.ts` : EbD de demande directe pour chaque état (brouillon, en attente, validé, refusé, annulé), non-régression EbD de déclaration et EbD via ERoR, `getDeclarationWorkflowResourceId` ne renvoie plus rien pour une demande directe.
- `is-cancelled-or-refused-event.spec.ts`, specs des filtres viewer, `transform-events` : cas EbD de demande directe.

### Vérification

- Planning collectif, données seedées DEP / RC de Céline Lefevre : une demande en attente apparaît avec bordure, validée elle devient un event réel, refusée elle porte la bordure refusée et disparaît quand la case « annulés et refusés » est décochée. Un EbD de déclaration (ADEC / PDEC) garde son comportement. Calendrier, accueil et synthèse : étapes 9 et 10.

---

## Étape 9 - Affichage transversal A : popups et widgets / ✅ Terminé

Statut : fait

Objectif : consulter, valider, refuser et lister une demande `eventByDay` depuis les popups et widgets existants, sans régression.

### Popups

- `routes/components/cronexia/workflow/WorkflowDemandConsultModal.svelte` : aucun changement de la modale elle-même (pas de `switch` sur le type) ; les lignes d'heures et l'event cible viennent du modèle de détail (étapes 3 et 5) et la validation sans fenêtre de conflit vient de l'étape 6. À vérifier : `buildWorkflowDemandDetailHref` (lien « Voir toutes les demandes ») avec la famille `hourlyEvent`.
- `routes/components/cronexia/calendrier-annuel/CalendarEventConsultModal.svelte`, `routes/components/cronexia/collective-schedule/modals/PlanningEventModal.svelte`, `PlanningEventDeleteModal.svelte`, `routes/components/common/accordion/DayTimelineAccordion.svelte` (`editEvent` : utiliser le discriminant de l'étape 8 ; un EbD de demande ouvre la consultation de la demande, pas la consultation de déclaration).
- `routes/functions/cronexia/event/event-modal-workflow-detail.helpers.ts`.
- L'édition d'un EbD rattaché à une demande doit respecter l'état de la demande (pas de modification directe d'une ligne de demande validée ou en attente).

### Widgets

- `routes/components/common/widgets/WidgetGererMesDemandes.svelte` et `WidgetValidationDemandes.svelte` : listes filtrées par type, ouverture de la consultation.
- `routes/components/common/home/HomeEmployee.svelte` (filtre ligne 280 : discriminant de l'étape 8), `HomeManager.svelte`, `HomeHrManager.svelte`.
- Widgets de changement d'état (valider / refuser, WRLS) : vérification seulement.

### Décision

- Timeline du jour : `resolveTimelineEventOpenTarget`. Une déclaration ouvre la consultation comme avant. Une demande directe ouvre la consultation si son modèle est dans les données de la page ; sans modèle, pas d'édition pour `pending`, `validated` ou `awaitingAttachements`.
- Accueil : une demande directe dans « autres événements » suit `isEventRangeOnResourceVisibleInPlanning`. Le raccourci déclaration ne change pas. Le bloc des absences en heures avait déjà le statut.
- Widgets « gérer mes demandes » et « demandes à valider » : déjà tous les types, dates et libellé `eventByDay` compris. Pas de filtre ajouté. Accueils manager et RH : hébergement du widget seulement. Lien « Voir toutes les demandes » : onglet choisi par le nom du workflow.
- Planning : `isEventByDayDirectMutationBlocked` refuse l'édition et la suppression d'un `EventByDay` en `pending`, `validated` ou `awaitingAttachements`. `CalendarEventConsultModal` ne fait qu'afficher.
- `resolvePlanningWorkflowForHourAbsence` reste l'étape 10 : il délègue encore aux absences en jours et renvoie `null`. Le clic planning n'ouvre donc pas encore la demande.

### Specs

Depuis `cronexia-gta-front-v2/app` :

- `src/routes/functions/cronexia/event/timeline-event-open-target.spec.ts`
- `src/routes/functions/cronexia/workflow/workflow-demand-consult.helpers.spec.ts`
- `src/routes/functions/cronexia/event/event-by-day-direct-mutation.spec.ts`

### Vérification

- Accueil employé : demande DEP en attente listée dans le widget, consultation ouverte au clic.
- Accueil manager : validation d'une demande DEP depuis le widget.
- Timeline du jour : un EbD de demande ouvre la consultation ; un EbD de déclaration ne change pas.
- Pas de modification directe d'une ligne en attente ou validée. Le clic planning qui ouvre la demande est fait à l'étape 10.

---

## Étape 10 - Affichage transversal B : planning, calendriers, pointages / ✅ Terminé

Statut : fait

Objectif : les demandes `eventByDay` apparaissent avec le bon état dans le planning, les calendriers, la synthèse, les anomalies et les pages d'absences en heures, en appliquant la règle de l'étape 8 sur le payload de l'étape 0.

### Planning

- `routes/functions/cronexia/planning/planning-workflow-resolve.helpers.ts` :
  - `RawWorkflowItem` : ajouter `typedEventByDay` ;
  - nouveau test de type d'item `eventByDay` ;
  - nouveau résolveur (par `typedEventByDay.eventByDays[].idEventByDay`, repli sur la date) appelé par `resolvePlanningWorkflowForHourAbsence` (qui délègue aujourd'hui à la version « jours » et renverrait `null`) ;
  - `resolvePlanningWorkflowFromModalClick` : brancher les catégories `hourAbs` et `otherEvents` avec `idEventByDay` sur ce résolveur ;
  - `workflowStatePriority` et `filterWorkflowCandidatesByClickStatus` : vérifier le comportement avec plusieurs demandes sur la même date.
- `routes/functions/cronexia/planning/collective/planning-data.mapper.ts` (statuts déjà dérivés de `ev.workflowResource`, à vérifier), `planning-event-resize.helpers.ts` (une ligne d'heures de demande ne se redimensionne pas librement).
- `routes/components/cronexia/collective-schedule/CollectiveSchedulePage.svelte`, `CollectiveScheduleGrid.svelte`.

### Calendriers

- `routes/functions/cronexia/calendrier-annuel/planning-data-to-events.ts` : map `hourlyAbsences` (ligne 1248) : statut issu de `workflowState` et de `workflowResource` (vérifier la dérivation via `mapWorkflowResourceStateToPlanningStatus`, pas seulement `workflowState`), pas de filtre de visibilité aujourd'hui sur les EbD : appliquer la règle de l'étape 8 ; ne pas confondre avec la pastille « hour-wf » réservée aux EbD générés.
- `routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.ts` (« Demandes en cours ») :
  - `WorkflowMeta` : ajouter `targetEventForTypeEventByDay { code labelShort type }` ;
  - `classifyPendingWorkflow` : pour `eventByDay`, classement par le type de l'event cible (`Absence` donne `absence`, `Presence` et `Neutral` donnent `other`), pas par code ni par nom ; DEP et RC sortent donc en `absence` ;
  - `eventCode` : lire aussi la cible heures ;
  - `periodStart` / `periodEnd` (AM / PM) non applicables aux heures.
- `index-calendar-events-by-date.ts`, `render-day-absences.ts`, `calendar-event-consult.helpers.ts`, `routes/functions/cronexia/calendar/calendar-day-hours.ts`, `routes/functions/cronexia/planning/home-planning-widget.helpers.ts`.
- `routes/components/cronexia/calendrier-annuel/PersonalCalendarPage.svelte`, `CalendarDayCell.svelte`.

### Pointages, synthèse, anomalies, absences en heures

- `routes/(app)/(with-filters)/summary/.../+page.svelte` (ligne 128) et `routes/functions/cronexia/anomaly/transform-events.ts` : un EbD de demande en attente ou refusée ne doit produire ni anomalie ni doublon.
- `routes/components/cronexia/absence/HoursAbsence.svelte`, `HoursAbsenceArrayTr.svelte`, `routes/functions/cronexia/event-by-day/parse-event-by-day.ts` : drapeau `workflowResourceId` et état déjà portés ; appliquer la règle des pages de gestion (saisie directe, en attente, validé) via `isAbsenceVisibleOnGestionPages`.
- `routes/functions/cronexia/event/check-timeline-event-conflicts.ts` : conflits de créneaux avec une ligne de demande (règle `isConflictingWorkflowState`).

### Décision

- Clic planning : `resolvePlanningWorkflowForHourAbsence` ne délègue plus aux jours. Une demande est reconnue seulement si `workflow.type` vaut `eventByDay`. Match par `idEventByDay`, sinon par la date de `typedEventByDay`. Deux demandes le même jour se départagent par l'état cliqué. `workflowStatePriority` n'a pas changé. La page envoie une ligne avec `idEventByDay` et sans plage jours vers ce résolveur. Le mapper, la bordure de la grille et le refus de déplacement d'une ligne liée à une demande étaient déjà en place.
- Calendrier : les saisies en heures prennent le statut via `getEventByDayWorkflowFields` et sortent en pastille `hour-input`. La pastille `hour-wf` reste réservée aux événements générés. Les barres d'heures utilisent la bordure du statut. `PersonalCalendarPage` et `CalendarDayCell` n'ont pas changé.
- Demandes en cours : une demande `eventByDay` est classée par le type de l'event cible (`Absence` → absence, `Presence` ou `Neutral` → autre). Le code affiché vient de cette cible. Pas de demi-journée.
- Synthèse et timeline : une demande directe en attente ou refusée n'est plus marquée anomalie éditable. La bordure de statut reste. Les absences en heures filtrent déjà par `isAbsenceVisibleOnGestionPages`. `parse-event-by-day` copie déjà l'état. Les conflits occupent déjà le créneau selon `isConflictingWorkflowState`.

### Specs

Depuis `cronexia-gta-front-v2/app` :

- `src/routes/functions/cronexia/planning/planning-workflow-resolve.helpers.spec.ts`
- `src/routes/functions/cronexia/calendrier-annuel/planning-data-to-events.hour-absences.spec.ts`
- `src/routes/functions/cronexia/calendrier-annuel/calendar-pending-requests.helpers.spec.ts`
- `src/routes/functions/cronexia/anomaly/transform-events.spec.ts`

### Vérification

- Une demande DEP en attente apparaît en pending dans le calendrier personnel et le planning, avec la même bordure qu'une absence en attente ; validée elle devient un event réel ; refusée elle porte la bordure refusée. Même contrôle sur la synthèse et les anomalies.
- « Demandes en cours » : la demande DEP en attente est classée absence et suit les filtres d'absences.
- Clic sur une ligne d'heures de demande dans le planning : la demande s'ouvre.

---

## Étape 11 - Pages droits : prises RC, soldes / ✅ Terminé

Statut : fait

Objectif : les pages `rights` reflètent les demandes RC en heures, sans erreur ni double comptage.

### Fichiers à modifier

- Employé : `routes/components/cronexia/rights-employee/fetch-employee-rights-take-ranges.ts` et `employee-rights-takes.ts`. Les prises RC viennent aujourd'hui de `eventRangeByDays`. Ajouter les EbD RC (requête EbD avec `workflowResource.state`, disponible grâce à l'étape 0) et appliquer la règle de comptage (sans demande, validée ou en attente), alignée sur l'étape 8.
- `routes/components/cronexia/rights-employee/employee-rights-balances.ts` : DRC reste sur `ArResourceBalance` (pas de repli compteur).
- Page legacy `vacation-rights` : `routes/functions/cronexia/vacation-rights/resolve-workflow-right-key.ts`, `routes/components/cronexia/vacation-rights/VacationRightsDemandsSection.svelte`, `routes/components/cronexia/workflow/AbsenceWorkflowSoldePanel.svelte` (clés `cp|rtt|tt`) : décider d'ajouter la clé `rc` pour afficher ou filtrer les demandes RC.

### Points d'attention

- Les soldes DRC (`ArResourceBalance`, seeds de la grande étape 2 du backend) ne sont pas lus par la garde de solde (plafond 35 h en dur). Le front peut afficher un solde DRC de 6,5 h et un plafond différent à la création : incohérence connue, à ne pas masquer.
- Pages RH `rights/individual|collective` : aucune modification.

### Décision

- Pas de clé `rc`. `resolveWorkflowRightKey` reste `null` pour un `eventByDay` dont l'event est `RC`, même avec `isRightsCalculationAssociated`. La page legacy `vacation-rights`, `VacationRightsDemandsSection` et `AbsenceWorkflowSoldePanel` ne changent pas. Les demandes RC n'y sont ni listées ni filtrées. Pages RH : rien.
- Le solde de la carte DRC reste `ArResourceBalance` (Maxime : 6,5 h, pris 3,5 h). Aucun repli sur les compteurs CP / RTT / TT. Valider une demande RC ne bouge pas ce chiffre. L'écart avec le plafond 35 h à la création n'est pas masqué.
- Les prises du graphique : plages `eventRangeByDays`, plus les `EventByDay` de code `RC` sans demande ou en demande directe (`workflow.type` `eventByDay`). Comptées : sans demande, `validated`, `pending`. Écartées : brouillon, refusé, annulé, justificatif, déclaration (ADEC / PDEC), autre code. `idEventRangeOnResource` n'est pas sur `EventByDay` (seulement sur le payload fusionné) : il n'est pas ajouté à `resourcesEventByDaysByPeriod`. Le mapper écarte quand même une ligne qui porterait cet id, pour ne pas compter deux fois une absence en jours.
- Le pot DRC n'a pas d'exercice : le graphique charge ces prises (année civile), pas le journal. CP / RTT avec exercice restent sur le journal. Les deux sources ne sont jamais additionnées.
- Pas de régénération des types générés.

### Specs

Depuis `cronexia-gta-front-v2/app` :

- `src/routes/components/cronexia/rights-employee/employee-rights-takes.spec.ts`
- `src/routes/components/cronexia/rights-employee/employee-rights-balances.spec.ts`
- `src/routes/functions/cronexia/vacation-rights/resolve-workflow-right-key.spec.ts`

### Vérification

- Maxime : solde DRC 6,5 h, prise en heures cohérente après validation d'une demande RC. Une demande en attente est déjà dans le graphique ; une demande refusée n'y est pas.

---

## Étape 12 - Documentation et vérification finale / ✅ Terminé

Statut : doc faite, vérification par l'équipe en attente

### Fichiers à modifier

- `routes/api/README.md` et READMEs de `routes/functions/cronexia/workflow-tab/` : type `eventByDay`, famille `hourlyEvent`, règle de visibilité.
- `cronexia-suivi-2/suivi/11-novembre/261120-suivi.md` (ou le suivi du jour) : section tests front GTA-1744.
- Backend : plan `GTA-1744-wf-events-hourly-backend.md` (mentionner l'étape 0 de ce plan) et README des payloads EbD si besoin.
- Régénérer les types front si le backend a changé depuis l'étape 1.

### Décision

- Pas de régénération des types front.
- Docs de payload EbD déjà à jour (demande directe ou déclaration, clé directe prioritaire, aucun filtre d'état) : non réécrites.
- README unique `routes/functions/cronexia/workflow-tab/README.md` : famille `hourlyEvent`, visibilité alignée sur les ERoR. Note `eventByDay` ajoutée dans `routes/api/README.md`.
- Checklist front dans `cronexia-suivi-2/suivi/11-novembre/261123-suivi.md`. Le plan backend mentionne l'étape 0 de ce plan.

### Vérification (par l'équipe)

- `bun run type-check`, lint, vitest ciblé puis suite complète ; Jest backend pour l'étape 0.
- Scénario manuel de bout en bout sur DEP et RC : création, soumission, validation, refus, annulation, sur les trois pages principales (admin organize, `/demands`, `/request-management`).
- Contrôle visuel : calendriers, planning, accueil, widgets, pages droits.
- Non-régression : ERoR (absences, télétravail), changement d'horaire, pointages, déclarations jours et heures, EbD de déclaration (ADEC / PDEC).

## Risques et points ouverts

- Étape 0 : résolu. Le stamp pose `workflow { type }` (`event-by-day-workflow-resource.ts`, fichier renommé). Les requêtes front le sélectionnent.
- Étape 1 : résolu. Les `switch` et `Record<WorkflowTypeEnum, …>` couvrent `eventByDay`.
- Édition d'un brouillon : tranché à l'étape 7. Création seule, pas d'édition des lignes. Le back refuse `eventByDays.create` si des lignes existent déjà (047).
- Point d'entrée de création RC : hors GTA-1744, toujours ouvert.
- Cohérence entre le plafond RC en dur (2100 min) et les soldes DRC affichés : toujours ouvert, écart non masqué (étape 11).
- Contrôle de conflits à la validation pour les EbD : volontairement absent, à rouvrir si le métier le demande.
