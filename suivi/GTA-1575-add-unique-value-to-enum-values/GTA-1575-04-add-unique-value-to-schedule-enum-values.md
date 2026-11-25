# GTA-1575 — Valeurs des référentiels horaire (String) : ajout d'un code unique obligatoire

Ticket parent : [GTA-1575-00-add-unique-value-to-enum-values.md](./GTA-1575-00-add-unique-value-to-enum-values.md)

Référence déjà livrée : [GTA-1575-01-add-unique-value-to-resources-STR-enum-values.md](./GTA-1575-01-add-unique-value-to-resources-STR-enum-values.md).

Cette slice copie ce comportement sur `ScheduleEnumStrVal`. Les enums cycles et les référentiels ressource restent hors scope. Ne pas modifier ces modules.

---

## Décisions

- Nouveau champ `code` **sur la valeur**, pas sur l'enum. `value` reste un `String` (pas de `@db.Citext` sur `value`).
- `code` est un `String @db.Citext`. Pas de `@unique` global.
- L'unicité globale de `value` (`String @unique`) disparaît. Elle est remplacée par `@@unique(name: "compositeId", [scheduleEnumId, code])`.
- Un même code peut exister dans deux enums différents. `value` n'est plus unique, ni globalement ni dans un enum.
- `code` est modifiable tant que la valeur n'est pas référencée, puis verrouillé. Le libellé (`value`) reste toujours modifiable.
- Exécution du plan : lorsqu'une étape est terminée, suffixer avec " / ✅ Terminé".

### Hors scope

Pas de valeurs numériques : `ScheduleEnum` n'a que le type `String`. Pas d'écran admin horaire. Ne pas ajouter `code` au front.

Les lookups `findFirst({ value })` peuvent devenir ambigus si deux libellés sont identiques — c'est accepté pour l'instant.

### Écarts avec la slice texte ressource

- Une seule relation : `scheduleEnumVals`. Le verrou ne compte que celle-là.
- Un seul seed crée des lignes, encore appelé depuis `seeds-new`. Pas d'autre seed.
- `value` est aujourd'hui une clé unique globale, y compris dans find-unique, update et delete. Retirer cet argument. Ne pas changer le corps du delete.
- Pas d'input composite aujourd'hui. Le créer.
- Pas d'étape 5. `CRO_RES_ENUMVAL_000000005` existe déjà. Le réutiliser. Ne pas créer de nouveau code.

---

## Étape 0 — Note de suivi / ✅ Terminé

Écriture de ce fichier pour `ScheduleEnumStrVal`.

---

## Étape 1 — Schéma Prisma / ✅ Terminé

Fichier : `cronexia-gta-back/app/prisma/schema/schedule-enum-str-val.prisma`

- Ajouter `code String @db.Citext` à côté de `value`. Obligatoire, pas de `@unique` global. Le type de `value` ne change pas.
- Retirer `@unique` sur `value`.
- Ajouter `@@unique(name: "compositeId", [scheduleEnumId, code])`.
- Laisser `scheduleEnumId` optionnel.

Les migrations sont gitignorées et recréées au reset. Pas de backfill. Appliquer via le reset + seed habituel.

---

## Étape 2 — Seed / ✅ Terminé

Un seul fichier, appelé par `seeds-new/100-post-comon/post-common.orchestrator.ts`. Les cinq lignes appartiennent à `scheduleType`. Convention des codes : ASCII majuscules, comme le seed texte ressource.

Fichier : `cronexia-gta-back/app/prisma/seeds/schedules/schedule-enum-str-val.seeds.ts`

- `Day` → `DAY`
- `AM` → `AM`
- `PM` → `PM`
- `Night` → `NIGHT`
- `Rest` → `REST`

Ne pas modifier l'orchestrateur.

---

## Étape 3 — Contrat Nest / GraphQL / ✅ Terminé

Module `schedule-enum-str-vals` uniquement. Un fichier par sous-étape. `code` suit `value`. L'input composite est nouveau : `code` (string) et `scheduleEnumId`.

Les inputs imbriqués, le module, les find args ne listent pas les scalaires. Ne pas les toucher.

| # | Fichier | Action |
|---|---------|--------|
| 3.1 | `dto/create-schedule-enum-str-val.input.ts` | `code` requis / ✅ Terminé |
| 3.2 | `dto/create-many-schedule-enum-str-vals.input.ts` | `code` requis / ✅ Terminé |
| 3.3 | `dto/update-schedule-enum-str-val.input.ts` | Vérifier que `PartialType` hérite de `code` optionnel, ne pas ajouter de second champ / ✅ Terminé |
| 3.4 | `entities/schedule-enum-str-val.entity.ts` | `code` à côté de `value` / ✅ Terminé |
| 3.5 | `models/schedule-enum-str-val.model.ts` | `code` à côté de `value` / ✅ Terminé |
| 3.6 | `dto/where-schedule-enum-str-val.input.ts` | `code` optionnel / ✅ Terminé |
| 3.7 | `dto/order-by-schedule-enum-str-val.input.ts` | `code` optionnel / ✅ Terminé |
| 3.8 | `enums/schedule-enum-str-val-distinct.enum.ts` | Ajouter `code`, l'inclure dans `allFields` / ✅ Terminé |
| 3.9 | `dto/composite-id-schedule-enum-str-vals.input.ts` | Créer le fichier. Parties `code` (String) et `scheduleEnumId`. Pas de partie `value` / ✅ Terminé |
| 3.10 | `dto/find-unique-schedule-enum-str-val.ts` | Retirer l'argument unique `value`. Ajouter `compositeId`. Description `[scheduleEnumId, code]`. L'argument `id` reste / ✅ Terminé |
| 3.11 | `schedule-enum-str-vals.resolver.ts` | Exemple findUnique : remplacer `value: "Jour"` par `compositeId: { code, scheduleEnumId }`. findUnique, update et delete cessent de copier `value` dans le where Prisma et transmettent `compositeId`. Les deux listes `distinct === 'all'` → `['fieldnameHelper', 'value', 'code']`, branche `code` ajoutée. Le corps du delete ne change pas. Le `ResolveField isCodeLocked` est en étape 4.5. / ✅ Terminé |

---

## Étape 4 — Verrouillage du code / ✅ Terminé

Relation présente sur le modèle (le delete ne la contrôle pas ; ne pas changer le delete) :

- `scheduleEnumVals`

Comparaison : trim + insensible à la casse. Envoyer le même code, ou omettre `code`, ne verrouille pas le libellé.

Copier les fonctions texte. Ne pas les fusionner avec le module ressource.

### 4.1 — Fonction utilitaire / ✅ Terminé

Nouveau fichier sous `src/schedule-enum-str-vals/functions/`, calqué sur `is-resource-enum-str-val-code-change-locked.ts`.

`findUnique` avec `_count` de `scheduleEnumVals`, plus la comparaison. Exporter `isScheduleEnumStrValCodeLocked` et `isScheduleEnumStrValCodeChangeLocked`.

### 4.2 — Spec / ✅ Terminé

Spec à côté de la fonction, mêmes cas que le texte (ligne absente, aucune relation, même code après trim et casse, code différent, une seule relation suffit). Ici la seule relation est `scheduleEnumVals`. Ne pas la lancer ici. Demander à l'utilisateur de la lancer.

### 4.3 — Dictionnaire d'erreurs / ✅ Terminé

Fichier : `src/_utility/error/cronexia-error-dictionnary.ts`

Réutiliser `CRO_RES_ENUMVAL_000000005`. Élargir seulement `messageTech` pour citer aussi `ScheduleEnumStrValsService.update`. Le message humain reste celui déjà en place.

### 4.4 — Service / ✅ Terminé

Fichier : `src/schedule-enum-str-vals/schedule-enum-str-vals.service.ts`

`update` appelle la fonction quand `data.code` est présent (string ou `{ set }`). `ConflictException` avec `CRO_RES_ENUMVAL_000000005` si la valeur est utilisée et que le code change réellement. Copier le helper `nextCode` dans ce fichier. Ne pas importer celui du module ressource.

### 4.5 — ResolveField `isCodeLocked` / ✅ Terminé

Même resolver que 3.11. `@ResolveField('isCodeLocked')` via `isScheduleEnumStrValCodeLocked`. Injecter `PrismaService`. Ne pas stocker le champ. Aucune requête front ne le demande.

---

## Étape 5 — Interface admin

Pas d'écran admin pour les enums horaires. Aucun fichier front à modifier.
