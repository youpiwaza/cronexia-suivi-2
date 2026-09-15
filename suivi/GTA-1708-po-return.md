# GTA-1708 / Returns to treat from the PO

(in french)

## 1 / Décalage de l'élément survolé au drag and drop — **done**

(Note dev : Je ne reproduis pas le comportement)

Quand on drag depuis la liste des raccourcis ou des liens disponibles, il y a un gros décalage entre la position du curseur de la souris et la partie du menu en train d'être draggée. Cela rend la manipulation compliquée (illustration ci-dessous avec “Calendrier d’absences” qui part beaucoup trop en dessous par rapport au curseur de la souris)

cf. @cronexia-suivi-2\suivi\GTA-1708-po-return---decalage-drag.jpg

---

## 2 / Les raccourcis affichés ne tiennent pas compte des habilitations — **done**

Note: raccourcis = MenuQuickLinks

Par exemple, un salarié à accès aux raccourcis des écrans “compteurs par période” et “compteurs par date”, “vue déclaration” alors qu’ils n’ont pas les droits pour les afficher.

Notes dev :

- Table @cronexia-gta-back\app\prisma\schema\user-right.prisma
- Seeds :  @cronexia-gta-back\app\prisma\seeds-new\01-required\user-right\user-right.seeds.ts

Je ne sais pas si on peut directement réutiliser/implémenter une relation entre les liens du menus et la table de droits, ou si il serait mieux de rajouter une propriété dédiée ?

À traiter en même temps que : "Le lien vers le planning d'équipe est en doublon" :

- On a rapatrié de manière "bête et méchante" les anciens liens en dur, quitte à faire des doublons si le lien était présent dans différents rôles ; mais on devrait plutôt avoir les liens avec une relation [n-m] vers les UserProfile associés ?

---

## 3 / resourceTimeManagementMethod special behavior — **done**

cf. @cronexia-gta-back\app\prisma\seeds-new\50-dev\resource-fields\resource-fields.dev.seed.ts , lines 376 > 391

Les salariés qui ne sont pas soumis aux pointages voient le raccourci “Badger”, ceux qui badgent voient le raccourci “Déclaratif” (ils ne sont pas concernés). Les salariés concernés par le déclaratif voient à la fois le lien vers le déclaratif en jours et celui en heures alors qu’ils ne peuvent être concernés que par l’un des 2. Celui en heures est nommé “Déclarer mes jours” et l’autre “Déclaratif” (mettre Déclarer mes heures).

Note dev : Plutôt que de gérer ce genre de comportements au cas par cas, je serai plutôt d'avis de généraliser en rajoutant un champ dédié de type ENUM, permettant d'avoir une granularité plus fine au niveau du front. ~~specialBehavior:ENUM<none (default)|resourceTimeManagementMethodClockings|resourceTimeManagementMethodDeclaration> ou quelque chose de similaire ?

Cela permettrait également de rajouter de manière assez simple de nouveaux futurs comportements (versatilité)

---

## 4 / Ajustement label bouton — **done**

Au niveau des raccourcis personnalisés, au lieu d’indiquer “Réinitialiser aux défauts du rôle”, juste mettre “Réinitialiser”

---

## 6 / Ajuster les liens vers les pages compteurs — **done**

Le manager a des liens vers compteurs (tout court), compteurs par période et compteurs par date: il faut reprendre le nom des 3 onglets de la page compteurs
