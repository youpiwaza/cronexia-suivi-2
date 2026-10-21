# Audit d'avancement — Absences en droit

21 octobre 2026. Statuts à reporter dans la colonne « Géré » du récap fonctionnel.

## Grille

- **Géré** : le comportement tourne, pas seulement le champ en base.
- **Géré partiellement** : le champ, le CRUD ou les seeds existent, mais le moteur est incomplet ou ne couvre qu'un cas.
- **Non implémenté** : pas de champ, ou aucun traitement.

## Constat moteur

La génération ne crée que les mouvements d'acquisition « en cours » (`addInProgress`), et seulement pour un droit géré par exercice dont la valeur d'acquisition est une constante, pour les ressources des populations cibles. Chaque date reçoit cette valeur telle quelle (montant par période, 2,5 ou 3 dans les seeds).

Les droits non gérés par exercice et l'évaluation des compteurs sont encore des TODO : rien n'est produit. Les soldes ne sont pas recalculés. Les 18 natures de mouvement existent dans le référentiel. L'exemple 1 (années n-1, n, n+1) est chargé en données statiques, il n'est pas produit par le moteur.

## 1. Objet et vocabulaire

### 1.1 Vocabulaire

| Terme | Statut | Commentaire |
| --- | --- | --- |
| Droit | Géré partiellement | Paramétrage et versions en place. Acquisition, consommation, report et perte ne sont pas enchaînés. |
| Event | Géré partiellement | Plusieurs droits peuvent pointer le même event. Pas de décompte à la pose. |
| Ressource | Géré | Mouvements et soldes rattachés à la ressource, donc à son matricule. |
| Population | Géré partiellement | L'éligibilité filtre la génération, seulement pour un droit géré par exercice et une valeur constante. |
| Exercice | Géré partiellement | Une période d'acquisition et une période de prise par version. Le cas « non géré par exercice » n'est pas généré. |
| En cours | Géré partiellement | Seul montant produit par la génération. |
| Acquis | Géré partiellement | Colonne et seeds d'exemple. Pas produits par la génération. Pas de bascule quand acquisition et prise coïncident. |
| Report | Géré partiellement | Délai, plafond et automatique stockés, plus les seeds d'exemple. Pas de bascule. |
| Perdus / payés | Géré partiellement | Natures au référentiel et dans les seeds. Pas de colonne dédiée, pas de neutralisation calculée. |
| Compteur | Géré partiellement | Liens prévus (acquisition, plafond de report, minoration, majoration, contrôle). Aucun n'est évalué. |
| Mouvement | Géré partiellement | Ligne de trace en place. Seul l'ajout d'en cours est produit. Les autres natures sont au référentiel et dans les seeds. |

## 2. Le besoin : principes généraux

### 2.1 Populations et volumes

| Réf. | Statut | Commentaire |
| --- | --- | --- |
| PG-01 | Géré partiellement | Filtre par population à la génération, seulement si le droit est géré par exercice et la valeur est une constante. |
| PG-09 | Géré partiellement | Plusieurs droits peuvent pointer le même event (`ArPriority`), avec des populations par version. Pas de résolution à la pose. |
| PG-13 | Géré partiellement | Jours ou heures stocké. La génération ne distingue pas l'unité. |
| PG-14 | Géré partiellement | Constante écrite telle quelle sur chaque date (2,5 ou 3 dans les seeds). Compteur non évalué. |

### 2.2 Acquisition et exercices

| Réf. | Statut | Commentaire |
| --- | --- | --- |
| PG-02 | Géré partiellement | Dates relatives stockées. La génération lit les dates concrètes de l'exercice. Le cas sans exercice n'est pas généré. |
| PG-04 | Géré partiellement | Un exercice par version. Seeds n-1, n, n+1. Pas de cycle de vie entre exercices. |
| PG-10 | Géré partiellement | Politique d'anticipation stockée, non appliquée à la pose. |
| PG-11 | Géré partiellement | Lien vers un compteur de minoration stocké, non évalué. Pas de lien aux absences minorantes. |
| PG-12 | Non implémenté | Même montant pour chaque ressource de la population, sans entrée, sortie ni taux. |
| PG-19 | Géré partiellement | Remise à zéro à la sortie stockée en booléen. Aucun mouvement généré. |

### 2.3 Prise et contrôles

| Réf. | Statut | Commentaire |
| --- | --- | --- |
| PG-03 | Géré partiellement | Dates de prise stockées (relatives et dates d'exercice), non contrôlées à la pose. |
| PG-05 | Non implémenté | Pas de moteur de prise, donc pas d'ordre entre exercices. |
| PG-07 | Géré partiellement | Jonction droit / event en place, CRUD de test. Pas de décompte. |
| PG-08 | Géré partiellement | Priorité entière, unique par event. Non consommée à la prise. |
| PG-15 | Géré partiellement | Délai de consommation stocké sur la population cible. Génération hors exercice absente. |
| PG-22 | Non implémenté | Pas de paramètre de plafond de prises sur une période. |
| PG-23 | Non implémenté | Pas de paramètre de jours consécutifs maximum. |

### 2.4 Report et perte

| Réf. | Statut | Commentaire |
| --- | --- | --- |
| PG-06 | Géré partiellement | Délai, plafond et report automatique stockés. Natures et seeds d'exemple. Pas de bascule. |
| PG-21 | Non implémenté | Pas d'alerte avant perte. |

### 2.5 Ajustements et transferts

| Réf. | Statut | Commentaire |
| --- | --- | --- |
| PG-16 | Géré partiellement | Natures d'ajustement manuel et saisie d'instance en page de test. Soldes non recalculés. Classé en deuxième temps dans le récap. |
| PG-17 | Géré partiellement | Population autorisée et plafond stockés. Pas d'exécution. Écran prévu plus tard dans le récap. |

### 2.6 Soldes et restitution

| Réf. | Statut | Commentaire |
| --- | --- | --- |
| PG-18 | Géré partiellement | Modèle de solde et seeds de l'exemple 1. Pas de calcul à date ni prévisionnel. |
| PG-20 | Non implémenté | Pas de restitution des valeurs du droit dans des compteurs. |

## 3. Paramétrage d'un droit

### 3.1 Identification

| Paramètre | Statut | Commentaire |
| --- | --- | --- |
| Code du droit | Géré | Stocké, unique, éditable en CRUD de test. |
| Libellé court | Géré | |
| Libellé long | Géré | |
| Verrou une fois les droits calculés | Géré partiellement | Le flag est affiché en lecture seule et l'info-bulle annonce un verrouillage. Le formulaire d'édition ne bloque pas les champs. Pas de bouton de forçage, ni de suppression des calculs, ni de régénération. |

### 3.2 Gestion, population et acquisition

| Paramètre | Statut | Commentaire |
| --- | --- | --- |
| Mode de gestion | Géré partiellement | Jours ou heures stocké. Le calcul ne distingue pas l'unité. |
| Population cible | Géré | Plusieurs populations par version. La génération s'appuie dessus. |
| Remise à zéro à la sortie de la population cible | Géré partiellement | Booléen stocké. Aucun mouvement de remise à zéro. |
| Valeur d'acquisition | Géré partiellement | Constante écrite telle quelle sur chaque date. Compteur chargé mais non évalué. |
| Périodicité d'acquisition | Géré | Les dates périodiques sont produites quand la valeur est une constante. Sans périodicité, la génération s'arrête. |
| Event associé | Géré partiellement | Priorités stockées sur le droit, pas sur la version. Pas de décompte à la pose. |

### 3.3 Exercice et dates

| Paramètre | Statut | Commentaire |
| --- | --- | --- |
| Droit géré par un exercice | Géré partiellement | Génération seulement si oui. Le cas non est un TODO. |
| Date de début d'acquisition | Géré partiellement | Date relative stockée. La génération lit la date concrète de l'exercice. |
| Date de fin d'acquisition | Géré partiellement | Date relative stockée. La génération lit la date concrète de l'exercice. |
| Date de début de prise | Géré partiellement | Stockée, non contrôlée à la pose. |
| Date de fin de prise | Géré partiellement | Stockée, non contrôlée à la pose. |
| Anticipation des droits en cours cumulés à la date du jour | Géré partiellement | Une des trois valeurs de l'enum. Non appliquée à la pose. |
| Anticipation des droits en cours non encore cumulés | Géré partiellement | Même enum. Non appliquée à la pose. |
| Date d'ouverture du droit | Géré partiellement | Champ stocké, inutilisé. |
| Délai de prise à compter de la date d'acquisition | Géré partiellement | Stocké sur la population cible, pour les droits hors exercice. Cette génération n'existe pas. |

### 3.4 Prise et contrôles

| Paramètre | Statut | Commentaire |
| --- | --- | --- |
| Vérification de l'appartenance à la population cible à la date de prise | Non implémenté | Aucun champ. Écart avec le récap d'octobre 2026. |
| Solde minimum autorisé | Géré partiellement | Un nombre par population cible. Pas de contrôle à la pose. Pas de second seuil collaborateur / gestionnaire. |
| Population autorisée pour transfert de solde | Géré partiellement | Population et plafond (constante ou compteur) stockés. Pas d'écran ni d'exécution. Le récap reporte l'écran. |

### 3.5 Report

| Paramètre | Statut | Commentaire |
| --- | --- | --- |
| Délai de report | Géré partiellement | Stocké par population. Pas de bascule en fin de prise. |
| Plafond de report | Géré partiellement | Constante ou compteur stockés. Non appliqués. |
| Report automatique | Géré partiellement | Booléen stocké. La surcharge manuelle du délai et du plafond, sans modifier le droit, n'est pas modélisée. Le récap la renvoie à un descriptif séparé. |

### 3.6 Compteurs et ajustements manuels

| Paramètre | Statut | Commentaire |
| --- | --- | --- |
| Compteur de minoration / prorata | Géré partiellement | Lien stocké, non évalué. |
| Compteur de majoration | Géré partiellement | Lien stocké, non évalué. |
| Compteur de contrôle des prises | Géré partiellement | Lien stocké, non évalué. Seul emplacement possible pour les plafonds PG-22 et PG-23, encore inerte. |
| Ajustement manuel des droits en cours | Géré partiellement | Nature de mouvement et saisie en page de test. Soldes non recalculés. Marqué en deuxième temps. |
| Ajustement manuel des droits acquis | Géré partiellement | Nature de mouvement et saisie en page de test. Soldes non recalculés. Marqué en deuxième temps. |
| Ajustement manuel de report | Géré partiellement | Nature de mouvement et saisie en page de test. Soldes non recalculés. Marqué en deuxième temps. |

## 4. Règles de gestion

### 4.1 Cycle de vie et ordre de décompte

| Règle | Statut | Commentaire |
| --- | --- | --- |
| Périodes d'acquisition et de prise identiques : uniquement des acquis | Non implémenté | Quand la génération produit des lignes, ce sont des « en cours ». Jamais uniquement des acquis. |
| Décompte : report, puis acquis, puis en cours si anticipation | Non implémenté | Pas de moteur de prise. |
| Fin de report : reliquat perdu ou payé | Non implémenté | Les natures existent, elles ne sont pas produites. |
| Sans report : reliquat perdu ou payé en fin de prise | Non implémenté | Les natures existent, elles ne sont pas produites. |
| Tracer tous les mouvements | Géré partiellement | Seul l'ajout d'en cours est produit. Les autres natures sont dans le référentiel et les seeds. |

### 4.2 Validation d'une pose

| Règle | Statut | Commentaire |
| --- | --- | --- |
| Contrôle à la pose (date retenue, prises jusqu'à la fin d'exercice, solde minimum, existence du droit, profil, période de prise) | Non implémenté | Pas de lien avec la pose d'un event. Les trois exemples (CP période légale, CP année civile, RTT) ont le même statut. |

### 4.3 Historisation et calcul des soldes

| Règle | Statut | Commentaire |
| --- | --- | --- |
| Une seule ligne par date d'effet et code droit | Non implémenté | Pas de contrainte d'unicité. Plusieurs natures le même jour, y compris dans les seeds. À clarifier avec le métier. |
| Solde à date et solde prévisionnel | Géré partiellement | Dates d'effet, de création, de mise à jour et de dernier calcul présentes. Pas de lecture « dernière ligne inférieure ou égale à la date ». |
| Valider la pose sur le solde prévisionnel | Non implémenté | Pas de contrôle de pose. |
| Provision sur l'exercice suivant, puis transformation à l'ouverture | Géré partiellement | Nature de mouvement et cumul de provision en base. Pas de transformation à l'ouverture de l'exercice suivant. |

## 5. Données à gérer par ressource

### 5.1 Informations d'un mouvement

| Champ | Statut | Commentaire |
| --- | --- | --- |
| Matricule | Géré | Lien vers la ressource. |
| Date de création / Date de mise à jour | Géré partiellement | Renseignées automatiquement à l'enregistrement. Les dates du fichier d'exemple ne sont pas rejouées. |
| Code droit | Géré partiellement | Porté par la version, pas recopié sur la ligne. |
| Date d'effet du mouvement | Géré | |
| Date d'expiration du droit | Non implémenté | |
| Nature du mouvement | Géré | Lien vers le référentiel des natures. |
| Référence de l'exercice | Géré | Lien exercice et libellé d'aide. Nulle si le droit n'a pas d'exercice. |
| Référence instance event | Non implémenté | Pas de lien vers l'absence en jours ou en heures. |
| Date de fin de validité du droit | Non implémenté | |
| Droits en cours | Géré | Produit par la génération et par les seeds. |
| Droits acquis | Géré partiellement | Colonne présente. Seeds et CRUD, pas la génération. |
| Droits reports | Géré partiellement | Colonne présente. Seeds et CRUD, pas la génération. |
| Droits perdus / payés | Géré partiellement | Pas de colonne dédiée. Les seeds replient ce montant dans les trois colonnes de montant. |
| Pris sur en cours | Géré partiellement | Pas de colonne dédiée. Les seeds le portent en montant négatif sur les droits en cours. |
| Pris sur acquis | Géré partiellement | Pas de colonne dédiée. Les seeds le portent en montant négatif sur les acquis. |
| Pris sur report | Géré partiellement | Pas de colonne dédiée. Les seeds le portent en montant négatif sur le report. |

### 5.2 Cumuls et soldes sur l'exercice

Tous les champs existent sur le solde par ressource. Ils sont remplis par les seeds de l'exemple 1, jamais recalculés.

| Champ | Statut | Commentaire |
| --- | --- | --- |
| Cumul droits report sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Cumul droits report perdus / payés sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Cumul pris report sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Cumul droits acquis sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Cumul droits acquis perdus / payés sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Cumul pris acquis sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Cumul en cours sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Cumul pris en cours sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Cumul provision en cours sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Solde report sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Solde acquis sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |
| Solde en cours sur l'exercice | Géré partiellement | Seed de l'exemple 1, jamais recalculé. |

### 5.3 Liste des natures de mouvement

| N° | Nature | Statut | Commentaire |
| --- | --- | --- | --- |
| 1 | Ajout d'en cours | Géré | Produit par la génération. |
| 2 | Prise d'en cours sur exercice courant | Géré partiellement | Référentiel et lignes de l'exemple 1. Pas produite par le moteur. |
| 3 | Prise d'en cours sur exercice suivant | Géré partiellement | Référentiel et lignes de l'exemple 1. Pas produite par le moteur. |
| 4 | Transfert en cours vers acquis | Géré partiellement | Référentiel et lignes de l'exemple 1. Chargée à la génération, puis non écrite. |
| 5 | Prise d'acquis | Géré partiellement | Référentiel et lignes de l'exemple 1. |
| 6 | Perte d'acquis | Géré partiellement | Référentiel et lignes de l'exemple 1. Pas produite par le moteur. |
| 7 | Paiement d'acquis | Géré partiellement | Référentiel seul. |
| 8 | Transfert acquis vers report | Géré partiellement | Référentiel et lignes de l'exemple 1. |
| 9 | Prise de report | Géré partiellement | Référentiel et lignes de l'exemple 1. Pas produite par le moteur. |
| 10 | Perte de report | Géré partiellement | Référentiel et lignes de l'exemple 1. Pas produite par le moteur. |
| 11 | Paiement de report | Géré partiellement | Référentiel seul. |
| 12 | Ajustement manuel d'en cours | Géré partiellement | Référentiel et saisie en page de test. Deuxième temps dans le récap. |
| 13 | Ajustement manuel d'acquis | Géré partiellement | Référentiel et saisie en page de test. Deuxième temps dans le récap. |
| 14 | Ajustement manuel de report | Géré partiellement | Référentiel et saisie en page de test. Deuxième temps dans le récap. |

Le référentiel contient aussi quatre natures absentes du récap : bascule automatique en cours vers acquis, acquis vers report, acquis vers perte, acquis vers paiement. Elles ne sont pas produites par le moteur.

## 6. Ce que les informations doivent permettre de faire

| N° | Attendu | Statut | Commentaire |
| --- | --- | --- | --- |
| 1 | Soldes à une date, y compris prévisionnel | Géré partiellement | Données et seeds présents. Pas de lecture à une date donnée. |
| 2 | Expliquer la valeur des soldes | Géré partiellement | Les lignes de mouvement sont consultables en page de test. Pas d'explication calculée. |
| 3 | Bascule en cours vers acquis | Non implémenté | Nature chargée à la génération, puis non écrite. |
| 4 | Bascule acquis vers report, si report automatique | Non implémenté | |
| 5 | Bascule acquis vers perdu ou payé | Non implémenté | |
| 6 | Distinguer les droits par exercice | Géré partiellement | Lien exercice sur les mouvements et les soldes. Pas de cycle de vie entre exercices. |
| 7 | Rejeter une prise sans droit ou à solde insuffisant, selon le profil | Non implémenté | |
| 8 | Vérifier que la pose est dans la période de prise de l'exercice | Non implémenté | |

## Écarts avec le récap d'octobre 2026

- La vérification d'appartenance à la population cible à la date de prise n'a pas de champ.
- La règle « une seule ligne par date d'effet et code droit » est incompatible avec plusieurs natures le même jour, y compris dans les seeds d'exemple.
- Le mouvement n'a ni date d'expiration, ni date de fin de validité, ni lien vers l'instance d'event.
- Les montants perdus ou payés, et les pris sur en cours, acquis et report, ne sont pas des colonnes séparées.
- PG-22 et PG-23 n'ont pas de paramètre. Le compteur de contrôle des prises est le seul emplacement possible, et il n'est pas évalué.
- `RelativePeriod` n'est pas utilisé par les absences en droit. Les délais passent par `Period`. Les `RelativeDate` sont stockées et ne sont pas résolues à la génération.
- Quatre natures « bascule automatique » existent en plus des 14 du récap. Elles ne sont pas produites.
- Le plafond de transfert est en base. Il n'apparaît pas dans le tableau 3.4 du récap.
