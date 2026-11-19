# Audit de périmètre démo — Qu'est-ce qui est opérationnel..

.. Qu'est-ce qui est inerte / non raccordé, et reste à mettre en place

---

## Global

- Toolbars // TODO
- Menu utilisateur // TODO
- Menus // OK ?
- Filtres // OK

---

## Pages

### Accueil super.admin

- Profil — OK (🔨 édition de la photo encore à brancher)
- Référentiels, workflows, gestion du temps, sécurité et accès, personnalisation — Partiel : 🔨 textes en dur, liens du menu réel

### Accueil admin

Identique à l'accueil super.admin.

### Accueil Gestionnaire RH

- Profil, absents, télétravail, déplacement, anomalies, validation des demandes — OK
- Indicateurs — Partiel : anomalies réelles, 🔨 absentéisme et heures mock
- Reporting — Partiel : 🔨 catalogue en dur, navigation réelle
- Communication — Mock : populations réelles, 🔨 envoi factice

### Accueil Manager

Identique à l'accueil gestionnaire RH, sauf la validation au niveau manager.

### Accueil Collaborateur

- Profil, pointages (badge réel, affiché seulement en pointage réel), demandes, mes droits, planning, calendrier d'absences, emploi du temps — OK
- Compteurs — Partiel : valeurs réelles, 🔨 codes en dur, masqué par défaut
- Liens RH — Partiel : 🔨 URL publiques en dur
- Infos — Mock : 🔨 « marquer comme lu » reste local

Un profil inconnu n'affiche que le widget profil, avec des données réelles.

---

### Absences

- Toutes, jours, heures — OK (listes, création et filtres sur les API d'absences et de population)
- Heures masquées si la population est entièrement gérée en jours (règle produit, pas un trou)

---

### Anomalies

- Liste et corrections (pointages, événements, horaire, suppression) — OK (API instances, population, événements, horaires)

---

### Pointages

- Liste, pagination, recherche, création et modification — OK (API table par période et population)

---

### Planning collectif

- Grille, favoris, saisie (événements, pointages, horaire) — OK
- Contrôle des droits — Mock, bouton visible seulement en mode debug : 🔨 données et actions en dur

---

### Compteurs

- Période, date, ressource — OK (résultats, groupes, calcul et export)

---

### Délégations

- Validation des demandes des titulaires — OK
- 🔨 Dossier, planning, anomalies et droits d'outrepassement : pas encore

---

### Dossier collaborateur

- Fiche, historique, photo et délégations — OK

---

### Planning individuel

- Grille par mois, favoris, saisie (événements, pointages, horaire) — OK
- Contrôle des droits — même mock que le planning collectif, en mode debug : 🔨 données et actions en dur

---

### Populations

- Liste, création, modification, suppression — OK
- Sélecteur de collaborateurs — Partiel : 🔨 liste texte, pas encore le sélecteur normalisé

---

### Gestion des demandes

- Onglets, validation, vues déclaration (jours et heures, lecture seule) — OK

---

### Synthèse

- Grille (anomalies, pointages, événements, compteurs, horaires) et corrections — OK

---

### Suivi des droits

- Individuel et collectif : identité, soldes, mouvements — OK
- Filtres (unité, soldes négatifs, date de calcul, regroupement) — Partiel : 🔨 locaux, pas de recalcul
- Export — 🔨 la modale s'ouvre, rien n'est téléchargé
- Actions groupées — 🔨 Initialiser et Ajuster sans effet ; Reporter et Transférer désactivés

---

### Authentification

- Modes de connexion (mot de passe et SSO) : activation, édition, test — OK (liste fixe, pas de création ni suppression)

---

### Calendriers

- Liste, détail (jours, types, populations), création et suppression — OK

---

### Réaction au conflit

- Mode par profil : lecture et enregistrement — OK

---

### Référentiels

- Liste, valeurs (texte et nombre), création et suppression — OK

---

### Champs

- Gestion et organisation (onglets, ordre) — OK
- Champ organisation — 🔨 type verrouillé, le module organisations n'est pas migré

---

### Widgets d'accueil

- Visibilité et personnalisation par rôle — OK

---

### Législation des droits

- Ordre de décompte, limites, simulation — Mock : 🔨 données en dur, enregistrement local
- Ajouter une population — 🔨 désactivé

---

### Comptes verrouillés

- Liste et déblocage — OK

---

### Liens rapides

- Défauts par rôle — OK

---

### Organisations

- Liste, niveaux, création et suppression — OK

---

### Population

Identique à Populations (même écran, sélecteur encore en liste texte).

---

### Paramétrage d'un droit

- Fiche — Mock : 🔨 fixture, le code d'URL n'est pas lu, pas d'enregistrement
- Nouveau et filtre — 🔨 désactivés
- Report et perte — 🔨 populations cibles encore à définir

---

### Initialisation des droits

- Populations et ressources — OK
- Simulation, exécution, historique, modèles — Mock : 🔨 en local, pas d'API
- Ajustement manuel, report manuel, transfert de solde — 🔨 onglets inactifs

---

### Appareils connectés

- Liste et déconnexion — OK

---

### Onglets de workflow

- Création, modification, ordre et suppression — OK

---

### Calendrier d'absences

- Mois, absences et nouvelle demande — OK
