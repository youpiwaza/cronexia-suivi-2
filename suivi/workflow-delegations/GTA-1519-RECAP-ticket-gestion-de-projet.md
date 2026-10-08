# 🧠🌊✔️ Workflows / RECAP / 👉 Délégations

Workflows context: cronexia-suivi-2\suivi\________________workflow-context.md

---

🎯🥇 Les délégués sont à passer avant les outrepassements https://cronexia.atlassian.net/browse/GTA-1520

---

~~❔ GTA-1456 Est-ce que ça correspond bien aux délégués ou il s'agit d'autre chose ?~~

~~🔙👪 PO: Je suis gestionnaire, personne n'a encore validé > je doit pouvoir passer outre~~

~~MEME SI je ne fait pas partie du workflow~~

~~Il s'agit d'un droit spécifique (~auth ?)~~

~~PO: ~super délégué / délégué de tout le monde~~

//

~~C'EST BIEN AUTRE CHOSE QUE LES DELEGUES~~

~les délégués

Doivent être désignés

Sont scopés par rapport aux personnes qu'elles délèguent

(plus restreint)

---

## 🧠 Points clés

Permettre à un autre utilisateur de valider les demandes en son nom, lui transférant ainsi ses propres droits (ex: Un manager délègue à sa secrétaire la possibilité de valider/refuser les demandes)

Un utilisateur peut avoir jusqu'à 3 délégués, configurables depuis le dossier resource

La délégation peut être activée ou non, configurables depuis le dossier resource

---

Premier jet GDP & découpage 2eme jet

Ce document contient beaucoup plus de détails techniques, afin de ne pas encombrer ce ticket RECAP

cf. ./260819-workflow-delegations.md

---

## Dev

### 🎯 Priorisation rapide

- Passer tout le back (garder en recettage dev, le temps de voir si des ajustements sont nécessaires)
  - Respecter l’ordre des tickets Frontend
  - Possibilité de passer les pages admins avant la page générale

### 💾 Backend  // ⏱️ 3,5 j

Persister qui a vraiment agi vs pour qui, et empêcher de se choisir soi-même comme délégué au niveau champ.

https://cronexia.atlassian.net/browse/GTA-1651   // ⏱️ 0,5 j

Mise à jour des jeux de données de recette & Ajout de 2 nouvelles instances de RF afin de pouvoir activer ou non la délégation, par utilisateur

https://cronexia.atlassian.net/browse/GTA-1652     // ⏱️ 0,5 j

Savoir si une délégation est active et pour qui, sans encore exposer d'API.

https://cronexia.atlassian.net/browse/GTA-1653   // ⏱️ 0,35 j

Refuser en base qu'on se désigne soi-même délégué.

https://cronexia.atlassian.net/browse/GTA-1654   // ⏱️ 0,15 j

Un délégué voit la même file de demandes que le titulaire.

https://cronexia.atlassian.net/browse/GTA-1655   // ⏱️ 0,25 j

Un délégué peut valider/refuser au nom du titulaire, avec trace des deux identités.

https://cronexia.atlassian.net/browse/GTA-1656     // ⏱️ 0,5 j

Exposer les délégations actives pour l’UPI connecté, ainsi que les traces/logs pour les validations faites par délégations

https://cronexia.atlassian.net/browse/GTA-1657     // ⏱️ 0,25 j

Evolution des notifications afin qu'elles soient également envoyées aux délégués, si la délégation est activée par le UPI de référence.

https://cronexia.atlassian.net/browse/GTA-1658    // ⏱️ 0,25 j

🎨🌐 Maj des queries & api/ front (repasse & tests poussés)

https://cronexia.atlassian.net/browse/GTA-1659     // ⏱️ 0,75 j

---

### 🎨 Frontend // ⏱️ 3,75 j + 0,5 j maxime

Nouveau menu dynamique pour les délégués, afin de leur donner accès aux pages concernées

https://cronexia.atlassian.net/browse/GTA-1660      // ⏱️ 0,5 j

🔗 Passer les deux tickets ensemble

Page dynamique pour les délégations, réutilisant les composants Workflows.

https://cronexia.atlassian.net/browse/GTA-1661      // ⏱️ 1,25 j

🔗 Passer les deux tickets ensemble

Mise à jour des détails des demandes (dans les accordéons)

https://cronexia.atlassian.net/browse/GTA-1662     // ⏱️ 1,5 j

🔔 Ajustements Notifications > textes & liens pour délégués

https://cronexia.atlassian.net/browse/GTA-1665    // ⏱️ 0,1 j

Dossier resource : vérification du bon fonctionnement des 2 nouveaux switchs & nouvelle prop RF.excludeSelf

MAXIME https://cronexia.atlassian.net/browse/GTA-1663    // ⏱️ 0,5 j

Mise à jour & contrôle des composants Workflows réutilisés dans les Widgets & le Chatbot AI

https://cronexia.atlassian.net/browse/GTA-1664     // ⏱️ XXX j

