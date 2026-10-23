# Droits aux congés — consultation individuelle (Gestionnaire RH)

Intégration visuelle uniquement. Fixture statique, contrôles de page visibles et désactivés. Cocher chaque case au fur et à mesure.

Références visuelles :

- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/mockups/2-gestionnaire-rh---consultation-individuelle.png`
- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/ai-integrations-propositions/1. Consultation individuelle des droits-html/Main.dc.html`

Règles communes : `cronexia-suivi-2/suivi/GTA-1833-abs-rights/current-implementations-statuses/00-main-integration-guidelines.md`. La page salarié (`rights-employee`) est l'exemple de passe visuelle, pas un écran à recopier.

## Cadre (ne pas rouvrir)

- Pas de GraphQL. Les params d'URL ne sont pas lus. Export et « Voir la ligne » restent visibles et désactivés. Individuel / Collectif sont des `PageTabs` : liens nus `/rights/individual` et `/rights/collective`. Le layout réécrit population et période. La ressource n'est pas recopiée dans l'href.
- Menu latéral, barre du haut et filtres population / resource / période de `LayoutAppMain.svelte` inchangés. Route dans `(with-filters)`.
- La liste de droits (virgules) reste hors de l'URL. `buildCorrectedFilterUrl` n'est pas modifié : il ne conserve pas `unit`, `details`, `balanceCalculationDate`.
- Ne pas toucher `(without-filters)/rights/[right]/dateStart/[[dateStart]]`, ni le `.gitkeep` de `(with-filters)/rights/[right]`.
- Le `h1` vient de `PageTitle` dans le header (`Droits aux congés`). Le corps de page ne le répète pas.
- Composants sous `cronexia-gta-front-v2/app/src/routes/components/cronexia/rights-hr-individual/`. Pas de nouveau composant Material.
- Codes réels : `DCP` (« Droits à Congés payés ») et `RTT_2025` (« Droits à RTT »), tous deux en jours. Deux lignes heures `DRC` (« Droit repos comp. remplacement »), maquette HTML, hors des sommes. La troisième carte KPI reste une maquette heures (`Repos compensateur · DRC`, `06:30`), elle aussi hors des sommes.
- Les cartes KPI lisent l'exercice ouvert de chaque droit, pas la somme des lignes. Solde à date DCP ouvert : 32. Prévisionnel des cartes : maquette `27,33` (DCP) et `2,47` (RTT). Solde prév. des jours ouverts reprend ces chiffres. Pris prév. maquette : DCP ouvert `5`, RTT `1`, jours clôturés `0`, lignes `DRC` `00:00`. Le `versionNumber` seedé vaut `1` ; les N° de fixture des jours restent `2` et `3`.

## 1. Routes

Même composant sur les deux routes profondes. Le stub ne rend pas la fixture : le layout redirige tant que `population` manque.

- [x] `routes/(app)/(with-filters)/rights/individual/+page.svelte` : ligne de chargement, comme `individual-schedule/+page.svelte`. Pas de `+page.server.ts`.
- [x] `rights/individual/population/[population]/resource/[resource]/dateStart/[dateStart]/dateEnd/[dateEnd]/+page.svelte` : placeholder, en attendant l'assemblage.
- [x] `.../unit/[unit]/details/[details]/balanceCalculationDate/[balanceCalculationDate]/+page.svelte` : le même placeholder. Valeurs prévues plus tard : `unit` `all` | `days` | `hours`, `details` `true` | `false`, date `YYYY-MM-DD`.

## 2. Accès

Un seul motif, `/^\/rights\/individual(\/|$)/`, dans les deux fichiers. Pas de règle large sur `/rights`. Le motif salarié `/^\/rights\/[^/]+\/dateStart(\/|$)/` ne matche pas ces chemins.

- [x] `page-config.ts` : titre `Droits aux congés`, `hasToolbar: false`, `heightManagement: 'classic'`, `headerFilterIsDateOrPeriodPerPage: 'period'`, `showAllRessources: false`. Sans ressource, l'état vide existant reste. Avec une ressource, la fixture s'affiche sans la lire.
- [x] `page-rights-config.ts` : le même motif, droit `PAGE_ABSENCES` (déjà sur le profil Gestionnaire RH). Pas de nouveau droit. Pas d'édition de `*.seed.ts`. Premier match du tableau : aucune entrée antérieure ne couvre `/rights/individual`.

## 3. Fixture

- [x] `rights-hr-individual/hr-individual-rights-fixture.ts`. Un helper renvoie libellés et totaux. Les composants ne recalculent pas.
- [x] `DCP` et `RTT_2025` dans les exercices jours. Libellés d'unité `Jours` et `Heures`. Deux lignes `DRC` en heures, hors des sommes et de `openExercise`. La troisième carte KPI est la maquette heures, hors des sommes.
- [x] DCP ouvert, acquisition 01/06/2026–31/05/2027, N° `3`. Cumuls : en cours 8, acquis 25, report 5, pris report 3, pris acquis 1, perdu report 2. Soldes courants : report 0, acquis 24, en cours 8. Solde à date 32. Pris 4. Perdu/payé 2. Pris prév. `5`. Solde prév. `27,33`.
- [x] DCP clôturé, acquisition 01/06/2025–31/05/2026, N° `2`. Soldes courants 0, pris 13,5, perdu 4,5, autres colonnes de cumul `—`. Pris prév. `0`. Solde prév. `0`. Le helper pose `isClosed` (fin avant le 12/10/2026). Ces pris / perdu ne s'ajoutent pas à la carte DCP ouverte.
- [x] `RTT_2025`, un exercice replié 01/01/2026–31/12/2026, N° `3`. Solde à date 3 (acquis seul). Pris prév. `1`. Solde prév. `2,47`.
- [x] `DRC` 28/08/2026–28/10/2026 : acquis `07:00`, pris `03:30`, solde `03:30`, pris prév. `00:00`, solde prév. `03:30`, autres cellules `—`, pastille `Expire dans 16 j`. `DRC` 15/09/2026–15/11/2026 : acquis `03:00`, pris `00:00`, solde `03:00`, pris prév. `00:00`, solde prév. `03:00`, pas de pastille. `managedBy` `days` | `hours`.
- [x] Mouvements du DCP ouvert : transfert acquis +25, transfert report +5, ajout en cours +8, prise report −3, prise acquis −1, perte report −2. Deux lignes Non géré exclues : « Nouvel exercice » et la prise prévisionnelle.
- [x] Règles : ordre Report, puis Acquis, puis En cours ; plafond de report 5 j, délai 3 mois, report automatique ; anticipation depuis `takeByAnticipationPolicy`. « Solde minimum autorisé » : Non géré.
- [x] Identité et contrôles en chaînes de fixture, pas lus depuis la ressource ni l'URL. Camille Durand, matricule, population, « Entrée le » (pas de colonne date d'entrée sur `Resource`). Période `01/06/2025 – 31/05/2027`, droits `DCP, RTT_2025`, unité Tous, détail coché, date de calcul 12/10/2026. Bandeau : délai de report DCP, pas la ligne DRC 03:30. Colonnes Pris prév. et Solde prév. visibles. Les lignes heures n'entrent pas dans les sommes.

## 4. Identité, filtres, bandeau

`disabled` passe par les props du composant.

- [x] Identité : initiales, nom, matricule, population, entrée. Onglets `PageTabs` (`HrRightsPageTabs`) : liens nus vers `/rights/individual` et `/rights/collective`, onglet actif selon l'URL. `Exporter` désactivé.
- [x] Filtres actifs, valeurs initiales de la fixture. Période : `MdOutlinedSvelecte` `size="S"`, même chrome que les filtres du header. Droits : `ChipGroupSelect` (puces `DCP` et `RTT_2025`). Tous / Jours / Heures via `FilterPills` (`showCounts={false}`, `allTogglesEvery`) : les trois cochés au départ ; Jours ne coche que Jours, Heures ne coche que Heures ; Tous bascule les deux ensemble (actif = les deux cochés, inactif = les deux décochés). `MdCheckbox` pour le détail. Champ date et chevrons actifs. Le filtre de période du header reste actif. Pas de navigation ni de GraphQL depuis ces champs.
- [x] Bandeau : `colors.warning.subtle` via `getColorInlineStyle`, hors `md-elevated-card`, comme `EmployeeRightsBanner.svelte`. « Voir la ligne » désactivé.

## 5. Cartes KPI

- [x] Trois cartes. `HrIndividualRightsKpiDaysCard` pour DCP et `RTT_2025` (exercice ouvert) : titre sans le préfixe « Droits à » (`Congés payés · DCP`, `RTT · RTT_2025`), pastille `colors.primary.subtle` « Exercice … » en `text-s`, prévisionnel maquette `27,33` et `2,47`, légende à deux décimales (`24,00`). `HrIndividualRightsKpiHoursCard` pour la maquette : `Repos compensateur · DRC`, pastille `colors.secondary.subtle` « Sans exercice », soldes `06:30`, légende `Acquis 06:30`, « Prochaine expiration le 28/10/2026 » en `text-s` alignée à droite. Hors des sommes. Le chiffre du solde à date reprend la couleur Acquis. Le chiffre du prévisionnel et le point Report reprennent `colors.warning.classic`.
- [x] Barre empilée en CSS. Acquis `SOLDE_CONGE_COLORS.cp`, Report `colors.warning.classic`, en cours `tt`. Pas d'ECharts. Une tranche à 0 reste dans la légende et ne prend pas de largeur.

## 6. Exercices, mouvements, règles

- [x] Un `TableAdvanced` pour les exercices, en `children` (le mode `contents` n'insère rien entre deux lignes). Recherche, options, filtre, tri et pagination désactivés, `isHoverable`, `hasShell={false}`. `HrIndividualRightsExerciseDaysTr` : badge Clôturé (lit `isClosed` seulement). `HrIndividualRightsExerciseHoursTr` : pastille warning `Expire dans 16 j` quand la ligne en a une. Le parent choisit selon `managedBy`. Chevron `expand_more` / `expand_less`. Clic sur la ligne, Entrée et Espace basculent. Le tableau d'exercices n'affiche plus « Non géré ».
- [x] Une ligne ouverte à la fois. Départ : l'exercice qui porte les mouvements (DCP ouvert). Les autres lignes, y compris les deux `DRC`, partent repliées. Le panneau s'insère sous la ligne ouverte (`TableRowAccordion`, `colSpan` 15). Même fixture pour chaque ligne : mouvements du DCP ouvert et règles partagées.
- [x] `HrIndividualRightsExerciseDetail` : mouvements `flex: 1 1 40rem`, règles `flex: 0 0 20rem`. Sous `62rem` de conteneur, les règles passent en pleine largeur. Le filet et le padding viennent de `TableRowAccordion`.

## 7. Assemblage

- [x] `HrIndividualRightsPage.svelte`. Ordre de la maquette : identité, filtres, bandeau, KPI, carte des exercices. `width: 100%`, `max-width: 1600px`, `margin-inline: auto`, `box-sizing: border-box`. Cartes : `--md-elevated-card-container-color: var(--md-sys-color-surface-container-lowest)`, élévation `0`, bordure `1px` `outline-variant`. Barre de filtres horizontale.
- [x] Remplacer les placeholders des deux routes profondes par ce composant. Le stub `rights/individual/+page.svelte` reste une ligne de chargement. Toujours un seul `h1`, celui du header.

## 8. Menu

Les seeds sont des `create`, pas des upsert. Le lien n'apparaît qu'après un reset des seeds required. Ne pas modifier `menu-node.seed.ts`, `menu-link.seed.ts`, ni `menu-link-on-user-profile.seed.ts`. Pas de raccourci.

- [x] `menu-link-catalog.const.ts` : lien `droits_consultation_individuelle`, label `Consultation individuelle`, href `/rights/individual`, icône `calendar2Heart`, profils `HR_MANAGER` et `SUPER_ADMIN`, droit `PAGE_ABSENCES`.
- [x] `menu-node-trees.const.ts` : dans `MENU_NODE_TREE_HR_MANAGER` seulement, après `absences`, dossier `droits_conges` / `Droits à congés` / icône `calendar2Heart`, avec ce seul lien. L'arbre super admin embarque déjà l'arbre RH.

## 9. Vérification navigateur

- [ ] `/rights/individual` sans ressource affiche l'état vide existant, pas la fixture. Après sélection d'une ressource, l'URL à 4 paramètres affiche la fixture.
- [ ] Une URL longue dont population, ressource et période correspondent déjà aux filtres résolus affiche la même fixture. Une URL longue qui ne correspond pas est réécrite vers l'URL à 4 paramètres.
- [ ] Un seul titre « Droits aux congés ». Les contrôles de page désactivés ne naviguent pas. Population, ressource et période du header naviguent encore.
- [ ] Solde à date DCP 32, depuis l'exercice ouvert seulement. Prévisionnel des cartes : `27,33` et `2,47`, hors des sommes. Pris prév. : `5`, `0`, `1`, puis `00:00` sur les deux lignes `DRC`. Solde prév. : `27,33`, `0`, `2,47`, puis `03:30` et `03:00`. La carte heures affiche `06:30` sans entrer dans les sommes.
- [ ] Tant que les seeds required ne sont pas rejoués, l'entrée de menu est absente. Le noter en rendant la main.

## Hors scope

- [ ] Brancher les filtres de page, l'export et « Voir la ligne » — tâche ultérieure. L'onglet Collectif ouvre `/rights/collective`.
- [ ] Lire les params d'URL, y compris la liste de droits — tâche ultérieure.
- [ ] Conserver `unit`, `details` et `balanceCalculationDate` dans `buildCorrectedFilterUrl` — tâche ultérieure.
- [ ] GraphQL — hors de cette passe.
