# GTA-1911 / Génération des anomalies selon l'état des events / ✅ Done

Découpe de [01-GTA-1911---ticket-de-base.md](01-GTA-1911---ticket-de-base.md), lignes « génération des anomalies » (états Annulé / Brouillon / Refusé, et état A valider).

Un event compte pour le générateur d'anomalies seulement s'il n'a pas de workflow, ou si sa demande est à l'état Validé. Tout autre état est ignoré, y compris pour les anomalies de conflit (CONFLIMLTP, CONFLIMLTPNEUTRE, CONFLIEXCL, CONFLIOVRL). Les conflits d'une demande A valider restent portés par le contrôle de chevauchement à la saisie, qui est un autre ticket.

Le filtre est dans `main` depuis la PR #96 (`cba79633`, commit `4f6cb56a`, 12/11/2026, Ferhat). Jours et heures : sans workflow, ou `validated`. A valider ne compte plus. La popup de conflit le compte toujours. Les branches GTA-1789 ont été effacées, pas commentées. Ce chantier ne les rétablit pas.

La régénération à l'entrée et à la sortie de Validé est livrée sur `feat-1911-events-states-impacts`. Aujourd'hui et le futur restent exclus. Pas de régénération ponctuelle des journées déjà en base.

Hors de ce ticket : compteurs ([GTA-1915](https://cronexia.atlassian.net/jira/browse/GTA-1915)), conflits à la saisie, affichage des états dans le front.

---

## Règle cible

`WorkflowStateEnum` dans `cronexia-gta-back\app\prisma\schema\workflow.prisma`.

| État | Effet sur la génération |
| --- | --- |
| Pas de workflow (`workflowResourceId` null, saisie admin / gestionnaire) | Compte |
| `validated` — Validé | Compte |
| `pending` — A valider | Ignoré (dans `main` depuis la PR #96) |
| `awaitingAttachements` — En attente de justificatif | Ignoré avec A valider. Le filtre mergé le dit. Ce chantier ne le rouvre pas |
| `draft` — Brouillon | Ignoré |
| `refused` — Refusé | Ignoré |
| `cancelled` — Annulé | Ignoré |

Même règle pour une absence en jours (`EventRangeOnResource`), une absence en heures (`EventByDay`) et une déclaration en heures. Les écarts ADEC / PDEC d'une déclaration ne comptent qu'une fois la déclaration validée, comme les autres events de cette déclaration.

---

## Filtre

Liste blanche dans `build-counted-workflow-state-where.ts`, déjà dans `main` :

- Jours : `workflowResourceId` null, ou `workflowResource.state = validated`.
- Heures : saisie directe, déclaration sans demande, ou déclaration `validated`. ADEC / PDEC passent par la même branche `validated`.
- `pending` et `awaitingAttachements` ne passent plus.
- Le spec `build-counted-workflow-state-where.spec.ts` attend « null ou `validated` » pour les deux fonctions.

Le générateur ne relit pas l'état au moment d'écrire les anomalies. Il consomme les events déjà filtrés par `resourcesManualEventRangeByDaysByPeriod` et `resourcesManualEventByDaysByPeriod`. Le filtre suffit pour le prochain calcul. Il ne corrige pas les journées déjà générées : d'où l'empilement ci-dessous.

---

## Régénération livrée

`enqueueEventGenerationForPastPeriod` borne la période à hier. Aujourd'hui et le futur restent ignorés.

`workflowResourceGenerationPeriod` donne la période selon le sujet, sans regarder l'état. L'appelant tranche l'entrée ou la sortie de Validé.

- `eventRangeOnResource` : `dateStart` → `dateEnd`
- `declarationDays` : dates des `DeclarationDaily`
- `declarationHours` : dates des `DeclarationHourly`
- `scheduleOverload` : `effectDate` min → max
- `clockingOverload` et `remoteWorkByScheduleTypeOverload` : rien. Le pointage régénère déjà (`clockings.service.ts` appelle `resourcesGenerateEventsByPeriod`). Pas de second empilement.

`enqueueEventGenerationForWorkflowResource` enchaîne les deux. Il remplace `enqueueEventGenerationAfterScheduleOverloadValidated` et `scheduleOverloadGenerationPeriod`. Une surcharge d'horaire validée n'empile qu'une fois.

Les resolvers n'injectent pas la file (`EventGenerationQueueModule` importe `ResourcesModule`). `ResourcesService.enqueueEventGenerationForWorkflowResource` passe par le `moduleRef` déjà en place.

Entrée dans Validé, l'event commence à compter :

- Dernier niveau validé, ou outrepassement qui ne laisse plus aucun niveau `pending` / `awaitingAttachements`. `userProfileInstanceUpdateWrlsStatusWithCascade` empile si l'état de la demande après cascade est `validated`. Un niveau intermédiaire laisse la demande `pending` : rien.
- Soumission d'un workflow à 0 niveau. `resourcesSubmitWorkflowResource` : le brouillon soumis en `pending` devient `validated` (`resolveDemandStateWithoutValidator`). L'empilement est à côté du recalcul des compteurs.

Sortie de Validé, l'event cesse de compter :

- Annulation d'une demande validée sans valideur (`workflowLevels` à 0) dans `resourcesCancelWorkflowResource`. La demande et son sujet sont supprimés. Ce n'est pas un passage à `cancelled`. Les dates sont déjà dans `wr` (`WORKFLOW_RESOURCE_RESOURCES_CANCEL_INCLUDE`), lues avant le delete. L'empilement est après le commit, seulement si la suppression a réussi.
- Mutation `deleteWorkflowResource` (`workflow-resources.resolver.ts`). Elle supprime n'importe quelle demande, validée comprise. Avant la cascade, une lecture charge l'état et les dates. Après le delete, empilement seulement si l'état était `validated` (`enqueueEventGenerationIfWorkflowResourceWasValidated`).

Rien à empiler quand les deux états ignorent déjà l'event :

- Brouillon → A valider, ou → En attente de justificatif.
- A valider ↔ En attente de justificatif.
- A valider ou En attente de justificatif → Refusé, y compris l'auto-refus pour délai de pièces jointes.
- Suppression d'un brouillon ou d'une demande encore en attente (première branche de `resourcesCancelWorkflowResource`, et `deleteWorkflowResource` hors `validated`).

Annulation d'une demande validée qui a des valideurs : non implémentée. `resourcesCancelWorkflowResource` lève `CRO_WR_000000008`. Le jour où elle existera, elle devra empiler. Rien codé pour ce cas.

---

## Données déjà générées

Décision : pas de régénération ponctuelle. Une anomalie déjà clôturée par une demande A valider reste en l'état jusqu'à la prochaine génération naturelle de la journée (édition de pointage, changement de cycle, ou une des transitions ci-dessus). Refuser ou supprimer cette demande ne la rouvre pas : les deux états sont ignorés, et ces chemins n'empilent pas.

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

- Surcharge d'horaire chargée pour les horaires en vigueur : `resources-schedule-instances-core-by-period.ts` ne charge une surcharge que si elle n'a pas de workflow ou si la demande est `validated`.
- Surcharge des pointages théoriques 2 et 3 utilisée pour la plage repas : `resource-merge-times-by-day.ts` ne prend la déclaration que si `workflowResource.state = validated`.

### Hors impact (un autre filtre, un autre ticket)

- Reporting absences : `resources-manual-event-by-days-by-period-absence-only.ts` et `resources-event-range-on-resources-by-period-absence-only.ts`. Le second sélectionne `workflowResource.state` pour l'affichage, il ne filtre pas avec `buildCountedWorkflowStateWhere`.
- Fusion planning : `merge-daily-absences.ts`, `merge-hourly-absences.ts`, `merge-other-events.ts`.
- Chevauchement à la saisie : `build-event-range-on-resource-overlap-where.ts` (exclut `refused` et `cancelled`, garde `draft` et `pending`). Le popup front `isConflictingWorkflowState` a sa propre liste.
- Compteurs et sommes de quantités : `buildEventRangeOnResourceWhereForQuantitySum` dans `resources.service.ts` (réalisé = validé, prévisionnel = validé + A valider). GTA-1915.
- Demandes de modification de pointage : `Clocking.workflowResourceId` n'a pas de filtre d'état dans les entrées du générateur. À traiter avec le sujet pointage, pas ici.

---

## Non-régression

### Specs

À lancer à la main. Écrites, pas encore rejouées dans ce chantier.

- `build-counted-workflow-state-where.spec.ts` : déjà à jour dans `4f6cb56a`. « null ou `validated` ».
- `workflow-resource-generation-period.spec.ts` : une période par type de sujet, rien pour un pointage ou un télétravail par type d'horaire.
- `enqueue-event-generation-for-workflow-resource.spec.ts` : un seul appel, fin bornée à hier, rien si la période est vide ou future.
- `user-profile-instance-update-wrls-status-with-cascade.spec.ts` : empile pour une absence, une déclaration ou une surcharge qui atteint `validated`. N'empile pas si la demande reste `pending` ou est refusée.
- `resources-submit-workflow-resource.spec.ts` : empile quand la soumission sans valideur pose `validated`. Pas pour `pending` ni `awaitingAttachements`.
- `resources-cancel-workflow-resource.spec.ts` : empile après suppression d'une demande validée sans valideur, avec les dates lues avant le delete. Pas pour un brouillon, une demande encore en attente, ou un delete en échec.
- `enqueue-event-generation-if-workflow-resource-was-validated.spec.ts` : empile seulement si l'état supprimé était `validated`. Pas de spec du resolver `deleteWorkflowResource`.

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
- Validé → `deleteWorkflowResource` : l'anomalie se rouvre.
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

1. `awaitingAttachements` est ignoré avec A valider par le filtre mergé. Ce chantier ne change pas ce point. Toujours ouvert si PO veut le faire compter.
2. Anomalies déjà clôturées par une demande A valider : correction à la prochaine génération naturelle. Pas de script de rattrapage.

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
  - période du sujet : `cronexia-gta-back\app\src\resources\functions\events\generate\workflow-resource-generation-period.ts`
  - empilement borné à hier : `cronexia-gta-back\app\src\resources\functions\events\generate\queue\enqueue-event-generation-for-past-period.ts`
  - empilement par sujet : `cronexia-gta-back\app\src\resources\functions\events\generate\queue\enqueue-event-generation-for-workflow-resource.ts`
  - après delete si l'état était `validated` : `cronexia-gta-back\app\src\resources\functions\events\generate\queue\enqueue-event-generation-if-workflow-resource-was-validated.ts`
  - accès file depuis les resolvers : `ResourcesService.enqueueEventGenerationForWorkflowResource` dans `cronexia-gta-back\app\src\resources\resources.service.ts`
- Déclencheurs
  - validation : `cronexia-gta-back\app\src\user-profile-instances\functions\workflow-resource\user-profile-instance-update-wrls-status-with-cascade.ts`
  - soumission sans valideur : `cronexia-gta-back\app\src\resources\functions\workflow-resource\resources-submit-workflow-resource.ts`
  - état sans valideur : `cronexia-gta-back\app\src\workflow-resources\functions\resolve-demand-state-without-validator.ts`
  - annulation / suppression : `cronexia-gta-back\app\src\resources\functions\workflow-resource\resources-cancel-workflow-resource.ts`
  - suppression admin : `deleteWorkflowResource` dans `cronexia-gta-back\app\src\workflow-resources\workflow-resources.resolver.ts`
  - cascade de suppression : `cronexia-gta-back\app\src\resources\functions\workflow-resource\delete-workflow-resource-cascade.ts`
- Enum
  - `cronexia-gta-back\app\prisma\schema\workflow.prisma` (`enum WorkflowStateEnum`)
- Seeds
  - `cronexia-gta-back\app\prisma\seeds-new\02-recommended\workflow\workflow.seed.md`
