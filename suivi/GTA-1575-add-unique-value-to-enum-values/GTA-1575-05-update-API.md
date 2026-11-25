# GTA-1575 — API client : résolution des référentiels par code

Ticket parent : [GTA-1575-00-add-unique-value-to-enum-values.md](./GTA-1575-00-add-unique-value-to-enum-values.md)

Références déjà livrées : [GTA-1575-01](./GTA-1575-01-add-unique-value-to-resources-STR-enum-values.md), [GTA-1575-02](./GTA-1575-02-add-unique-value-to-resources-INT-enum-values.md), [GTA-1575-03](./GTA-1575-03-add-unique-value-to-cycle-enum-values.md), [GTA-1575-04](./GTA-1575-04-add-unique-value-to-schedule-enum-values.md).

Les slices 01 et 02 ont laissé l'API client résoudre `EnumString` et `EnumNumber` par le libellé (`value`). Cette slice fait passer create, update, correction, import CSV et les exemples Swagger sur le `code` de la valeur.

---

## Décisions

- Périmètre : l'API client `api/resource` uniquement.
- La clé JSON `value` de l'enveloppe historisée (`{ value, effectDate }`) ne change pas de nom. Pour une liste, son contenu est le `code` de la valeur.
- Organisation : l'objet préféré est `{ code, referentiel }`. La clé `value` à la place de `code` reste acceptée. Si les deux sont envoyées, `code` est utilisé. Le contenu est le `code` de la valeur, pas le libellé.
- `referentiel` reste le code du référentiel (`ResourceEnum.code`).
- Pas de repli sur le libellé. Exemples de seeds : `CDI` reste `CDI`, `Île-de-France` devient `ILE_DE_FRANCE`, l'échelon `14` a le code `"14"`, `Service 1` devient `SERVICE_01`.
- Lookup : `findFirst` sur `code`, borné au référentiel du champ. `code` est en citext, la casse est déjà ignorée. Trim de la chaîne reçue avant la requête.
- Un nombre JSON est converti avec `String(...)` : `14` et `"14"` tombent sur le code `"14"`. Ne plus passer par `Number()`, pour qu'un code non numérique reste acceptable.
- Organisation : chercher ce code string à la fois sur `resourceEnumStrVal` et sur `resourceEnumNbrVal`, filtré par `resourceEnum.code`. Le branchement « seulement si la valeur est un nombre » disparaît.
- Upsert réutilise la création et la modification. Aucun lookup à part.
- Exécution du plan : lorsqu'une étape est terminée, suffixer avec " / ✅ Terminé".
- Les tests se lancent à la main, à l'étape 9. Ne pas les lancer depuis l'agent.

### Hors scope

- GraphQL admin, front, seeds, verrouillage du code : déjà livrés dans les slices 01 à 04.
- Cycles et horaires : pas de contrôleur REST. Leur GraphQL expose déjà `code`.
- Populations, compteurs, et tout lookup qui n'est pas `api/resource`.
- Renommer la clé `value` de l'enveloppe historisée (`{ value, effectDate }`).

---

## Étape 0 — Note de suivi / ✅ Terminé

Écriture de ce fichier.

---

## Étape 1 — Message « code introuvable » / ✅ Terminé

Fichiers :

- `cronexia-gta-back/app/src/resources/client-api/functions/missing-reference-message.ts`
- `cronexia-gta-back/app/src/resources/client-api/functions/missing-reference-message.spec.ts`

« la valeur « X » est introuvable » devient « le code « X » est introuvable ».

Le motif lu par le rapport de lot est dans le même fichier. L'écriture du message et sa relecture bougent ensemble. Aligner les attentes de la spec.

Ne pas toucher aux services dans cette étape.

---

## Étape 2 — Création / ✅ Terminé

Fichiers :

- `cronexia-gta-back/app/src/resources/client-api/resources-client.service.ts`
- `cronexia-gta-back/app/src/resources/client-api/resources-client-referentiel.spec.ts`

`EnumString` (vers la ligne 967) et `EnumNumber` (vers 1009) : `where.code` à la place de `where.value`, après trim et `String(...)`.

Organisation (vers 1148) : les deux branches cherchent `code`. Retirer le test « valeur numérique ».

Le mock de la spec lit `where.value`. Le faire lire `where.code`, et aligner le message sur l'étape 1.

Ne pas ouvrir le service de modification.

---

## Étape 3 — Modification, résolution / ✅ Terminé

Fichier : `cronexia-gta-back/app/src/resources/client-api/update-resource.service.ts`

Seulement les lookups d'écriture.

- Validation `EnumString` (vers 1143) et `EnumNumber` (vers 1164) : même résolution que l'étape 2.
- Organisation (vers 1253) : même recherche par `code` que la création.

La relecture et la comparaison restent pour l'étape 4, dans le même fichier. La modification n'est pas terminée tant que l'étape 4 n'est pas faite.

---

## Étape 4 — Modification, valeur détenue / ✅ Terminé

Même fichier que l'étape 3 : `cronexia-gta-back/app/src/resources/client-api/update-resource.service.ts`

Sans cette étape, une clôture `{ value, effectDateEnd }` compare un code envoyé à un libellé relu.

- `getHeldValue` : sélectionner `code` pour `EnumString`, `EnumNumber` (vers 635) et l'organisation (vers 661). L'organisation relue est `{ code, referentiel }`.
- `sameHeldValue` : retirer `EnumNumber` du cas `Number(sent) === Number(held)`. Comparer les deux codes en chaînes trimées, insensible à la casse, comme le verrou du code.

---

## Étape 5 — Correction / ✅ Terminé

Fichier : `cronexia-gta-back/app/src/resources/client-api/resource-correction.service.ts`

- Unicité (vers 375) : résoudre `newValue` par `code`, comme en création.
- Écriture : le service pose aujourd'hui `data.value` sur `ResourceEnumVal`, qui n'a pas cette colonne. Pour un `EnumString` ou un `EnumNumber`, reconnecter `resourceEnumStrVal` ou `resourceEnumNbrVal` depuis l'id résolu, et détacher l'autre relation. `newValue: null` reste une désaffectation.
- Date, suppression et autres types : les laisser tels quels.
- Pas de nouvelle spec : ce service n'en a pas.

---

## Étape 6 — Import CSV / ✅ Terminé

- `cronexia-gta-back/app/src/resources/client-api/csv-import/resource-csv-import.constant.ts` : retirer `EnumNumber` de `CSV_IMPORT_NUMERIC_TYPES`. La cellule `14` reste la chaîne `"14"`.
- Le parseur met la cellule dans la clé `code` de l'objet organisation (`{ code, referentiel }`). Les services acceptent encore `value`.
- `cronexia-gta-back/app/src/resources/client-api/csv-import/resource-csv-import.controller.ts` : dans `CSV_FORMAT_DOC`, indiquer que la cellule d'un champ liste ou d'organisation est le code de la valeur.
- `cronexia-gta-back/app/src/resources/client-api/csv-import/functions/resource-csv-import.spec.ts` : ajouter un cas `EnumNumber` dont la cellule reste une chaîne. Les cas `CDD` / `CDI` et `{ value: 'Service 1', referentiel }` ne résolvent rien en base : les laisser.

---

## Étape 7 — Exemples Swagger dynamiques / ✅ Terminé

Fichier : `cronexia-gta-back/app/src/resources/client-api/swagger-dynamic.setup.ts`

- Charger `code` et `value`. L'exemple copiable est le code. Chaque puce de description est `` `CODE` — libellé ``.
- `EnumNumber` : l'exemple est le code string, plus un nombre.
- Organisation : `sampleValue` et `sampleValueAlt` sont des codes. L'exemple copiable est `{ code, referentiel }`. `referentiel` ne change pas.

---

## Étape 8 — Textes statiques des contrôleurs / ✅ Terminé

Ces descriptions ne sont pas écrasées par le Swagger dynamique.

- `cronexia-gta-back/app/src/resources/client-api/resources-client.controller.ts` : les listes n'acceptent que les codes référencés.
- `cronexia-gta-back/app/src/resources/client-api/update-resource.controller.ts` : l'exemple organisation `Secteur A` / `Secteur B` devient un code (`SECTEUR_A` / `SECTEUR_B`). `CDI` et `CDD` sont déjà des codes : les laisser.

---

## Étape 9 — Vérification

Demander à l'utilisateur de lancer les specs touchées :

- `missing-reference-message.spec.ts`
- `resources-client-referentiel.spec.ts`
- `resource-csv-import.spec.ts`
- `read-organization-value-code.spec.ts`

Ne pas les lancer depuis l'agent.

---

## Étape 10 — Enveloppe organisation `{ code, referentiel }` / ✅ Terminé

La clé `value` imbriquée dans l'objet organisation prêtait à confusion : elle portait un code. Le contrat préféré devient `{ "code": "SECTEUR_A", "referentiel": "Secteur" }`, à l'intérieur de l'enveloppe historisée qui, elle, garde sa clé `value`.

`value` dans l'objet organisation reste acceptée. Une chaîne vide ou absente retombe sur `value`. Si les deux sont renseignées, `code` gagne.

Fichiers :

- `functions/read-organization-value-code.ts` : lecture partagée (création, modification, clôture).
- `resources-client.service.ts`, `update-resource.service.ts` : résolution et comparaison.
- `swagger-dynamic.setup.ts`, `update-resource.controller.ts`, `resources-client.controller.ts` : exemples et textes sur `code`, avec la mention que `value` reste acceptée.
- Import CSV : la cellule est posée dans `code`. Le fichier CSV, lui, ne change pas de colonnes.
