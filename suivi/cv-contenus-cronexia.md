## Cronexia / Lead développeur web full stack

CDI, depuis décembre 2023 jusqu’à présent.

Prise en charge, depuis décembre 2023, de la conception et du développement d’un logiciel de gestion des temps et des activités, de l’expression du besoin jusqu’à la mise en production. Le périmètre couvre le paramétrage et l’évolution continue des règles de gestion : dossiers des collaborateurs, plannings, absences et circuits de validation, au plus près des usages métier.

### Missions

- **Ressources et rôles.** Mise en place du dossier collaborateur à informations configurables : texte, dates, nombres, listes, heures, liens entre personnes, cycles, badges et organisations. Plusieurs structures coexistent (juridique, géographique), chacune avec ses niveaux ; les rôles rattachés aux personnes (manager, ressources humaines) déterminent les droits d’accès et les valideurs.

- **Emplois du temps et calendriers.** Conception des plannings individuel et d’équipe. Des calendriers de référence portent les jours particuliers et les spécificités locales, et s’appliquent à des groupes de personnes, indépendamment de l’affichage du planning de chaque collaborateur.

- **Cycles et horaires.** Définition d’horaires types — début et fin de journée, pointages attendus, durées du matin, de l’après-midi et de la journée — enchaînés dans des cycles. Une personne peut se voir appliquer un autre horaire sur une période donnée.

- **Événements.** Catalogue d’événements de présence, d’absence ou neutres (congés, maladie, télétravail, astreinte, déplacement), saisis en journée, en demi-journée, en durée ou sur une plage horaire, à la main ou par génération. Le décompte suit les jours ouvrés, ouvrables ou calendaires, ou un compteur.

- **Flux de validation.** Circuits de demande à plusieurs niveaux, selon les populations concernées : congé sur une période, changement d’horaire, correction de pointage, déclaration de présence ou d’heures. Le paramétrage inclut les pièces jointes, les délais avant la date d’effet et la délégation.

- **Absences en droits.** Paramétrage d’un droit : exercice, acquisition, prise, report, perte et populations concernées. Un même congé peut puiser dans plusieurs droits selon un ordre (ancienneté, puis congés payés), avec suivi des soldes, des calculs et des ajustements.

- **Assistant conversationnel.** Assistant en langage courant, dans le périmètre autorisé de l’utilisateur : poser, consulter, modifier ou annuler une absence, lire un solde, suivre ou décider une demande, ouvrir un écran de l’application.

- **Pilotage.** Animation de l’équipe de développement, arbitrages techniques, livraison et exploitation (conteneurs, mises à jour, environnement en ligne).

### Technologies

TypeScript, NestJS, GraphQL, PostgreSQL, Prisma, Svelte / SvelteKit, Docker. Redis et files d’attente pour les traitements longs (génération, exports). Tests automatisés. Authentification et SSO.
