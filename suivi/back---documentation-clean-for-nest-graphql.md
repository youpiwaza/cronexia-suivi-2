Update/implement proper documentation with GraphQL queries for XXX_RESOLVER, XXX_DOCS_FOLDER

Schema file : XXX

Pay attention to ids and examples, to be populated from seeds in XXX

---

Queries are to be implemented in /docs subfolder, cf. boilerplate reference : cronexia-gta-back\__boilerplates\classname-kebab\docs

Some old implemented classes might not have the folder, if so create related files, and update imports and use accordingly in resolver, cf. cronexia-gta-back\__boilerplates\classname-kebab\classname-kebabs.resolver.ts

- lines 47 to 54
- each occurence of "description: "

---

For the current class query

Do NOT add dev fields :

- id_CLASSNAME
- createdAt
- updatedAt
- createdBy
- updatedBy

Do NOT add foreign keys fields ("Id" suffix) : ~ relationId

---

For relationships nested queries

Gather fields from related schema files (if not found, it's probably in cronexia-gta-back\app\prisma\schema\schema.prisma, be careful it's a huge file)

Do NOT add dev fields nor foreign keys fields

If the relationship is one to many > RELATION_CLASSNAME with first letter lowercase (camelCase)

If the relationship is many to one > RELATION_CLASSNAMEs with first letter lowercase (camelCase) and "s" suffix

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
