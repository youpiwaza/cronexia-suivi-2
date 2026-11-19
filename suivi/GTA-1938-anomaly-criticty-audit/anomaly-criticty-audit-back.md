# Audit — criticité des anomalies, backend (`criticalityLevel`)

Périmètre : backend uniquement.

- Schéma : `cronexia-gta-back/app/prisma/schema/anomaly.prisma`, `cronexia-gta-back/app/prisma/schema/anomaly-instance.prisma`
- Seed : `cronexia-gta-back/app/prisma/seeds/anomalies/anomalies.seed.ts`
- Code : `cronexia-gta-back/app/src` (CRUD anomalies / instances, génération d’événements, compteurs, planning, reporting)

Pas de changement de code. Le client Prisma généré et `schema.gql` ne font que refléter le modèle.

## Réponse courte

Oui, `criticalityLevel` est utilisé. Valeurs : `info`, `warning`, `error`.

Il est porté par le catalogue `Anomaly`, pas par `AnomalyInstance`. Il sert à choisir et à valider le **statut** de l’instance, à filtrer les requêtes, et à renvoyer la valeur au planning et au reporting.

Il ne choisit pas le texte. Les messages viennent du `label` du catalogue, ou d’une `description` d’instance construite selon le type d’anomalie (souvent en dur, par UUID).

Le seed mélange les trois niveaux. La génération automatique des événements, des conflits et des pointages impairs ne produit que des anomalies seedées en `error`. Les niveaux `info` et `warning` passent par la fonction compteur `ANOMALY()`, ou par une création manuelle (GraphQL, fixture de test).

## 1. Modèle

`Anomaly.criticalityLevel` est obligatoire. Enum `AnomalyCriticalityLevelEnum` : `info`, `warning`, `error`.

`AnomalyInstance` n’a pas de criticité. Le reflet côté instance est `status` (`acquitted`, `info`, `toBeTreated`, `toWatch`, `treated`). Le texte libre est `description` (optionnel). Une valeur de compteur peut être stockée dans `counterResultValue`.

Une anomalie a donc une seule criticité, pour toutes ses instances.

## 2. Correspondance statut

Fichier : `cronexia-gta-back/app/src/anomaly-instances/functions/service/validate-or-set-anomaly-instance-status.ts`.

Appelé à la création unitaire, à la création en lot, et à la mise à jour du statut (`anomaly-instances.service.ts`).

Si aucun statut n’est fourni, un défaut est posé. S’il est fourni, il est contrôlé. Un statut incompatible lève une erreur.

| Criticité | Statut par défaut | Statuts autorisés |
| --- | --- | --- |
| `info` | `info` | `info`, `acquitted` |
| `warning` | `toWatch` | `toWatch` |
| `error` | `toBeTreated` | `toBeTreated`, `treated` |

Une instance déjà `treated` ne peut plus être mise à jour.

## 3. Résolution horaire

Fichier : `cronexia-gta-back/app/src/resources/functions/events/generate/functions/resolved-status-for-criticality.ts`.

Quand une plage d’anomalie horaire est couverte par une saisie, le statut « résolu » dépend de la criticité :

| Criticité | Statut résolu | Ligne écrite |
| --- | --- | --- |
| `error` | `treated` | oui |
| `info` | `acquitted` | oui |
| `warning` | aucun | non |

`warning` ne produit pas de ligne résolue. Le préfixe `RESOLUE` / `RESOLUE PARTIELLEMENT` n’est donc jamais appliqué à un `warning`.

La description résolue est le texte d’origine, préfixé. Exemples dans `mark-anomaly-instance-resolved.ts` et dans `resources-generate-events-by-period.ts` : `RESOLUE {description}` ou `RESOLUE PARTIELLEMENT {description} … résolue via {événements}`.

Même règle au moment de réinjecter en base les instances déjà couvertes : `warning` est ignoré, `error` et `info` sont recréés avec le statut résolu.

## 4. Où la criticité est lue

Création et mise à jour d’instance : le service charge l’anomalie liée et passe `criticalityLevel` au validateur de statut.

Génération d’événements (`resources-generate-events-query-by-period.ts`) : toutes les anomalies sont chargées dans une map `idAnomaly → criticalityLevel`. Cette map est lue pour les événements générés marqués anomalie (`ABSINJ`, `PNA`, repli `INCONNU`) et pour les lignes résolues. Elle n’est pas lue pour les pointages impairs ni pour les conflits (voir section 6). Le `createMany` final repasse quand même par le validateur : un statut forcé en dur doit rester compatible avec la criticité en base, sinon l’insertion échoue.

Requête dédiée : `getAnomalyInstances(..., criticalityLevel)` filtre `anomaly.criticalityLevel`. Fichiers : `anomaly-instances.resolver.ts`, `get-anomaly-instances.ts`.

Planning : `merge-anomaly-instances.ts` recopie `anomaly.criticalityLevel` sur le modèle aplati. Si la relation manque, la valeur retombe sur `info`.

Reporting compteurs : `resolve-counter-report-rows.ts` expose `anomaly.label` et `anomaly.criticalityLevel` (colonne `anomalyCriticality`), tels quels. Pas de libellé dérivé de la criticité.

Verrou à la mise à jour du catalogue (`anomalies.service.ts`) :

- `isCustom = false` : seul `label` peut être modifié.
- `isCustom = true` et au moins une instance liée : `criticalityLevel` ne peut plus changer.
- `isCustom = false` : suppression interdite. `isCustom = true` : suppression refusée si d’autres enregistrements référencent l’anomalie.

## 5. Catalogue seed

Fichier : `cronexia-gta-back/app/prisma/seeds/anomalies/anomalies.seed.ts`.

`info`

- `DEMCONGAV` — Demande de congé à valider — `workflow`
- `TESTCPT` — Une anomalie de test déclenchée par un compteur — `counter`, custom

`warning`

- `TEMPJMAX` — Temps journalier maximum dépassé — `counter`, custom
- `CPT_VAL_SUP` — Valeur du compteur supérieure à 10h — `counter`, custom

`error` (le reste)

- Pointages : `POINTIMP`, `CLKMAXVAL`, `POINTABS`
- Événements : `ABSINJ`, `PNA`
- Champs ressource : `REQFIELD`, `UNIQUEVAL`, `UNIQUEHIST`, `CONDREQ`, `NUMMINVAL`, `NUMMAXVAL`, `STRMINLEN`, `STRMAXLEN`, `EMAILINVAL`, `PHONEINVAL`, `DATEMINVAL`, `DATEMAXVAL`, `TIMEMINVAL`, `TIMEMAXVAL`
- Conflits : `CONFLIEXCL`, `CONFLIOVRL`, `CONFLIMLTP`, `CONFLIMLTPNEUTRE`
- Autres : `INCONNU`, `DRTINSUF`

Les trois niveaux existent donc dans le référentiel. Ils ne sont pas tous produits par un générateur.

## 6. Ce qui est vraiment généré dans `app/src`

### Pointages impairs — `POINTIMP` (`error`)

`resources-generate-events-query-by-period.ts`, jour avec `date.isAnomaly`.

- `anomalyId` en dur.
- Statut forcé à `toBeTreated`.
- Description fixe : `Pointages impairs pour cette journée : {nombre}`.
- La map de criticité n’est pas consultée. Le validateur du `createMany` accepte ce statut tant que `POINTIMP` reste `error`.

### Événements générés — `ABSINJ`, `PNA`, repli `INCONNU` (tous `error` au seed)

`event-id-to-anomaly-id.ts` ne mappe que `AINJ → ABSINJ` et `PNA → PNA`. Tout autre `eventId` tombe sur `INCONNU`.

`create-anomaly-instance-to-generate.ts` lit la criticité dans la map, puis :

- description : `{libellé} pour {resourceId}`
- statut : défaut du validateur (`toBeTreated` pour ces trois codes)

Le libellé ne vient pas de la base. Il vient du switch `anomaly-id-to-label.ts`.

### Conflits — tous `error` au seed

`create-partial-anomaly-instance-to-generate.ts` force `status = toBeTreated` sans lire la criticité. Le texte dépend de l’UUID, pas du niveau :

- `CONFLIMLTP` (`…0027`) : préfixe et liste des codes d’événements manuels
- `CONFLIEXCL` (`…0020`) : chevauchement exclusif, horaires et libellé de l’événement manuel
- `CONFLIOVRL` (`…0021`) : overlap, même forme
- `CONFLIMLTPNEUTRE` (`…0028`) : ouvert par `reconcile-neutral-conflicts.ts`, même constructeur, donc le même statut forcé ; pas de branche de description dédiée (libellé du switch seulement)

Appels dans `resources-generate-events-query-by-period.ts` pour `0027`, `0020`, `0021`.

### Compteurs — `ANOMALY(code, valeur?)`

Définition : `cronexia-gta-back/app/src/_utility/functions/function-definition.ts`.

La fonction ne lit pas la criticité et ne remplit pas `description`. Elle connecte l’anomalie par **code** et, si le second paramètre est fourni, met cette valeur dans `counterResultValue` (string). Le statut est déduit plus tard par le validateur, selon la criticité du code en base.

Conséquence : un compteur peut produire `info`, `warning` ou `error`, selon le code passé à `ANOMALY()`.

- `CPT_VAL_SUP` est `warning` : une instance générée par ce code reçoit `toWatch` si aucun statut n’est passé.
- `TESTCPT` est l’exemple documenté de `ANOMALY('TESTCPT', …)` et il est `info` : statut par défaut `info`.
- `TEMPJMAX` est `warning` au seed, sans appel trouvé dans `app/src`.

### Présents au seed, sans générateur trouvé dans `app/src`

`CLKMAXVAL`, `POINTABS`, les anomalies de champ ressource (`REQFIELD` et suivantes), `DEMCONGAV`, `DRTINSUF`, `TEMPJMAX`.

Leur criticité ne sert alors qu’au catalogue, au filtre, et à une création manuelle.

Fixture de test, hors génération métier : `resources/functions/tests/add-anos-info-and-warning.ts` crée `TEST_INFO` / `TEST_WARN` et des instances déjà statutées. Ce n’est pas le pipeline de production. Le fichier insère aussi des instances `toBeTreated` / `treated` sur l’id de `CLKMAXVAL`, en contournant le validateur (Prisma direct).

## 7. Peut-on ajuster les messages selon la criticité ?

Non. Il n’existe pas de template de message par niveau. La criticité ne change pas la phrase. Elle change le statut, et le fait qu’une ligne résolue soit écrite ou non.

Deux textes distincts sont exposés :

- `Anomaly.label` : libellé catalogue, lu en direct (planning `labelShort`, reporting `anomaly`). Modifiable en base, y compris pour une anomalie non custom (`isCustom = false` : seul ce champ passe).
- `AnomalyInstance.description` : snapshot écrit à la génération. Pour les événements, il est fabriqué depuis `anomaly-id-to-label.ts`, pas depuis la colonne `label`. Changer le label en base ne réécrit ni ce switch, ni les descriptions déjà stockées.

Ajustements possibles aujourd’hui, sans lier le texte à la criticité :

- Changer `Anomaly.label` : visible là où l’UI affiche le catalogue. Les descriptions d’instances déjà générées restent anciennes.
- Changer le switch `anomaly-id-to-label.ts` et les branches par UUID de `create-partial-anomaly-instance-to-generate.ts` : c’est le texte des prochaines générations d’événements et de conflits. C’est du code, pas un paramètre.
- Second paramètre de `ANOMALY(code, valeur)` : stocké dans `counterResultValue`, pas dans `description`. Utile pour une valeur, pas pour une phrase par criticité.
- Pour avoir des phrases différentes, il faut des **codes d’anomalie distincts** (chacun avec son label et sa criticité). Une même anomalie ne peut pas avoir deux criticités.

Les statuts forcés (`POINTIMP`, conflits) supposent une criticité `error`. Passer ces codes en `info` ou `warning` ferait échouer le `createMany`, parce que `toBeTreated` ne serait plus autorisé. Les événements `ABSINJ` / `PNA` / `INCONNU`, eux, prendraient le statut par défaut de la nouvelle criticité, et un `warning` ne produirait plus de ligne résolue.
