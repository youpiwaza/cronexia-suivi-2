# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🛡️⚔️ Guard afin d'empêcher les doublons de délégués par UPI

## Dev

🛡️⚔️ On a pensé à mettre un guard afin qu'une personne ne puisse pas se désigner elle-même comme délégué

MAIS on a pas pensé à ce qu'une personne ne puisse pas attribuer plusieurs fois la même personne en délégué

- ~ex:
- Gestionnaire RH PO
  - Délégué 1 : isabelle petit
  - Délégué 2 : isabelle petit
  - Délégué 3 : isabelle petit

Ce qui entraînerai des problèmes, notamment au niveau de la gestion des notifications

À implémenter, attention à la gestion propre des erreurs (cronexia dictionnary)

---

### ✅ Done

- Guard `assertRupivNoDuplicateDelegate` : `CRO_RUPIV_000000002` (« Cette personne est déjà désignée comme délégué. ») si la personne écrite est déjà sur un autre slot `delegue1` / `delegue2` / `delegue3` de la même resource, à la date d'effet (dernière valeur `effectDate <=` date écrite). Match par `idUser` (deux UPI de la même personne). Sans `idUser`, repli sur la même UPI. Champs hors `delegue*` ignorés. Pas de JWT éditeur
- `createMany` : les lignes déjà acceptées du même payload comptent (Isabelle sur délégué 1 puis 2 dans le même appel = refusé)
- Mêmes branchements que GTA-1654 : `ResourceUserProfileInstanceValsService` `create` / `createMany` / `update` ; nested `create` resource (dossier) ; API client `UpdateResourceService` cas `UserProfileInstance` (create et update Prisma directs), avant l'écriture
- Hors scope inchangé : InputUPI (GTA-1663), `excludeSelf` (GTA-1654, code `CRO_RUPIV_000000001` inchangé)
