# GTA-1744 - Retour PO : affichage des heures dans les widgets collab

Contexte : `cronexia-suivi-2/suivi/GTA-1744-wf-events-hourly/` (plans 01 backend, 02 frontend).

Branche des retours : `feat-1744-wf-events-hourly-returns`.

Note courte. La repasse widget par widget, et les correctifs, se feront dans une passe dédiée.

## Retour PO

Collaborateur > Accueil > widgets : affichage des heures.

Faire une repasse sur tous les widgets de l'accueil collaborateur.

## Où c'est aujourd'hui

Accueil : `cronexia-gta-front-v2/app/src/routes/components/common/home/HomeEmployee.svelte`. Liste stable : `COLLABORATOR_WIDGET_IDS` dans `app/src/config/home-widget-visibility-config.ts`.

| Widget | Composant | Heures |
|---|---|---|
| Profil, Infos, Liens RH | `WidgetProfilUtilisateur`, `WidgetInfos`, `WidgetLiensRH` | Rien à afficher |
| Soldes congés, Compteurs | `WidgetSoldesConges`, `WidgetMesDroits`, `WidgetCompteurs` | Soldes, pas un créneau d'event |
| Pointages du jour | `WidgetPointagesDuJour` | Heures de badgeage, pas DEP / RC |
| Gérer mes demandes | `WidgetGererMesDemandes` | Période lue sur `typedEventRangeOnResource` (`typeDayStart` / `typeDayEnd` : Journée, Matin, Après-midi). Pas de lecture de `typedEventByDay` |
| Mon planning | `WidgetMonPlanning`, `WidgetMonPlanningHorizontal` | Créneau déjà peint si `timeStart` / `timeEnd` sont là |
| Calendrier des absences, Emploi du temps | `WidgetPersonalCalendarMonth` (`absences`, `timetable`) | À vérifier : le composant ne formate pas lui-même un créneau |

Formateur partagé, pas branché sur ces widgets : `routes/functions/cronexia/event/resolve-hourly-display.ts` (créneau si début / fin, sinon durée). La note 04 commente le choix de saisie « durée seule », sans le supprimer. L'affichage d'une durée calculée sur un créneau n'est pas tranché là.

## À trancher à la passe suivante

- Pour chaque widget de la liste : une ligne DEP / RC en heures s'affiche en créneau, ou retombe sur « Journée ».
- Priorité visible : « Gérer mes demandes », qui ne connaît que la période en jours.
- Planning : confirmer que le créneau vient bien d'un `EventByDay` de demande, pas seulement d'une déclaration.
- Calendriers : ouvrir le rendu des events du mois.
- Les widgets sans event (profil, infos, liens, soldes, compteurs, pointages) : une ligne dans la repasse, pas un correctif.

## Hors périmètre de cette note

- Pas de correctif, pas de repasse faite ici.
- Accueil manager et RH. La note 07 ne couvre que la demande fantôme, pas cette repasse.
- Bouton pour soumettre un déplacement (note 09), modalité (note 05), message horaire de repos (note 06).
