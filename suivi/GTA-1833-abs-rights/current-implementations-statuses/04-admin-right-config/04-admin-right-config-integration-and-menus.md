# Paramétrage d'un droit (Administrateur)

Intégration visuelle uniquement. Fixture statique. Rien n'est en place : cocher au fur et à mesure. Les contrôles de page sont visibles et figés (`disabled`, ou `isReadOnly` quand c'est la prop du composant). Pas de `name`. Le select de version est la seule exception : il change la fixture en local.

Références visuelles :

- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/mockups/4-paramétrage-droits-a-absences---CP.png`
- `cronexia-suivi-2/suivi/GTA-1833-abs-rights/ai-integrations-propositions/4. Paramétrage d'un droit-html/Fiche-droit.dc.html`

Règles communes : `cronexia-suivi-2/suivi/GTA-1833-abs-rights/current-implementations-statuses/00-main-integration-guidelines.md`. La page collective (`rights-hr-collective`) est la référence de coque. Le formulaire déjà en place sous `components/cronexia/absence-right/` est la référence des champs, pas un écran à recopier.

## Cadre (ne pas rouvrir)

- Pas de GraphQL. Pas de `+page.server.ts`. Les params d'URL ne sont pas lus. Annuler, Dupliquer et Enregistrer restent visibles et désactivés. Ils n'appellent pas `AbsenceRightForm`.
- Menu latéral, barre du haut et `LayoutAppMain.svelte` inchangés. Route dans `(without-filters)`.
- Le `h1` vient de `PageTitle` dans le header (`Paramétrage d'un droit`). Le corps de page ne le répète pas. Le droit sélectionné est un titre de vue `text-l` : `DCP · Droits à Congés payés`.
- Composants de page sous `cronexia-gta-front-v2/app/src/routes/components/cronexia/rights-admin-config/`. Pas de nouveau composant Material.
- La maquette dessine six cartes numérotées et des pastilles `1`–`6`. On ne les reproduit pas. Chaque section existante a déjà son titre `FormSection`. Les regrouper dans une seconde carte doublerait le titre, et le découpage ne colle pas (report et seconde population dans `VersionPopulationsSection`, solde minimum aussi dans `VersionConfigSection`, event dans `VersionEventsPrioritiesSection`, exercice concret dans `VersionExerciseSection`).
- Ne pas monter `ManageAbsenceRight`, `AbsenceRightArray`, ni `AbsenceRightForm`. Ne pas modifier les pages `_dev/test/absence-rights`. Ne pas modifier les sections `Version*`.
- `AbsenceRightDetails` et `AbsenceRightForm` lisent `arRightsVersions[0]`. Cette page ne reprend pas ce raccourci. La requête n'a pas d'`orderBy`.
- La version n'est pas dans l'URL. L'état local est un `idArVersion`. Départ : la date d'effet la plus récente (version 3), pas l'index 0.
- `isRightsAlreadyCalculated` reste `false`, comme le seed. Pas de bandeau cadenas. Pas de pastille « Droits déjà calculés ». Les sections de détail sont déjà en `isReadOnly` ; le flag ne change que l'infobulle de `VersionConfigSection`.
- Tailles : `text-m` pour le corps, `text-l` pour le titre de vue, `text-s` pour une note. Pas de `font-size` recopié du HTML. Espacements `--cronexia-space-3xs` à `--cronexia-space-sm`.
- Couleurs via `getColorInlineStyle`, en lisant `colorTheme.mode`. Pas de hex du HTML.
- Les enfants n'importent pas la fixture. Seule la page de route la passe. `AdminRightConfigPage` reçoit `absenceRights: AbsenceRightModel[]` et `absenceRight: AbsenceRightModel | null`.

## 1. Routes

Même composant avec ou sans code. Le paramètre n'est pas lu.

- [x] `routes/(app)/(without-filters)/admin/right/code/[[code]]/+page.svelte` rend `AdminRightConfigPage` avec la fixture. Pas de `+page.server.ts`.
- [x] `/admin/right/code` et `/admin/right/code/DCP` affichent la même fixture. `/admin/right` n'est pas une route.

## 2. Accès

Un motif `/^\/admin\/right(\/|$)/`. Pas de nouveau droit. Pas d'édition de `*.seed.ts`.

- [x] `page-config.ts` : le motif avec les autres entrées admin. `getPageConfig` trie par longueur de motif, donc il passe avant `/^\/admin/`. Titre `Paramétrage d'un droit`, `hasToolbar: false`, `heightManagement: 'classic'`, `headerFilterIsDateOrPeriodPerPage: null`, `showAllRessources: false`.
- [x] `page-rights-config.ts` : le même motif **avant** `/^\/admin/` (premier match, pas de tri). Droit `PAGE_ADMIN`.

## 3. Fixture

- [x] `rights-admin-config/admin-right-config-fixture.ts`. Retourne `{ absenceRights, absenceRight }` en `AbsenceRightModel`. Seule la page de route l'importe.
- [x] Droit `DCP`. `labelShort` `Droits CP`. `labelLong` `Droits à Congés payés`. `effectDateEnd` `2030-12-31`. `isRightsAlreadyCalculated` `false`. `isAllowToChangeEvents` `true`. Event `CP` (`Congés payés`).
- [x] Ligne de liste `RTT_2025`, libellé `Droits à RTT`, en jours. Pas de détail de version pour cette ligne. La liste compte `Droits (2)`. `DRTT`, `DRC`, `DCPA`, `DCET`, `DAFO` sont absents.
- [x] Trois versions sur `DCP`, mêmes dates relatives et mêmes populations. Dates relatives (mois relatif, donc `MM`) : début d'acquisition `01/MM/Année N-1`, fin `31/MM/Année N`, début de prise `01/MM/Année N+1`, fin `31/MM/Année N+1`. Périodicité `1 mois`. Anticipation `Droits cumulés à ce jour`. La date d'ouverture seedée n'est pas affichée : `VersionTakeSection` ne la montre que pour « non cumulés au-delà de ce jour ».
- [x] Version 1 : effet `2024-06-01`, libellé `Année N-1`, exercice `CP_EX_2025` (acquisition `01/06/2024–31/05/2025`, prise `01/06/2025–31/05/2026`). Liste de transferts vide.
- [x] Version 2 : effet `2025-06-01`, libellé `Année N`, exercice `CP_EX_2026` (acquisition `01/06/2025–31/05/2026`, prise `01/06/2026–31/05/2027`). Liste de transferts vide.
- [x] Version 3 : effet `2026-06-01`, libellé `Année N+1`, exercice `CP_EX_2027` (acquisition `01/06/2026–31/05/2027`, prise `01/06/2027–31/05/2028`). Seule version qui porte les transferts.
- [x] Deux populations cibles sur chaque version. Première : `Absences en droits > Max et Bob chevasson pour congés payés avec un acquisition de 2,5`, constante `2.5`, plafond `10`, report automatique, solde minimum `0`, délai de report `1 an`. Seconde : `Absences en droits > PO pour congés payés avec un acquisition de 3`, constante `3`, plafond `15`, report non automatique, solde minimum `-5`, même délai `1 an`. Pas de population « Tous ».
- [x] Transferts de la version 3 seulement. Plafond constant `10` sur la population `2,5`. Plafond compteur sur la population PO. `RTT_2025` n'a pas de transfert.
- [x] `buildAdminRightConfigSummary(version: ArVersionModel)` pour l'aside seulement. Les sections ne l'appellent pas. Elles lisent le modèle. Compteurs vides : les sections n'écrivent pas « Aucun ».
- [x] Départ affiché : version 3, choisie par date d'effet la plus récente.

## 4. Coque, en-tête, liste

`AdminRightConfigPage` reçoit `absenceRights` et `absenceRight`. Les enfants n'importent pas la fixture.

- [x] Coque : `width: 100%`, `max-width: 1600px`, `margin-inline: auto`, `box-sizing: border-box`, colonne, `gap: var(--cronexia-space-sm)`. Cartes de liste et d'aside : `--md-elevated-card-container-color: var(--md-sys-color-surface-container-lowest)`, élévation `0`, bordure `1px` `outline-variant`.
- [x] Trois colonnes, `container-type: inline-size`. Liste `flex: 0 0 16rem`, formulaire `flex: 1 1 40rem`, aside `flex: 0 0 20rem`. Sous `62rem`, chaque colonne `flex-basis: 100%`.
- [x] En-tête : titre `text-l` `DCP · Droits à Congés payés`. Pastille `Badge` Actif (`success` subtle), dérivée de `effectDateEnd` encore à venir. Pas de pastille « Droits déjà calculés ». `MdOutlinedButton` Annuler et Dupliquer, `MdFilledButton` Enregistrer, tous désactivés. Pas de second `h1`. Pas de bandeau cadenas.
- [x] Liste dans une `MdElevatedCard`. Filtre et `+ Nouveau` désactivés. Les lignes viennent de `absenceRights`. Ligne sélectionnée : `absenceRight.code`, fond `colors.primary.subtle`, barre primaire en inset. Clic sans effet. Prop optionnelle `onSelect(code)` non branchée. Ne pas réutiliser `AbsenceRightArray`.

## 5. Colonne formulaire

L'état `idArVersion` vit dans la page. Les champs du droit ne changent pas quand la version change.

- [x] `InputSvelecte` de version au-dessus de la pile. Options au format `01/06/2026 - Année N+1`. Départ : version 3. Le changement reste local : pas de navigation, pas d'URL.
- [x] Bloc du droit, champs existants en `isReadOnly`, sans `name` : code, libellé court, libellé long, `InputDate` de fin d'effet, `IsRightsAlreadyCalculated`, `InputSwitch` « Changement d'événements autorisé ».
- [x] Pile des sections existantes, non modifiées, dans l'ordre de `AbsenceRightDetails` : `VersionConfigSection`, `VersionAcquisitionSection`, `VersionTakeSection`, `VersionExerciseSection`, `VersionEventsPrioritiesSection`, `VersionPopulationsSection`, `VersionTransferSection`, `VersionCountersSection`. On leur passe l'`ArVersionModel` sélectionnée. Pas de carte autour d'une section. Pas de pastilles `1`–`6`.
- [x] La première population (`2.5`, plafond `10`, report automatique, minimum `0`) apparaît dans `VersionAcquisitionSection` et `VersionConfigSection`, puis à nouveau dans `VersionPopulationsSection` avec la seconde. On garde ce doublon : c'est la page de détail actuelle. Affichage `toString()` : `2.5`, pas `2,5`. Le délai de report passe par `periodToString` : `1 an`.
- [x] `VersionTransferSection` affiche son tableau (tri et pagination déjà dans le composant) sur la version 3 seulement. Versions 1 et 2 : la section ne rend rien. Pas de select « Aucune ». Pas de pastille « Développement futur ».
- [x] Sous la pile, deux lignes de texte **Non géré** : « Vérifier l'appartenance à la population cible à la date de prise », et les ajustements manuels (en cours, acquis, report) avec la mention `Phase 2`. Pas des champs ajoutés dans une section.

## 6. Aside

Quatre `MdElevatedCard`, alimentées par `buildAdminRightConfigSummary` de la version sélectionnée. Changer de version met à jour l'aside et la pile ensemble.

- [x] Résumé : code `DCP`, unité Jours, event `CP`, population de la première cible, acquisition `2,5 j par mois`, solde minimum `0 j`.
- [x] Frise : couleurs `colors.primary` et `colors.warning` via `getColorInlineStyle`. Libellés = dates absolues de l'exercice de la version, et report `1 an` / plafond `10` de la première cible. Pas de hex du HTML.
- [x] Règles en clair, cinq lignes dérivées. L'ordre de décompte (« report, puis acquis, puis en cours ») est la phrase statique de la page individuelle, pas un champ stocké.
- [x] Liens utiles visibles et inert. Pas de route législation.

## 7. Menu

Les seeds sont des `create`, pas des upsert. Le lien n'apparaît qu'après un reset des seeds required. Ne pas modifier `menu-node.seed.ts`, `menu-link.seed.ts`, ni `menu-link-on-user-profile.seed.ts`. Pas de raccourci.

- [x] `menu-link-catalog.const.ts` : lien `parametrage_droit`, label `Droits à absence`, href `/admin/right/code`, icône `calendar2Heart`, profils `ADMIN` et `SUPER_ADMIN`, droit `PAGE_ADMIN`.
- [x] `menu-node-trees.const.ts` : dans `MENU_NODE_TREE_ADMIN` seulement, dossier `droits_absence` / `Droits à absence` / icône `calendar2Heart`, avec ce seul lien. L'arbre super admin embarque déjà l'arbre admin. Pas de lien « Législations », pas de second « Populations » ni « Calendriers ».

## 8. Vérification navigateur

- [ ] Un seul titre « Paramétrage d'un droit ». Le corps affiche `DCP · Droits à Congés payés` sans second `h1`.
- [ ] `/admin/right/code` et `/admin/right/code/DCP` montrent la même fixture. Annuler, Dupliquer, Enregistrer, le filtre et `+ Nouveau` ne font rien.
- [ ] Le select de version passe l'exercice de `CP_EX_2027` à `CP_EX_2026` puis `CP_EX_2025`. Les cibles `2.5` et `3` ne bougent pas. Le tableau de transfert n'est là que sur la version 3.
- [ ] Report `1 an`, plafond `10` sur la première cible. Les deux populations sont listées. La liste contient 2 droits. Pas de bandeau cadenas.
- [ ] Clair et sombre : pastille Actif, ligne de liste sélectionnée, frise.
- [x] Tant que les seeds required ne sont pas rejoués, l'entrée de menu est absente. Le noter en rendant la main.

## Hors scope

Prochain plan : brancher le chargement déjà écrit dans `_dev/test/absence-rights/[[code]]/+page.server.ts` (`GET /api/absence-rights` et `GET /api/absence-right?code=`). Cette passe ne l'appelle pas.

- [ ] Lire `params.code` et remplacer la fixture par `data` du load. `AdminRightConfigPage` garde les props `absenceRights` et `absenceRight`. Les sections ne sont pas réécrites.
- [ ] Brancher `onSelect(code)` vers `/admin/right/code/{code}`. La liste itère déjà `absenceRights`.
- [ ] Enregistrer, annuler, dupliquer, filtre et `+ Nouveau` — tâche ultérieure. Ne pas recopier le raccourci `arRightsVersions[0]` de `AbsenceRightForm`.
