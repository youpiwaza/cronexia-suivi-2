# Audit — criticité des anomalies, frontend (`criticalityLevel`)

Périmètre : `cronexia-gta-front-v2/app/src`, hors `lib/generated/types/graphql/graphql.ts` (miroir généré du schéma).

Pas de changement de code. L’audit backend reste dans `anomaly-criticty-audit.md`.

## Réponse courte

Oui, le front utilise `criticalityLevel` (`error`, `warning`, `info`), toujours en lecture. Aucune mutation ne le pose.

Il sert au libellé français (Erreur / Alerte / Info), à la couleur de ligne et de badge, au tri, au filtre, aux compteurs du widget d’accueil, et au chargement « erreurs hors période ».

Il ne change pas le message. Le texte affiché reste `anomaly.label`, plus la valeur de compteur quand il y en a une.

Les trois niveaux sont affichés s’ils arrivent de l’API. Le planning collectif stocke le niveau puis ne s’en sert pas : une seule pastille `⚠`, tooltip = liste des libellés.

## 1. Traduction

Fichiers :

- `routes/components/cronexia/anomaly/enums/criticite-map.ts`
- `routes/components/cronexia/anomaly/enums/badge-map.ts`
- `routes/components/cronexia/anomaly/enums/class-map.ts`
- `routes/components/cronexia/anomaly/enums/status-label-map.ts`

| API | Libellé | Badge | Classe de ligne |
| --- | --- | --- | --- |
| `error` | Erreur | `danger` | `table-danger` |
| `warning` | Alerte | `warning` | `table-warning` |
| `info` | Info | `info` | `table-info` |

Le statut affiché ne vient pas de la criticité. `status-label-map.ts` traduit le statut d’instance :

- `toBeTreated` → À traiter
- `toWatch` → À surveiller
- `treated` → Traité
- `acquitted` → Acquitté
- `info` → Information

La correspondance statut / criticité est celle du back (une alerte est en général « À surveiller », une erreur « À traiter »). Le front ne la recalcule pas.

Une ligne « Traité » prend la classe `table-success`, quelle que soit la criticité (`transform-anomalies.ts`).

## 2. Page anomalies

`transform-anomalies.ts` lit `anomaly.criticalityLevel` et :

- met le libellé français dans `criticity` ;
- l’inclut dans `uniqueId` (matricule + date + statut + criticité + code) ;
- choisit `badge` et la classe CSS ;
- recopie `label` et `description` tels quels.

`aggregate-anomalies.ts` regroupe par cette clé, fusionne libellés et descriptions, puis trie : erreur, puis alerte, puis info, puis date décroissante, puis matricule. Si un « À traiter » existe le même jour pour le même matricule, les « Traité » de ce jour sont masqués. Ce masque porte sur le statut, pas sur la criticité.

`AnomaliesArray.svelte` :

- colonne et recherche « Criticité » ;
- pastilles Erreurs / Alertes / Info (`AnomalyCriticityFiltersBar.svelte`), choix mémorisé en cookie ;
- filtre local : une ligne passe si aucune pastille n’est cochée, ou si sa criticité française est cochée.

`AnomaliesArrayTr.svelte` affiche le badge (`Erreur`, `Alerte`, `Info`) et les pastilles de `label`. La description agrégée n’est pas rendue dans la ligne. L’accordéon compteur montre le code du compteur, son libellé, `anomaly.label`, et la valeur.

Suppression refusée si le statut est « À traiter », ou si la criticité affichée est « Alerte » (`canDelete`).

La modale du planning (`PlanningAnomaliesModal.svelte`) réutilise le même pipeline (`transform` + `aggregate` + `AnomaliesArray`).

## 3. Chargement

`load-anomalies-page.server.ts` et `fetch-anomalies.ts`.

- Période normale : matricule ou population + `dateStart` / `dateEnd`. Pas de `criticalityLevel`. Les trois niveaux reviennent, le filtre est local.
- « Inclure les erreurs hors période » : `criticalityLevel=error`, et les dates sont retirées. Seules les erreurs sont chargées, sans borne de période.

Relais HTTP → GraphQL :

- `routes/api/anomalies/instances/+server.ts`
- `lib/graphql/anomalies/queries/getAnomalyInstances.ts` (ajoute `criticalityLevel` à la requête seulement s’il est fourni)

`routes/api/reports/anomalies/instances/+server.ts` fait le même relais pour le rapport d’instances.

## 4. Autres écrans

### Widget d’accueil

`routes/components/common/widgets/WidgetAnomalies.svelte`.

Compte les lignes non traitées par libellé français (erreur / alerte / info). Icône et pastille selon ce libellé. Le texte de la ligne est `label`, plus nom et date. En cas d’égalité de code et de date, la ligne gardée est la plus grave.

### Synthèse

`SummaryArrayTr.svelte`, tri préalable dans la page synthèse (`error` = 0, `warning` = 1, `info` = 2).

`getCriticiteColor` :

- `error` → `--cronexia-danger`
- `warning` → `--cronexia-warning`
- `'Info'` (I majuscule) → `--cronexia-info`
- sinon → couleur de surface

L’API envoie `info` en minuscules. Le cas `'Info'` ne matche pas : une info prend la couleur par défaut, pas le bleu info.

Les icônes d’anomalie de la ligne utilisent toutes `anomalies[0].criticalityLevel`, donc la plus grave après le tri, pas la criticité de chaque libellé. Le tooltip compteur de la synthèse ajoute `(label)` à la valeur, sans couleur de criticité dédiée par compteur ; la couleur du texte de valeur passe par `getCriticiteColor` sur l’anomalie de ce compteur (même trou sur `info`).

### Compteurs

`CounterAnomalyValue.svelte`, utilisé par le tableau et le pivot.

Si un libellé d’anomalie est présent : badge toujours rouge (`--md-sys-color-error`), tooltip = ce libellé. `criticalityLevel` n’est pas lu. Une alerte ou une info de compteur a le même rendu qu’une erreur.

### Planning collectif

`planning-data.mapper.ts` copie `criticalityLevel` dans `DayAnomaly.level`. Le type déclare `number | null` ; l’API envoie la string `error` | `warning` | `info`. Les instances `treated` sont écartées. Dédoublonnage par code.

`CollectiveScheduleGrid.svelte` n’utilise pas `level`. Une pastille `⚠` par jour, tooltip = libellés joints par une virgule.

### Calendrier annuel

`createAnomaliesMap` dans `planning-data-to-events.ts` copie `criticalityLevel` sur chaque segment et ignore le statut `'Traité'`. Aucun autre fichier n’appelle cette fonction : la copie n’alimente pas d’écran.

## 5. Messages : peut-on les ajuster selon la criticité ?

Non, pas côté front. Il n’y a pas de template de phrase par niveau.

Textes dérivés de la criticité, et rien d’autre :

- Erreur, Alerte, Info (badge, filtre, colonne)
- suffixes du widget : « erreur(s) », « alerte(s) » ; le compteur info n’a pas de suffixe

Le libellé métier vient du back (`anomaly.label`). `description` est agrégée dans le modèle de ligne et sert au code neutre des conflits (`CONFLIMLTPNEUTRE`), elle n’est pas affichée comme message. La valeur de compteur est un nombre formaté, pas une phrase choisie selon la criticité.

Pour changer une phrase, il faut changer le catalogue ou la génération backend. Le front se contentera d’afficher le nouveau `label`, avec la couleur et le badge du niveau reçu.
