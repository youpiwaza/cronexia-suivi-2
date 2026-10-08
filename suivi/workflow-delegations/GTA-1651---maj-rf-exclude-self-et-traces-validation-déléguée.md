# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 💾🐯🌐 Maj RF.exclude self et traces validation déléguée

Persister qui a vraiment agi vs pour qui, et empêcher de se choisir soi-même comme délégué au niveau champ.

## Dev

- FKs + helpers + index Brin sur delegatedForValidatorId / lastDelegatedForValidatorId (même style que validatorId)
- Relations inverses sur UserProfileInstance
- ResourceField.excludeSelf Boolean @default(false)

Fichiers : workflow-resource.prisma, workflow-resource-level-state.prisma, resource-field.prisma, relations UserProfileInstance

---

### Le ticket comprend

- 💾 La mise à jour de la structure de BDD
- 🌱 Mise à jour des seeds dev d’exemples
- 🐯🌐 Mise à jour de NestJs & GraphQL
- 🔭 hors scope : maj queries & api front, à passer dans GTA-1659

---

### ✅ Done

- 💾 Prisma : `delegatedFor*` (WRLS) + `lastDelegatedFor*` (WR) — FK nullable, helper, Brin, `onDelete: SetNull` ; inverses UPI ; `ResourceField.excludeSelf` `@default(false)`
- 🐯🌐 GraphQL CRUD miroir (WR / WRLS / UPI inverses `…AsDelegatedForValidator` / `…AsLastDelegatedForValidator` / RF). Helper non writable. Pas de guard écriture `excludeSelf` (GTA-1654)
- 🌱 Seeds 21/22 SO + CMAR + ENFM : acteur Durand/Georges, titulaire Murielle/Pierre-Olivier. Recap : `cronexia-gta-back/.../workflow-resource/new-delegations-examples.md`
- Hors scope inchangé : RF recipe `isDelegation*` + `excludeSelf: true` sur `delegue*` (GTA-1652), acting-as (GTA-1655/1656), `myActiveDelegations` (GTA-1657), queries front (GTA-1659)
