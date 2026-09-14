# Replace classic ~throw error with our custom error management system

Tech references:

- Documentation on how to implement and use : `cronexia-gta-back\_docs\12-erreurs-gestion-cronexia.md` (in french)
- Main entry point : `cronexia-gta-back\app\src\_utility\error\cronexia-error-dictionnary.ts`
- Examples (already implemented):
  - `cronexia-gta-back\app\src\resources\resources.service.ts`, line 287
  - `cronexia-gta-back\app\src\resources\resources.service.ts`, line 369
  - `cronexia-gta-back\app\src\badge-on-resources\badge-on-resources.service.ts`, line 640

---

Ask for an error prefix if needed, for example for the context "workflow", the prefix should be "CRO_WKFW_", resulting in the first error to be "CRO_WKFW_00000001".

Try to preserve the french formulation, the most important part is the addError function parameter cronexiaError > 'fr-FR'.messageHuman.

---

Procedure for each error to replace:

Step 1: Replace the current "throw" error with our error management system.

Step 2: Adjust the return (models) if needed (and interfaces, etc.)

Step 3: Adjust frontend if needed:

- Step 3a: GraphQl queries in `cronexia-gta-front\app\src\lib\graphql`
  - (related folder available in kebab-case), or just ask
  - example for Resource: `cronexia-gta-front\app\src\lib\graphql\resources`
- Step 3b: Frontend api in `cronexia-gta-front\app\src\routes\api`
  - (related folder available in kebab-case, both singular and plural), or just ask
  - example for Resource:
    - `cronexia-gta-front\app\src\routes\api\resource`
    - `cronexia-gta-front\app\src\routes\api\resources`

---

Where to search for errors to replace:

- XXX
- XXX
- XXX

---

## Technical notes

- Pay attention to End of lines (EOL) > Use LF only
  - Do NOT use CRLF
- Preserve spacing and spacing comments
  - "// ---"
  - "// * 🔗 Relations" once per relation group
- Respect project conventions
- do NOT use JSDoc comments, use project comments
- Do not update GraphQL generated files/types, they'll be reset automatically
- If the resolver is too big, do not create python script or such, just list me the list of copy/paste or delete to do
- Split plan into mangeable steps

Don't hesitate to ask questions if needed
