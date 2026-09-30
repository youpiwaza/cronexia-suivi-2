# GTA-1757 / 🐛 Dossier resource > Erreur GraphQL sur champ historisé `city`

Le 400 GraphQL est construit par le formulaire. Ce n'est pas une ligne seed, et ce n'est pas la ligne Swagger renvoyée telle quelle.

`city` n'est pas requis : une désaffectation par `null` est valide. Le payload refusé n'est pas ce `null`. C'est un `undefined` JavaScript, traité comme si un id de ville avait été choisi.

## Constat

Log : `MER_ERR_GQL_VALIDATION`, 400, Mercurius. Coupé avant tout resolver, donc avant les contraintes et Prisma.

Variable `$data` invalide sur `data.resourceEnumVals.create[0]` :

- matricule `300009F` (Inès Morel)
- champ `city`
- `effectDate` `2026-01-01`
- `description` : `city "undefined" le 2026-01-01`
- `resourceEnumStrVal` : `{ connect: {} }`
- `historisedEnumValueId` **absent**

`CreateResourceEnumValInput.historisedEnumValueId` est `String!` (`cronexia-gta-back/app/src/schema.gql`). En Prisma la colonne est `String?`.

La description `city "undefined" le …` n'existe que dans les actions Svelte (`resource-create-histo.ts`, même gabarit dans `resource-edit-histo.ts` et `resource-update.ts`). Le clear REST, lui, écrit `city (vidé)`, et seulement s'il y a déjà une ligne ce jour-là. Le mot `undefined` est l'interpolation JS, puis `JSON.stringify` retire la clé.

## `null` et `undefined` ne sont pas la même chose

`null` = désaffecter. La clé est présente.

- Envoi attendu : `resourceEnumStrVal: null`, et `historisedEnumValueId` = l'id de la ville qu'on retire.
- `process-resource-enum-val.ts` exige cet id. Un clear dont l'id est `null` est refusé là, plus tard, par une autre erreur.
- Le lint du formulaire transforme la string `"null"` en `null`.
- Une ligne en base sans valeur d'enum revient au formulaire en `value: null` (`transform-resource-enum-vals.ts`). Rien sur ce chemin ne change `null` en `undefined`.
- Réenregistrer ce `null` donne `resourceEnumStrVal: null` et l'id précédent. Ce n'est pas `{ connect: {} }`.

`undefined` = la propriété n'a jamais été posée. Ni une ville, ni une désaffectation.

- FormData ne contient pas `undefined`. Si Svelecte ne poste pas `city`, le hidden `isHistorised_city` crée quand même `{}`, donc `.value` reste `undefined`.
- JSON retire les clés `undefined`. GraphQL dit que `historisedEnumValueId` n'a pas été fourni.
- Un vrai `null` envoyé sur ce champ donnerait une autre erreur (`String!` ne peut pas être null) et `resourceEnumStrVal: null`, pas `{ connect: {} }`.

Le mélange est ce test :

```ts
historisedEnumValueId: value !== null ? value : precedentValue,
if (value !== null) {
  resourceEnumStrVal = { connect: { id: value } };
}
```

`undefined !== null` est vrai. Une sélection absente est traitée comme « on a un id ». Les deux clés deviennent `undefined` et disparaissent. Un vrai `null` prend l'autre branche. Le log est la première.

## D'où vient le `undefined`

Action `?/createHisto`, ligne **Ajouter** de la popup.

- `cronexia-gta-front-v2/app/src/routes/components/cronexia/resource/modals/ModalHisto/Add.svelte`
- `cronexia-gta-front-v2/app/src/routes/functions/cronexia/resource/file/form/action/resource-create-histo.ts`

- `form-extract-from-hidden-fields.ts` crée l'objet via `isHistorised_city`, sans `value`.
- Svelecte n'émet le contrôle nommé que si une valeur est choisie.
- `Add.svelte` force `customFieldsConstraint.isRequired = true`, mais `AllFieldsLoop.svelte` lit `resourceField.isRequired`. Le select reste optionnel et `clearable` (`InputEnum`, défaut).

`resource-edit-histo.ts` et `resource-update.ts` ont le même trou `!== null`, mais ils ignorent la ligne si `value === undefined`. Ils ne produisent pas ce payload tant que ce garde tient.

## Test Swagger (autre personne)

Exemple exécuté : « Vider une valeur à une date donnée », corps :

```json
{ "city": { "value": null, "effectDate": "2026-01-01" } }
```

`buildClearAtDateUpdateExample` dans `swagger-dynamic.setup.ts` prend le premier champ historisé non requis (`orderBy: name asc`) et fige la date `2026-01-01`. Sur cette base, ce champ est `city`. `isRequired: false` explique que le `null` est accepté. `isUnique` / `isUniqueInHistory` restent à false et ne sont pas la cause du 400.

`setFieldToNull` dans `update-resource.service.ts`, pour `EnumString` / `EnumNumber` :

- Pas de `ResourceEnumVal` ce jour-là → retourne false, **n'insère rien**. Inès a Reims au **2022-07-11**, donc un clear au **2026-01-01** ne crée pas de ligne. L'appel peut réussir sans résultat `cleared`.
- Une ligne existe ce jour-là → disconnect de `resourceEnumStrVal` / `resourceEnumNbrVal`, sans toucher `historisedEnumValueId`. String, nombre et date, eux, créent un vrai marqueur null. Les enums non.

Les create/update enum non-null du même service n'écrivent pas non plus `historisedEnumValueId`. REST passe par Prisma, donc il contourne la règle GraphQL (`String!` + refus de désaffectation sans id). Il ne contourne pas `isRequired` : un `null` sur un champ requis est rejeté avant l'écriture.

Cet appel n'a pas fabriqué le body refusé. Il laisse un trou à part : un enum optionnel ne se désaffecte pas comme les autres types, et un succès silencieux est possible.

## Seeds démo

- `city` : `EnumString`, historisé, enum `resourceEnumCity`.
  - `cronexia-gta-back/app/prisma/seeds-new/25-demo/resource-fields/resource-fields.demo.seed.ts`
- Contrainte (`custom-field-constraints.demo.seed.ts`) : `fieldType: enum`, `isRequired: false`, `isUnique: false`, `isUniqueInHistory` omis → défaut `false`. Le schéma dit que `isUnique` ne s'applique pas aux enums.
- Options : Paris, Reims, Lyon, … avec uuid. Pas d'option vide.
- Ligne seed de `300009F` : Reims, avec `historisedEnumValueId`, au **2022-07-11**.

## Pistes écartées pour ce 400

- Contraintes requis / unique / unique dans l'historique : pas atteintes, et pas ce qui retire la clé.
- Conversion d'un `null` stocké en `undefined` : non. Le log est la branche « on a un id ».
- Option vide dans la liste : non.
- Ligne seed Reims rejouée : la date ne correspond pas, et la description n'est pas celle de la base.
- L'exemple Swagger a bien visé `city` au `2026-01-01`, mais pour un enum il n'insère pas la ligne qui produirait `{ connect: {} }`.

## Correctifs possibles

Garder `null` comme désaffectation (relation null, `historisedEnumValueId` = id précédent). Ne pas le traiter comme une erreur.

1. Front, le 400 réel — `resource-create-histo.ts` : ne pas construire de `connect` si la valeur est `undefined` ou `''` (`EnumStringInput` et `EnumNumberInput`). Erreur de formulaire. Même garde sur les branches `connect` de `resource-edit-histo.ts` et `resource-update.ts`.
2. `Add.svelte` — `isRequired` sur le champ lui-même (prop lue par `AllFieldsLoop`), uniquement sur la ligne Ajouter. La contrainte démo reste `isRequired: false` sur le dossier.
3. REST — pour `value: null` sur un enum : soit refuser tant qu'il n'y a pas de vraie désaffectation, soit créer le marqueur attendu par GraphQL (`historisedEnumValueId` copié de la valeur précédente, relation null). Ne pas répondre succès quand rien n'a été écrit.
4. REST — sur create/update enum non-null, poser `historisedEnumValueId` sur l'id connecté, pour qu'une désaffectation UI ultérieure soit valide.
5. Exemple Swagger — ne garder `2026-01-01` + `value: null` que sur un type que l'API sait vraiment vider (string, nombre, date), ou sur un enum seulement une fois le marqueur en place.
