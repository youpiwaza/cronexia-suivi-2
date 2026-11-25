# GTA-1575 — Valeurs des référentiels ressource (String) : ajout d'un code unique obligatoire

Ticket parent : [GTA-1575-00-add-unique-value-to-enum-values.md](./GTA-1575-00-add-unique-value-to-enum-values.md)

Première implémentation de référence. Les valeurs Number des ressources, les enums cycles et les enums horaires sont hors scope ici.

---

## Décisions

- Nouveau champ `code` **sur la valeur**, pas sur l'enum.
- L'unicité passe de `[resourceEnumId, value]` à `[resourceEnumId, code]`.
- Un même code peut exister dans deux enums différents. `value` n'est plus unique à l'intérieur d'un enum.
- `code` est modifiable tant que la valeur n'est pas référencée, puis verrouillé. Le libellé (`value`) reste toujours modifiable.
- Exécution du plan : lorsqu'une étape est terminée, suffixer avec " / ✅ Terminé".

### Hors scope

L'API client (create/update/correction/swagger) continue de résoudre `EnumString` via le libellé (`value`). Ce comportement ne change pas dans cette slice. Les lookups `findFirst({ value })` peuvent devenir ambigus si deux libellés sont identiques — c'est accepté pour l'instant.

---

## Étape 0 — Note de suivi / ✅ Terminé

Écriture de ce fichier.

---

## Étape 1 — Schéma Prisma / ✅ Terminé

Fichier : `cronexia-gta-back/app/prisma/schema/resource-enum-str-val.prisma`

- Ajouter `code String @db.Citext` à côté de `value` (même type insensible à la casse). Obligatoire, pas de `@unique` global.
- Remplacer la contrainte d'unicité nommée : `@@unique(name: "compositeId", [resourceEnumId, value])` → `@@unique(name: "compositeId", [resourceEnumId, code])`.
- Laisser `resourceEnumId` optionnel comme aujourd'hui.

Les migrations sont gitignorées et recréées au reset de la BDD. Pas de script de backfill : les lignes existantes ne peuvent pas satisfaire un `code` obligatoire. Appliquer via le reset + seed habituel.

---

## Étape 2 — Seeds

Convention (à écrire une fois en commentaire dans le seed recommandé) : ASCII majuscules, accents supprimés, espaces et tirets remplacés par `_`.

Exemples : `CDI` → `CDI`, `Île-de-France` → `ILE_DE_FRANCE`, `En heures avec pointages réels` → `EN_HEURES_AVEC_POINTAGES_REELS`. Les codes sont uniques par enum parent, donc `Cadre` dans status et `Cadre` dans category donnent tous les deux `CADRE`.

### 2.1 — Seed recommandé, partie 1 / ✅ Terminé

Fichier : `cronexia-gta-back/app/prisma/seeds-new/02-recommended/resource-enums/resource-enum-str-val.seed.ts`

Sections Contract, Quality, Region, OutReason, Job, Status. `code` littéral sur chaque ligne, plus le commentaire de convention.

### 2.2 — Seed recommandé, partie 2 / ✅ Terminé

Même fichier. Sections Cycle, Calendar, Country, City, ResourceTimeManagementMethod, Category.

### 2.3 — Seed dev / ✅ Terminé

Fichier : `cronexia-gta-back/app/prisma/seeds-new/50-dev/resource-enums/resource-enum-str-val.dev.seed.ts`

Même convention, `code` littéral sur chaque ligne.

### 2.4 — Seed demo / ✅ Terminé

Fichier : `cronexia-gta-back/app/prisma/seeds-new/25-demo/resource-enums/resource-enum-str-val.demo.seed.ts`

Codes générés dans les boucles : `POLE_01`, `DIRECTION_01`, `SERVICE_01`, `SECTEUR_01`, `SOCIETE_01`, `ETABLISSEMENT_01` (avec padding 2 chiffres).
Ajouter aussi `code: string` dans l'annotation de type inline du tableau `data`.

### 2.5 — Seed demo-arte / ✅ Terminé

Fichier : `cronexia-gta-back/app/prisma/seeds-new/26-demo-arte/resource-enums/resource-enum-str-val.demo.seed.ts`

Mêmes codes de boucle que 2.4. Même correction de l'annotation de type.

---

## Étape 3 — Contrat Nest / GraphQL

Module string values uniquement. Un fichier par sous-étape. `code` suit `value`, sauf pour l'input composite qui remplace `value` par `code`.

Les fichiers non concernés (inputs imbriqués, module, find args, modèle d'erreur) ne listent pas les scalaires → à ne pas toucher.

| # | Fichier | Action |
|---|---------|--------|
| 3.1 | `dto/create-resource-enum-str-val.input.ts` | `code` requis / ✅ Terminé |
| 3.2 | `dto/create-many-resource-enum-str-vals.input.ts` | `code` requis / ✅ Terminé |
| 3.3 | `dto/update-resource-enum-str-val.input.ts` | `PartialType` hérite de `code` optionnel, aucun second champ / ✅ Terminé |
| 3.4 | `entities/resource-enum-str-val.entity.ts` | `code` à côté de `value` / ✅ Terminé |
| 3.5 | `models/resource-enum-str-val.model.ts` | `code` à côté de `value` / ✅ Terminé |
| 3.6 | `dto/where-resource-enum-str-val.input.ts` | `code` optionnel / ✅ Terminé |
| 3.7 | `dto/order-by-resource-enum-str-val.input.ts` | `code` optionnel / ✅ Terminé |
| 3.8 | `enums/resource-enum-str-val-distinct.enum.ts` | Ajouter `code`, l'inclure dans `allFields` / ✅ Terminé |
| 3.9 | `dto/composite-id-resource-enum-str-vals.input.ts` | Remplacer la partie `value` par `code` / ✅ Terminé |
| 3.10 | `dto/find-unique-resource-enum-str-val.ts` | Description mise à jour `[resourceEnumId, code]` / ✅ Terminé |
| 3.11 | `resource-enum-str-vals.resolver.ts` | Exemple findUnique → `compositeId: { code, resourceEnumId }`. Les deux listes `distinct === 'all'` → `['fieldnameHelper', 'value', 'code']`, branche `code` ajoutée. Le `ResolveField isCodeLocked` est en étape 4.5. / ✅ Terminé |

---

## Étape 4 — Verrouillage du code

Relations gardées (identiques au chemin de suppression, plus les horaires) :

- `resourceEnumVals` (dossier)
- `organizationLevelValues`
- `popCritValues`
- `customFieldsConstraints`
- `scheduleOnTimeManagementMethods`

Comparaison : trim + insensible à la casse. Envoyer le même code, ou omettre `code`, ne verrouille ni le libellé ni `isValid`.

### 4.1 — Fonction utilitaire / ✅ Terminé

Nouveau fichier sous `src/resource-enum-str-vals/functions/` : un `findUnique` avec `_count` sur les cinq relations + la comparaison. Les trois autres enums copieront cette fonction.

### 4.2 — Spec / ✅ Terminé

Fichier spec à côté de la fonction, couvrant la décision compare-et-verrouille. Ne pas la lancer ici — demander à l'utilisateur de la lancer.

### 4.3 — Dictionnaire d'erreurs / ✅ Terminé

Fichier : `src/_utility/error/cronexia-error-dictionnary.ts`

Ajouter `CRO_RES_ENUMVAL_000000005` (message fr + en : impossible de modifier le code, valeur déjà utilisée).

### 4.4 — Service / ✅ Terminé

Fichier : `src/resource-enum-str-vals/resource-enum-str-vals.service.ts`

La méthode `update` appelle la fonction quand `data.code` est présent. Lance `ConflictException` avec le code d'erreur si la valeur est utilisée et que le code change réellement.

### 4.5 — ResolveField `isCodeLocked` / ✅ Terminé

Même resolver que 3.11. `@ResolveField('isCodeLocked')` utilisant la fonction. Les requêtes admin (étape 5) le demandent. Les autres requêtes ne le demandent pas.

---

## Étape 5 — Interface admin (valeurs texte uniquement)

Les valeurs numériques dans les mêmes écrans restent inchangées. Ne pas ajouter `code` aux requêtes organisation, dossier, population ou `me`. Ces écrans continuent d'afficher `value` et de connecter par id.

| # | Fichier | Action |
|---|---------|--------|
| 5.1 | `lib/graphql/resource-enums/queries/resourceEnums.ts` | `code` et `isCodeLocked` sur `resourceEnumStrVals` uniquement / ✅ Terminé |
| 5.2 | `lib/graphql/resource-enums/queries/resourceEnum.ts` | Idem / ✅ Terminé |
| 5.3 | `lib/graphql/resource-enums/mutations/create-resource-enum-str-val.ts` | La sélection retourne `code` / ✅ Terminé |
| 5.4 | `lib/graphql/resource-enums/mutations/update-resource-enum-str-val.ts` | La sélection retourne `code` / ✅ Terminé |
| 5.5 | `routes/api/resource-enum-str-val/create/+server.ts` | `code` requis ; message de conflit → "Ce code existe déjà pour ce référentiel" / ✅ Terminé |
| 5.6 | `routes/api/resource-enum-str-val/update/+server.ts` | `code` transmis ; même message de conflit / ✅ Terminé |
| 5.7 | `components/cronexia/resource-enum/ResourceEnumValForm.svelte` | Champ Code requis si `enumType === 'String'`. En édition, `isReadOnly` si `isCodeLocked` avec un court message. Libellé toujours éditable. Ajouter `code?: string` et `isCodeLocked?: boolean` au type `ResourceEnumValFormData`. Lancer l'autofixer Svelte. / ✅ Terminé |
| 5.8 | `components/cronexia/resource-enum/ResourceEnumDetails.svelte` | Colonne Code sur le tableau des valeurs texte uniquement. Lancer l'autofixer Svelte. / ✅ Terminé |
| 5.9 | `components/cronexia/resource-enum/ManageResourceEnum.svelte` | Passer `code` et `isCodeLocked` dans le formulaire d'édition. Lancer l'autofixer Svelte. / ✅ Terminé |
| 5.10 | Vérification manuelle | Après redémarrage de l'API, régénérer les types GraphQL front (`bun run codegen---generate-graphql-types-from-back`). Vérifier dans le navigateur : créer une valeur texte sans code (bloqué), créer avec code, modifier le libellé, modifier le code tant qu'inutilisé, confirmer que le champ code est en lecture seule dès que la valeur est référencée. |
