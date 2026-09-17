# 🌱 TODO

List of pending tasks.

## Légende

- 🚀 En cours / **1 MAX A LA FOIS**
- ✅ Terminé
- ⏩ Suite
- 🎯 objectifs
  - Priorités 🥇🥈🥉🏅🏆💥💥💥
- 📝 Doc
- 🚧 WIP / Work In Progress / Entamé, pas terminé
- 📌 A tester / Recettage
- 🐛 bug
- 🔍 Lecture/Vidéos
- 🚨 Attention
- 🌱 Plus tard, besoin dépendance ou flemme sur le coup
- ♻️ Récurrent / Refacto
- 🐯🌐 NestJs / GraphQL
- 🎨🌐 Front / GraphQL & api/
- 🚚 Contenus/notes dans les autres fichiers TODO
- 💩 KO
  - ⏳ en attente
- 🤏 Petite partie
- 👌 Cleaner / ajouter des types
- 📧 email envoyé/à envoyer
- ✨ Rien à toucher, déjà en place
- 👪 Réunion ou call
- ❌ Nope
- 💾 BDD ou Back / 🎨 Front
- 👀 voir
- ❓❔ Question / Question répondue
- 🔨 chop²
- 🔧 config
- 👨‍💻 Notes dev
  - 👷 Exemple / Note pour aider les autres devs
  - 🤵‍♂️ Attentes métier / utilisateur
- ⚡️🐌 Optimisation / Lenteur
- 🧠 Réflexions / Algos
  - 🔀 Alternative / Formattage
- ⬆️⬇️ Upgrade / Downgrade ou Envoi / Reception de datas
- ⏱️⏱️⏱️ Benchmarks OU tâche Avec estimations de temps
  - ➕ Taf en plus / Non compté dans l'estimation
  - ➕📝 Création d'un nouveau ticket
- 💡📅🔢📝⌚ Types > Boolean / Date / Number / String / Time
- 👴⚰️ Obsolete / Dead code
- ⚗️♨️ Filter / reduce // merge
- 🔮 Anticiper les besoins futurs
- 🔙 Revert changes / Return type
- 🧰 Toolbox / utility
  - 🏭 Boilerplate
- 🧹 Cleaner le code, virer les console.log
  - 🛡️ Guards
- ⛓️ Contraintes
- 🔗 Relation
- 🛣️ Création de routes / roadmaps
- 📜 Gestion de l'historique
- 🧮 Inventorier
  - ✂️ Découper
- 🔭 Scope
- 👥 Dédoublonner
- 👶💪🤮 Facile / Pas facile
- 🤖 Automatique / généré
  - 🦾 Fonctions
- 💯 Résultat / Retour / Complété
- 👪 Réunions / Calls / Ensemble d'utilisateurs
- 💬 Typo / Traduction / Vocabulaire
- 🧩 Composant
- 🍪 Cookies
- 🔐 auth
- ⚔️ Conflits

## Raccourcis Cursor

- [Tuto / docs](https://docs.cursor.com/en/welcome)
- Ctrl + Shift + $ // Agent > Onglet à droite questions, etc.
- Ctrl + K // Inline edit
- [Bugbot](https://docs.cursor.com/en/bugbot)

---

## Organisation

- rieng

## Dev

- TODO: 🔐 Remove dev test security exception
  - `/_dev/test/workflow-attachments` ouvert à `patrick.gere-en-heure` (login / resourceId / matricule) — `assert-page-access.ts`

🌐🔍⚡️ [GQL cheat sheet](https://github.com/sogko/graphql-schema-language-cheat-sheet)

- ♻️ Au niveau des relations (entity/dto/model)
  - Ptet moyen de créer les champs à importer dans leurs entités respectives
  - PUIS de les importer/implémenter la ou l'on en a besoin
  - ~ similaire à 1TM & MT1 > ~des ArgsType/InputType avec les champs uniques, les champs classiques, les champs relatifs aux relation 1TM & MT1.... Puis importer à leurs places
  - Nesté > connexion & creation > Merdier conversion "id" en "idRLEATION_MAJ"
    - Prévoir DTO idXXX original pour les créations/connexions/etc. nestées ??? Ca éviterai les conversions
- 🌱🤖 Tests unitaires
  - Routes dédiées sur chacune des entité
  - async > await avec plusieurs call aux services, permettrait de tester create/update, etc. de manière auto
    - create etc. > fixer ids afin d'éviter de viander à coté

---

- ♻️ ENUMs > certaines sont identiques > ex: ResBV, ResDV, ResNV, ResSV,
- ♻️ Cronexia mandatory > createdAt, updatedAt, createdBy, updatedBy > Générique
- 🌱 Id / Unicité à partir de champs multiples @@id / @@unique
  - ⏳👪 Propositions envoyées à PO, en attente de retours
  - 🔍 "multi-field ID (composite ID)"
  - `@@unique(fields: [firstName, lastName], name: "fullname")`
  - `@@id([firstName, lastName])`
  - 📝 [PC doc](https://www.prisma.io/docs/orm/reference/prisma-client-reference#get-the-user-record-with-firstname-of-alice-and-lastname-of-smith-unique)
  - [@@unique & @@id & @@index](https://www.prisma.io/docs/orm/reference/prisma-schema-reference#unique-1)
  - ~RSV > matricule + champs + effectDate (pas besoin de la valeur)
- 🌱♻️ TODO: Refacto GraphQL trop longue à mettre en place pour le moment
  - 👷 Confort recettage > GUIDs fixes explicites
    - ✅🌱 Remplacer les GUIDs par des valeurs définies explicites.
    - ✅🌐🐯📝 Maj docs GQL
    - 🤏🌐 Maj Requête de test
    - 🤡 Maj mockaroo
  - Tout passer en class inheritance/generics ? [yay](https://docs.nestjs.com/graphql/resolvers#class-inheritance)
    - **ArgsType** / Teeeeeeeeeechniquement si le where est populé par create-input, il peut être générique ?
    - Doc GQL > Args descriptions ~skip take where whereOpen, etc. > Faire une doc générique
  - Refaire les input types en [refacto](https://docs.nestjs.com/graphql/mapped-types#pick)
    - Tous les champs
      - Droits corrects
      - Droits optionnels ? (Pas besoin, cf. update ?)
    - Champs uniques
  - Distinct > allFields & none puis héritage
  - create createMany > createMany c'est le même sans les relations (pas de création nestée)
  - create > relations required, but not in case of a nested create, ex: resource > create > ResNV
    - > Make a nested create
- 🔍📝 Prisma Client
  - Maths non concurentielles sur champs > [Atomic number operations](https://www.prisma.io/docs/orm/reference/prisma-client-reference#atomic-number-operations)
  - ⚡️ Perfs [The transaction API](https://www.prisma.io/docs/orm/prisma-client/queries/transactions#the-transaction-api)
- ♻️ ResourceStringValue & ResourceNumberValue dans le sous dossier de StructureResource
  - ❤️ [how to achieve model-specific type inference from prisma model without explicitly passing the index string to PrismaClient object?](https://stackforgeeks.com/blog/how-to-achieve-modelspecific-type-inference-from-prisma-model-without-explicitly-passing-the-index-string-to-prismaclient-object)
