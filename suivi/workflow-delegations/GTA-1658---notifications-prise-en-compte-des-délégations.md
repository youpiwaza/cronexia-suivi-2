# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🐯🌐🔔 Notifications, prise en compte des délégations

Evolution des notifications afin qu'elles soient également envoyées aux délégués, si la délégation est activée par le UPI de référence.

## Dev

Contrat : délégation effective → fan-out table Notification vers titulaire + délégués. Pas de toasts.

forwarded_to_validator (et autres kinds validateur) : mêmes destinataires délégués si isDelegationEffective au moment de la notif

Copy collab si on affiche « pour Y »

// TODO: Implement later when XXX right is implemented si d'autres canaux (mail, etc.)
