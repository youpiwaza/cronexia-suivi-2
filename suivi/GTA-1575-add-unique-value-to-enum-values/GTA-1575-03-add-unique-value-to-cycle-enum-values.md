# GTA-1575 — Valeurs des référentiels cycle (String) : ajout d'un code unique obligatoire

Ticket parent : [GTA-1575-00-add-unique-value-to-enum-values.md](./GTA-1575-00-add-unique-value-to-enum-values.md)

Référence déjà livrée : [GTA-1575-01-add-unique-value-to-resources-STR-enum-values.md](./GTA-1575-01-add-unique-value-to-resources-STR-enum-values.md).

Cette slice copie ce comportement sur `CycleEnumStrVal`. Les enums horaires et les référentiels ressource restent hors scope. Ne pas modifier ces modules.

---

## Décisions

- Nouveau champ `code` **sur la valeur**, pas sur l'enum. `value` reste un `String` (pas de `@db.Citext` sur `value`).
- `code` est un `String @db.Citext`. Pas de `@unique` global.
- Il n'y a pas de contrainte d'unicité aujourd'hui. Ajouter `@@unique(name: "compositeId", [cycleEnumId, code])`.
- Un même code peut exister dans deux enums différents. `value` n'est pas unique à l'intérieur d'un enum.
- `code` est modifiable tant que la valeur n'est pas référencée, puis verrouillé. Le libellé (`value`) reste toujours modifiable.
- Exécution du plan : lorsqu'une étape est terminée, suffixer avec " / ✅ Terminé".

### Hors scope

Pas de valeurs numériques : `CycleEnum` n'a que le type `String`. Pas d'écran admin cycle. Ne pas ajouter `code` au front.

Les lookups `findFirst({ value })` peuvent devenir ambigus si deux libellés sont identiques — c'est accepté pour l'instant.

### Écarts avec la slice texte ressource

- Une seule relation : `cycleEnumVals`. Le verrou ne compte que celle-là.
- Aucun seed ne crée de `CycleEnumStrVal`. Ne pas en ajouter.
- Pas d'input composite aujourd'hui, et find-unique ne prend que l'id. Les créer, ne pas remplacer un `value` existant.
- Pas d'étape 5. `CRO_RES_ENUMVAL_000000005` existe déjà. Le réutiliser. Ne pas créer de nouveau code.

---

## Étape 0 — Note de suivi / ✅ Terminé

Écriture de ce fichier pour `CycleEnumStrVal`.

---

## Étape 1 — Schéma Prisma / ✅ Terminé

Fichier : `cronexia-gta-back/app/prisma/schema/cycle-enum-str-val.prisma`

- Ajouter `code String @db.Citext` à côté de `value`. Obligatoire, pas de `@unique` global. `value String` ne change pas.
- Ajouter `@@unique(name: "compositeId", [cycleEnumId, code])`. Il n'y a rien à remplacer.
- Laisser `cycleEnumId` optionnel.

Les migrations sont gitignorées et recréées au reset. Pas de backfill. Appliquer via le reset habituel.

---

## Étape 2 — Seed / ✅ Terminé

Aucun fichier. Aucun seed n'insère de `CycleEnumStrVal`. Ne pas en créer.

---

## Étape 3 — Contrat Nest / GraphQL / ✅ Terminé

Module `cycle-enum-str-vals` uniquement. Un fichier par sous-étape. `code` suit `value`. L'input composite est nouveau : `code` (string) et `cycleEnumId`.

Les inputs imbriqués, le module, les find args ne listent pas les scalaires. Ne pas les toucher.

| # | Fichier | Action |
|---|---------|--------|
| 3.1 | `dto/create-cycle-enum-str-val.input.ts` | `code` requis / ✅ Terminé |
| 3.2 | `dto/create-many-cycle-enum-str-vals.input.ts` | `code` requis / ✅ Terminé |
| 3.3 | `dto/update-cycle-enum-str-val.input.ts` | Vérifier que `PartialType` hérite de `code` optionnel, ne pas ajouter de second champ / ✅ Terminé |
| 3.4 | `entities/cycle-enum-str-val.entity.ts` | `code` à côté de `value` / ✅ Terminé |
| 3.5 | `models/cycle-enum-str-val.model.ts` | `code` à côté de `value` / ✅ Terminé |
| 3.6 | `dto/where-cycle-enum-str-val.input.ts` | `code` optionnel / ✅ Terminé |
| 3.7 | `dto/order-by-cycle-enum-str-val.input.ts` | `code` optionnel / ✅ Terminé |
| 3.8 | `enums/cycle-enum-str-val-distinct.enum.ts` | Ajouter `code`, l'inclure dans `allFields` / ✅ Terminé |
| 3.9 | `dto/composite-id-cycle-enum-str-vals.input.ts` | Créer le fichier. Parties `code` (String) et `cycleEnumId`. Pas de partie `value` / ✅ Terminé |
| 3.10 | `dto/find-unique-cycle-enum-str-val.ts` | Ajouter `compositeId`. Description `[cycleEnumId, code]`. L'argument `id` reste / ✅ Terminé |
| 3.11 | `cycle-enum-str-vals.resolver.ts` | Exemple findUnique → `compositeId: { code, cycleEnumId }`. Les deux listes `distinct === 'all'` → `['fieldnameHelper', 'value', 'code']`, branche `code` ajoutée. Le `ResolveField isCodeLocked` est en étape 4.5. / ✅ Terminé |

---

## Étape 4 — Verrouillage du code / ✅ Terminé

Relation présente sur le modèle (le delete ne la contrôle pas ; ne pas changer le delete) :

- `cycleEnumVals`

Comparaison : trim + insensible à la casse. Envoyer le même code, ou omettre `code`, ne verrouille pas le libellé.

Copier les fonctions texte. Ne pas les fusionner avec le module ressource.

### 4.1 — Fonction utilitaire / ✅ Terminé

Nouveau fichier sous `src/cycle-enum-str-vals/functions/`, calqué sur `is-resource-enum-str-val-code-change-locked.ts`.

`findUnique` avec `_count` de `cycleEnumVals`, plus la comparaison. Exporter `isCycleEnumStrValCodeLocked` et `isCycleEnumStrValCodeChangeLocked`.

### 4.2 — Spec / ✅ Terminé

Spec à côté de la fonction, mêmes cas que le texte (ligne absente, aucune relation, même code après trim et casse, code différent, une seule relation suffit). Ici la seule relation est `cycleEnumVals`. Ne pas la lancer ici. Demander à l'utilisateur de la lancer.

### 4.3 — Dictionnaire d'erreurs / ✅ Terminé

Fichier : `src/_utility/error/cronexia-error-dictionnary.ts`

Réutiliser `CRO_RES_ENUMVAL_000000005`. Élargir seulement `messageTech` pour citer aussi `CycleEnumStrValsService.update`. Le message humain reste celui déjà en place.

### 4.4 — Service / ✅ Terminé

Fichier : `src/cycle-enum-str-vals/cycle-enum-str-vals.service.ts`

`update` appelle la fonction quand `data.code` est présent (string ou `{ set }`). `ConflictException` avec `CRO_RES_ENUMVAL_000000005` si la valeur est utilisée et que le code change réellement. Copier le helper `nextCode` dans ce fichier. Ne pas importer celui du module ressource.

### 4.5 — ResolveField `isCodeLocked` / ✅ Terminé

Même resolver que 3.11. `@ResolveField('isCodeLocked')` via `isCycleEnumStrValCodeLocked`. Injecter `PrismaService`. Ne pas stocker le champ. Aucune requête front ne le demande.

---

## Étape 5 — Interface admin

Pas d'écran admin pour les enums cycle. Aucun fichier front à modifier.
