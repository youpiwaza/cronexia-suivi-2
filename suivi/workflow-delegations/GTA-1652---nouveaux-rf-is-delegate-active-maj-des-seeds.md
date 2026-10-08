# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🌱 Nouveaux RF ~isDelegateActive & Maj des seeds

Mise à jour des jeux de données de recette (flags, 3 titulaires avec au moins un délégué, cas absence / collab).

Ajout de 2 nouvelles instances de RF afin de pouvoir activer ou non la délégation, par utilisateur

## Dev

isDelegationActive + isDelegationWhenAbsent + CFC + onglet Délégués (ordre : 2 Booleans puis 3 pickers) + locks

excludeSelf: true sur delegue1/2/3

Au moins un delegue* sur Maxime Manager, Murielle Manager, Pierre-Olivier Courtois Gestionnaire RH (Maxime Manager = trou à combler ; pas d'inventaire des .seed.ts)

BolVal (matrices S1–S4) + RUPIV délégué EMPLOYEE (S5) + au moins un Event absence recette

Scénarios 21/22 : traces FK déjà seedées (GTA-1651). Ce ticket = flags RF + délégués effectifs pour que l’API acting-as puisse les utiliser.

Fichiers : resource-fields.dev.seed.ts (+ demo), CFC, tabs, field-lock-overrides.ts, habilitation RUPIV (traces WR 21/22 déjà en GTA-1651)

---

### ✅ Done

- 🌱 RF `isDelegationActive` / `isDelegationWhenAbsent` (historisés, `isCustom` false) + CFC + onglet Délégués (pos. 1–2 Boolean XS, pickers `delegue*` en 3–5) — dev, demo, demo-arte. `excludeSelf: true` sur `delegue1/2/3`. Locks back `field-lock-overrides.ts` + miroir front `FIELD_OVERRIDES`
- 🌱 Resource `f5bf_Maxime_Durand` liée à `maxime.durand` (MANAGER seul). RUPIV `a146`–`a149` : manager / hr / `delegue1` Durand, `delegue2` Murielle = Patrick EMPLOYEE. BolVal S1 / S2 / S4 (`effectDate` 2023-12-01). CP Pierre-Olivier `2026-01-01` → `2027-06-30` sans `EventRangeByDay` (S3 = même fiche une fois hors plage)
- 📝 Recap : `user-roles.md` + `new-delegations-examples.md` (21/22 effectifs via S1 / S2)
- Hors scope inchangé : generate Prisma / reseed manuel, guard écriture `excludeSelf` (GTA-1654), acting-as (GTA-1655/1656), `myActiveDelegations` (GTA-1657), queries front (GTA-1659), UX InputUPI (GTA-1663). Helper effectif livré en GTA-1653.
