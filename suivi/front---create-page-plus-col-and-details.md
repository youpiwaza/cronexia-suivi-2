# Créer une page dans \tests dans le front avec liste en tableau, affichage détails dans ~card et formulaires basiques

Create a new test page in order to test display queries and form (post) queries for XXX (this is the classname).

Page title is "XXX" in french, without the prefix.

---

Best reference overall : Most advanced example is AbsenceRights :

- Page :
  - cronexia-gta-front\app\src\routes\(app)\_dev\test\absence-rights
  - cronexia-gta-front\app\src\routes\(app)\_dev\test\movement
- Components :
  - cronexia-gta-front\app\src\routes\components\cronexia\absence-right\elements\absence-right
  - cronexia-gta-front\app\src\routes\components\cronexia\ar-movement

---

- Add a new folder in cronexia-gta-front\app\src\routes\(app)\_dev\test\CLASS_NAME in kebab-case
  - example for RelativeDate : Add a new folder in cronexia-gta-front\app\src\routes\(app)\_dev\test\relative-date

- also update cronexia-gta-front\app\src\config\page-config.ts accordingly

---

Phase 1: Display

- First column : create a dedicated component in cronexia-gta-front\app\src\routes\components\cronexia\CLASS_NAME\*CLASS_NAME*Array
  - exemple for RelativeDate > RelativeDateArray
  - containing an advanced table cronexia-gta-front\app\src\routes\components\common\tables\advanced\TableAdvanced.svelte, 3 columns, containing a radio button (allow selection for toolbar use), code and labelShort
  - example : cronexia-gta-front\app\src\routes\(app)\_dev\test\absence-rights\[[code]]\+page.svelte line 365
  - Implementations examples are here : cronexia-gta-front\app\src\routes\(app)\_dev\test\tables\cronexia\advanced-table\+page.svelte
- Second column : fill the card with inputs, according to the types of the fields
  - example : cronexia-gta-front\app\src\routes\(app)\_dev\test\absence-rights\[[code]]\+page.svelte line 396
- add a new +page.server.ts containing the frontend api call, to populate +page.svelte with datas
  - exemples:
    - cronexia-gta-front\app\src\routes\(app)\cycles\[...params]\+page.server.ts
    - cronexia-gta-front\app\src\routes\(app)\anomalies\[...params]\+page.server.ts
- add a new +page.svelte containing the newly created component, with injected datas, in order to display each database column + line
  - create a simple layout : .row > .col-3 + .col-9
    - First colum will contain a list of ~titles, second column will contain a big .card will all fields in inputs.
  - cronexia-gta-front\app\src\routes\(app)\_dev\test\absence-rights\[[code]]\+page.svelte
- Do not gather fields outside of the return Model ~=
  - idCLASS_NAME
  - createdAt
  - updatedAt
  - createdBy
  - updatedBy
- For types and props, use those generated in the frontend, from the backend
  - cf. src/generated/graphql/graphql.ts
  - exemple : import type { RelativeDateModel } from '$typesGraphql';

---

Phase 2: Add to Menu

- Add the newly created page to the secondary menu
  - cronexia-gta-front\app\src\routes\functions\common\menu\secondary\links-by-profile\dev.ts
  - With a "new" tag
  - if adding an icon > cronexia-gta-front\app\src\config\icon-config.ts

---

Phase 3: Forms

- Update cronexia-gta-front\app\src\config\page-config.ts to allow the page to use the toolbar
- create 3 components: forms in cronexia-gta-front\app\src\routes\components\cronexia\CLASS_NAME\forms\
  - *CLASS_NAME*Form
    - Used for both create AND update
  - *CLASS_NAME*FormDelete
  - They will be just basic forms:
    - create and update with each field to populate (do not add the field managed automatically by the backend)
    - Delete : a select displaying a list of unique field and a validation button
  - reference for forms:
    - cronexia-gta-front\app\src\routes\components\cronexia\absence-right\forms
- On toolbar buttons click: the corresponding form is displayed in a popup, similar to the other pages
  - references (for the toolbar implementation):
    - cronexia-gta-front\app\src\routes\(app)\admin\population\[[populationName]]

---

References for the class to implement:

- backend database schema: XXX
- backend seeds: XXX
- backend nestjs & graphql : XXX
- frontend graphql queries:
  - XXX
- frontend api:
  - XXX
  - XXXs

---

References of already implemented test page :

- cronexia-gta-front\app\src\routes\(app)\_dev\test\absence-rights
- cronexia-gta-front\app\src\routes\(app)\_dev\test\movement-instance\[[idArMovementInstance]]
- components : cronexia-gta-front\app\src\routes\components\cronexia\ar-movement-instance

---

Notes:

- Respect project conventions
- DO NOT use JSDoc, use project comments conventions
- For the *CLASS_NAME*Array component, it should display all database columns, including technical fields
- Technical Notes
  - Use Svelte 5 syntax ($state(), $derived, $props(), onclick instead of on:click)
  - Follow import organization convention (Svelte/packages, Utility, Functions, Components, Variables, Behavior)

Imports conventions :

// 📦️ Svelte / Packages

// 👌 Types & props

// 🔧 Config

// 🧺 Variables

// 🧰 Utility

// 🦾 Functions

// 🌐 GraphQL Queries

// 🧩 Components

---

This is complex task, don't hesitate if you have any question
