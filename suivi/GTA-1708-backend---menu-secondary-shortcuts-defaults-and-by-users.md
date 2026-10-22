# Menu secondary > Quick links : Dynamic defaults and per users

Currently, quick links in menus @cronexia-gta-front-v2\app\src\routes\components\common\menu\main\MenuSecondary.svelte line ~241, are hardcoded per role @cronexia-gta-back\app\prisma\schema\user-profile.prisma

We need to make those dynamic.

We need to be able to store an ordered set of quick links both for each role defaults, and per User+role @cronexia-gta-back\app\prisma\schema\user-profile-instance.prisma basis

Scope: Frontend implementation (update MenuSecondary, tests, etc.) is OUT OF SCOPE

---

## Backend

### Database

**One table** `MenuQuickLink` (same payload for role defaults and per-user overloads). Two tables would duplicate Prisma + Nest CRUD for identical fields.

Precedent: `PlanningFavorite` (one table, optional owner). Here owners are different entities, so do **not** copy `isCustom` + nullable `userId` blindly.

#### Ownership

- `userProfileId` **always required** — which role this list belongs to
- `userProfileInstanceId` **optional**
  - `null` = default for that role
  - set = overload for that UPI (User+role)
- Discriminator = `userProfileInstanceId IS NULL`
- **Do not** add `isDefaultPerRole` (redundant, easy to desync)
- Attach customs to **UPI**, not `User` (Maxime employee ≠ Maxime manager)

#### Shape

One **row per shortcut** (not a JSON blob), with `position`. Prefer a stable `code` (e.g. `planning`, `calendar`, `demands`, `clocking-badge`) rather than duplicating `href` / icon / label already in the frontend (`$links`, `iconsMenuSecondary`).

```prisma
model MenuQuickLink {
  idMenuQuickLink String    @id @default(uuid()) @db.Uuid
  createdAt       DateTime  @default(now())
  updatedAt       DateTime? @updatedAt
  createdBy       String    @default("admin")
  updatedBy       String?

  position Int
  code     String

  userProfile   UserProfile @relation(fields: [userProfileId], references: [idUserProfile])
  userProfileId String      @db.Uuid

  userProfileInstance   UserProfileInstance? @relation(fields: [userProfileInstanceId], references: [idUserProfileInstance])
  userProfileInstanceId String?              @db.Uuid

  @@index([userProfileId(ops: UuidBloomOps)], type: Brin)
  @@index([userProfileInstanceId(ops: UuidBloomOps)], type: Brin)
}
```

Uniqueness (“one default list per role”, “one position per UPI”) cannot be a plain Prisma `@@unique` (NULL ≠ NULL). Enforce in the service; optional Cockroach partial unique indexes later.

#### Read / write

For the connected UPI:

1. Load rows with that `userProfileInstanceId`
2. If any exist → that is the **full** list (no merge)
3. Else load rows with that UPI’s `userProfileId` and `userProfileInstanceId: null`

First user customization = copy role defaults onto the UPI, then edit that copy. Users with no rows keep inheriting role defaults.

---

### Seeds

We'll provide seeds for

- Each current role (employee, manager, HrManager, admin, super.admin)
  - common to all seeds sets (demo, demo-arte, dev), to implment in @cronexia-gta-back\app\prisma\seeds-new\01-required
  - Reuse content hard coded  in MenuSecondary

- Dev set only : custom quick links for Maxime @cronexia-gta-back\app\prisma\seeds-new\50-dev\resource\123456A.seed.ts in order to be able to test frontend implementation
  - Overload for Maxime employee
  - Overload for Maxime manager

- Demo @cronexia-gta-back\app\prisma\seeds-new\25-demo & demo-arte @cronexia-gta-back\app\prisma\seeds-new\26-demo-arte seeds are built in a more optimized way
  - create helper function to be able to quickly implement defaults to resources, to be integrated in @cronexia-gta-back\app\prisma\seeds-new\25-demo\resource\_bp_add_one_resource-to-demo-w-refacto.ts, similarly to what's already in place for other contexts
  - If applicable, also use it for Maxime's dev seeds

---

### NestJs and GraphQL

Implement in NestJs and GraphQL, following recomandations:

- NestJs @cronexia-suivi-2\suivi\back---implement-crud-in-nestjs-and-graphql.md
- GraphQL doc @cronexia-suivi-2\suivi\back---documentation-clean-for-nest-graphql.md

---

### Related frontend : queries and apis

Implement frontend queries and apis, following recomandations: @cronexia-suivi-2\suivi\front---create-queries-and-api.md
