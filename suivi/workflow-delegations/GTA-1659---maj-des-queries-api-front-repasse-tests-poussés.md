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

📌 Double check de l’ensemble des routes (recup & forms)

📌🔙 Ticket à laisser ouvert en recettage dev afin de pouvoir traiter les éventuels retours de Moez

- Note max: S’il reste du temps soit on skip, soit j’en profite pour passer des tests unitaires
