# Mes droits & soldes — page salarié

Intégration visuelle uniquement. Fixture statique, filtres et formulaires inertes. Cocher chaque case au fur et à mesure.

Références visuelles :

- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/mockups/1-collaborateur---mes-droits-et-soldes.png`
- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/ai-integrations-propositions/3 bis. Espace salarié d'après la copie d'écran (interactif)-html/Salarie-2.dc.html`

Le dossier « 1. Consultation individuelle » est l'écran RH, hors de cette page.

## Cadre (ne pas rouvrir)

- Nouvelle route seulement. `/vacation-rights`, le widget d'accueil et le lien chatbot restent sur la page compteurs.
- Pas de GraphQL. Période, droit, heures, téléchargement, « en savoir plus » et lignes de prises sont visibles et désactivés. Le changement d'onglet est un état local.
- Menu latéral, barre du haut et filtres globaux de `LayoutAppMain.svelte` inchangés. Route dans `(without-filters)`.
- Code droit `DCP` (`absence-right.seed.ts`, libellé « Droits à Congés payés »). `CP` est le code event. Les params d'URL ne sont pas lus. Période de fixture : 01/06/2023–31/05/2024.
- Le `h1` vient de `PageTitle` dans le header. Le corps de page ne le répète pas.
- Composants sous `cronexia-gta-front-v2/app/src/routes/components/cronexia/rights-employee/`. Pas de nouveau composant Material.
- Ancienneté et fractionnement affichés **Non géré**, exclus de toutes les sommes. Les totaux mockup 25 / 18,5 ne sont pas recopiés.
- Chiffres, report consommé en premier : acquis brut 19, report brut 3, pris 3 sur report + 3,5 sur acquis = 6,5, soldes courants 15,5 / 0 / 0, solde 15,5, total synthèse 22.

## 1. Route et accès

- [x] `routes/(app)/(without-filters)/rights/[right]/dateStart/[[dateStart]]/+page.svelte` avec un placeholder. Même forme que `vacation-rights/dateStart/[[dateStart]]`. Pas de `+page.server.ts`.
- [x] Entrée `page-config.ts` : pattern `/^\/rights\/[^/]+\/dateStart(\/|$)/`, titre `Mes droits & soldes`, `hasToolbar: false`, `heightManagement: 'classic'`, `headerFilterIsDateOrPeriodPerPage: null`.
- [x] Même pattern dans `page-rights-config.ts`, à côté de `/vacation-rights`, droit `PAGE_VACATION_RIGHTS`. Pas de règle large sur `/rights` (les routes RH futures en dépendent ; un chemin sans match est ouvert).

## 2. Fixture

- [x] `rights-employee/employee-rights-fixture.ts`, champs alignés sur `ArResourceBalance` : trois soldes, cumuls bruts, trois cumuls de pris, dates d'exercice, lignes de mouvement (`effectDate`, nature, quantité, `inProgress | acquisition | report`, solde après), lignes d'absence (début, fin, type, durée, statut).
- [x] Chiffres du cadre ci-dessus. Lignes placeholder (ancienneté, fractionnement, en cours de prise) libellées Non géré et exclues des sommes.
- [x] Un helper renvoie solde, KPI acquis / pris / en cours et total synthèse. Les composants ne recalculent pas.
- [x] Mouvements d'exemple : entrée de report, acquisition mensuelle, prises sur report, prises sur acquis. Pas de mouvement ancienneté ni fractionnement.
- [x] Libellés d'heures en chaînes statiques sur la fixture.

## 3. Bandeau et carte KPI

- [x] `EmployeeRightsBanner.svelte` : `MdElevatedCard` + `MdIcon`, texte d'alerte statique du mockup.
- [x] `EmployeeRightsKpiCard.svelte` : libellé du droit, période de référence, quatre KPI (solde, acquis, pris, en cours) plus l'autre unité en statique, et `MdOutlinedButton` désactivé « Télécharger le récapitulatif ».

## 4. Onglets

- [x] `EmployeeRightsTabs.svelte` : `MdTabs` + `MdPrimaryTab`, `activeTabIndex` local seulement.
- [x] Deux panneaux vides : Vue simple et Vue avancée, avec les sous-titres du mockup.

## 5. Vue simple

- [x] `EmployeeRightsSynthesis.svelte` : lignes du helper, Non géré visibles et hors du total, solde en dernière ligne.
- [x] `EmployeeRightsDonut.svelte` : `EChartsWhenSized`, même init `echarts/core` que `VacationSoldeCard.svelte`.
- [x] Parts du donut = les trois soldes courants. Ancienneté et fractionnement en légende seulement, sans part. Centre = solde.

## 6. Vue avancée

- [x] `EmployeeRightsMovements.svelte` : `TableAdvanced` (`contents` en chaînes, `hasShell={false}`, `isHoverable`).
- [x] Colonnes Date, Nature du mouvement, Quantité, Décompté sur, Solde après.
- [x] Pied de tableau : ordre de décompte report, puis acquis, puis en cours.

## 7. Historique des prises

- [x] `EmployeeRightsHistory.svelte` : `TableAdvanced` (`contents` en chaînes, `hasShell={false}`, `isHoverable`).
- [x] Colonnes Date de début, Date de fin, Type, Durée, Statut. Statut via `Badge` (`colorsWorkflowStatus` Validated, `pill`).
- [x] `MdTextButton` désactivé « Voir toutes mes prises ».

## 8. Colonne latérale

- [x] `EmployeeRightsFilters.svelte` : deux `InputSvelecte` `size="S"` désactivés (`isClearable={false}`, pas de `name` ; période = exercice de la fixture, droit `DCP`, libellé « Droits à Congés payés ») et `MdSwitchWithLabel` désactivé « Afficher en heures ». `disabled` passe par les props rest.
- [x] `EmployeeRightsInfo.svelte` : prochaine période d'acquisition, date limite de prise, report autorisé, depuis les dates de la fixture.
- [x] `ButtonWithIcon` « En savoir plus sur vos droits » (`open_in_new`, `trailing`, `block`), actif, sans destination.

## 9. Assemblage

- [x] `EmployeeRightsPage.svelte` : bandeau, carte KPI, onglets, puis deux colonnes. Colonne principale : vue simple = synthèse + donut, vue avancée = mouvements, historique sous les deux. Colonne latérale : filtres puis infos.
- [x] Remplacer le placeholder de l'étape 1 par ce composant. Toujours un seul `h1`, celui du header.
- [x] Page `width: 100%`, `max-width: 1600px`, `margin-inline: auto`, `box-sizing: border-box`. Colonne principale `flex: 1 1 40rem`, `min-width: min(100%, 40rem)`. Aside `flex: 0 0 20rem`, `max-width: 100%`. Sous `62rem` de conteneur, aside `flex-basis: 100%`.

## 10. Seeds menu

Les seeds sont des `create`, pas des upsert. Le nouvel href n'apparaît qu'après un reset des seeds required.

- [x] `menu-link-catalog.const.ts` : lien `droits`, label `Mes droits & soldes`, href `/rights/DCP/dateStart`. Conserver `iconKey`, profils `EMPLOYEE` et `SUPER_ADMIN`, droit `PAGE_VACATION_RIGHTS`.
- [x] `menu-quick-link-defaults.const.ts` : ajouter `{ position: 8, name: 'droits' }` à `MENU_QUICK_LINK_DEFAULTS_EMPLOYEE`.
- [x] Ne pas modifier l'arbre employé (`link('droits')` est déjà là), ni `menu-node.seed.ts`, ni `menu-link.seed.ts`, ni `menu-link-on-user-profile.seed.ts`.

## 11. Vérification navigateur

- [ ] `/rights/DCP/dateStart` et `/rights/DCP/dateStart/2023-06-01` affichent la même fixture.
- [ ] Un seul titre « Mes droits & soldes ». Basculer Vue simple / Vue avancée. Les contrôles désactivés ne naviguent pas.
- [ ] Total synthèse 22, solde 15,5, lignes Non géré visibles et absentes du donut.
- [ ] Tant que les seeds required ne sont pas rejoués, le menu et le raccourci pointent encore vers `/vacation-rights`. Le noter en rendant la main.

## Hors scope

- [ ] Brancher les selects, le switch heures, le téléchargement, « en savoir plus » et la navigation des prises — tâche ultérieure.
- [ ] Résoudre l'exercice courant ou rediriger un `dateStart` invalide — tâche ultérieure.
- [ ] Remplacer `/vacation-rights`, le widget d'accueil ou le lien chatbot — hors de cette page.

---
---
---

## Adjustment made after the first pass of integration

Passe visuelle. Route, seeds et GraphQL inchangés.

Tokens `--cronexia-space-*` (`+layout.svelte`) : `3xs` 0.25rem, `2xs` 0.5rem, `xs` 0.75rem, `sm` 1rem.

### Largeurs

- Page : `width: 100%`, `max-width: 1600px`, `margin-inline: auto`, `box-sizing: border-box`.
- Colonne principale : `flex: 1 1 40rem`, `min-width: min(100%, 40rem)`. Aside : `flex: 0 0 20rem`, `max-width: 100%`. Sous `62rem` de conteneur, aside `flex-basis: 100%`.
- Vue simple : enfants `flex: 1 1 18rem`, `min-width: min(100%, 18rem)`.
- KPI : identité `flex: 1.4 1 220px`, métriques `flex: 1 1 120px`, solde `flex: 1.2 1 160px`, actions `flex: 1 1 100%`.
- Donut : anneau `168px`, légende `flex: 1 1 170px`. Selects `width: 100%`.
- Onglets : barre `width: 100%`, `md-tabs` en `fit-content` / `max-width: 100%`, `md-primary-tab` en `flex: none`.

### Marges et paddings

- Page : `--cronexia-space-2xs` / `clamp(0rem, 2vw, var(--cronexia-space-sm))` / `--cronexia-space-sm`.
- Gap page, onglets, colonnes, colonne principale, aside, synthèse/donut : `--cronexia-space-sm`. Panneaux simple et avancé : `margin-top: var(--cronexia-space-sm)`.
- Bandeau : padding `--cronexia-space-xs` `--cronexia-space-sm`, gap `--cronexia-space-xs`, `border-radius: 12px`.
- KPI : corps padding `--cronexia-space-sm`, gap `--cronexia-space-sm` `0`. Identité padding-right `--cronexia-space-sm`, gap `--cronexia-space-xs`. Métriques padding-inline `--cronexia-space-sm`, gap `--cronexia-space-3xs`. Solde padding `--cronexia-space-xs` `--cronexia-space-sm`, `border-radius: 12px`.
- Titres de carte (`h3` filtres, infos, synthèse, donut, en-tête mouvements) : padding `--cronexia-space-xs` `--cronexia-space-sm`, filet bas `outline-variant`. Historique : `SIZE_SPACE_PAD.L` / `XL` (`xs` / `sm`). Pied historique : `M` / `XL` (`2xs` / `sm`). Pied mouvements : `L` / `XL`. `.table-advanced` `gap: 0`.
- Synthèse : liste `--cronexia-space-3xs` `--cronexia-space-sm` `0`, lignes padding `--cronexia-space-xs` `0`. Pied solde padding `--cronexia-space-xs` `--cronexia-space-sm`, `border-radius: 0`.
- Infos : liste padding et gap `--cronexia-space-sm`, lignes gap `--cronexia-space-xs`. Pied bouton : `0` `--cronexia-space-2xs` `--cronexia-space-2xs` `--cronexia-space-sm`.
- Donut : corps padding bas `--cronexia-space-sm`, layout padding et gap `--cronexia-space-sm`, légende gap `--cronexia-space-xs`, note gap `--cronexia-space-2xs` et padding inline `--cronexia-space-sm`.

### Couleurs

- Cartes : `--md-elevated-card-container-color: var(--md-sys-color-surface-container-lowest)`, élévation `0`, bordure `1px` `outline-variant`. Synthèse : `overflow: hidden`.
- Bandeau : `colors.warning.subtle` (fond, texte, bordure), hors `md-elevated-card`.
- Filet d'onglets : `outline`. Fond d'onglet : `--md-primary-tab-container-color: transparent`.
- Solde KPI et pied de synthèse : `colors.primary.subtle`. Filet entre métriques : `outline-variant`, absent sur le solde. Libellé Pris : `tertiary`. En cours : `secondary`. Alternatif : `on-surface-variant` (solde : `inherit`, opacité `0.8`).
- Donut : acquis `SOLDE_CONGE_COLORS.cp`, report `rtt`, en cours `tt`, ancienneté `var(--cronexia-info)`, fractionnement `var(--cronexia-warning)`. Anneau : `getComputedStyle` pour les `var()`. Centre : couleur CP. `2` jours et `1` jour restent hors solde et hors total `22`.

### Tailles

- KPI : `.text-2xl` via `--cronexia-font-size-2xl: 2rem` et `--cronexia-line-height-2xl: 2.5rem` dans `app/static/app.css`. Unité `text-m`. Titres de vue `text-l`, corps `text-m`, note du donut `text-s`.
- `IconCronexia` : bandeau `1.25rem`, KPI `2.25rem` (`primary`), infos `22px` (`primary`), note donut `1rem`. « Télécharger le récapitulatif » garde `MdIcon`.
- `ButtonWithIcon` `block` : `font-size` S, `min-height: 2.5rem`, icône `18px`, `color: primary`, largeur `100%`, padding inline `0`, `border-radius: 0.75rem`. `open_in_new`, `trailing`, actif, sans destination.
- Donut : rayon `64%`–`85%`, centre `fontSize: 26` / `lineHeight: 30`, unité `13` / `18`, pastilles `--cronexia-space-2xs`.
