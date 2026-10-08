# 💾 Back / 🌊✔️Workflows / 👉 Délégations / 🐯🌐🛣️ Nouvelle route "mes délégations actives"

Exposer les délégations actives pour l’UPI connecté, ainsi que les traces/logs pour les validations faites par délégations

## Dev

Exposer delegatedForValidator { user { resource { firstName lastName } } } (+ helpers) sur WRLS et WR (lastDelegatedFor*)

Query myActiveDelegations (nom TBD) pour le menu : id UPI titulaire, nom, matricule, photo, rôle — filtrée par isDelegationEffective

Exposer excludeSelf sur le modèle GraphQL ResourceField (dossier + admin fields)

Module déjà UserProfileInstances — pas forcément un nouveau module
