# Intégration des pages droits d'absence

Règles communes de chaque passe visuelle. La page salarié est l'exemple déjà fait, pas un écran à recopier. Le détail d'une page (champs, route, checklist) reste dans son fichier de statut.

Référence travaillée :

- `cronexia-gta-front-v2/app/src/routes/(app)/(without-filters)/rights`
- `cronexia-gta-front-v2/app/src/routes/components/cronexia/rights-employee/`
- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/current-implementations-statuses/01-employee-rights/01-employee-rights-integration-and-menus.md`

Les chemins des pages restantes sont déjà posés dans `cronexia-suivi-2/suivi/10-octobre/261022-suivi.md` : consultation individuelle RH, consultation collective, paramétrage d'un droit, législation (ordre de décompte), outil d'initialisation.

## Périmètre d'une passe visuelle

Contenu principal seulement.

- Fixture statique. Les contrôles sont visibles et désactivés. `disabled` passe par les props du composant.
- Pas de GraphQL. Pas de branchement des filtres, des formulaires, des téléchargements ni des navigations.
- `cronexia-gta-front-v2/app/src/routes/components/common/layout/LayoutAppMain.svelte` reste inchangé : en-tête, menu latéral, filtres population, resource et période. Les menus dessinés sur les maquettes sont hors sujet.
- Le lien de la page s'ajoute dans `cronexia-gta-back/app/prisma/seeds-new/01-required/menu-link/const/menu-link-catalog.const.ts`. Un raccourci s'ajoute dans `cronexia-gta-back/app/prisma/seeds-new/01-required/menu-quick-link/const/menu-quick-link-defaults.const.ts` seulement s'il est utile. Les fichiers `*.seed.ts` qui consomment ces constantes restent inchangés.
- Un seul `h1`, celui de `PageTitle` dans le header. Le corps de page ne le répète pas.
- Le branchement du comportement est une tâche ultérieure.

## Priorité des sources

1. La maquette PNG fixe la disposition.
2. Le HTML d'intégration IA est un indice de structure. Il peut inventer des champs, des menus ou des couleurs.
3. La structure droits d'absence déjà en place gagne en cas de conflit : seeds, modèles, CRUD sous `cronexia-gta-front-v2/app/src/routes/(app)/(without-filters)/_dev/test`.
4. Une ligne présente sur la maquette mais absente du métier s'affiche **Non géré** et sort de toutes les sommes. La page salarié n'a pas recopié les totaux 25 / 18,5 de la maquette.

Demander avant d'ajouter un champ sans équivalent, ou un composant Material de bas niveau.

## Où placer le code

- Route sur le chemin déjà choisi dans le suivi, groupe `(with-filters)` ou `(without-filters)` selon la note de la page.
- Composants de la page sous `cronexia-gta-front-v2/app/src/routes/components/cronexia/rights-<contexte>/`.
- Réutiliser les wrappers Material et le catalogue `cronexia-gta-front-v2/app/src/routes/(app)/(without-filters)/demo`. Pas de nouveau composant de bas niveau sans validation.
- Une barre de filtres de page s'aligne sur les filtres du header (`FilterPopulation`, `FilterResource`, `FilterPeriod` : `MdOutlinedSvelecte` ou le date picker, `size="S"`, fond `surface`, typo `text-s`). Pas `InputSvelecte` : c'est la coque de formulaire, plus basse et teintée. Choix unique : `MdOutlinedSvelecte` `size="S"`. Choix multiple : `ChipGroupSelect`. Tant que le contrôle est figé : `disabled` (`ChipGroupSelect` n'en a pas : `inert` sur l'enveloppe), pas de `name`. `InputSvelecte` reste le select d'un formulaire (colonne de filtres salarié).
- Deux déclarations, avec un motif limité à la route de la page. Pas de règle large sur `/rights` : un chemin sans match reste ouvert, et `/rights/individual/...` ne doit pas hériter du droit salarié.
  - `cronexia-gta-front-v2/app/src/config/page-config.ts` : titre du `PageTitle`, `hasToolbar`, `heightManagement`, `headerFilterIsDateOrPeriodPerPage`, `showAllRessources`. La page salarié est `/^\/rights\/[^/]+\/dateStart(\/|$)/`, titre `Mes droits & soldes`, `hasToolbar: false`, `heightManagement: 'classic'`, filtre d'en-tête `null`, `showAllRessources: false`. Elle reste distincte de `/vacation-rights`.
  - `cronexia-gta-front-v2/app/src/routes/functions/common/auth/page-rights-config.ts` : le même motif, avec le droit déjà prévu pour ce public. La page salarié réutilise `PAGE_VACATION_RIGHTS`.

## Cartes et coque de page

Cartes `MdElevatedCard`, comme sur `EmployeeRightsPage.svelte` :

- `--md-elevated-card-container-color: var(--md-sys-color-surface-container-lowest)`
- `--md-elevated-card-container-elevation: 0`
- `border: 1px solid var(--md-sys-color-outline-variant)`

Un bandeau d'alerte utilise `colors.warning.subtle` via `getColorInlineStyle`, hors `md-elevated-card` (`EmployeeRightsBanner.svelte`).

Coque de page :

- `width: 100%`, `max-width: 1600px`, `margin-inline: auto`, `box-sizing: border-box`
- colonne flex, `gap: var(--cronexia-space-sm)`
- padding `var(--cronexia-space-2xs) clamp(0rem, 2vw, var(--cronexia-space-sm)) var(--cronexia-space-sm)`

Deux colonnes, comme `EmployeeRightsTabs.svelte`. Le conteneur a `container-type: inline-size`. Colonne principale `flex: 1 1 40rem`, `min-width: min(100%, 40rem)`. Aside `flex: 0 0 20rem`, `max-width: 100%`. Sous `62rem` de conteneur, aside `flex-basis: 100%`.

Titres de carte (`h3`) : classe `text-m`, padding `--cronexia-space-xs` `--cronexia-space-sm`, filet bas `outline-variant`.

Onglets `MdTabs` + `MdPrimaryTab`, index actif en état local. Barre en `width: 100%`, filet `outline` (`outline-variant` disparaît sur le fond de page). `md-tabs` en `fit-content` et `max-width: 100%`, `md-primary-tab` en `flex: none`, fond `--md-primary-tab-container-color: transparent`.

## Tailles et espacements

Corps en `text-m`. `text-s` pour une note, `text-l` pour un titre de vue, `text-2xl` seulement pour un chiffre de KPI. Démo : `cronexia-gta-front-v2/app/src/routes/(app)/(without-filters)/demo/components/size/CronexiaSize.svelte`.

Espacements via les tokens de `cronexia-gta-front-v2/app/src/routes/+layout.svelte` :

- `--cronexia-space-3xs` : 0.25rem
- `--cronexia-space-2xs` : 0.5rem
- `--cronexia-space-xs` : 0.75rem
- `--cronexia-space-sm` : 1rem

`SIZE_SPACE_PAD` (`cronexia-gta-front-v2/app/src/routes/components/const/size-space.const.ts`) quand un bloc reprend déjà cette échelle : XS `0`, S `3xs`, M `2xs`, L `xs`, XL `sm`.

Gap entre blocs : `--cronexia-space-sm`. Pas de marges ni de tailles de police recopiées du HTML IA.

## Tableaux

`TableAdvanced` uniquement : `cronexia-gta-front-v2/app/src/routes/components/common/tables/advanced`. Pas de `Table` ni de `TableRow`.

Comme `EmployeeRightsMovements.svelte` :

- `contents` en chaînes, `valueNames` alignés sur les clés de ligne
- recherche, options de recherche, filtre, tri et pagination désactivés tant que la maquette ne les demande pas
- `hasShell={false}` quand une carte parente enveloppe déjà le tableau
- `isHoverable={true}`
- `.table-advanced` en `gap: 0`
- pied de tableau dans le snippet `footer`

Une cellule de statut passe par `Badge` et `colorsWorkflowStatus` (`EmployeeRightsHistory.svelte`). Les cas particuliers sont dans `cronexia-gta-front-v2/app/src/routes/(app)/(without-filters)/demo/components/table`.

## Couleurs

Source : `cronexia-gta-front-v2/app/src/config/color/const`, réexportée par `$config/color-config`. Démo : `demo/components/color/CronexiaColorScheme.svelte`.

- Teintes génériques : `colors.primary`, `secondary`, `success`, `info`, `warning`, `danger`, variantes `classic` et `subtle`. Les appliquer avec `getColorInlineStyle` pour suivre le thème clair et sombre.
- Surfaces et filets : `--md-sys-color-surface-container-lowest`, `outline`, `outline-variant`, `on-surface`, `on-surface-variant`.
- Métier : `SOLDE_CONGE_COLORS` (`cronexia-gta-front-v2/app/src/routes/functions/cronexia/workflow/soldes-conges-chart.helpers.ts`), `colorsWorkflowStatus`.

Ne pas coller les hex du HTML IA. Si une teinte n'a pas de token, demander.

Graphique : `EChartsWhenSized`, même init `echarts/core` que `VacationSoldeCard.svelte`. Les `var()` lues par le canvas passent par `getComputedStyle`.

## Fixture

- Champs alignés sur le modèle droits déjà existant. Un helper renvoie les chiffres dérivés (soldes, KPI, totaux). Les composants ne recalculent pas.
- Libellés d'unité en chaînes statiques sur la fixture.
- Les paramètres d'URL ne sont pas lus dans cette passe. Les selects désactivés affichent les valeurs de la fixture.
- Lignes **Non géré** visibles, exclues des sommes et des parts de graphique.

## Processus par page

1. Checklist dans `cronexia-suivi-2/suivi/GTA-1833-abs-rights/current-implementations-statuses/`, un fichier par page.
2. Appliquer ces règles dès la première passe : couleurs, tailles, cartes, tableaux. La seconde passe de la page salarié ne se refait pas.
3. La vérification navigateur figure dans la checklist. Elle reste ouverte tant qu'elle n'a pas été confirmée.
4. Branchement des filtres et des formulaires : tâche suivante, hors de cette passe.
