# GTA-1575 — Valeurs des référentiels ressource (Number) : ajout d'un code unique obligatoire

Ticket parent : [GTA-1575-00-add-unique-value-to-enum-values.md](./GTA-1575-00-add-unique-value-to-enum-values.md)

Référence déjà livrée : [GTA-1575-01-add-unique-value-to-resources-STR-enum-values.md](./GTA-1575-01-add-unique-value-to-resources-STR-enum-values.md).

Cette slice copie ce comportement sur `ResourceEnumNbrVal`. Les enums cycles et horaires restent hors scope. Ne pas modifier le module string.

---

## Décisions

- Nouveau champ `code` **sur la valeur**, pas sur l'enum. `value` reste un `Int`.
- `code` est un `String @db.Citext`, comme sur les valeurs texte. Pas de `@unique` global.
- L'unicité passe de `[resourceEnumId, value]` à `[resourceEnumId, code]`.
- Un même code peut exister dans deux enums différents. `value` n'est plus unique à l'intérieur d'un enum.
- `code` est modifiable tant que la valeur n'est pas référencée, puis verrouillé. Le nombre (`value`) reste toujours modifiable.
- Exécution du plan : lorsqu'une étape est terminée, suffixer avec " / ✅ Terminé".

### Hors scope

L'API client (create/update/correction/swagger) continue de résoudre `EnumNumber` via le nombre (`value`). Les lookups `findFirst({ value })` peuvent devenir ambigus si deux nombres sont identiques — c'est accepté pour l'instant.

### Écarts avec la slice texte

- Pas de relation horaire sur `ResourceEnumNbrVal`. Le verrou compte quatre relations, pas cinq.
- Un seul seed crée des lignes : le seed dev. Pas de seed recommandé, démo, ni démo-arte.
- L'admin (formulaire, tableau, ouverture de l'édition) est déjà en place pour le texte. Ici on étend le même écran au type `Number`, sans second champ Code.
- `CRO_RES_ENUMVAL_000000005` existe déjà. Le réutiliser. Ne pas créer `000000006`.

---

## Étape 0 — Note de suivi / ✅ Terminé

Réécriture de ce fichier pour `ResourceEnumNbrVal`.

---

## Étape 1 — Schéma Prisma / ✅ Terminé

Fichier : `cronexia-gta-back/app/prisma/schema/resource-enum-nbr-val.prisma`

- Ajouter `code String @db.Citext` à côté de `value`. Obligatoire, pas de `@unique` global. `value Int` ne change pas.
- Remplacer la contrainte : `@@unique(name: "compositeId", [resourceEnumId, value])` → `@@unique(name: "compositeId", [resourceEnumId, code])`.
- Laisser `resourceEnumId` optionnel.

Les migrations sont gitignorées et recréées au reset. Pas de backfill. Appliquer via le reset + seed habituel.

---

## Étape 2 — Seed / ✅ Terminé

Un seul fichier. `code` = le nombre écrit en chaîne (`1`, `14`, `41`). Unique par enum parent, donc l'échelon `3` et le bureau `3` ont tous les deux le code `3`.

Fichier : `cronexia-gta-back/app/prisma/seeds-new/50-dev/resource-enums/resource-enum-nbr-val.dev.seed.ts`

- Échelon `1` … `14` → `code` `'1'` … `'14'`.
- Bureau `3`, `41`, `42` → `code` `'3'`, `'41'`, `'42'`.

Les seeds ressource qui rattachent un échelon par id ne créent pas de `ResourceEnumNbrVal`. Ne pas les modifier.

---

## Étape 3 — Contrat Nest / GraphQL

Module `resource-enum-nbr-vals` uniquement. Un fichier par sous-étape. `code` suit `value`, sauf l'input composite qui remplace le `value` entier par `code` (string).

Les inputs imbriqués, le module, les find args et le modèle d'erreur ne listent pas les scalaires. Ne pas les toucher.

| # | Fichier | Action |
|---|---------|--------|
| 3.1 | `dto/create-resource-enum-nbr-val.input.ts` | `code` requis / ✅ Terminé |
| 3.2 | `dto/create-many-resource-enum-nbr-vals.input.ts` | `code` requis / ✅ Terminé |
| 3.3 | `dto/update-resource-enum-nbr-val.input.ts` | `PartialType` hérite de `code` optionnel, aucun second champ / ✅ Terminé |
| 3.4 | `entities/resource-enum-nbr-val.entity.ts` | `code` à côté de `value` / ✅ Terminé |
| 3.5 | `models/resource-enum-nbr-val.model.ts` | `code` à côté de `value` / ✅ Terminé |
| 3.6 | `dto/where-resource-enum-nbr-val.input.ts` | `code` optionnel / ✅ Terminé |
| 3.7 | `dto/order-by-resource-enum-nbr-val.input.ts` | `code` optionnel / ✅ Terminé |
| 3.8 | `enums/resource-enum-nbr-val-distinct.enum.ts` | Ajouter `code`, l'inclure dans `allFields` / ✅ Terminé |
| 3.9 | `dto/composite-id-resource-enum-nbr-vals.input.ts` | Remplacer la partie `value` (Int) par `code` (String) / ✅ Terminé |
| 3.10 | `dto/find-unique-resource-enum-nbr-val.ts` | Description `[resourceEnumId, code]` / ✅ Terminé |
| 3.11 | `resource-enum-nbr-vals.resolver.ts` | Exemple findUnique → `compositeId: { code, resourceEnumId }`. Les deux listes `distinct === 'all'` → `['fieldnameHelper', 'value', 'code']`, branche `code` ajoutée. Le `ResolveField isCodeLocked` est en étape 4.5. / ✅ Terminé |

---

## Étape 4 — Verrouillage du code

Relations présentes sur le modèle (le delete les garde déjà ; ne pas changer le delete) :

- `resourceEnumVals` (dossier)
- `organizationLevelValues`
- `popCritValues`
- `customFieldsConstraints`

Pas de `scheduleOnTimeManagementMethods`.

Comparaison : trim + insensible à la casse. Envoyer le même code, ou omettre `code`, ne verrouille ni le nombre ni `isValid`.

Copier les fonctions texte. Ne pas les fusionner avec le module string.

### 4.1 — Fonction utilitaire / ✅ Terminé

Nouveau fichier sous `src/resource-enum-nbr-vals/functions/`, calqué sur `is-resource-enum-str-val-code-change-locked.ts`.

`findUnique` avec `_count` des quatre relations, plus la comparaison. Exporter `isResourceEnumNbrValCodeLocked` et `isResourceEnumNbrValCodeChangeLocked`.

### 4.2 — Spec / ✅ Terminé

Spec à côté de la fonction, mêmes cas que le texte (ligne absente, aucune relation, même code après trim et casse, code différent, une seule relation suffit). Ne pas la lancer ici. Demander à l'utilisateur de la lancer.

### 4.3 — Dictionnaire d'erreurs / ✅ Terminé

Réutiliser `CRO_RES_ENUMVAL_000000005`. Élargir seulement `messageTech` pour citer aussi `ResourceEnumNbrValsService.update`. Le message humain reste celui déjà en place.

### 4.4 — Service / ✅ Terminé

Fichier : `src/resource-enum-nbr-vals/resource-enum-nbr-vals.service.ts`

`update` appelle la fonction quand `data.code` est présent (string ou `{ set }`). `ConflictException` avec `CRO_RES_ENUMVAL_000000005` si la valeur est utilisée et que le code change réellement.

### 4.5 — ResolveField `isCodeLocked` / ✅ Terminé

Même resolver que 3.11. `@ResolveField('isCodeLocked')` via `isResourceEnumNbrValCodeLocked`. Injecter `PrismaService`. Les requêtes admin de l'étape 5 le demandent sur `resourceEnumNbrVals` seulement.

---

## Étape 5 — Interface admin (valeurs numériques)

Le champ Code, la colonne et le passage au formulaire existent déjà pour le texte. Les étendre au type `Number`. Ne pas ajouter `code` aux requêtes organisation, dossier, population ou `me`.

`ResourceEnumValFormData` a déjà `code` et `isCodeLocked`. Ne pas les rajouter.

| # | Fichier | Action |
|---|---------|--------|
| 5.1 | `lib/graphql/resource-enums/queries/resourceEnums.ts` | `code` et `isCodeLocked` sur `resourceEnumNbrVals` uniquement / ✅ Terminé |
| 5.2 | `lib/graphql/resource-enums/queries/resourceEnum.ts` | Idem / ✅ Terminé |
| 5.3 | `lib/graphql/resource-enums/mutations/create-resource-enum-nbr-val.ts` | La sélection retourne `code` / ✅ Terminé |
| 5.4 | `lib/graphql/resource-enums/mutations/update-resource-enum-nbr-val.ts` | La sélection retourne `code` / ✅ Terminé |
| 5.5 | `routes/api/resource-enum-nbr-val/create/+server.ts` | `code` requis, trimé ; conflit → "Ce code existe déjà pour ce référentiel" / ✅ Terminé |
| 5.6 | `routes/api/resource-enum-nbr-val/update/+server.ts` | `code` transmis s'il est non vide ; même message de conflit / ✅ Terminé |
| 5.7 | `components/cronexia/resource-enum/ResourceEnumValForm.svelte` | Afficher le champ Code aussi quand `enumType === 'Number'`. Mêmes règles que le texte : requis, lecture seule si `isCodeLocked`, le nombre reste éditable. L'envoi create/update vers les routes nbr inclut `code`. / ✅ Terminé |
| 5.8 | `components/cronexia/resource-enum/ResourceEnumDetails.svelte` | Colonne Code sur le tableau des valeurs numériques, comme pour le texte / ✅ Terminé |
| 5.9 | `components/cronexia/resource-enum/ManageResourceEnum.svelte` | Passer `code` et `isCodeLocked` dans la branche numérique de `openEditVal` / ✅ Terminé |
| 5.10 | Vérification manuelle | Après redémarrage de l'API, régénérer les types GraphQL front (`bun run codegen---generate-graphql-types-from-back`). Retirer alors les casts `code` / `isCodeLocked` devenus inutiles sur le texte et le nombre. Vérifier dans le navigateur un référentiel numérique : création sans code bloquée, création avec code, modification du nombre, modification du code tant qu'inutilisé, code en lecture seule dès que la valeur est référencée. |
