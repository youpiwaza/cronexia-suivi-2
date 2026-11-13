# Gestion des impacts de l'état des AGGREGATS (uniquement) d'Events sur les compteurs

## Métier

A l'heure actuelle l'impact de l'état des events sur différents points fonctionnels n'est gérée que partiellement. Or, un event à l'état "Validé" ne doit bien sûr pas avoir les mêmes conséquences métiers qu'un event à l'état "Refusé": ignorer l'état revient peu ou prou à éliminer tout intérêt à la notion de workflow de validation.

Ce qu'il convient de faire:

- Traiter les events à l'état "Annulé" "Brouillon" et "Refusé" comme devant être ignorés (comme s'ils n'existaient pas). C'est à dire que les events associés à cet état ne doivent avoir aucun impact sur
  - Les calculs de compteurs qui s'appuient sur des events (sachant que le mode de fonctionnement le plus souple et le plus optimal serait en réalité de pouvoir choisir dans les formules de compteurs les états des events à prendre en compte et ceux qui doivent être ignorés: @Maxime Chevasson  si tu penses que c'est faisable sans monter une usine à gaz, prévoir un ticket dédié). KO actuellement

## Dev

- 🧹 Note max : En profiter pour découper le fichier prisma des compteurs > chaque table à son fichier
- Jouable dans CtParam, rajout d'une relation n-m vers une nouvelle table qui comporterait les valeurs d'ENUMs à associer (afin de pouvoir choisir un ou plusieurs états), mais la représentation graphique dans le front serait peut être compliquée

---

PO Attention, doit prendre en compte les aggrégats d'events également

si je prends la formule du compteur PVA, aujourd'hui on écrit un truc comme ça

> Var presence = EventsAggregation "Groupe TT"

Et je voudrais qu'on puisse écrire un truc comme ça:

> Var presence = EventsAggregation "Groupe TT Etat Validé" + " EventsAggregation "Groupe TT Etat A valider"

Maj du scope du ticket, à ne gérer QUE pour les aggrégats (teams 09/11/26)

> Et d'ailleurs on pourrait se contenter de gérer le truc au niveau des agrégats uniquement
> Car comme indiqué dans mon commentaire, on ne va pas cibler des états différents par event dans un même compteur

---

## 🚨⬆️ 13/11/26 > Ajustements nécessaires sur certains compteurs

Suite à l'implémentation du @code\cronexia-suivi-2\suivi\GTA-1911---events-avec-etats

Le prévisionnel ne compte plus les demandes A valider. L'exception en dur (`pending` dans la somme de quantités, et dans `isWorkflowStateInEventRightsForecast`) est commentée, avec un `TODO:` pour la rétablir quand les états d'events seront des paramètres dynamiques.

Le solde prévisionnel devient « Validé sur toute la période ». Il ne diffère du solde à date que par les absences Validées futures.

Le contrôle de droits à la création, à la soumission et à la mise à jour lit ce même prévisionnel. Il ne voit plus les demandes A valider : un collaborateur peut empiler des demandes A valider au-delà de ses droits. La validation d'un niveau ne refait pas ce contrôle.

Les compteurs seedés CPPA / RTTPA / TTPA comptent encore A valider (paramètre `SOMME_ANNEE_ETAT` explicite), toujours en dur dans les calculs (exception).

La page « Mes droits & soldes » (`source="counters"`) aussi. Les soldes issus de la somme de quantités (accueil, calendrier, chatbot, discussion IA) ne le comptent plus. Les deux sources divergent.

Max: À aligner dans les formules, dans ce ticket, si j'ai le temps de passer également les statuts par event spécifique, en plus des aggrégats d'events (a priori oui vu que j'ai de l'avance sur 1911).

---

## Dev file locations

- Backend
  - Database
    - Events : cronexia-gta-back\app\prisma\schema\event.prisma
    - Events aggregations : cronexia-gta-back\app\prisma\schema\events-aggregation.prisma
    - Counters, all tables in one file : cronexia-gta-back\app\prisma\schema\counter.prisma
      - I'd recommand having a specific focus on `model CtParam` line 248
  - Seeds
    - Events cronexia-gta-back\app\prisma\seeds-new\02-recommended\event\events.seed.ts
    - Some counters related to
      - Events : cronexia-gta-back\app\prisma\seeds\counter\CPT23_EVENT_CP_QUANTITY.ts
      - Events aggregations : cronexia-gta-back\app\prisma\seeds\counter\CPT16_EVENTS_AGG__GROUPE_2__QUANTITY.ts
  - Counter calculation
    - cronexia-gta-back\app\src\ct-counters\ct-counters.resolver.ts line 2099
      - main function : cronexia-gta-back\app\src\ct-counters\ct-counters.service.ts line 1771
      - Events handling function in CtParam processing : cronexia-gta-back\app\src\ct-counters\functions\manage\param.ts line 191, event aggreg in line 221
- //
- Frontend
  - Will be tested in cronexia-gta-front-v2\app\src\routes\(app)\(with-filters)\counters
