# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🐯🌐🛣️ Nouvelle route "mes délégations actives"

Exposer les délégations actives pour l’UPI connecté, ainsi que les traces/logs pour les validations faites par délégations

## Dev

Exposer delegatedForValidator { user { resource { firstName lastName } } } (+ helpers) sur WRLS et WR (lastDelegatedFor*)

Query myActiveDelegations (nom TBD) pour le menu : id UPI titulaire, nom, matricule, photo, rôle — filtrée par isDelegationEffective

Exposer excludeSelf sur le modèle GraphQL ResourceField (dossier + admin fields)

Module déjà UserProfileInstances — pas forcément un nouveau module

---

### ✅ Done

- Traces WRLS `delegatedForValidator*` / WR `lastDelegatedFor*` et `ResourceField.excludeSelf` : déjà GTA-1651 (CRUD GraphQL + ResolveFields). Nested `delegatedForValidator { user { resource { firstName lastName } } }` déjà résolu. Pas de changement schéma Prisma
- Helper GTA-1653 : `ActiveDelegationTitulaire.photoId` (`User.photoId`, `null` si absent). Specs photo présente / absente
- Query `myActiveDelegations` sur `UserProfileInstances` : `@UseGuards(GqlJwtAuthGuard)` uniquement (`RightsGuard` commenté). Pas d'arguments. `[]` si aucune délégation effective. Shape `MyActiveDelegationModel` : `resourceId`, `matricule`, `label`, `photoId`, `userProfileInstances[]` (`idUserProfileInstance`, `label`, `userProfileCode`, `userProfileLabel`). UPI courantes, tri rang profil asc. v1 : `[0].idUserProfileInstance` = acting-as (argument `userProfileInstance` existant, GTA-1655 / GTA-1656)
- Fichiers : `cronexia-gta-back/app/src/user-profile-instances/models/my-active-delegation*.model.ts`, `docs/my-active-delegations.doc.ts`, resolver + `functions/delegation/resolve-active-delegations-for-user.ts`
- Hint FE GTA-1659 / GTA-1660 : query + `GET /api/user-profile-instance/my-active-delegations` ; menu visible ssi `length > 0` ; photo = `photoId` ; acting-as = `userProfileInstances[0].idUserProfileInstance`
- Hors scope inchangé : builders / codegen / route `/api` (GTA-1659), notifs (GTA-1658), menu FE (GTA-1660). Manual : regen `schema.gql` au prochain start API
