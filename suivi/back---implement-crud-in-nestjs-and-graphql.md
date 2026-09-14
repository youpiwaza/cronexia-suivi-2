# Implement in NestJs and Graphql

PRISMA_SCHEMA_FILE > Implement CLASSNAME in NestJs & graphql :

- Create example seeds IF NEEDED, references :
  - cronexia-gta-back\app\prisma\seeds\absence-right\absence-right.seed.ts
  - cronexia-gta-back\app\prisma\seeds\absence-right\ar-version.seed.ts
  - dont forget to load them in orchestrator IF NEEDED
- create the whole nestjs structure:
  - Class enum
    - each enum MUST have its own file
  - distinct enum
    - do NOT implement tech fields createdAt, updatedAt, createdBy, updatedBy, nor relationships XXXId fields
  - entity
  - model
    - if a relationship is one-to-many, pay attention to other model import tweak to prevent circular dependencies issues, cf. cronexia-gta-back\app\src\ar-exercises\models\ar-exercise.model.ts
    - see also **Circular dependency (models)** below (`require()` lazy imports)
  - dtos
    - create DTO : PAY ATTENTION to relations to implement at the end of the file !
    - order by DTO : no relations to implement, nor relationships XXXId fields
    - where DTO : no relations to implement, nor relationships XXXId fields
    - DO NOT forget nested DTOs in the nested folder, reference : cronexia-gta-back\__boilerplates\classname-kebab\dto\nested
      - DO implement all 3 files !
  - module
    - do NOT forget to include all other relationships
    - if some other relationships aren't implemented yet, add them but commented (with forwardRef)
  - service
  - resolver
    - unbloat : do not keep huge inline strings or repeated id-remap blocks in the resolver body
    - **GraphQL descriptions** : move `@Query` / `@Mutation` `description` template literals into a `docs/` folder (see **docs/ folder** below)
    - **findFirst / findMany / similar** : move merged args and GraphQL `id` → Prisma primary-key remapping into `functions/` (see **functions/ folder** below); older reference modules still inline some of this—prefer extracting for new code
  - don't forget to load the new module in cronexia-gta-back\app\src\app.module.ts
- All relations MUST be treated as either one-to-many/many-to-one/many-to-many (cf. boilerplates)
  - be RIGOUROUS with relationships implementations, pay attention to the kind of relation to implement for each relation
- Test all queries file : `_tests_all_queries`
  - include runnable query and mutation examples inside the descriptions in `docs/*.doc.ts` when applicable (same strings the resolver uses), so GraphQL Playground / schema docs stay self-contained

You can use as references:

- cronexia-gta-back\app\src\ar-exercises
- cronexia-gta-back\app\src\ar-versions
- cronexia-gta-back\app\src\ar-resource-balances
- cronexia-gta-back\app\src\resource-user-profile-instance-vals (combines `docs/`, `functions/`, and lazy `require()` model imports end-to-end)

Documentations:

- cronexia-gta-back\_docs\04.2-graphql-crud.md for fields
- cronexia-gta-back\_docs\04.3-graphql-relations.md for relations

Boilerplate folder:

- cronexia-gta-back\__boilerplates\classname-kebab
  - IGNORE cronexia-gta-back\__boilerplates\classname-kebab\queues
  - models\classname-kebab.model.ts (commented block ~lines 52–85) shows the **`require('…/other.model').OtherModel`** pattern for `@Field` types to avoid circular imports between GraphQL model classes

---

## docs/ folder (GraphQL descriptions and examples)

- For each feature module, add a `docs/` directory next to the resolver, with one file per operation shape when useful, for example:
  - `find-unique.doc.ts`, `find-first.doc.ts`, `find-many.doc.ts`, `create.doc.ts`, `create-many.doc.ts`, `update.doc.ts`, `delete.doc.ts`
- Each file exports a string constant (e.g. `export const FIND_UNIQUE_DOC = \`…\`;`).
- The resolver imports these constants and passes them to `description:` on `@Query` / `@Mutation` decorators.
- Put full **example GraphQL requests** (and variables blocks for mutations) inside those strings, including relation blocks where relevant—do not rely only on a separate `_tests_all_queries` file for discoverability.
- Live references: cronexia-gta-back\app\src\ar-versions\docs, cronexia-gta-back\app\src\ar-resource-balances\docs

---

## functions/ folder (resolver unbloating)

- Move repetitive logic out of the resolver into plain functions under `CLASSNAME/functions/`:
  - Building the merged object passed to Prisma for `findFirst` / `findMany` (skip, take, where, whereOpen, orderBy, orderByOpen, cursor, distinct).
  - Remapping GraphQL `id` to the real Prisma unique field name (e.g. `idWorkflow`, `idResourceUserProfileInstanceVal`) on `where`, `orderBy`, `cursor`, and nested structures.
  - Mapping `distinct` enum values to Prisma `distinct` field arrays if applicable.
- Reference: cronexia-gta-back\app\src\workflows\functions (e.g. `build-workflow-find-list-args.ts`, `remap-workflow-where-id.ts`, `apply-distinct-workflow.ts`)
- The resolver should mostly wire `@Args()`, call one or two builders, and delegate to the service.

---

## Circular dependency (models)

- GraphQL `@ObjectType` model files often reference other models for `@Field(() => OtherModel)`. Top-level `import { OtherModel } from '…'` can create circular dependency cycles (A imports B, B imports A).
- **Prefer lazy loading** for related models in `@Field` decorators:
  - `() => require('../../other-path/models/other.model').OtherModel`
  - Optionally use `import type { OtherModel } from '…'` only for TypeScript property types if needed, without pulling the decorator target from a static import of the same module’s runtime export.
- Boilerplate illustration: cronexia-gta-back\__boilerplates\classname-kebab\models\classname-kebab.model.ts (commented examples around lines 52–85).
- Also compare: cronexia-gta-back\app\src\ar-exercises\models\ar-exercise.model.ts

---

## Enum management : Stay DRY (one entrypoint)

Enum are now created and `registerEnumType` a single time, each in it's own file in `CLASSNAME/enums`. Boilerplate might be outdated.

All current classes should be up to date ; references :

- @cronexia-gta-back\app\src\configs\enums\config-type.enum.ts
- @cronexia-gta-back\app\src\configs\enums\config-distinct.enum.ts

---

## Technical notes:

- Respect project conventions
- do NOT use JSDoc comments, use project comments
- Do not update GraphQL generated files/types, they'll be reset automatically
- If you need to create functions, types and/or interface
  - Do NOT bloat the code :
  - Create one file PER functions, types, interface
  - Add then in a dedicated subfolder, respectively
    - function/
    - type/
    - interface

Don't hesitate to ask questions if needed, or ask for specific files for context
