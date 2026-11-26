# GTA-1744 - Retour PO : affichage selon la modalité de gestion du temps / ✅ Terminé

Contexte : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/` (plans 01 backend, 02 frontend).

Branche des retours : `feat-1744-wf-events-hourly-returns`.

Affichage seulement. La note 07 reste le blocage à la création côté serveur. Le valideur ne passe pas par ce filtre.

## Retour PO

Affichage conditionnel en fonction de la modalité de gestion du temps de la ressource.

Le PO ne précise pas quelles modalités voient DEP et RC. La règle retenue reprend le modèle déjà en place : « En jours » et « Dirigeants » n'ont pas de demandes en heures (`isManagementMethodByDays`).

## Règle

- Visibles : `En heures avec pointages théoriques`, `En heures avec pointages réels`.
- Masquées : `En jours`, `Dirigeants`, modalité nulle ou inconnue. Même repli que les familles déjà gated : sans modalité connue, on masque.

## Où c'est aujourd'hui

- Modalités : `cronexia-gta-front-v2/app/src/routes/functions/cronexia/resource/get-resource-time-management-method.ts`. Quatre valeurs : `En jours`, `Dirigeants` (les deux comptent comme « en jours »), `En heures avec pointages théoriques`, `En heures avec pointages réels`.
- Filtre collab des onglets `/demands` : `routes/functions/cronexia/workflow-tab/filter-employee-catalog-tabs-for-modality.ts`, appelé depuis `routes/(app)/(without-filters)/demands/+layout.server.ts`.
- Familles déjà masquées selon la modalité : `clockingOverload`, `declarationDays`, `declarationHours`.
- `hourlyEvent` n'est pas dans cette liste. Le commentaire du filtre et le spec `eventByDay reste visible en jours et en heures` le laissent affiché pour toutes les modalités.
- Le valideur charge son catalogue sans ce filtre : `routes/(app)/(with-filters)/request-management/+layout.server.ts`.
- Création `/demands` : `EmployeeDemandsTabContent.svelte` lit le catalogue déjà filtré (`employeeTabCreateAction`, `listCreatableHourlyEventWorkflows`). Pas de second garde à poser sur le bouton.
- Accueil : `WidgetGererMesDemandes.svelte` liste toutes les demandes via `buildAllSynthesisRows`. Il ne propose pas la carte Heures. `collaborator-home-widget-visibility.ts` ne gate que `pointagesDuJour`. Le planning d'équipe passe un catalogue vide à `WorkflowNewDemandButton` : la carte Heures y est déjà absente.

## Étape 1 — Onglets et création `/demands`

Fichier : `filter-employee-catalog-tabs-for-modality.ts`.

Ajouter `hourlyEvent` au set masqué pour « En jours », « Dirigeants », et le repli null / inconnu. Ne pas l'ajouter pour les deux modalités en heures.

L'onglet et la carte Heures disparaissent ensemble, parce que le bouton lit ce catalogue.

Spec : `filter-employee-catalog-tabs-for-modality.spec.ts`. Remplacer « visible en jours et en heures » par : masqué en jours, dirigeants, null et inconnu ; visible en pointages théoriques et réels. Le valideur n'est pas dans ce spec.

Lancé par l'équipe, pas par l'agent.

## Étape 2 — Accueil collab

Fichier : `WidgetGererMesDemandes.svelte`.

Même règle que l'étape 1 : hors des deux modalités en heures, retirer les lignes `eventByDay` de la liste. Le widget de visibilité et le bouton du planning d'équipe ne bougent pas.

## Inchangé

- Valideur, serveur, note 07 (pas de demande fantôme à l'insertion).
- Notes 04 (créneau), 06 (horaire de repos), 08 (rendu des heures dans les widgets), 09 (bouton déplacement).
