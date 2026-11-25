# Ajout d'un code obligatoire et unique aux valeurs des enums

## Métier

Actuellement je peux ajouter une valeur à un enum donné sans avoir à renseigner un code.

Le problème: les valeurs des enums peuvent être “volatiles” ce qui va poser des problèmes lors d’interfaçage avec des outils tiers. Les codes sont par nature plus stables et on peut empêcher de les modifier dès lors qu’ils sont utilisés sans que cela pose de problème majeur au niveau des informations visualisées dans le front contrairement à si on empêche une modification de la valeur.

Exemple: je me base actuellement sur les valeurs donc par exemple: “Midi-Pyrenees” pour une région. J’interface cette valeur depuis un outil tiers qui est mis à jour dans un 2eme temps pour corriger l’absence d’accent “Midi-Pyrénées” ce qui va créer une 2eme valeur dans l’enum Cronexia. Pour prévenir ce genre de problème, il faut ajouter la possibilité de passer un code “PYR” associée à la valeur. La mise à jour des données se fera en fonction du code et non de la valeur

## Dev

❌🔭 Out of scope: Mise à jour de l'API (comportement & valeurs).

Permettre l’unicité de chaque valeur, & lever l’ambiguïté des couples ENUM/Valeurs qui auraient des valeurs identiques dans des couples différents.

cf. discussion https://cronexia.atlassian.net/browse/GTA-1382?focusedCommentId=27990  > solution 2 choisie

### 🎯 Objectifs pour chaque

💥 Attention, on parle bien d'un code unique pour la valeur, et non l'enum !!

- 💾 Base de données
  - Rajouter le champ, unique
  - Changer la clé d'unicité composite dans les relations, de l'id vers le code
    - `@@unique(name: "compositeId", [resourceEnumId, value])` >> @@unique(name: "compositeId", [resourceEnumId, code])
- 🌱 Maj des seeds
- 🐯🌐 Maj nest & GQL
- 🎨🌐 Maj queries & implications front ~admin/enum, orgas, admin/orgas, dossier resource, etc.
- //
-

### Resources enum values

Locations:

- cronexia-gta-back\app\prisma\schema\resource-enum.prisma
- String values : cronexia-gta-back\app\prisma\schema\resource-enum-str-val.prisma
- Int values : cronexia-gta-back\app\prisma\schema\resource-enum-nbr-val.prisma

### Cycles enum values

Locations:

- cronexia-gta-back\app\prisma\schema\cycle-enum.prisma
- String values : cronexia-gta-back\app\prisma\schema\cycle-enum-str-val.prisma

### Schedules enum values

Locations:

- cronexia-gta-back\app\prisma\schema\schedule-enum.prisma
- String values : cronexia-gta-back\app\prisma\schema\schedule-enum-str-val.prisma
