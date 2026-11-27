# GTA-1744 - Retour : un seul événement, le libellé passe dans le titre

Contexte : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/` (plans 01 backend, 02 frontend).

Branche des retours : `feat-1744-wf-events-hourly-returns`.

Quand un onglet ne porte qu'un événement, la popup de création répète ce libellé dans le formulaire. En jours, c'est un svelecte Type désactivé. En heures, c'est la ligne « Événement » en texte. Les deux cas affichent le libellé dans le titre, et le champ disparaît. Plusieurs événements, ou plusieurs circuits pour le même événement, gardent leur sélecteur.

La valeur envoyée à la création ne change pas. En jours, `selectedEventName` reste le premier `eventOptions`. En heures, `selectedWorkflowId` reste le seul workflow.

Le code masqué est commenté, pas supprimé, pour pouvoir le remettre.

Une étape = un lot. Ordre à respecter. Les tests Vitest sont lancés par l'équipe, pas par l'agent. Svelte : autofixer sur chaque composant modifié avant de quitter l'étape.

## Aujourd'hui

`AbsencesWorkflowModal.svelte` affiche toujours un svelecte Type.

- `workflowOptions.length > 1` (GTA-1529) : choix du circuit, par exemple télétravail avec ou sans valideur.
- Sinon : choix de l'événement. `isSelectDisabled` le fige quand l'onglet n'a qu'un événement, et toujours pour le télétravail (`RemoteWorkRequestModal.svelte` passe `isSelectDisabled={true}` et le titre `Demande de télétravail`).

`HourlyEventWorkflowModal.svelte` : un seul workflow affiche « Événement » puis le libellé (`hourly-demand__target`). Plusieurs workflows gardent `MdOutlinedSelect`. Le titre est `Nouvelle demande en heures`.

Le widget, le calendrier et le bouton « Nouvelle demande » passent tous par la modale jours. Ne pas toucher leur branche à plusieurs événements.

## Étape 1 — Helper de titre et spec

Nouveau module à côté des autres helpers workflow :

- `cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/single-event-demand-title.ts`
- `single-event-demand-title.spec.ts` dans le même dossier

Entrées : chaînes et comptes. Pas de Svelte, pas de modale, pas de `$typesGraphql`.

- Un événement, titre générique `Nouvelle demande`, pas de choix de circuit : `Nouvelle demande de ${label}` (exemple : `Nouvelle demande de Congés payés`). La ligne Type est masquée.
- Un titre fourni par l'appelant (`Demande de télétravail`) reste tel quel. La ligne Type est quand même masquée s'il n'y a qu'un événement et pas de choix de circuit.
- Plusieurs événements : titre inchangé, svelecte affiché.
- Plusieurs circuits (`workflowOptions.length > 1`) : titre inchangé, svelecte de circuit affiché, svelecte d'événement masqué (comme aujourd'hui).
- Zéro événement, ou un libellé vide sur l'unique événement : titre générique, ligne Type laissée comme aujourd'hui (le svelecte jours reste ; les heures gardent `Nouvelle demande en heures` et le message vide).
- Heures, un workflow : `Nouvelle demande de ${label}` (exemple : `Nouvelle demande de Déplacement`). Heures, plusieurs workflows : `Nouvelle demande en heures`, select affiché.

Style du spec : `hourly-demand-slot-text.spec.ts` (`describe` / `it`, imports groupés avec une ligne vide et un commentaire de section `//`).

Suivre `cronexia-gta-front-v2/instructions-tests-unitaires.md` :

- le helper et le spec n'importent pas de valeur depuis `$typesGraphql` (pas de `WorkflowStateEnum` ni d'autre enum généré). Un `import type` ne pose pas problème. Les titres en français sont des chaînes.
- ne pas ajouter ce spec à `test.exclude` dans `cronexia-gta-front-v2/app/vite.config.ts`. Il doit tourner en CI.
- si une modification ultérieure fait charger au spec un fichier source qui importe une valeur depuis `$typesGraphql`, ajouter son chemin à la fin de la liste `exclude` existante, sous le même commentaire. Pas de `vi.mock('$typesGraphql')`, pas de copie des enums, pas de remplacement des enums par des chaînes en dur pour contourner la CI.

Lancé par l'équipe, pas par l'agent : depuis `cronexia-gta-front-v2/app`, `bun run test src/routes/functions/cronexia/workflow/single-event-demand-title.spec.ts`.

Fini quand le helper couvre les cas ci-dessus et que le spec ne charge pas `$typesGraphql`.

## Étape 2 — Popup jours

Fichier : `cronexia-gta-front-v2/app/src/routes/components/cronexia/workflow/AbsencesWorkflowModal.svelte`. Le titre vient du helper de l'étape 1.

Garder les deux branches actives :

- `workflowOptions.length > 1` : svelecte de circuit, inchangé.
- plusieurs événements (`eventOptions.length > 1`), ou zéro événement : svelecte d'événement, y compris le cas activé à plusieurs événements (`isSelectDisabled` s'applique encore).

Seule la branche à un événement (`eventOptions.length === 1` et pas de choix de circuit) est mise dans un commentaire HTML, avec une note pour la décommenter si on veut réafficher le champ. Ne pas supprimer `AbsenceWorkflowTypeSelect` ni la prop `isSelectDisabled` : la branche à plusieurs événements et le bloc commenté s'en servent encore.

`RemoteWorkRequestModal.svelte` n'est pas modifié. Il passe déjà `title="Demande de télétravail"`, ce titre reste. Son svelecte Type est la branche à un événement, il disparaît. Si plusieurs circuits de télétravail sont chargés, le svelecte de circuit reste.

Autofixer Svelte sur ce composant avant de quitter l'étape.

Fini quand un onglet à un événement jours n'a plus de champ Type et affiche `Nouvelle demande de {libellé}`, et qu'un onglet à plusieurs événements garde le svelecte et le titre `Nouvelle demande`.

## Étape 3 — Popup heures

Fichier : `cronexia-gta-front-v2/app/src/routes/components/cronexia/workflow/HourlyEventWorkflowModal.svelte`. Même helper.

`workflows.length > 1` garde `MdOutlinedSelect` (« Événement ») et le titre `Nouvelle demande en heures`.

`workflows.length === 1` commente le bloc texte (`hourly-demand__target`, « Événement », libellé) et le CSS qui ne sert qu'à ce bloc, sur le modèle du bloc durée déjà commenté. Le titre vient du helper.

`workflows.length === 0` garde le message vide et le titre générique.

Autofixer Svelte sur ce composant avant de quitter l'étape.

Fini quand une demande horaire à un événement n'a plus la ligne « Événement » et s'intitule `Nouvelle demande de Déplacement` (ou le `labelShort` du catalogue), et que plusieurs événements horaires gardent le select.

## Étape 4 — Vérification

Après le résultat du spec, à la main :

- un événement jours sur un onglet : pas de champ Type, titre `Nouvelle demande de {libellé}`. Plusieurs événements : svelecte toujours là, titre `Nouvelle demande`.
- télétravail à un circuit : pas de champ Type, titre toujours `Demande de télétravail`. Plusieurs circuits : svelecte de circuit toujours là.
- un événement horaire : plus de ligne « Événement », titre `Nouvelle demande de Déplacement`. Plusieurs événements horaires : select toujours là, titre `Nouvelle demande en heures`.

Fini quand ces trois parcours correspondent, et que la création envoie encore le même événement.

## Inchangé

- Soumission : `selectedEventName` et `selectedWorkflowId` restent ceux du seul événement quand le champ est masqué.
- Sélecteur à plusieurs événements (jours et heures) et sélecteur de circuit (GTA-1529).
- Titre du télétravail : `Demande de télétravail`.
- `RemoteWorkRequestModal.svelte` : aucun changement de fichier.
