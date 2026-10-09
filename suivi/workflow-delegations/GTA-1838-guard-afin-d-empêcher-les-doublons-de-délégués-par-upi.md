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
