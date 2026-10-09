# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🎨🌐 Maj des queries & api/ front (repasse & tests poussés)

Brancher le front (queries GraphQL + routes /api) pour que le menu et les pages puissent consommer le back.

## Dev

Patron user-profile-instance. Regen codegen après Backend-06

Query myActiveDelegations

Étendre userProfileInstanceGetWorkflowResource + mutation result : delegatedForValidator*

Param actingAs / UPI titulaire sur les appels existants

Miroir workflow-resource-to-validate + update-wrls-status-with-cascade : propager acting-as

GET /api/user-profile-instance/my-active-delegations

---

### Hint GTA-1656 (mutation cascade)

Pas de nouvel argument GraphQL. Pages Délégation : passer l'id UPI **titulaire** dans `userProfileInstance` existant. L'acteur est le JWT `supi` (bearer). Étendre la sélection de `userProfileInstanceUpdateWrlsStatusWithCascade` avec `delegatedForValidator*` / `delegatedForValidatorId` / `delegatedForValidatorHelper` et `lastDelegatedFor*` (`cronexia-gta-front-v2/app/src/lib/graphql/user-profile-instance/mutations/userProfileInstanceUpdateWrlsStatusWithCascade.ts`). `cronexia-gta-front-v2/app/src/routes/api/user-profile-instance/update-wrls-status-with-cascade/+server.ts` : pas de nouveau champ body. Hint query liste : GTA-1655 (même argument UPI titulaire).

---

### Hint GTA-1657 (myActiveDelegations + menu GTA-1660)

Back livré. Regen codegen après restart API (`schema.gql`).

- Query GraphQL `myActiveDelegations` (pas d'arguments, JWT). Patron : `cronexia-gta-front-v2/app/src/lib/graphql/user-profile-instance/queries/` (nouveau fichier, cf. `userProfileInstanceGetWorkflowResource.ts`)
- Route `GET /api/user-profile-instance/my-active-delegations` (miroir, comme `workflow-resource-to-validate`)
- Shape : `resourceId`, `matricule`, `label`, `photoId` (nullable, `GET /api/uploads/{photoId}`), `userProfileInstances[]` (`idUserProfileInstance`, `label`, `userProfileCode`, `userProfileLabel`)
- Acting-as v1 : `userProfileInstances[0].idUserProfileInstance` dans l'argument `userProfileInstance` existant (GTA-1655 / GTA-1656). Pas de champ `actingAs`

**Menu GTA-1660** — visible ssi `myActiveDelegations.length > 0` (tous profils, y compris EMPLOYEE). Une entrée par ligne (`label` + `photoId`). Hrefs **uniquement** sous `(with-filters)/` (bandeau inconditionnel). Pas `/demands`, pas without-filters. 1 titulaire : Délégation → Gestion des demandes ; N titulaires : Délégation → {Nom titulaire} → Gestion des demandes. Ne pas ajouter d'autres enfants en v1.

---

📌 Double check de l’ensemble des routes (recup & forms)

📌🔙 Ticket à laisser ouvert en recettage dev afin de pouvoir traiter les éventuels retours de Moez

- Note max: S’il reste du temps soit on skip, soit j’en profite pour passer des tests unitaires

---

### ✅ Done

- Query `myActiveDelegations` : `cronexia-gta-front-v2/app/src/lib/graphql/user-profile-instance/queries/myActiveDelegations.ts` (pas d'arguments, JWT). Shape : `resourceId`, `matricule`, `label`, `photoId`, `userProfileInstances[]` (`idUserProfileInstance`, `label`, `userProfileCode`, `userProfileLabel`)
- Route `GET /api/user-profile-instance/my-active-delegations` : `cronexia-gta-front-v2/app/src/routes/api/user-profile-instance/my-active-delegations/+server.ts` (miroir `user-profiles/codes`). `[]` = succès (menu masqué)
- Liste `userProfileInstanceGetWorkflowResource` : sélection étendue `delegatedForValidator*` / `lastDelegatedFor*` (+ nested `{ user { resource { firstName lastName } } }`). Arguments inchangés
- Mutation `userProfileInstanceUpdateWrlsStatusWithCascade` : même sélection sur WRLS + WR. Pas de re-select `workflowResourceLevelStates` (circular). Arguments / body inchangés
- Pas d'arg `actingAs`. Pages Délégation : UPI **titulaire** dans `idUserProfileInstance` / `userProfileInstance` existant. Inbox perso : UPI JWT. Commentaires sur `workflow-resource-to-validate` et `update-wrls-status-with-cascade`
- Repasse callers : request-management, workflow-tab, widget, AI, `fetch-workflow-mutations` — mêmes URLs et même champ UPI ; les champs trace arrivent dans la réponse existante (`null` = titulaire a agi)
- Hors scope : pages / menu (GTA-1660 / GTA-1661 / GTA-1662), codegen (`lib/generated`), tests unitaires (skip). Manual : restart API si `schema.gql` stale, puis `bun run codegen---generate-graphql-types-from-back` quand le FE a besoin des types

**Hint GTA-1660 / GTA-1661 / GTA-1662**

- Menu visible ssi `data.myActiveDelegations.length > 0` (tous profils, y compris EMPLOYEE). Photo : `GET /api/uploads/{photoId}`. Acting-as v1 = `userProfileInstances[0].idUserProfileInstance`
- Hrefs uniquement sous `(with-filters)/`. 1 titulaire : Délégation → Gestion des demandes ; N titulaires : Délégation → {Nom titulaire} → Gestion des demandes. Pas d'autres enfants en v1
- Liste / cascade : mêmes URLs ; swap uniquement l'id UPI (titulaire `[0]`) sur les pages Délégation
