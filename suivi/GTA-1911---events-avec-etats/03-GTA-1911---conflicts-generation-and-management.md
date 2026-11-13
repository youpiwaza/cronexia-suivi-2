# GTA-1911 / Génération et gestion des conflits selon l'état des events / ✅ Done

Découpe de [01-GTA-1911---ticket-de-base.md](01-GTA-1911---ticket-de-base.md), lignes « gestion des conflits entre events » (Annulé KO, Refusé et Brouillon OK, A valider à vérifier).

Deux règles, deux moments :

- Génération des anomalies de conflit (CONFLIMLTP, CONFLIMLTPNEUTRE, CONFLIEXCL, CONFLIOVRL) : même règle que [02-GTA-1911---anomaly-generation.md](02-GTA-1911---anomaly-generation.md). Le filtre est livré sur `hfix-1789-ajustement` (`4f6cb56a`, pas encore dans `main`) : sans workflow, ou Validé. A valider ne produit pas de CONFLI*. Les branches GTA-1789 ont été effacées, pas commentées. La régénération à l'entrée et à la sortie de Validé reste le ticket 02. Ce ticket ajoute les vérifications propres aux conflits à la saisie.
- Gestion à la saisie, à la soumission et à la validation : une demande A valider occupe la période. Brouillon, Refusé et Annulé ne l'occupent pas. C'est ici que le ticket de base dit « prise en compte » pour A valider.

Hors de ce ticket : compteurs ([GTA-1915](https://cronexia.atlassian.net/jira/browse/GTA-1915)), affichage des états dans le planning et les pages synthèse.

Estimation proposée : ⏱️ ~0,5 j. À confirmer après les deux questions PO en fin de ticket.

---

## Règle cible

`WorkflowStateEnum` dans `cronexia-gta-back\app\prisma\schema\workflow.prisma`.

| État | Anomalie CONFLI* générée | Compte à la saisie, la soumission, la validation |
| --- | --- | --- |
| Pas de workflow (saisie admin / gestionnaire) | Oui | Oui |
| `validated` — Validé | Oui | Oui |
| `pending` — A valider | Non (filtre livré sur `hfix-1789-ajustement`, pas encore dans `main`) | Oui |
| `awaitingAttachements` — En attente de justificatif | Non (même commit ; à confirmer PO) | Oui (hypothèse, à confirmer PO) |
| `draft` — Brouillon | Non | Non |
| `refused` — Refusé | Non | Non |
| `cancelled` — Annulé | Non | Non |

Les états debug `cancellationRequested` et `cancellationRefused` ne sont pas l'état métier Annulé. Tant que `WorkflowResource.state` reste `validated`, la demande occupe la période. Seul `state = cancelled` est ignoré.

---

## État des lieux

La détection entre events différents est dans le front. Un seul prédicat décide : `isConflictingWorkflowState` dans `event-range-on-resource-workflow.helpers.ts`. Pas d'état, ou état inconnu de ses listes : l'event compte. Il exclut Refusé (et les debug `refusedByLowerLevel`, `refusedByHigherLevel`, `refusedDueToMissingAttachementsConstraints`) et Brouillon. Il ne connaît pas `cancelled`. C'est le KO Annulé du ticket de base.

A valider et En attente de justificatif passent ce prédicat. La « prise en compte » du ticket de base est déjà là. Ce ticket la transforme en vérifications, pas en développement.

État par état, côté gestion :

- Refusé : ignoré par le prédicat. Conforme.
- Brouillon : ignoré par le prédicat front. Conforme sur les écrans qui l'utilisent. Les deux gardes back du même event comptent encore le brouillon (voir plus bas).
- Annulé : compté par le prédicat. KO.
- A valider : compté. Conforme, à rejouer en recette.
- En attente de justificatif : compté, comme A valider.

Deux chemins front sautent le prédicat sur les events en heures :

- `check-workflow-demand-conflicts.ts` filtre les events en jours (`isUserInput` puis `isConflictingWorkflowState`) et ne filtre les events en heures que par `isUserInput`. Une déclaration en heures Brouillon, Refusée ou Annulée compte encore au moment de soumettre un brouillon ou de valider une demande. `workflowState` est pourtant déjà posé : `resources-event-by-days-by-period.ts` tamponne `workflowResource` depuis `EventByDay → DeclarationHourly → Declaration → WorkflowResource` (`stampEventByDayDeclarationWorkflowResource`), et `parse-event-by-day.ts` le recopie. Une saisie en heures sans déclaration a `workflowState` null et doit continuer de compter.
- Les deux `catch` de `HoursAbsence.svelte` retombent sur la liste locale filtrée par `isAbsenceCountedForConflicts` seul. Le `catch` de `DaysAbsence.svelte` applique déjà les deux filtres.

Gardes back, même event seulement (pas un CP contre un RTT) :

- `buildEventRangeOnResourceOverlapWhere`, appelé par create, createMany et update de `EventRangeOnResourcesService`. Exclut `refused` et `cancelled`. Garde `draft`, `pending`, `awaitingAttachements`, `validated`, et l'absence de workflow. Le refus est `CRO_EROR_000000002`.
- `guardDuplicatesWorkflowResource`, à la création de demande et à la soumission. Même exclusion `refused` / `cancelled`, même conservation du brouillon. Pour `eventRangeOnResource`, le dédoublon porte sur le même `Event.name`, tous workflows confondus.

Conséquence : une saisie directe peut être refusée par le back à cause d'un brouillon que le front ne montre pas comme conflit. Le ticket de base dit Brouillon ignoré. Le front l'est, le back ne l'est pas. Question PO, pas un changement silencieux.

Annulé n'est posé par aucun code applicatif. `userProfileInstanceUpdateWrlsStatusWithCascade` rejette `newState === cancelled` (`CRO_WR_000000035`). L'annulation collaborateur supprime la demande (`resourcesCancelWorkflowResource`), elle ne passe pas l'état à `cancelled`. Les lignes Annulé de la recette viennent des seeds.

Génération CONFLI* : le générateur ne relit pas l'état. Il consomme les events déjà filtrés par le ticket 02. Rien à coder ici pour le calcul. Les CONFLI* déjà en base suivent la décision « données déjà générées » du ticket 02.

---

## Ce qu'il convient de faire

### 1. Front : ignorer l'état métier Annulé

Dans `isConflictingWorkflowState`, exclure la clé normalisée `cancelled`, au même titre que Refusé et Brouillon.

Ne pas reprendre toute la liste debug `CANCELLED_LIKE_KEYS`. `cancellationRequested` et `cancellationRefused` restent comptés quand ils arrivent comme chaîne : ce ne sont pas `WorkflowResource.state`.

### 2. Front : le même filtre sur les events en heures

- `check-workflow-demand-conflicts.ts` : appliquer `isConflictingWorkflowState` à `hoursAbsencesToCheck`, après le filtre `isUserInput` déjà en place. ADEC / PDEC (`isUserInput` false) restent hors de ce contrôle, comme aujourd'hui.
- `HoursAbsence.svelte`, les deux branches `catch` : ajouter `isConflictingWorkflowState` à côté de `isAbsenceCountedForConflicts`.

### 3. Back : le brouillon dans les gardes du même event

Selon la réponse PO. Proposition : ajouter `draft` au `notIn` de `buildEventRangeOnResourceOverlapWhere` et de `guardDuplicatesWorkflowResource`, aligné sur le front. `pending` et `awaitingAttachements` restent bloquants. `refused` et `cancelled` le restent.

### 4. Génération

Aucun code de filtre dans ce ticket. Le filtre « sans workflow ou Validé » est livré sur `hfix-1789-ajustement` (`4f6cb56a`), pas encore dans `main`. L'empilement à l'entrée et à la sortie de Validé reste le ticket 02. La popup et les gardes de saisie continuent de compter A valider : le commit front de la même branche (`ef25e855`) ne touche pas `isConflictingWorkflowState`, il déplace l'anneau de survol sur la frise d'anomalies. Les contrôles CONFLI* de la recette ci-dessous se jouent après le merge du filtre, et après l'empilement du ticket 02 pour les transitions.

---

## Inventaire des impacts

### Écrans qui passent par le prédicat

Un changement de `isConflictingWorkflowState` les atteint tous. Aujourd'hui chacun filtre ainsi :

| Entrée | Fichier | Filtre actuel |
| --- | --- | --- |
| Absences en jours, création et modification | `DaysAbsence.svelte` | `isAbsenceCountedForConflicts` puis `isConflictingWorkflowState`, jours et heures. Le `catch` fait les deux. |
| Absences en heures, création et modification | `HoursAbsence.svelte` | Idem sur le chemin nominal. Les deux `catch` oublient l'état. |
| Synthèse, anomalies, popup planning | `check-timeline-event-conflicts.ts` | Les deux filtres, jours et heures. Appelé par `DayTimelineAccordion.svelte`, `PlanningEventModal.svelte`, `CollectiveSchedulePage.svelte`. |
| Brouillons du planning collectif | `scan-planning-draft-conflicts.ts` | Délègue à `checkTimelineEventConflicts`. Les pastilles pas encore enregistrées sont ajoutées après le filtre : ce sont les saisies en cours, pas des events Annulés. |
| Soumission d'un brouillon | `check-workflow-demand-conflicts.ts` | Jours : `isUserInput` puis le prédicat. Heures : `isUserInput` seul. Appelé par `WidgetGererMesDemandes.svelte`, `AbsencesWorkflowModal.svelte`, `use-workflow-collab-demand-actions.svelte.ts`. |
| Validation, unitaire et en masse | `scan-validation-conflicts.ts` | Même fonction. Appelé par `WidgetValidationDemandes.svelte`, `ValidatorDemandsTabShell.svelte`, `WorkflowDemandConsultModal.svelte`. La demande examinée est retirée via `excludeWorkflowResourceId` pour ne pas se détecter elle-même. |
| Chatbot | `cronexia-gateway.ts` | `isUserInput` puis le prédicat, events en jours. |

`isAbsenceCountedForConflicts` (`absence-etat-filter.ts`) est un autre filtre : saisie utilisateur, ou event généré lié à une déclaration déjà Validée (ADEC / PDEC). Il ne connaît pas Annulé. On ne le change pas. L'exclusion d'état reste dans le prédicat, appliqué juste après.

### Modes de conflit

`resolve-conflict-reaction.ts` et `conflict-mode.ts` (Interdit, Évité, Acceptable) ne changent pas. Moins de conflits les atteignent : un event Annulé ne déclenche plus un rejet Interdit, ni une fenêtre Évité / Acceptable.

### Remplacement (GTA-1432)

`replaceMany` et `resolve-event-range-replaceability.ts` ne changent pas. Un event ignoré n'est plus proposé au remplacement, parce qu'il n'est plus détecté. Le back reste l'autorité : `CRO_EROR_000000007` si la demande n'est plus supprimable, `CRO_EROR_000000008` si le retrait scinderait une demande (`workflowResourceId` est unique).

### Hors impact

- Filtre du générateur et empilement : ticket 02.
- Affichage planning, bordures, pastilles : `isEventRangeOnResourceVisibleInPlanning` et `mapWorkflowResourceStateToPlanningStatus`.
- Widgets d'accueil (`HomeManager.svelte`, `HomeHrManager.svelte`) et présence chatbot (`presence.ts`) : ils passent par `isEventRangeOnResourceStrictlyValidated`. Cette fonction range `cancelled` avec les états « validés » (`STRICTLY_VALIDATED_KEYS`). Un event Annulé peut donc compter dans « absent aujourd'hui » / « en TT aujourd'hui ». À traiter avec l'affichage, pas dans ce ticket.
- Reporting absences, compteurs, sommes de quantités.

---

## Non-régression

### Specs à mettre à jour

À lancer à la main.

- `event-range-on-resource-workflow.helpers.spec.ts` : le fichier couvre aujourd'hui l'affichage (`getEventByDayWorkflowFields`), pas le prédicat. Ajouter les cas de `isConflictingWorkflowState` : null, `validated`, `pending`, `awaitingAttachements` comptent ; `draft`, `refused`, `cancelled` ne comptent pas ; `cancellationRequested` compte.
- `check-timeline-event-conflicts.spec.ts` : un event Annulé en face ne produit pas de groupe. Un event A valider en produit un.
- `absence-etat-filter.spec.ts` : relecture seule. `isAbsenceCountedForConflicts` ne change pas.
- Si la réponse PO exclut le brouillon des gardes back : `guard-duplicates-workflow-resource.spec.ts`, et le spec du where de chevauchement s'il existe à côté de `is-overlap.spec.ts` (`is-overlap.spec.ts` lui-même teste les types de journée, pas l'état).

### Recette

Event déjà en base, pour chaque état, contre une nouvelle saisie en jours, une nouvelle saisie en heures, et une nouvelle demande. Résultat attendu : conflit, ou pas de conflit. Rejouer sur chaque entrée du tableau d'inventaire (absences jours, absences heures, synthèse / anomalies, planning, soumission, validation).

| État de l'event déjà posé | Conflit à la saisie / soumission / validation | CONFLI* après génération (ticket 02) |
| --- | --- | --- |
| Pas de workflow | Oui | Oui |
| Validé | Oui | Oui |
| A valider | Oui | Non |
| En attente de justificatif | Oui | Non |
| Brouillon | Non (front). Back : selon la réponse PO | Non |
| Refusé | Non | Non |
| Annulé | Non | Non |

Modes, sur un event Validé et sur un event A valider (le comportement ne change pas) :

- Interdit : la nouvelle saisie est rejetée.
- Évité : remplacement obligatoire quand le remplacement est possible, sinon « tout conserver ».
- Acceptable : remplacer, ou tout conserver. Deux events Validés conservés produisent un CONFLI* à la génération. Un A valider conservé en face d'un Validé n'en produit pas, jusqu'à la validation.

Flux de validation :

- Valider une demande alors qu'un gestionnaire a posé un event par-dessus entre-temps : la fenêtre d'arbitrage s'ouvre.
- La demande ne se détecte pas elle-même (`excludeWorkflowResourceId`).
- Validation d'un niveau intermédiaire (la demande reste A valider) : elle continue d'occuper la période pour les saisies suivantes, et ne produit toujours pas de CONFLI*.

### Jeux de données

L'UI ne sait pas poser l'état Annulé. La recette Annulé part des seeds dev, qui ont déjà des demandes `cancelled` :

- `cronexia-gta-back\app\prisma\seeds-new\50-dev\workflow-resource\event-cp\workflow-resource-06-etienne-roux-event-cp-validation.seed.ts`
- `cronexia-gta-back\app\prisma\seeds-new\50-dev\workflow-resource\event-rtt\workflow-resource-07-celine-lefevre-event-rtt-validation.seed.ts`
- `cronexia-gta-back\app\prisma\seeds-new\50-dev\workflow-resource\remote-work-by-event-range-on-resource\workflow-resource-01-maxime-c-tt-event-validation.seed.ts`
- Déclaration en heures annulée : `cronexia-gta-back\app\prisma\seeds-new\50-dev\workflow-resource\declaration-hours\workflow-resource-04-patrick-declaration-hours.seed.ts`

Brouillon, A valider, Refusé : faire vivre une demande. En attente de justificatif : template `SICK_CHILD_ATTACHMENT_REQUIRED_DEFERRED` dans `workflow.seed.md`.

---

## Questions PO

1. Les gardes back du même event (`CRO_EROR_000000002` et le dédoublon de demande) doivent-elles ignorer le Brouillon, comme le front ? Proposition : oui.
2. `awaitingAttachements` compte à la saisie, comme A valider. C'est l'inverse du ticket 02, où il est ignoré pour la génération. À confirmer.

---

## Dev

### Emplacements des fichiers

- Prédicat front
  - `cronexia-gta-front-v2\app\src\routes\functions\cronexia\event-range-on-resource\event-range-on-resource-workflow.helpers.ts`
  - spec : `event-range-on-resource-workflow.helpers.spec.ts` (même dossier)
- Events en heures sans le prédicat
  - `cronexia-gta-front-v2\app\src\routes\functions\cronexia\event-range-on-resource\check-workflow-demand-conflicts.ts`
  - `cronexia-gta-front-v2\app\src\routes\components\cronexia\absence\HoursAbsence.svelte`
  - parse : `cronexia-gta-front-v2\app\src\routes\functions\cronexia\event-by-day\parse-event-by-day.ts`
  - tampon back : `cronexia-gta-back\app\src\resources\functions\events\event-by-day-declaration-workflow-resource.ts`
- Gardes back, si la réponse PO le demande
  - `cronexia-gta-back\app\src\event-range-on-resources\functions\service\build-event-range-on-resource-overlap-where.ts`
  - appelé par `cronexia-gta-back\app\src\event-range-on-resources\event-range-on-resources.service.ts`
  - `cronexia-gta-back\app\src\workflow-resources\functions\guard-duplicates-workflow-resource.ts`
- Génération CONFLI* (ticket 02, pas de code ici)
  - `cronexia-gta-back\app\src\resources\functions\events\generate\resources-generate-events-query-by-period.ts`
- Remplacement, à ne pas modifier
  - `cronexia-gta-back\app\src\event-range-on-resources\functions\replace\resolve-event-range-replaceability.ts`
- Enum
  - `cronexia-gta-back\app\prisma\schema\workflow.prisma` (`enum WorkflowStateEnum`)
- Seeds Annulé
  - `cronexia-gta-back\app\prisma\seeds-new\50-dev\workflow-resource\event-cp\workflow-resource-06-etienne-roux-event-cp-validation.seed.ts`
  - `cronexia-gta-back\app\prisma\seeds-new\50-dev\workflow-resource\declaration-hours\workflow-resource-04-patrick-declaration-hours.seed.ts`
