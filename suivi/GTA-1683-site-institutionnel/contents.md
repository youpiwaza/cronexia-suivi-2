# Contenus site vitrine Cronexia

Textes en français, à coller dans Divi. Cette première partie est interne : ce qu’on peut affirmer, puis le catalogue des fonctionnalités déjà livrées, du plus important au plus secondaire.

## Garde-fous

À ne pas affirmer tel quel sur le site.

- **Paie.** Pas de génération de paie aujourd’hui. Les rapports couvrent les absences et les compteurs (PDF ou Excel). Au présent, dire « contrôler le temps avant la paie ». La génération des paies se parle uniquement au futur, dans le bloc à venir.
- **Logiciels tiers et badgeuses physiques.** Aujourd’hui : import CSV des collaborateurs, API REST et GraphQL, pointage dans l’application. Pas de connecteur nommé (Silae, ADP, Sage, pointeuse physique). L’interfaçage avec les badgeuses et les logiciels tiers se parle uniquement au futur.
- **Droits, RTT, télétravail.** Des écrans existent déjà (Mes droits, génération des droits, soldes CP / RTT / télétravail, absences). Ne pas les présenter comme absents. La promesse « à venir » porte sur la gestion et la génération complètes de ces droits. Au présent, rester sur le suivi et la pose.
- **IA.** La gestion des anomalies est livrée. L’assistant conversationnel (poser une absence, consulter un solde) existe, encore en démo. « Suggestions de résolution » et « aide à la mise en place » sont une promesse : les garder au conditionnel, ou les valider en interne avant de les présenter comme disponibles.
- **Témoignages.** Aucun client nommé dans le produit. Prévoir des logos et des citations réels, ou laisser le bandeau vide le temps d’avoir les accords.

## Catalogue des fonctionnalités livrées

Par ordre d’importance. Les icônes sont des classes Font Awesome, disponibles dans le sélecteur Divi.

### 1. Plannings

- Icône : `fa-calendar-days`
- Titre : Plannings
- Description courte : Planifiez vos équipes au jour le jour, en collectif ou en individuel.
- Description succincte : Planning collectif, planning individuel et planning d’équipe. Horaires, cycles et exceptions restent dans la même grille, avec les compteurs utiles sous les yeux. Chaque profil ne voit que son périmètre.

### 2. Absences et congés

- Icône : `fa-umbrella-beach`
- Titre : Absences et congés
- Description courte : Posez, suivez et validez les absences, des congés payés aux absences exceptionnelles.
- Description succincte : Absences en jours ou en heures, calendrier personnel et consultation des soldes. Le collaborateur suit ses compteurs ; le manager traite les demandes.
- Note : la génération complète des droits (CP, RTT, télétravail) est une évolution. Ce n’est pas le message principal de cette fonctionnalité.

### 3. Pointage

- Icône : `fa-fingerprint`
- Titre : Pointage
- Description courte : Enregistrez les présences en quelques secondes, au bureau ou à distance.
- Description succincte : Badgeuse intégrée et tableau des pointages par période, population ou collaborateur. Les écarts avec l’horaire prévu remontent dans le suivi, sans fichier à part.

### 4. Demandes et validations

- Icône : `fa-diagram-project`
- Titre : Demandes et validations
- Description courte : Des circuits de validation calés sur vos règles.
- Description succincte : Le collaborateur dépose une demande, avec pièce jointe si besoin. Les valideurs travaillent dans une file dédiée : statuts, conflits, plusieurs niveaux. Les onglets de demandes se configurent selon vos processus.

### 5. Compteurs

- Icône : `fa-calculator`
- Titre : Compteurs
- Description courte : Des compteurs configurables pour fiabiliser le suivi du temps.
- Description succincte : Formules paramétrables, résultats par période, par date ou par personne. Les éléments variables se lisent dans l’outil au lieu d’être recalculés à la main.
- Note : la génération des paies viendra s’appuyer sur ces compteurs. Ne pas le présenter comme déjà disponible.

### 6. Anomalies

- Icône : `fa-triangle-exclamation`
- Titre : Anomalies
- Description courte : Les écarts de temps sont visibles et traités avant la clôture.
- Description succincte : Pointage manquant, incohérence de compteur, niveau de criticité. Managers et RH corrigent sur la période, dans le même écran que le reste du suivi.

### 7. Déclaration d’activité

- Icône : `fa-clipboard-check`
- Titre : Déclaration d’activité
- Description courte : Les collaborateurs déclarent leurs jours ou leurs heures, les managers contrôlent.
- Description succincte : Grilles en jours et en heures, vues semaine ou mois. Utile pour les forfaits jours et le suivi d’activité quand tout le monde ne badge pas.

### 8. Synthèse et tableaux de bord

- Icône : `fa-table-columns`
- Titre : Synthèse et tableaux de bord
- Description courte : Une vue unique pour suivre présence, absences, pointages et compteurs.
- Description succincte : Synthèse par collaborateur et par période. L’accueil s’adapte au profil : collaborateur, manager, RH ou administrateur (demandes à valider, absents du jour, soldes, anomalies).

### 9. Rapports

- Icône : `fa-file-lines`
- Titre : Rapports
- Description courte : Produisez vos rapports d’absences et de compteurs, prêts à contrôler ou à transmettre.
- Description succincte : Catalogue (absences en jours, en heures ou les deux, compteurs), options d’édition, favoris et droits d’export. Génération PDF ou Excel, y compris en différé sur les gros volumes.

### 10. Équipes, populations et dossiers

- Icône : `fa-users`
- Titre : Équipes, populations et dossiers
- Description courte : Organisez vos effectifs et limitez chaque écran au bon périmètre.
- Description succincte : Dossier collaborateur, populations (équipe, site, métier) et organisations à plusieurs niveaux. Un manager ne traite que les personnes de son périmètre.

### 11. Personnalisation

- Icône : `fa-sliders`
- Titre : Personnalisation
- Description courte : Rôles, champs, menus et droits se règlent sur votre organisation.
- Description succincte : Profils collaborateur, manager, RH et administrateur. Champs de dossier sur mesure, calendriers et jours spécifiques, politiques de conflits, onglets de workflows, formules de compteurs, raccourcis de menu par rôle.

### 12. Assistant intelligent

- Icône : `fa-robot`
- Titre : Assistant intelligent
- Description courte : Une aide pour les tâches courantes, les anomalies et la prise en main.
- Description succincte : Consulter un solde, poser une absence, retrouver un écran.
- Note : l’assistant est encore en démo. « Repérer une anomalie et proposer une piste de correction » et « accompagner le paramétrage » se publient au conditionnel, tant qu’ils ne sont pas ouverts aux utilisateurs. La détection des anomalies, elle, est déjà livrée (point 6).

### 13. Intégration (REST et GraphQL)

- Icône : `fa-plug`
- Titre : Intégration
- Description courte : Cronexia se connecte à votre système d’information, sans ressaisie.
- Description succincte : API REST pour les dossiers collaborateurs et l’import CSV. API GraphQL pour le métier (planning, absences, compteurs, workflows). Rapports et fichiers passent par les mêmes accès.
- Note : réserver cet encart à un public DSI. Pas dans le hero. Ne pas le confondre avec les connecteurs de badgeuses physiques, qui restent à venir.

## Hors page marketing

Indicateurs graphiques (écran encore vide), sessions et appareils connectés, thème de l’interface.

## Fonctionnalités à venir

À afficher avec un libellé visible, du type « Bientôt » ou « En cours de développement ». Pas dans le hero, pas dans les trois points forts de l’accueil. Emplacement prévu : un bloc en bas de la page Produit, après les fonctionnalités livrées.

### Droits et télétravail

- Icône : `fa-house-laptop`
- Titre : Droits et télétravail
- Description courte : Congés payés, RTT et télétravail seront générés selon vos règles.
- Description succincte : Cronexia prendra en charge la gestion et la génération des droits (congés payés, RTT, etc.) ainsi que du télétravail. Les demandes et les soldes déjà en place s’y rattacheront.

### Génération des paies

- Icône : `fa-file-invoice-dollar`
- Titre : Génération des paies
- Description courte : Les paies seront produites à partir des temps déjà validés.
- Description succincte : Absences, compteurs et éléments variables alimenteront la génération des paies, sans reprise manuelle en fin de mois.

### Badgeuses et logiciels tiers

- Icône : `fa-id-card`
- Titre : Badgeuses et logiciels tiers
- Description courte : Les badgeuses physiques et vos autres logiciels se connecteront à Cronexia.
- Description succincte : L’interfaçage couvrira les pointeuses sur site et, plus largement, les logiciels déjà en place. Le pointage dans l’application et l’import des collaborateurs restent disponibles dès maintenant.

## Page Accueil

Layout Divi (SaaS landing) : hero, trois blurbs, deux ou trois rangées texte et image alternées, témoignages, appel à l’action final.

### Hero

- Titre : La gestion des temps, sans le projet de six mois.
- Accroche : Cronexia est une GTA en SaaS : plannings, pointages, absences et validations, prêts à l’emploi, et ajustables à votre organisation.
- Bouton principal : Demander une démo
- Bouton secondaire : Voir le produit

### Trois points forts

#### Solution SaaS

- Icône : `fa-cloud`
- Titre : En ligne, tout de suite
- Texte : Vos équipes se connectent, les mises à jour suivent. Pas de serveur à maintenir, pas de version qui diverge d’un site à l’autre.

#### Clé en main

- Icône : `fa-rocket`
- Titre : Opérationnel rapidement
- Texte : L’essentiel est déjà là : plannings, absences, pointage, demandes. Vous importez vos collaborateurs, et vos outils pourront s’y connecter.

#### Intelligence artificielle

- Icône : `fa-robot`
- Titre : Une aide au quotidien
- Texte : L’assistant décharge les tâches répétitives, signale les anomalies et propose une piste pour les corriger. Il aide aussi à prendre l’outil en main.
- Note : ce texte va plus loin que ce qui est ouvert aux utilisateurs. Tant que l’assistant reste en démo, publier plutôt : « Les anomalies remontent dans l’outil. Un assistant aide à retrouver un solde, poser une absence ou ouvrir le bon écran. »

### Bloc large, texte à gauche

Illustration : capture du planning collectif.

- Titre : Voyez le temps de toute l’équipe, sur une seule grille
- Texte : Planning collectif, planning individuel, planning d’équipe. Horaires, absences et compteurs restent alignés. Le manager agit sur son périmètre ; le collaborateur consulte le sien.
- Bouton : Découvrir les plannings
- Lien : page Produit

### Bloc large, texte à droite

Illustration : file de demandes ou calendrier d’absences.

- Titre : Les demandes avancent toutes seules jusqu’à la validation
- Texte : Congés, absences, déclarations : le collaborateur dépose, le manager valide, les soldes se mettent à jour. Les circuits suivent vos niveaux, pas un modèle figé.
- Bouton : Voir les demandes et les absences
- Lien : page Produit

### Bloc large optionnel, texte à gauche

Recommandé. C’est le lien avec l’intelligence artificielle, sans entrer dans la technique. Illustration : écran des anomalies ou de la synthèse.

- Titre : Repérez les écarts avant la clôture
- Texte : Pointages manquants, compteurs incohérents, absences en conflit : ils remontent au bon moment, avec le contexte pour corriger. Moins de reprises au moment de clôturer la période.
- Bouton : Voir le pilotage
- Lien : page Produit

### Témoignages

- Titre : Ils pilotent leur temps avec Cronexia
- Note : tant que les citations ne sont pas validées, n’afficher que des logos, ou masquer le bloc. Ne pas inventer de noms.

### Appel à l’action

- Titre : Voyons ensemble ce que Cronexia change pour vos équipes.
- Bouton : Demander une démo

## Page Produit

Layout Divi (SaaS features) : introduction, deux rangées texte et image alternées, colonnes de fonctionnalités, bloc plus technique, bloc « Bientôt », appel à l’action.

### Introduction

- Titre : Une GTA complète, du planning jusqu’au compteur
- Texte : Cronexia couvre le quotidien des collaborateurs, le pilotage des managers et le contrôle des RH. Le socle est prêt. Les rôles, les champs, les circuits et les compteurs se règlent sur votre accord d’entreprise. Droits, paie et badgeuses physiques arrivent ensuite.

### Bloc large, texte à gauche

Illustration : pointage et synthèse.

- Titre : Du pointage au compteur, sans rupture
- Texte : Badgeuse, déclaratif jours ou heures, absences, anomalies et compteurs parlent le même langage. La synthèse d’une personne sur une période tient sur un écran.
- Bouton : Demander une démo

### Bloc large, texte à droite

Illustration : accueil manager ou circuit de validation.

- Titre : Chaque profil a son accueil, et ses droits
- Texte : Collaborateur, manager, RH, administrateur : les menus, les raccourcis et les données visibles changent avec le rôle. Un manager valide les demandes de son équipe. Un RH suit les populations et les rapports.
- Bouton : Parler de votre organisation

### Ce que vos équipes utilisent chaque jour

Six fonctionnalités, en trois colonnes.

- Icône : `fa-calendar-days` — Titre : Plannings — Collectif, individuel et équipe, avec horaires et cycles.
- Icône : `fa-umbrella-beach` — Titre : Absences et congés — Jours ou heures, calendrier et suivi des soldes.
- Icône : `fa-users` — Titre : Équipes — Populations, organisations et dossier collaborateur.
- Icône : `fa-diagram-project` — Titre : Demandes — Dépôt, pièces jointes, validation à plusieurs niveaux.
- Icône : `fa-fingerprint` — Titre : Pointage — Badgeuse et contrôle des présences sur la période.
- Icône : `fa-calculator` — Titre : Compteurs — Formules et résultats par période, par date ou par personne.

### Ce qui rend l’outil durable

Trois colonnes, plus sobres. Reporting, personnalisation et intégration, en langage métier. Ne pas détailler GraphQL dans le hero : une phrase ici suffit. Le détail technique se garde pour une démo ou une page ressources.

- Icône : `fa-file-lines` — Titre : Rapports — Absences et compteurs en PDF ou Excel, avec les droits d’export qui vont avec.
- Icône : `fa-sliders` — Titre : Personnalisation — Champs, calendriers, conflits, workflows et compteurs se paramètrent sans redévelopper l’outil.
- Icône : `fa-plug` — Titre : Ouvert à votre SI — Import CSV des collaborateurs, API REST et API GraphQL pour relier Cronexia à vos applications.

### Bloc optionnel

À ajouter si la maquette a encore de la place. Une rangée de texte : déclaration d’activité et anomalies.

- Titre : Déclarer, contrôler, corriger
- Texte : Forfait jours ou horaires badgés, le déclaratif et les anomalies couvrent les deux. Les écarts se traitent avant d’arriver dans les rapports de fin de période.

### La suite du produit

Trois colonnes, visuellement plus discrètes que les fonctionnalités livrées. Pastille ou sous-titre : « En cours de développement ».

- Icône : `fa-house-laptop` — Titre : Droits et télétravail — Génération des congés payés, des RTT et du télétravail selon vos règles.
- Icône : `fa-file-invoice-dollar` — Titre : Paie — Génération des paies à partir des temps, absences et compteurs déjà validés.
- Icône : `fa-id-card` — Titre : Badgeuses et logiciels tiers — Connexion aux pointeuses physiques et aux logiciels déjà en place.

### Appel à l’action

- Titre : On paramètre Cronexia sur vos règles, pas l’inverse.
- Bouton : Demander une démo
