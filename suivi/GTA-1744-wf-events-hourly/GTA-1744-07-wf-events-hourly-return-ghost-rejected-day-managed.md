# GTA-1744 - Retour PO : demande fantôme pour une ressource en jours

Contexte : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/` (plans 01 backend, 02 frontend, note 05 modalité).

Branche des retours : `feat-1744-wf-events-hourly-returns`.

Refuser une demande `eventByDay` avant d'écrire le `WorkflowResource`, quand la ressource n'est pas gérée en heures. Même règle que la note 05.

## Retour PO

Manager > Accueil > widget. La demande de déplacement rejetée pour Maxime, parce qu'il est géré en jours, apparaît quand même dans le widget de son manager. Elle est rejetée, mais créée en version fantôme.

## Cause

Une demande `eventByDay` est refusée par la modalité, mais le `WorkflowResource` est déjà enregistré.

Dans `cronexia-gta-back/app/src/workflow-resources/workflow-resources.resolver.ts`, `createWorkflowResourceAndAssociateUploads` et les niveaux de validation sont écrits avant les lignes. Le commentaire vers la ligne 1014 le dit : `eventByDays` passe par `EventByDaysService.create` après le WR. Ce service appelle `event-by-days/functions/service/generate-event-by-day.ts`, qui lève `CRO_EBD_000000001` (« La saisie d'un événement en heures pour une ressource gérée en jours est interdite ») via `is-event-rejected-for-resource-mode.ts`. Il n'y a pas de transaction autour du WR et des lignes. L'exception n'efface pas le WR. Aucune ligne `EventByDay` n'est créée : le `throw` est avant `prisma.eventByDay.create`.

L'état reste celui envoyé à la création, en pratique `pending`. Ce n'est pas `refused`.

`WidgetValidationDemandes.svelte` saute `draft`, `validated`, `refused`, `cancelled`. Une demande encore `pending` s'affiche. Le widget a raison. Le trou est l'insertion.

`WidgetDeplacementAujourdhui` liste des personnes, pas des demandes. Sans `EventByDay`, cette demande n'y apparaît pas.

La note 05 masque déjà la carte Heures au collab (`isHourlyEventVisibleForModality`). Le resolver ne lit pas `resourceTimeManagementMethod`. Un appel direct, ou un catalogue valideur non filtré, crée encore le WR.

Même trou à la mise à jour : vers la ligne 1579 le WR est mis à jour, puis les lignes sont créées vers la ligne 1590. Un échec de modalité laisse le WR déjà modifié.

## Règle

Même règle que la note 05, sur la ressource de la demande, à la date de chaque ligne (valeur historisée) :

- Autorisé : `En heures avec pointages théoriques`, `En heures avec pointages réels`.
- Refusé avant écriture : `En jours`, `Dirigeants`, modalité absente, inconnue, ou autre (`En durée`).

Le garde horaire de repos (note 06) ne change pas. Les déclarations d'heures ne passent pas par ce garde.

## Étape 1 — Dictionnaire

Fichier : `cronexia-gta-back/app/src/_utility/error/cronexia-error-dictionnary.ts`.

Ajouter `CRO_WR_000000052` à côté de `051`. `050` reste réservé.

- `fr-FR` : `La demande n'est pas autorisée pour une ressource qui n'est pas gérée en heures`
- `en-US` : `The request is not allowed for a resource that is not managed in hours.`
- `messageTech` : demande `eventByDay`, variables `{resourceMode}` et `{date}`.

`CRO_EBD_000000001` et `002` restent pour la saisie directe d'un `EventByDay`.

## Étape 2 — Garde avant écriture

Nouveau fichier sous `cronexia-gta-back/app/src/workflow-resources/functions/`, sur le modèle du garde repos.

Fonction pure, spec à côté : une modalité est autorisée seulement pour les deux constantes heures de `_utility/resource-fields/get-resource-time-management-method-field.ts` (`RESOURCE_TIME_MANAGEMENT_THEORETICAL_CLOCKINGS`, `RESOURCE_TIME_MANAGEMENT_REAL_CLOCKINGS`). `isManagementModeByDays` couvre `En jours` et `Dirigeants`, les deux refusés.

Chargement : même lecture historisée que `generateEventByDay` (`getResourcesValuesFirstsBeforePeriod` sur le champ `resourceTimeManagementMethod`), une fois par date de ligne. Dès qu'une date n'est pas autorisée, `BadRequestException` avec `CRO_WR_000000052`. Pas d'écriture.

Dans le resolver :

- Création : après le garde repos, avant `createWorkflowResourceAndAssociateUploads`, seulement si le workflow est `eventByDay` et qu'il y a des lignes.
- Mise à jour `eventByDays.create` : avant `workflowResourcesService.update`.

`generateEventByDay` reste en place pour les créations d'`EventByDay` hors demande.

## Étape 3 — Repli front et spec

Fichier : `cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/hourly-event-workflow-create.helpers.ts`.

Ajouter `CRO_WR_000000052` dans `HOURLY_EVENT_CREATE_ERROR_BY_CODE`, même phrase que le dictionnaire. Le message API passe avant le repli. La modale et les widgets ne changent pas.

Spec : `hourly-event-workflow-create.helpers.spec.ts`. Message vide ou égal au code `052` vers la phrase courte. Message API non vide avec `052` vers ce message. Lancé par l'équipe, pas par l'agent. Le spec du prédicat de modalité aussi.

## Inchangé

- Widget « Validation des demandes » et « En déplacement aujourd'hui ».
- Filtre d'affichage collab (note 05), message horaire de repos (note 06), créneau, widgets heures, bouton déplacement.
- Saisie `EventByDay` hors workflow (`CRO_EBD_000000001` / `002`).
