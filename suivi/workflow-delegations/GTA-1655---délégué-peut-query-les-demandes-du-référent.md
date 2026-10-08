# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🐯🌐🔍 Délégué peut query les demandes du référent

Un délégué voit la même file de demandes que le titulaire.

## Dev

userProfileInstanceGetWorkflowResource : si actingAs (ou UPI args = titulaire) + JWT délégué actif → réutiliser la résolution RUPIV du titulaire (ne pas inventer un 2e algorithme)

JWT obligatoire : l'appelant possède l'UPI ou est délégué actif

Réponse : WR identiques au titulaire (rangs, includeLowerValidationLevels, badges)

Champs virtuels resourceCurrentValidator* restent le titulaire attendu (RUPIV demandeur), pas le délégué

---

### ✅ Done

- Gate `assertJwtMayActAsUpi` : owner si JWT possède l'UPI (sans `assertUserIsActiveDelegateOf`) ; sinon délégué actif. `CRO_WR_UPI_000000003` UPI inconnue ; `000000004` plus effective ; `000000005` ni propriétaire ni délégué. Dossier `cronexia-gta-back/app/src/user-profile-instances/functions/workflow-resource/functions/delegation/`
- Query `userProfileInstanceGetWorkflowResource` : `@UseGuards(GqlJwtAuthGuard)` uniquement (`RightsGuard` / `API_USER_PROFILE_INSTANCE_VALIDATOR_READ` encore commenté). Pas d'arg `actingAs` : `userProfileInstance` = file listée (UPI JWT ou UPI courante du titulaire). Listing / rangs / badges inchangés
- `resourceCurrentValidator*` reste le validateur attendu (RUPIV demandeur), pas le délégué JWT
- Hint FE GTA-1659 / GTA-1661 : pages Délégation passent l'id UPI **titulaire** dans l'argument existant (`cronexia-gta-front-v2/app/src/lib/graphql/user-profile-instance/queries/userProfileInstanceGetWorkflowResource.ts`)
- Hors scope inchangé : mutation / traces `delegatedFor*` (GTA-1656), `myActiveDelegations` (GTA-1657), builders `/api` (GTA-1659), menu FE (GTA-1660 / GTA-1661). Manual : regen `schema.gql` au prochain start API (description query)
