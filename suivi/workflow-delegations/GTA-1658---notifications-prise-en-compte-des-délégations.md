# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🐯🌐🔔 Notifications, prise en compte des délégations

Evolution des notifications afin qu'elles soient également envoyées aux délégués, si la délégation est activée par le UPI de référence.

## Dev

Contrat : délégation effective → fan-out table Notification vers titulaire + délégués. Pas de toasts.

forwarded_to_validator (et autres kinds validateur) : mêmes destinataires délégués si isDelegationEffective au moment de la notif

Copy collab si on affiche « pour Y »

// TODO: Implement later when XXX right is implemented si d'autres canaux (mail, etc.)

---

### ✅ Done

- Fan-out table `Notification` dans `createWorkflowNotification` (`fanOutValidatorNotifications`). Délégation **effective** au moment de la notif → destinataires = UPI titulaire + UPI stockées dans `delegue*` (`resolveEffectiveDelegateReceiverUpiIds`). Sinon titulaire seul. Même message. Pas de toasts
- Kinds validateur : `forwarded_to_validator`, `submitted_to_validator`, `cancelled_to_validator` (templates custom). Type de workflow non géré : skip existant, helper non appelé
- Destinataires délégués = UPI du slot (dédupliquées par `idUser`). Saut : slot vide, soi-même, même resource que le titulaire. Pas toutes les UPI courantes de la personne
- `status_update_to_collaborator` : pas de fan-out. Si `delegatedForUpiId`, `withDelegatedForClause` insère ` par {acteur} pour {titulaire}` avant le premier point
- Expéditeur d'un forward délégué = UPI acteur (`validatorUpiId`). Soumission : expéditeur inchangé (UPI collaborateur)
- `// TODO: Implement later when a mail (or other channel) right is implemented` dans le fan-out. Pas d'autre canal
- Fichiers : `cronexia-gta-back/app/src/notifications/functions/create-workflow-notification.ts`, `workflow-notification-message-templates.ts`, `.../delegation/resolve-effective-delegate-receiver-upi-ids.ts`
- Hors scope inchangé : textes & liens front (GTA-1665), menu (GTA-1660), builders `/api` (GTA-1659)

### Seeds de recette

Après reset dev, une notification validateur sur les demandes Patrick d'octobre 2026 part vers le titulaire et les UPI stockées dans `delegue*` :

- Rang 1 (Manager, Murielle) : Murielle + Maxime Durand (délégué 1) + Patrick (délégué 2)
- Rang 2 (Gestionnaire RH, Pierre-Olivier) : Pierre-Olivier + Maxime Durand (délégué 1) + Georges Malville (délégué 2)

Murielle est toujours active (`isDelegationActive`). Pierre-Olivier l'est seulement parce que son CP (01/01/2026 → 30/06/2027) couvre le jour de la notification.
