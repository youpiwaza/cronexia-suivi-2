# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🐯🌐🖊️ Délégué peut valider/refuser les demandes du référent

Un délégué peut valider/refuser au nom du titulaire, avec trace des deux identités.

## Dev

Autoriser comme titulaire ; écrire validator* = UPI JWT ; delegatedFor* = titulaire si acting-as, sinon null

Helper acteur = deriveUserProfileInstanceHelperOrThrow sur l'UPI JWT ; helper titulaire idem sur UPI héritée

Commentaire refus inchangé

Specs markdown validated/refused : sortir « délégués » du hors-périmètre

Commentaire obligatoire dans le guard : // TODO: Later : un délégué hérite des droits d'outrepassement éventuels (délégation d'un Gestionnaire RH) — acting-as UPI HR doit permettre l'override rang 1

---

### ✅ Done

- Gate `resolveWrlsDelegationWrite` (`assertJwtMayActAsUpi` + paire d'écriture). Owner : `validator*` / `lastValidator*` = UPI argument, `delegatedFor*` / `lastDelegatedFor*` null. Délégué : acteur = JWT `supi`, titulaire = UPI argument. `CRO_WR_UPI_000000003` UPI inconnue / `supi` invalide ; `000000004` plus effective ; `000000005` ni propriétaire ni délégué. Dossier `cronexia-gta-back/app/src/user-profile-instances/functions/workflow-resource/functions/delegation/`
- Mutation `userProfileInstanceUpdateWrlsStatusWithCascade` : `@UseGuards(GqlJwtAuthGuard)` uniquement (`RightsGuard` / `API_USER_PROFILE_INSTANCE_VALIDATE_WRLS` encore commenté). Pas d'arg `actingAs` : `userProfileInstance` = UPI d'autorisation (UPI JWT ou UPI courante du titulaire). Guard rangs sur cette UPI. Helpers acteur + titulaire. Même paire sur cascade validated inf. / refused sup. ; refused inf. inchangée (état seul)
- Commentaire refus inchangé. Expéditeur notif = acteur. TODO Later outrepassement RH dans `guard-upi-can-validate-wrls.ts` (acting-as UPI HR doit permettre l'override rang 1)
- Hint FE GTA-1659 / GTA-1661 : pages Délégation passent l'id UPI **titulaire** dans l'argument existant ; étendre la sélection mutation `delegatedFor*` / `lastDelegatedFor*` (`cronexia-gta-front-v2/app/src/lib/graphql/user-profile-instance/mutations/userProfileInstanceUpdateWrlsStatusWithCascade.ts`). `/api/user-profile-instance/update-wrls-status-with-cascade` : pas de nouveau champ body
- Hors scope inchangé : `myActiveDelegations` (GTA-1657), fan-out notifs délégués (GTA-1658), builders `/api` (GTA-1659), menu FE (GTA-1660 / GTA-1661). Manual : regen `schema.gql` au prochain start API (description mutation)
