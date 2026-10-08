# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🐯🌐 Helpers résolution délégations

Savoir si une délégation est active et pour qui, sans encore exposer d'API.

## Dev

isDelegationEffective(titulaireResourceId, now) — formule OU inclusif (BolVal + EventRangeOnResource type Absence)

resolveActiveDelegationsForUser(jwtUserId) → titulaires (UPI + resource + label) seulement si effective

assertUserIsActiveDelegateOf(jwtUserId, titulaireUpiId) — refuse si plus effective (ex. fin d'absence)

Match délégué par user/resource

Interdits : soi-même, pas effective, delegue* vide, transitivité

Fichiers : cronexia-gta-back/app/src/user-profile-instances/functions/workflow-resource/. Helper absence près des queries EventRange existantes.

---

Prend en compte la résolution du comportement du 2eme champ Boolean ~ isDelegationEffective si Référent absent aux dates dateStart <= now <= dateEnd

---

### ✅ Done

- Helpers Prisma / purs, **pas d'API GraphQL**. Dossier `cronexia-gta-back/app/src/user-profile-instances/functions/workflow-resource/functions/delegation/`. Absence : `.../resources/functions/events/times/has-absence-event-range-covering-date.ts`
- Effectif = `isDelegationActive` **ou** (`isDelegationWhenAbsent` **et** `EventRangeOnResource` type Absence, **jour calendaire UTC** `dateStart <= now <= dateEnd`). Half-days ignorés, pas de filtre WR. Latest BolVal `effectDate <= now`
- `resolveActiveDelegationsForUser(jwtUserId, now)` — 1 ligne / resource titulaire, seulement si un `delegue*` courant match (userId ou `user.resourceId`) **et** effective. Interdits : soi-même, `delegue*` vide, transitivité
- Shape (à reprendre GTA-1657 / menu FE) : `{ resourceId, matricule, label, userProfileInstances: [{ idUserProfileInstance, label, userProfileCode, userProfileLabel }] }` — UPIs courantes du titulaire (`effectDateStart/End`, rank asc)
- `assertUserIsActiveDelegateOf` — `CRO_WR_UPI_000000003` UPI inconnue ; `000000004` plus effective (ex. fin d'absence) ; `000000005` pas délégué actif
- Hors scope inchangé : GraphQL `myActiveDelegations` (GTA-1657), acting-as query/mutation (GTA-1655/1656), guard RUPIV `excludeSelf` (GTA-1654), builders front (GTA-1659)
