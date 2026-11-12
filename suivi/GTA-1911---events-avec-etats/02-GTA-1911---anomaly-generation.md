# GTA-1911 / Génération des anomalies selon l'état des events

Découpe de [01-GTA-1911---ticket-de-base.md](01-GTA-1911---ticket-de-base.md), lignes « génération des anomalies » (états Annulé / Brouillon / Refusé, et état A valider).

Un event compte pour le générateur d'anomalies seulement s'il n'a pas de workflow, ou si sa demande est à l'état Validé. Tout autre état est ignoré, y compris pour les anomalies de conflit (CONFLIMLTP, CONFLIMLTPNEUTRE, CONFLIEXCL, CONFLIOVRL). Les conflits d'une demande A valider restent portés par le contrôle de chevauchement à la saisie, qui est un autre ticket.

Le filtre est livré par Ferhat le 12/11/2026, commit `4f6cb56a` sur `hfix-1789-ajustement` (pas encore dans `main`). Jours et heures : sans workflow, ou `validated`. A valider ne compte plus. La popup de conflit le compte toujours. Les branches GTA-1789 ont été effacées, pas commentées.

Hors de ce ticket : compteurs ([GTA-1915](https://cronexia.atlassian.net/jira/browse/GTA-1915)), conflits à la saisie, affichage des états dans le front.

Estimation proposée : ⏱️ ~1 j (le 0,1 j du ticket de base ne couvre que le filtre). À confirmer après les deux questions PO en fin de ticket.

---

## Règle cible

`WorkflowStateEnum` dans `cronexia-gta-back\app\prisma\schema\workflow.prisma`.

| État | Effet sur la génération |
| --- | --- |
| Pas de workflow (`workflowResourceId` null, saisie admin / gestionnaire) | Compte |
| `validated` — Validé | Compte |
| `pending` — A valider | Ignoré (livré sur `hfix-1789-ajustement`) |
| `awaitingAttachements` — En attente de justificatif | Ignoré avec A valider (le commentaire du commit le dit ; à confirmer PO) |
| `draft` — Brouillon | Ignoré |
| `refused` — Refusé | Ignoré |
| `cancelled` — Annulé | Ignoré |

Même règle pour une absence en jours (`EventRangeOnResource`), une absence en heures (`EventByDay`) et une déclaration en heures. Les écarts ADEC / PDEC d'une déclaration ne comptent qu'une fois la déclaration validée, comme les autres events de cette déclaration.

---

## État des lieux

Le filtre du générateur, sur `hfix-1789-ajustement` (`4f6cb56a`, pas encore dans `main`), est une liste blanche dans `build-counted-workflow-state-where.ts` :

- Jours : `workflowResourceId` null, ou `workflowResource.state = validated`.
- Heures : saisie directe, déclaration sans demande, ou déclaration `validated`. La branche qui laissait passer un event saisi d'une déclaration en attente est retirée. ADEC / PDEC n'ont plus de cas particulier : ils passent par la même branche `validated`.
- `pending` et `awaitingAttachements` ne passent plus. `WORKFLOW_STATES_NOT_COUNTED_AS_INPUT` et `DECLARATION_DEVIATION_EVENT_IDS` sont retirés du fichier.
- Le spec `build-counted-workflow-state-where.spec.ts` attend déjà « null ou `validated` » pour les deux fonctions.

`main` a encore la liste noire GTA-1789 (`notIn [draft, refused, cancelled]`), qui laisse passer A valider. Le comportement décrit ci-dessus arrive avec le merge de la branche.
- Le générateur ne relit pas l'état au moment d'écrire les anomalies. Il consomme les events déjà filtrés par `resourcesManualEventRangeByDaysByPeriod` et `resourcesManualEventByDaysByPeriod`. Changer le filtre suffit pour le calcul. Ça ne suffit pas pour les journées déjà générées.

Régénération aujourd'hui quand une demande change d'état :

- Une surcharge d'horaire qui passe à `validated` empile la génération des jours passés (`enqueueEventGenerationAfterScheduleOverloadValidated`, appelé depuis `userProfileInstanceUpdateWrlsStatusWithCascade`).
- Les autres sujets (absence, déclaration) n'empilent rien à la validation.
- La soumission d'un workflow sans valideur passe la demande à `validated` et ne recalcule que les compteurs.
- L'annulation d'une demande validée sans valideur supprime la demande et son event, et ne régénère pas.

Conséquence sur les données déjà en base : une absence A valider a pu clôturer une anomalie (ABSINJ, PNA, conflit). Cette clôture reste en base tant que la période n'est pas régénérée.

---

## Ce qu'il convient de faire

### 1. Filtre : sans workflow, ou Validé

Livré sur `hfix-1789-ajustement`, commit `4f6cb56a` (12/11/2026, Ferhat). Pas encore dans `main`.

`buildCountedWorkflowStateWhere` et `buildCountedDeclarationEventByDayWhere` ne gardent que la saisie sans workflow et l'état `validated`. Le commentaire du fichier dit que brouillon, en attente de validation, en attente de justificatif, refusée et annulée sont ignorées, et que la popup de conflit compte encore « en attente ».

Écart avec ce ticket : les branches GTA-1789 ont été effacées, pas commentées. `WORKFLOW_STATES_NOT_COUNTED_AS_INPUT` aussi. Les rétablir demande de les réécrire. Si on veut garder la marche arrière dans le fichier, les remettre en commentaire sur cette branche, avec un `// TODO:` « règle GTA-1789, décommenter si A valider doit de nouveau compter ».

Le même commit supprime `merge-same-attendance-manual-events.ts` et son spec, sans appelant depuis `bdd79147`. Le comportement vivant est `resolvingManualEventCoverage`.

### 2. Régénérer quand la demande entre dans Validé, ou le quitte

`enqueueEventGenerationForPastPeriod` borne déjà la période à hier. Aujourd'hui et le futur restent ignorés.

Entrées dans Validé, l'event commence à compter, il faut empiler :

- Soumission d'un workflow à 0 niveau. `resourcesSubmitWorkflowResource` appelle `resolveDemandStateWithoutValidator` : le brouillon soumis en `pending` devient `validated`. Le recalcul des compteurs est déjà là (`enqueueCounterRecalcForWrEventRange`). La génération d'events ne l'est pas.
- Validation du dernier niveau, ou outrepassement qui ne laisse plus aucun niveau `pending` / `awaitingAttachements`. `buildValidatedWorkflowResourcePatch` pose alors `state: validated`, appliqué dans `userProfileInstanceUpdateWrlsStatusWithCascade`. L'empilement actuel ne part que si `workflow.type === scheduleOverload`.

Sortie de Validé, l'event cesse de compter, il faut empiler :

- Annulation d'une demande validée sans valideur (`workflowLevels` à 0) dans `resourcesCancelWorkflowResource`. La demande et son sujet sont supprimés (`deleteWorkflowResourceCascade` : `EventRangeOnResource` et ses jours, `EventByDay` de la déclaration, lignes de surcharge d'horaire). Ce n'est pas un passage à `cancelled`. Les dates sont à lire avant la suppression, et l'empilement se fait après le commit, sur le même modèle que la génération après changement de cycle dans `resources.service.ts`.

Généraliser `enqueueEventGenerationAfterScheduleOverloadValidated` en un seul empilement, appelé à la place de l'actuel, pour ne pas empiler deux fois une surcharge d'horaire. La période dépend du sujet de la demande :

- `eventRangeOnResource` : `dateStart` → `dateEnd`
- `declaration` : dates des `DeclarationDaily` / `DeclarationHourly`
- `scheduleOverLoads` : `effectDate` min → max (comportement actuel de `scheduleOverloadGenerationPeriod`)

Transitions qui ne franchissent pas Validé. Avec le nouveau filtre, les deux états ignorent l'event, aucun empilement :

- Brouillon → A valider, ou → En attente de justificatif (`resourcesSubmitWorkflowResource`, workflow avec niveaux).
- A valider ↔ En attente de justificatif (`recomputeDeferredDemandStateAfterWrlsValidated`).
- A valider ou En attente de justificatif → Refusé. Le validateur ne peut agir que sur ces deux états (`isWrActionableForValidator`). L'auto-refus pour délai de pièces jointes (`applyDeferredAttachmentDeadlineAutoRefuse`) part des mêmes états.
- Suppression d'un brouillon ou d'une demande encore en attente (`resourcesCancelWorkflowResource`, première branche).

Annulation d'une demande validée qui a des valideurs : non implémentée. `resourcesCancelWorkflowResource` lève `CRO_WR_000000008` (TODO demande d'annulation). Le jour où elle existera, elle devra empiler la génération. Rien à coder pour ce cas dans ce ticket.

Demandes de pointage (`clockingOverload`) : le filtre d'état des events ne les lit pas. Ne pas ajouter un second empilement si l'enregistrement du pointage régénère déjà (`clockings.service.ts` appelle `resourcesGenerateEventsByPeriod`).

### 3. Données déjà générées

Les anomalies déjà clôturées par une demande A valider restent en l'état jusqu'à une régénération de la période. Refuser ou supprimer cette demande ne les rouvre pas : les deux états sont ignorés, et aucun des chemins ci-dessus n'empile. Décision PO en fin de ticket : régénération ponctuelle, ou correction au fil de l'eau.

---

## Inventaire des impacts

### Fichiers dont le résultat change

Les deux requêtes appliquent le filtre. Tout ce qui les appelle hérite du changement.

- `cronexia-gta-back\app\src\resources\functions\events\times\resources-manual-event-range-by-days-by-period.ts`
- `cronexia-gta-back\app\src\resources\functions\events\times\resources-manual-event-by-days-by-period.ts`

Chaîne de génération, dans l'ordre :

1. `resource-merge-manual-events-times-by-day.ts`
2. `resource-merge-times-by-day.ts`
3. `resources-generate-events-query-by-period.ts` (CONFLIMLTP, CONFLIMLTPNEUTRE, CONFLIEXCL, CONFLIOVRL, ABSINJ, PNA, couverture d'absence)
4. `resources-generate-events-by-period.ts` (supprime les events générés de la période, réécrit events et instances d'anomalies)

Requêtes GraphQL qui exposent ces fonctions dans `resources.resolver.ts` :

- `resourcesManualEventByDaysByPeriod`
- `resourcesManualEventRangeByDaysByPeriod`
- `resourceMergeManualEventsTimesByDay`
- `resourceMergeTimesByDay`
- `resourcesGenerateEventsQueryByPeriod`
- `resourcesGenerateEventsByPeriod`

Front : `cronexia-gta-front-v2\app\src\routes\api\event\resources-manual-event-by-days-by-period\+server.ts` appelle la requête du même nom. Aucun autre fichier du front ne référence cette route ni son helper GraphQL. Un appel manuel de la route renverra moins d'events (les demandes A valider sortent). Aucun écran ne s'en sert.

Régénérations déjà en place, déclencheur inchangé, nouveau filtre appliqué au passage :

- Édition de pointage, `clockings.service.ts` → `resourcesGenerateEventsByPeriod`.
- Changement de cycle, `resources.service.ts` → `enqueueEventGenerationForPastPeriod`.
- File `event-generation-queue.processor.ts`.

### Effets métier attendus

- Une absence A valider sur un jour passé laisse l'anomalie d'absence ouverte (ABSINJ). Elle se ferme quand la demande passe à Validé, via l'empilement, sans régénération lancée à la main.
- Une demande A valider ne produit pas de CONFLI* avec une autre saisie. Deux events Validés (ou sans workflow) qui se chevauchent continuent d'en produire.
- Une anomalie déjà marquée RESOLUE, traitée ou acquittée, dont la clé n'est plus émise, suit le comportement actuel de `resourcesGenerateEventsByPeriod` (statut selon la criticité, pas de doublon). Si la période est régénérée alors que la demande est encore A valider, une anomalie que cette demande avait fermée se rouvre.

### Déjà conforme, à ne pas retoucher

- Surcharge d'horaire : `scheduleOverloadGenerationPeriod` ne renvoie une période que pour `scheduleOverload` + `validated`. `resources-schedule-instances-core-by-period.ts` ne charge une surcharge que si elle n'a pas de workflow ou si la demande est `validated`.
- Surcharge des pointages théoriques 2 et 3 utilisée pour la plage repas : `resource-merge-times-by-day.ts` ne prend la déclaration que si `workflowResource.state = validated`.

### Hors impact (un autre filtre, un autre ticket)

- Reporting absences : `resources-manual-event-by-days-by-period-absence-only.ts` et `resources-event-range-on-resources-by-period-absence-only.ts`. Le second sélectionne `workflowResource.state` pour l'affichage, il ne filtre pas avec `buildCountedWorkflowStateWhere`.
- Fusion planning : `merge-daily-absences.ts`, `merge-hourly-absences.ts`, `merge-other-events.ts`.
- Chevauchement à la saisie : `build-event-range-on-resource-overlap-where.ts` (exclut `refused` et `cancelled`, garde `draft` et `pending`). Le popup front `isConflictingWorkflowState` a sa propre liste.
- Compteurs et sommes de quantités : `buildEventRangeOnResourceWhereForQuantitySum` dans `resources.service.ts` (réalisé = validé, prévisionnel = validé + A valider). GTA-1915.
- Demandes de modification de pointage : `Clocking.workflowResourceId` n'a pas de filtre d'état dans les entrées du générateur. À traiter avec le sujet pointage, pas ici.

---

## Non-régression

### Specs à mettre à jour

À lancer à la main.

- `build-counted-workflow-state-where.spec.ts` : déjà à jour dans `4f6cb56a`. Les deux fonctions attendent « null ou `validated` ». Relancer à la main sur la branche.
- `user-profile-instance-update-wrls-status-with-cascade.spec.ts` : l'empilement part pour une absence ou une déclaration qui atteint `validated`, et continue de partir une seule fois pour une surcharge d'horaire validée.
- `resources-cancel-workflow-resource.spec.ts` : empilement après suppression d'une demande validée sans valideur, avec les dates lues avant le delete. Pas d'empilement pour un brouillon ou une demande encore en attente.
- `resources-submit-workflow-resource.spec.ts` : empilement quand la soumission sans valideur pose `validated`. Pas d'empilement pour une soumission qui reste `pending` ou `awaitingAttachements`.
- Spec de la fonction d'empilement généralisée : période selon le sujet, rien à empiler si l'état résultant n'est pas `validated` (hors annulation), rien si la période clampée à hier est vide.

### Recette sur un jour passé

Pour chaque état : absence en jours, absence en heures, déclaration en heures. Résultat attendu : anomalie d'absence ouverte pour tous les états sauf Validé et saisie sans workflow.

| État de la demande | Anomalie d'absence | Conflit avec un autre event Validé |
| --- | --- | --- |
| Pas de workflow | Fermée par l'event | Oui s'il y a chevauchement |
| Validé | Fermée par l'event | Oui s'il y a chevauchement |
| A valider | Ouverte | Non |
| En attente de justificatif | Ouverte | Non |
| Brouillon | Ouverte | Non |
| Refusé | Ouverte | Non |
| Annulé | Ouverte | Non |

Transitions, sans bouton de régénération :

- A valider → Validé : l'anomalie se ferme.
- Validé → suppression (workflow sans valideur, dans le délai) : l'anomalie se rouvre.
- A valider → Refusé : l'anomalie reste ouverte. Rien ne change.
- Validation d'un niveau intermédiaire (la demande reste A valider) : l'anomalie reste ouverte.

Comportements inchangés à rejouer :

- Saisie directe sans workflow.
- Chevauchement de deux events Validés : CONFLI* toujours émis.
- Surcharge d'horaire validée : les jours passés se régénèrent encore, une seule fois.
- Anomalie déjà traitée ou acquittée : pas de doublon à la régénération.
- Jour courant et jours futurs : toujours exclus de la génération.
- Édition d'un pointage sur la période : la régénération existante tourne encore, avec le nouveau filtre.

### Jeux de données

Les seeds décrivent des modèles de workflow, pas une instance par état. Recette : faire vivre la demande.

- Modèles : `cronexia-gta-back\app\prisma\seeds-new\02-recommended\workflow\workflow.seed.md`
- Télétravail sans valideur (soumission → Validé, annulation → suppression) : template `WORKFLOW_EVENT_TT_NO_VALIDATOR` dans ce fichier.
- Enfant malade, pièces jointes en différé (état En attente de justificatif) : template `SICK_CHILD_ATTACHMENT_REQUIRED_DEFERRED`.
- Instances déjà seedées, point de départ : `workflow-resource\remote-work-by-event-range-on-resource\workflow-resource-01-maxime-c-tt-event-validation.md` et `workflow-resource\schedule-overload\workflow-resource-02-patrick-so-2-validations.md`.

---

## Questions PO

1. `awaitingAttachements` est ignoré avec A valider dans `4f6cb56a` (le commentaire du fichier le dit). À confirmer.
2. Anomalies déjà clôturées par une demande A valider : régénération ponctuelle des périodes concernées, ou correction à la prochaine génération naturelle de ces journées ?

---

## Dev

### Emplacements des fichiers

- Règle d'état
  - `cronexia-gta-back\app\src\resources\functions\events\times\build-counted-workflow-state-where.ts`
  - spec : `build-counted-workflow-state-where.spec.ts` (même dossier)
- Requêtes qui appliquent la règle
  - `cronexia-gta-back\app\src\resources\functions\events\times\resources-manual-event-range-by-days-by-period.ts`
  - `cronexia-gta-back\app\src\resources\functions\events\times\resources-manual-event-by-days-by-period.ts`
- Génération
  - `cronexia-gta-back\app\src\resources\functions\events\generate\resources-generate-events-query-by-period.ts`
  - `cronexia-gta-back\app\src\resources\functions\events\generate\resources-generate-events-by-period.ts`
  - empilement : `cronexia-gta-back\app\src\resources\functions\events\generate\queue\enqueue-event-generation-for-past-period.ts`
- Déclencheurs à brancher
  - validation : `cronexia-gta-back\app\src\user-profile-instances\functions\workflow-resource\user-profile-instance-update-wrls-status-with-cascade.ts`
  - empilement actuel, à généraliser : `cronexia-gta-back\app\src\user-profile-instances\functions\workflow-resource\functions\enqueue-event-generation-after-schedule-overload-validated.ts`
  - période surcharge : `cronexia-gta-back\app\src\resources\functions\events\generate\schedule-overload-generation-period.ts`
  - soumission sans valideur : `cronexia-gta-back\app\src\resources\functions\workflow-resource\resources-submit-workflow-resource.ts`
  - état sans valideur : `cronexia-gta-back\app\src\workflow-resources\functions\resolve-demand-state-without-validator.ts`
  - annulation / suppression : `cronexia-gta-back\app\src\resources\functions\workflow-resource\resources-cancel-workflow-resource.ts`
  - cascade de suppression : `cronexia-gta-back\app\src\resources\functions\workflow-resource\delete-workflow-resource-cascade.ts`
- Enum
  - `cronexia-gta-back\app\prisma\schema\workflow.prisma` (`enum WorkflowStateEnum`)
- Seeds
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\workflow\workflow.seed.md`
