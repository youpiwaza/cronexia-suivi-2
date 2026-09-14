# Implement Fix for circular dependency in NestJS Models

Two distinct problems require two distinct fixes.

---

## Problem 1 — Model-level: SWC rejects `import()` types in decorator metadata

**Symptom**: Nest/SWC panics at compile time with:

```
Bad type for decorator: TsImportType(TsImportType { ... value: "../../path/to/some.model" ... })
```

**Cause**: Using an inline dynamic import type as a property type annotation while that property carries a decorator (`@Field`, `@IsOptional`, etc.). SWC cannot emit decorator metadata for `import('…').XModel`.

**Wrong patterns** (both cause the error):

```ts
// ❌ static value import + used in @Field directly
import { SomeModel } from '../some/some.model';
@Field(() => SomeModel, { ... })
someField: SomeModel;

// ❌ inline import() type as property type
@Field(() => require('../some/some.model').SomeModel, { ... })
someField: import('../some/some.model').SomeModel;
```

**Correct pattern** — two rules, both required:

```ts
// ✅ 1. type-only import (erased at compile time — no runtime module load)
import type { SomeModel } from '../some/some.model';

// ✅ 2. require() inside @Field arrow (lazy — resolved after all modules load)
@Field(
  () => require('../some/some.model').SomeModel,
  {
    name: 'someField',
    description: 'Related SomeModel',
    nullable: true,
  },
)
@IsOptional()
someField?: SomeModel;  // property type uses the type-only import — OK for SWC
```

For arrays:

```ts
import type { SomeModel } from '../some/some.model';

@Field(
  () => [require('../some/some.model').SomeModel],
  {
    name: 'someFields',
    nullable: 'itemsAndList',
  },
)
@IsOptional()
someFields?: SomeModel[];
```

**Real examples** in the codebase:

- `cronexia-gta-back/app/src/ar-population-targets/models/ar-population-target.model.ts` — multiple relations
- `cronexia-gta-back/app/src/population-on-workflows/models/population-on-workflow.model.ts` — two relations (`population`, `workflow`)
- `cronexia-gta-back/app/src/workflow-levels/models/workflow-level.model.ts` — `workflow` and `validator` fields

**Boilerplate** (keep up to date): `cronexia-gta-back/__boilerplates/classname-kebab/models/classname-kebab.model.ts`

---

## Problem 2 — Module-level: Node.js TDZ crash from bidirectional static imports

**Symptom**: Nest starts, SWC compiles fine, but Node.js crashes at runtime with:

```
ReferenceError: Cannot access 'SomeModule' before initialization
```

**Cause**: Two modules statically import each other at the top of their files. Node.js evaluates circular imports partially (TDZ), so one module receives an uninitialized reference when loaded from a third module that does not use `forwardRef`.

NestJS `forwardRef(() => SomeModule)` only tells the NestJS DI container to resolve the dependency lazily — it does **not** fix the Node.js module-load cycle.

**Wrong pattern** (creates a bidirectional cycle):

```ts
// populations.module.ts
import { PopulationOnWorkflowsModule } from '../population-on-workflows/population-on-workflows.module';
// ...
forwardRef(() => PopulationOnWorkflowsModule),

// population-on-workflows.module.ts
import { PopulationsModule } from '../populations/populations.module';
// ...
forwardRef(() => PopulationsModule),
```

Any third module (e.g. `_pdf-gen.module.ts`) importing `PopulationsModule` directly will get the uninitialized value.

**Rule**: only the "child" (more specific) module imports the "parent" (more fundamental) modules — never the other way around.

```
population-on-workflows.module  -->  populations.module     (correct)
population-on-workflows.module  -->  workflows.module       (correct)
populations.module              -->  population-on-workflows.module  (WRONG — creates cycle)
workflows.module                -->  population-on-workflows.module  (WRONG — creates cycle)
```

**Fix**: remove the `PopulationOnWorkflowsModule` import and `forwardRef(() => PopulationOnWorkflowsModule)` from both `populations.module.ts` and `workflows.module.ts`.

The back-reference fields (`populationOnWorkflows`) remain on `WorkflowModel` and `PopulationModel` as optional typed fields. They are populated only when the service/Prisma query explicitly includes them (`include: { populationOnWorkflows: true }`). No `@ResolveField` is needed in `WorkflowsResolver` or `PopulationsResolver` for this to work safely.

**Real example**: `cronexia-gta-back/app/src/populations/populations.module.ts` and `cronexia-gta-back/app/src/workflows/workflows.module.ts` after the fix applied in April 2026.

---

## Summary

| Problem | Symptom | Fix |
|---|---|---|
| SWC decorator metadata | Compile panic `Bad type for decorator: TsImportType` | `import type` for property + `require()` inside `@Field` |
| Node.js TDZ cycle | Runtime `ReferenceError: Cannot access '…' before initialization` | Remove the inbound import from the parent module; keep the cycle one-directional |
