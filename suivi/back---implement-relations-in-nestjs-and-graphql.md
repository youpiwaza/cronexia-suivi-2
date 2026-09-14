# Implement relations in NestJs and Graphql

From the PRISMA_SCHEMA_FILE > Implement CLASSNAME in NestJs & graphql :

There is a specific list of files to update, depending on the type of relation to implement, there are some boilerplates and references to help implementing properly.

Do not skip any file

---

## Boilerplates indications

- Relationsship are commented by default, but need to be un-commented
- Boilerplates terms to replace
  - CLASSNAME_MAJ_FIRST REMOVE > Current class name, with first letter capitaliazed (PascalCase)
  - CLASSNAME_LOWC_FIRST REMOVE > Current class name, converted to lowercase and words separated by "-" (kebab-case)
  - CLASSNAME_FILE_KEBAB_CASE REMOVE > Current class name
  - RELATION_MAJ_FIRST REMOVE > Relationship class name, with first letter capitaliazed (PascalCase)
  - RELATION_LOWC_FIRST REMOVE > Relationship class name, with first letter lowercased (camelCase)
  - RELATION_FILE_KEBAB_CASE REMOVE > Relationship class name, converted to lowercase and words separated by "-" (kebab-case)

---

Great already implemented reference : cronexia-gta-back\app\src\ar-resource-balances

---

## Note about Circular dependency, for Models implementation

- GraphQL `@ObjectType` model files often reference other models for `@Field(() => OtherModel)`. Top-level `import { OtherModel } from '…'` can create circular dependency cycles (A imports B, B imports A).
- **Prefer lazy loading** for related models in `@Field` decorators:
  - `() => require('../../other-path/models/other.model').OtherModel`
  - Optionally use `import type { OtherModel } from '…'` only for TypeScript property types if needed, without pulling the decorator target from a static import of the same module’s runtime export.
- Boilerplate illustration: cronexia-gta-back\__boilerplates\classname-kebab\models\classname-kebab.model.ts (commented examples around lines 52–85).
- Also compare: cronexia-gta-back\app\src\ar-exercises\models\ar-exercise.model.ts

---

## One to many relationship

- Entity file : boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\entities\classname-kebab.entity.ts
  - line 102 to 118
  - Copy lines 102 to 104 and replace commented relationship (same 2 lines from schema)
  - lines 106 to 118 re-use, using only optionnal or required depending of the relation in the schema

- Model file : boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\models\classname-kebab.model.ts
  - Import relationship Model
  - Lines 53 to 66

- DTO/create : boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\dto\create-classname-kebab.input.ts
  - Import relationship NestedRELATION_MAJ_FIRSTOneToManyInput
  - Line 47 to 58

- DTO/create-many : boilerplate file :
  - Line 45 to 57

- resolver : boilerplate file :
  - cronexia-gta-back\__boilerplates\classname-kebab\classname-kebabs.resolver.ts
  - line 14 & 15 : must be uncommented
  - line 21 : Class must be imported from PrismaClient
  - Line 44 & 45 : Model Model & Service must be imported
    - let a blank line between each different relationship group
  - line 52 : add relationship service to constructor
  - lines 96 to 117 : reuse strictly the boilerplate to implement the relationship

- module : boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\classname-kebabs.module.ts
  - line 12 : import relationship module
  - line 19 : add import through forwardRef()

---

## Many to one relationship

- Entity file : boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\entities\classname-kebab.entity.ts
  - Copy lines 96 to 98 and replace commented relationship (same 2 lines from schema), stays commented (virtual relationship)

- Model file : boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\models\classname-kebab.model.ts
  - Import relationship Model
  - Lines 70 to 85

- DTO/create : boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\dto\create-classname-kebab.input.ts
  - Import relationship NestedRELATION_MAJ_FIRSTOneToManyInput
  - Line 62 to 69

- DTO/create-many : Nothing to add

- resolver : boilerplate file :
  - cronexia-gta-back\__boilerplates\classname-kebab\classname-kebabs.resolver.ts
  - line 14 & 15 : must be uncommented
  - line 21 : Class must be imported from PrismaClient
  - Line 44 & 45 : Model Model & Service must be imported
    - let a blank line between each different relationship group
  - line 52 : add relationship service to constructor
  - lines 76 to 92 : reuse strictly the boilerplate to implement the relationship

- module : boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\classname-kebabs.module.ts
  - line 12 : import relationship module
  - line 19 : add import through forwardRef()

---

## Many to many relationship

- Mostly same things as Many to one relation ship
- Exception for the resolver > resolvefield :
  - boilerplate file : cronexia-gta-back\__boilerplates\classname-kebab\classname-kebabs.resolver.ts
  - Use lines 121 to 152

---

## Graphql documentation update

Should be in a dedicated /docs folder, boilerplate ref : cronexia-gta-back\__boilerplates\classname-kebab\docs

Do not that not all old classes have this folder implemented and that documentation can be inline in resolver.

- For the current class, use all non dev fields
  - all fields except
    - createdAt
    - updatedAt
    - createdBy
    - updatedBy
- For relationship fields, use all related non dev fields
  - if the relation is one to many : use singular
  - if the relation is many to one or many to many : use plural

---

## Technical notes

- Preserve spacing and spacing comments
  - "// ---"
  - "// * 🔗 Relations" once per relation group
- Respect project conventions
- do NOT use JSDoc comments, use project comments
- Do not update GraphQL generated files/types, they'll be reset automatically

Don't hesitate to ask questions if needed
