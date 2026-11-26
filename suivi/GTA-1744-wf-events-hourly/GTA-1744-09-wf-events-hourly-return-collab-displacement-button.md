# GTA-1744 - Retour PO : bouton déplacement sur « Gérer mes demandes »

Contexte : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/` (plans 01 backend, 02 frontend, note 05 modalité).

Branche des retours : `feat-1744-wf-events-hourly-returns`.

Note courte. Le branchement du bouton se fera dans une passe dédiée.

## Retour PO

Collaborateur uniquement > Accueil > widget « Gérer mes demandes » : ajouter un bouton pour soumettre une demande de déplacement.

Le manager et le RH n'ont pas ce widget. Leur accueil a « Validation des demandes », qui ne crée pas de demande. Le bouton ne se pose que sur l'accueil collaborateur.

## Où c'est aujourd'hui

- Widget : `cronexia-gta-front-v2/app/src/routes/components/common/widgets/WidgetGererMesDemandes.svelte`, monté dans `HomeEmployee.svelte`. Deux présentations, tuiles et boutons compacts (`layout="buttons"`), passent par `WorkflowNewDemandCards`.
- Cartes proposées : absences, horaires, télétravail, pointages (si pointages réels). `canRequestHourlyEvent` n'est pas passé : il vaut `false`, et la carte `hourlyEvents` est alors masquée (`WorkflowNewDemandCards.svelte`).
- `selectNewDemand` ouvre absences, télétravail, changement d'horaire, pointages. Pas de cas `hourlyEvents`, et pas de `HourlyEventWorkflowModal` dans le widget.
- La page demandes a déjà le parcours : `WorkflowNewDemandButton.svelte` affiche la carte « Heures » (`workflow-new-demand-items.ts`, id `hourlyEvents`) dès qu'un workflow en heures est disponible, et ouvre `HourlyEventWorkflowModal.svelte`.

## À trancher à la passe suivante

- Réutiliser cette carte et cette modale dans le widget, les deux présentations. Pas une troisième modale.
- Le libellé existant est « Heures » / « Demande en heures », pas « Déplacement ». Le PO demande un déplacement : confirmer si le bouton est le parcours heures (DEP, et RC s'il est proposable) ou un libellé déplacement.
- Visibilité : même règle que la page demandes (`listCreatableHourlyEventWorkflows` non vide), plus la règle d'affichage retenue en note 05. Cette note ne fige pas encore « masqué en jours ».

## Hors périmètre de cette note

- Pas de correctif, pas de nouveau bouton dessiné ici.
- Affichage des heures dans les widgets (note 08), créneau / durée, message horaire de repos.
