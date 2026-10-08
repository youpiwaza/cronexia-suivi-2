# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🐯🌐🛡️ Guard écriture ResourceUserProfileInstanceVal

Refuser en base qu'on se désigne soi-même délégué.

## Dev

Create/update ResourceUserProfileInstanceVal : si le RF a excludeSelf === true et l'UPI cible appartient à la même resource que resourceId de la valeur → BadRequestException Cronexia

Indépendant du JWT éditeur (RH qui pose Murielle sur Murielle = refusé pareil)

---

### ✅ Done

- Guard `assertRupivExcludeSelf` : `CRO_RUPIV_000000001` si `ResourceField.excludeSelf` et `UserProfileInstance.user.resourceId` = `resourceId` de la valeur. Match par resource user (toute UPI de la même personne). Pas de JWT éditeur
- Branché sur `ResourceUserProfileInstanceValsService` `create` / `createMany` / `update` (avant le delete same-`effectDate`). Couvre GraphQL + dossier employee-file (nested `create`)
- Branché sur l'API client `UpdateResourceService` cas `UserProfileInstance` (create et update Prisma directs)
- Hint FE GTA-1663 : si le picker est bypassé, l'API renvoie `CRO_RUPIV_000000001`. InputUPI disabled reste l'UX ; ce guard est le filet serveur
- Hors scope inchangé : generate Prisma / seeds, InputUPI (GTA-1663), acting-as (GTA-1655/1656), `myActiveDelegations` (GTA-1657), queries front (GTA-1659)
