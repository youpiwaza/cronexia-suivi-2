# Create frontend api files for XXX

We got the backend already implemented (routes, DTOs) in the folder XXX through NestJs and GraphQL.

Structure and datas:

- Database: XXX
- Seeds: XXX

TODO: Implement the frontend API following project recommandations:

- Create the GraphQL queries export files in cronexia-gta-front\app\src\lib\graphql
  - in a queries\ folder
    - a findUnique query with proper params
    - a findMany query
  - in a mutations\ folder
    - create
    - update
    - delete

References:

- (best reference) cronexia-gta-front\app\src\lib\graphql\absence-right
- cronexia-gta-front\app\src\lib\graphql\ar-priority
- cronexia-gta-front\app\src\lib\graphql\ar-version
- cronexia-gta-front\app\src\lib\graphql\relative-period

Notes:

- class folder name isn't plural
- filenames are in camelCase (it's the only instance of camelCase file naming in the project, to match GraphQL queries names)
- file naming conventions MUST be
  - findUnique > CLASSNAME.ts (single)
  - findMany > CLASSNAMEs.ts (plural)
  - create > createCLASSNAMEs.ts
  - update > updateCLASSNAMEs.ts
  - delete > deleteCLASSNAMEs.ts
- DO NOT implement those technical fields in graphql queries since they are not present in the Models
  - createdAt
  - updatedAt
  - createdBy
  - updatedBy

---

- Create all the related front api helpers in cronexia-gta-front\app\src\routes\api

References:

- (best reference) cronexia-gta-front\app\src\routes\api\absence-right
  - cronexia-gta-front\app\src\routes\api\absence-rights
- cronexia-gta-front\app\src\routes\api\ar-priority
  - cronexia-gta-front\app\src\routes\api\ar-priorities
- cronexia-gta-front\app\src\routes\api\relative-period
  - cronexia-gta-front\app\src\routes\api\relative-periods
- if available, every backend folder should have a `/docs` folder available with all comon queries

Notes:

- class folder name isn't plural for
  - findUnique
  - create
  - update
  - delete
- class folder name is plural for
  - findMany
- filenames are in kebab-case
- if necessary, update models to return idCLASSNAME since we'll need them for update forms

Don't hesite to ask questions if you need clarifications

---

Notes:

- Some of the current implementations (references) don't respect the single/plural implementations yet
- For the GraphQL folder structure, use kebab-case singular (Like AbsenceRight > 'absence-right')
- For the findMany API route use structure (example with AbsenceRight)
  - absence-right
    - +server.ts // findUnique
    - create/+server.ts
    - update/+server.ts
    - delete/+server.ts
  - absence-rights
    - +server.ts // findMany
- Do not use JSDoc comment, respect project conventions

---

Implementation Details:

- GraphQL Query/Mutation Patterns
  - Each file exports the GraphQL query/mutation string and an operation constant
  - Follow the pattern from absence-right and relative-period examples
  - Include all model fields in return statements
- API Route Patterns
  - Use handleGraphQLResponse utility for error handling
  - Use handleApiError utility for exception handling
  - Use parseRequestData utility for parsing FormData/JSON
  - Use fetchOptionsGet for GET requests
  - Use fetchOptionsPost for POST requests
  - Follow the structure from absence-right and relative-period examples
- Do not update GraphQL generated files/types, they'll be reset automatically
- Details
  - When a string contains a ', don't escape the character, use ``
    - Example:
      - do not : 'La date de début d\'acquisition est requise'
      - do : `La date de début d'acquisition est requise`
  - When checking for parameters validity (for example in api > create)
    - do not : test individually and return a json for each error
    - do : create an error array, push the error string if there is, than return only one error with concatenated strings (thourgh join()), cf. cronexia-gta-front\app\src\routes\api\ar-movement-instance\create\+server.ts

---

Notes:

- Split plan into mangeable steps
- Respect project conventions
- DO NOT use JSDoc, use project comments conventions
- For the *CLASS_NAME*Array component, it should display all database columns, including technical fields
- Technical Notes
  - Use Svelte 5 syntax ($state(), $derived, $props(), onclick instead of on:click)
  - Follow import organization convention (Svelte/packages, Utility, Functions, Components, Variables, Behavior)
  - No need to test in cursor browser, i'm testing live in watch mode
  - Do not update GraphQL generated files/types, they'll be reset automatically

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
