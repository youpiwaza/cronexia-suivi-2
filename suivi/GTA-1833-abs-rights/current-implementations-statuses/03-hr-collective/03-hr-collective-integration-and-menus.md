# Droits aux congés — consultation collective (Gestionnaire RH)

Intégration visuelle uniquement. Fixture statique, contrôles de page visibles et désactivés. Le code de la passe est en place. La vérification navigateur (section 9) reste ouverte : le 23/10, `/rights/collective` a redirigé vers `/login`, le corps de page n'a pas été vu.

Références visuelles :

- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/mockups/3-gestionnaire-rh---consultation-collective.png`
- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/ai-integrations-propositions/2. Consultation collective (population)-html/Collectif.dc.html`

Règles communes : `cronexia-suivi-2/suivi/GTA-1833-abs-rights/current-implementations-statuses/00-main-integration-guidelines.md`. La page individuelle (`rights-hr-individual`) est la référence de passe visuelle, pas un écran à recopier.

## Cadre (ne pas rouvrir)

- Pas de GraphQL. Les params d'URL ne sont pas lus pour remplir la page. Export et liens de cartes restent visibles et désactivés. Initialiser et Ajuster manuellement sont actifs visuellement, sans action. Reporter et Transférer restent désactivés. Les cases du tableau sélectionnent en local, sans action groupée.
- Menu latéral, barre du haut et filtres population / resource / période de `LayoutAppMain.svelte` inchangés. Route dans `(with-filters)`.
- Pas de barre « Rechercher un salarié ». Le HTML la dessine dans le bandeau déjà fourni par le layout.
- `buildCorrectedFilterUrl` n'est pas modifié : il ne conserve pas `unit`, `negativeBalanceOnly`, `balanceCalculationDate`, `groupBy`.
- Ne pas toucher `(without-filters)/rights/[right]/dateStart/[[dateStart]]`, ni le `.gitkeep` de `(with-filters)/rights/[right]`, ni les routes `rights/individual` (sauf les onglets, section 4).
- Le `h1` vient de `PageTitle` dans le header (`Droits aux congés`). Le corps de page ne le répète pas.
- Composants sous `cronexia-gta-front-v2/app/src/routes/components/cronexia/rights-hr-collective/`. Pas de nouveau composant Material.
- Codes réels : `DCP` et `RTT_2025`, en jours. La maquette écrit `DRTT` : afficher `RTT_2025`. Une ligne heures `DRC` (« Droit repos comp. remplacement »), hors des sommes de jours. Pas de droit seedé `DRC`.
- La maquette annonce 48 ressources, 144 lignes, 4 soldes prévisionnels négatifs, 7 expirations, 2 absences en attente. Le helper compte la fixture visible : 4 ressources, 9 lignes, 2 négatifs jours, 1 expiration. De la maquette : `−1,53`, `−2,17`, et le `2` des absences en attente.
- « Absences en attente de droits » affiche `2` (maquette), hors des sommes. La note d'expiration est `Dont 0 reportés automatiquement`.
- Tailles : `text-m` pour le corps, les filtres et les titres de carte (`h3`). `text-s` pour une note, le tableau, les en-têtes de groupe et le bandeau d'actions. `text-2xl` seulement pour un chiffre de KPI. Pas de `font-size` recopié du HTML. Espacements `--cronexia-space-3xs` à `--cronexia-space-sm`.
- Couleurs via `getColorInlineStyle`, en lisant `colorTheme.mode`. Pas de hex du HTML. Colonnes prévisionnelles : `var(--cronexia-warning-bg-subtle)`.

## 1. Routes

Même composant sur les deux routes profondes. Le stub ne rend pas la fixture : le layout redirige tant que `population` manque.

- [x] `routes/(app)/(with-filters)/rights/collective/+page.svelte` : ligne de chargement, comme `rights/individual/+page.svelte`. Pas de `+page.server.ts`.
- [x] `rights/collective/population/[population]/resource/[resource]/dateStart/[dateStart]/dateEnd/[dateEnd]/+page.svelte` : rend `HrCollectiveRightsPage`. Les params ne sont pas lus.
- [x] `.../unit/[unit]/negativeBalanceOnly/[negativeBalanceOnly]/balanceCalculationDate/[balanceCalculationDate]/groupBy/[groupBy]/+page.svelte` : le même composant. Valeurs prévues plus tard : `unit` `all` | `days` | `hours`, booléen, date `YYYY-MM-DD`, `groupBy` `resource`. Ces segments ne sont pas lus.

## 2. Accès

Un seul motif, `/^\/rights\/collective(\/|$)/`, dans les deux fichiers. À côté de l'individuel, avant le motif salarié. Pas de règle large sur `/rights`. Le motif salarié `/^\/rights\/[^/]+\/dateStart(\/|$)/` ne matche pas ces chemins.

- [x] `page-config.ts` : titre `Droits aux congés`, `hasToolbar: false`, `heightManagement: 'classic'`, `headerFilterIsDateOrPeriodPerPage: 'period'`, `showAllRessources: true`. Sans population, l'état vide existant reste. Avec population et période, la fixture s'affiche sans lire la ressource (y compris `ALL`).
- [x] `page-rights-config.ts` : le même motif, droit `PAGE_ABSENCES` (déjà sur le profil Gestionnaire RH). Pas de nouveau droit. Pas d'édition de `*.seed.ts`. Premier match : aucune entrée antérieure ne couvre `/rights/collective`.

## 3. Fixture

- [x] `rights-hr-collective/hr-collective-rights-fixture.ts`. Un helper renvoie libellés, comptes de groupe, comptes de KPI et cellules. Les composants ne recalculent pas.
- [x] Quatre ressources. En-tête de groupe : `Prénom Nom (matricule) · N lignes`. Ligne de droit : `Nom Prénom`. Population `Pilotes` (sous-titre et header). Période `01/06/2025 – 31/05/2027` (header). Droits du filtre `DCP, RTT_2025`. Unité Tous. Regroupements `Ressource`. Date de calcul 12/10/2026. Case « Soldes négatifs uniquement » décochée. Ces contrôles ne changent pas les lignes.
- [x] Georges Lambert, matricule `234501`, 3 lignes. DCP ouvert, acquisition 01/06/2026–31/05/2027, N° `3`. Mêmes cumuls que l'individuel : en cours 8, acquis 25, report 5, pris report 3, pris acquis 1. Droits `38,00`. Pris `4,00`. Pris prév. `5,00`. Solde prév. `27,33`.
- [x] Même ressource, `RTT_2025`, 01/01/2026–31/12/2026, N° `3`. Acquis 3, prises 0. Droits `3,00`. Pris `0,00`. Pris prév. `1,00`. Solde prév. `2,47`.
- [x] Même ressource, `DRC` heures, 28/08/2026–28/10/2026, N° `—`. Droits `07:00`, pris `03:30`, pris prév. `00:00`, solde prév. `03:30`. Pastille `Expire le 28/10`. Hors des sommes de jours et du compte de négatifs.
- [x] Jérôme Roux, `234518`, 2 lignes. DCP comme Lambert. `RTT_2025` : mêmes Droits et Pris que le RTT de Lambert. Solde prév. `−1,53` (seule valeur prise sur la maquette pour cette ligne). Badge `Solde négatif`. Case cochée.
- [x] Philippe Garnier, `234532`, 2 lignes. DCP : mêmes Droits et Pris que Lambert. Solde prév. `−2,17` (seule valeur prise sur la maquette pour cette ligne). Badge `Solde négatif`. Case cochée. `RTT_2025` comme Lambert, solde prév. `2,47`, case décochée.
- [x] Bruno Moreau, `234547`, 2 lignes. DCP comme Lambert. `RTT_2025` : mêmes Droits et Pris. Solde prév. `0,00`.
- [x] Helper. Droits jours = cumuls en cours + acquis + report. Pris jours = cumuls de prises. Heures en `HH:MM`, non additionnées aux jours. KPI 1 = 4 ressources. Sous-titre = `Population Pilotes · 4 ressources · 9 lignes de droits`. KPI 2 = 2 (lignes jours au solde prév. négatif). KPI 3 = 1 (pastille d'expiration). KPI 4 = `2`. Note d'expiration = `Dont 0 reportés automatiquement`. Libellé d'unité tableau : `JOUR` / `HEURE`.
- [x] Détail ouvert : réutiliser la fixture individuelle telle quelle (`HrIndividualRightsExerciseDetail`). Mêmes mouvements du DCP ouvert et mêmes règles pour chaque ligne, y compris `DRC`. Le collectif ne redéfinit pas ces lignes.

## 4. En-tête, onglets, filtres

`disabled` passe par les props du composant. Les filtres de page sont locaux : ils ne naviguent pas et ne filtrent pas le tableau.

- [x] Sous-titre `text-m`, couleur `on-surface-variant`. Pas d'avatar. `Exporter` désactivé. Pas de second `h1`. Pas de champ de recherche.
- [x] `PageTabs` (pas `MdTabs`). Liens nus `/rights/individual` et `/rights/collective`. `activeKey` depuis le pathname. Pas de pastille. Le layout réécrit population et période depuis les cookies. La ressource n'est pas recopiée dans l'href : l'individuel est `showAllRessources: false`, le collectif est `true`. Annuler le `margin-bottom` de `PageTabs` sur ces deux pages seulement, le gap de la coque suffit. Ne pas modifier `PageTabs.svelte`.
- [x] Mêmes onglets dans `HrIndividualRightsIdentity.svelte`, via `HrRightsPageTabs`. Le doc individuel ne dit plus que le clic reste local : les deux href sont nues.
- [x] Filtres dans une `MdElevatedCard`, barre horizontale. Pas de second champ Population ni « Période affichée » : ceux du header suffisent. Regroupements : `MdOutlinedSvelecte` `size="S"`, une option de fixture, chrome `text-s`. Droits : `ChipGroupSelect`, puces `DCP` et `RTT_2025` (`DRC` hors du filtre). Unité : `FilterPills` (`showCounts={false}`, `allTogglesEvery`), départ Tous. `MdCheckbox` « Soldes négatifs uniquement », dernier contrôle aligné à gauche, sur la même ligne. Champ date et chevrons alignés à droite. Le filtre Population du header reste le seul qui navigue.

## 5. Cartes KPI

Pas les cartes jours/heures de l'individuel : le contenu n'est pas le même.

- [x] Quatre cartes. Chiffre `text-2xl`, libellé `text-m`, note `text-s`. Carte 1 neutre : « Ressources dans la population », valeur 4. Carte 2 : « Soldes prévisionnels négatifs », valeur 2, bordure et chiffre `colors.warning.classic`. « Filtrer pour les traiter » désactivé. Carte 3 : « Droits expirant sous 30 jours », valeur 1, même teinte warning. Note `Dont 0 reportés automatiquement`. Carte 4 neutre : « Absences en attente de droits », valeur `2`. Padding vertical `2xs`. « Voir les anomalies de planning » désactivé.

## 6. Tableau

- [x] Un `TableAdvanced`, mode `children`. Recherche, options, filtre, tri et pagination désactivés. `isHoverable`, `hasShell={false}`. Le `text-s` est posé sur le `.table-advanced` enfant direct (la racine du composant porte `text-m`, un parent ne suffit pas). `gap: 0` sur ce même enfant, pas sur le tableau des mouvements du détail. Largeurs de colonnes en `ch` + `0.7rem`, padding inline `0.35rem`, comme le tableau d'exercices. Colonnes : case, Ressource, Code, Libellé du droit, Unité, Début, Fin, N°, Droits, Pris, Pris prév., Solde prév., Alerte. Nombres à droite à partir de Droits. Ressource prend la largeur restante (`width: 100%`). Libellé et Alerte ont une largeur fixe.
- [x] En-tête de ressource. Chevron `chevron_right` replié (pointe vers la droite), `expand_more` ouvert (pointe vers le bas), `--md-icon-size: 20px`. Clic, Entrée et Espace basculent. Chaque ressource est indépendante. Départ : toutes ouvertes. Replié : les lignes de cette ressource et leurs accordéons ne sont pas rendus. Fond `surface-container-high`, distinct du détail ouvert (`surface-container-low`). Filet bas `on-surface` à 22 %. Case de la ressource : coche tout le groupe, état indéterminé si une partie seulement est cochée. Le clic sur la case ne replie pas le groupe.
- [x] Deux composants de ligne, jours et heures. Le parent choisit selon `managedBy`. Clic, Entrée et Espace basculent. Chaque ligne est indépendante : plusieurs peuvent rester ouvertes. Départ : toutes repliées. La case est active et ne bascule pas la ligne. La case d'en-tête coche ou décoche toutes les lignes. Départ : Roux `RTT_2025` et Garnier `DCP`. Le compte du bandeau suit la sélection (`1 ligne sélectionnée` / `N lignes sélectionnées`).
- [x] Ligne ouverte : `TableRowAccordion`, enfant direct du `tbody`, `colSpan` 13, sans `accentColor`. Contenu : `HrIndividualRightsExerciseDetail` (mouvements et règles). Fond de la ligne ouverte : `primary-container`. Lignes cochées (Roux `RTT_2025`, Garnier `DCP`) : `colors.primary.subtle`, distinct de la ligne ouverte.
- [x] En-têtes Pris prév. et Solde prév. : `--cronexia-warning-bg-subtle`. Solde prév. négatif : `colors.danger.classic`, badge `Badge` `color="danger"` `variant="subtle"`. Expiration : `Badge` `color="warning"` `variant="subtle"`.
- [x] Bandeau d'actions dans la carte, sous le tableau. Fond `surface` (blanc en clair). « N lignes sélectionnées » en gras, `on-surface`. « Actions groupées : » et la note en `on-surface-variant`, note en `text-s`, alignée à droite. Boutons actifs : Initialiser, Ajuster manuellement (couleur outlined par défaut, hauteur `2rem`). Boutons désactivés : Reporter (phase 2), Transférer (à venir). Padding vertical identique à l'en-tête de carte : `xs`.

## 7. Assemblage

- [x] Coque `HrCollectiveRightsPage.svelte`. `width: 100%`, `max-width: 1600px`, `margin-inline: auto`, `box-sizing: border-box`. Colonne, `gap: var(--cronexia-space-sm)`. Cartes : `--md-elevated-card-container-color: var(--md-sys-color-surface-container-lowest)`, élévation `0`, bordure `1px` `outline-variant`. Pas de second `h1`. Pas de recherche.
- [x] Ordre de la maquette dans cette coque : en-tête, filtres, KPI, carte du tableau.
- [x] Remplacer les placeholders des deux routes profondes par ce composant. Le stub `rights/collective/+page.svelte` reste une ligne de chargement. Toujours un seul `h1`, celui du header.

## 8. Menu

Les seeds sont des `create`, pas des upsert. Le lien n'apparaît qu'après un reset des seeds required. Ne pas modifier `menu-node.seed.ts`, `menu-link.seed.ts`, ni `menu-link-on-user-profile.seed.ts`. Pas de raccourci.

- [x] `menu-link-catalog.const.ts` : lien `droits_consultation_collective`, label `Consultation collective`, href `/rights/collective`, icône `calendar2Heart`, profils `HR_MANAGER` et `SUPER_ADMIN`, droit `PAGE_ABSENCES`.
- [x] `menu-node-trees.const.ts` : dans le dossier `droits_conges` de `MENU_NODE_TREE_HR_MANAGER`, après `droits_consultation_individuelle`. L'arbre super admin embarque déjà l'arbre RH.

## 9. Vérification navigateur

Passe du 23/10 arrêtée sur `http://127.0.0.1:5173/login`. Un bandeau Vite montrait un `bind:activeTabIndex` déjà retiré de `HrIndividualRightsIdentity.svelte` ; après rechargement, le formulaire de connexion s'affiche sans cette erreur. Les cases ci-dessous restent ouvertes.

- [ ] `/rights/collective` sans population affiche l'état vide existant, pas la fixture. Avec population et période, l'URL à 4 paramètres affiche la fixture, y compris si la ressource vaut `ALL`.
- [ ] Une URL longue dont population, ressource et période correspondent déjà aux filtres résolus affiche la même fixture. Une URL longue qui ne correspond pas est réécrite vers l'URL à 4 paramètres.
- [ ] Un seul titre « Droits aux congés ». Pas de barre « Rechercher un salarié ». Les contrôles de page désactivés ne naviguent pas. Population, ressource et période du header naviguent encore.
- [ ] Onglet Individuel ouvre `/rights/individual` sans emporter la ressource du collectif. Onglet Collectif, depuis l'individuel, ouvre `/rights/collective` sans emporter la ressource unique. Population et période suivent les cookies.
- [ ] Replier une ressource masque ses lignes. Ouvrir une ligne insère mouvements et règles. Plusieurs lignes peuvent rester ouvertes. Départ : groupes ouverts, lignes repliées.
- [ ] KPI 4, sous-titre 9 lignes, négatifs 2, expiration 1. Solde prév. Lambert DCP `27,33`, Roux `RTT_2025` `−1,53`, Garnier DCP `−2,17`. La ligne `DRC` n'entre pas dans les négatifs. Carte 4 : `2`. Note d'expiration : `Dont 0 reportés automatiquement`.
- [ ] Clair et sombre : cartes warning, colonnes prévisionnelles, négatif, badges, ligne ouverte, bandeau inverse.
- [ ] Tant que les seeds required ne sont pas rejoués, l'entrée de menu est absente. Le noter en rendant la main.

## Hors scope

- [ ] Brancher les filtres de page, l'export, les actions groupées et les liens de cartes — tâche ultérieure. Les cases sélectionnent déjà en local.
- [ ] Lire les params d'URL — tâche ultérieure.
- [ ] Conserver `unit`, `negativeBalanceOnly`, `balanceCalculationDate` et `groupBy` dans `buildCorrectedFilterUrl` — tâche ultérieure.
- [ ] GraphQL — hors de cette passe.
