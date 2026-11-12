# GTA-1789 / Commentaire d'un autre développeur qui à touché au même sujet

ATTENTION? CERTAINS TRAVAUX au niveaux de la génération des anomalies/conflits ont peut être été déjà implémentés dans le backend

---

(copié collé sans mise en page depuis jira)

## GTA-1789 : ce qui a été fait

### Le cas signalé

Un gestionnaire RH saisit une absence (ex. DEL) sur un créneau où un ADEC existe déjà. La popup de chevauchement ne s'affiche pas. Ensuite, la page Anomalies montre un conflit (CONFLIMLTP) et une absence injustifiée (AINJ).

### Pourquoi

Les conflits sont contrôlés à deux endroits, qui n'appliquaient pas la même règle :

| Contrôle | Quand | Demande en brouillon ou refusée |
| --- | --- | --- |
| Popup de conflit (front) | avant l'enregistrement | ignorée : elle ne réserve rien |
| Générateur d'anomalies (back) | après coup, page Anomalies | comptée comme une vraie saisie |

Le générateur lisait toutes les saisies sans regarder l'état de leur demande. C'est vrai pour les ADEC / PDEC d'une déclaration en heures, et aussi pour les CP / RTT. Reproduit : un CP refusé ou en brouillon + une DEL le même jour → CONFLIMLTP « CP, DEL ».

### Pourquoi les événements restent créés dès le brouillon

La réponse fournie par PO sur ce ticket était : aucun événement créé en brouillon, ADEC / PDEC créés seulement à la validation de la déclaration.

Appliquée à la lettre, cette règle contredit une décision antérieure, GTA-1770 (« Gestion de la visibilité des status des events ADEC/PDEC ») :

lors du call du 23/09, à la question de l'affichage de ces événements et de leurs statuts hors de la page de déclaration, PO a répondu « Oui pour l'affichage » ;

Maxime a alors exposé le statut de la demande (brouillon, en attente, validée, refusée) sur chaque événement de déclaration, et l'a branché sur la synthèse, les anomalies, les plannings collectif et individuel, les calendriers, la page absences, les favoris et les widgets d'accueil.

Ne créer ces événements qu'à la validation les ferait disparaître de toutes ces pages tant que la déclaration n'est pas validée : un brouillon, une déclaration en attente ou refusée n'y apparaîtrait plus.

Les deux décisions se concilient : les événements existent dès le brouillon, pour l'affichage avec leur statut (GTA-1770), mais ils ne comptent pas avant le moment prévu par PO. Ils ne déclenchent donc ni conflit ni AINJ, ce qui était l'objet de ce ticket.

### Règle retenue

Les événements d'une déclaration en heures restent créés dès le brouillon et affichés avec leur statut. Rien n'est retiré de l'affichage.

Ce qui change, c'est ce qui compte pour les conflits (règle fournie par PO : ADEC / PDEC seulement une fois la déclaration validée) :

| État de la demande | Événements saisis | ADEC / PDEC |
| --- | --- | --- |
| Brouillon | ne comptent pas | ne comptent pas |
| En attente | comptent | ne comptent pas |
| Validée | comptent | comptent |
| Refusée, annulée | ne comptent pas | ne comptent pas |

Pour les absences en jours (CP, RTT…) : brouillon, refusée et annulée ne comptent plus dans le générateur. Elles étaient déjà ignorées par la popup.

Une demande en attente compte comme absence, dans le générateur comme dans la popup (règle confirmée par PO).

### Ce qui a été fait

Back, générateur d'anomalies : les deux requêtes de saisies manuelles appliquent la règle ci-dessus (absences en jours et événements en heures). Plusieurs absences superposées justifient ensemble la plage (voir plus bas).

Front, popup de conflit : un ADEC / PDEC compte seulement si la déclaration est validée, comme dans le générateur. Le filtre d'affichage de la page absences est inchangé.

### Tests

Testés en local, avec les écrans réels :

déclaration en brouillon : l'ADEC reste affiché dans la synthèse ;

DEL sur l'ADEC d'une déclaration en attente : pas de popup, aucune anomalie après génération ;

DEL sur l'ADEC d'une déclaration validée : popup, puis CONFLIMLTP après génération ;

CP refusé ou en brouillon + DEL : plus de conflit ; CP validé + DEL : CONFLIMLTP (témoin).

ADEC validé + DEL superposés : CONFLIMLTP seulement, plus d'AINJ ; chevauchement partiel : conflit sur la plage commune seulement ;

non-régression : pour un collaborateur qui pointe avec des trous de pointage, anomalies et événements générés identiques au générateur d'origine.

Tests unitaires : back 1205 / 1205, front 1668 (suites complètes vertes, après mise à jour avec main).

### AINJ sur une plage justifiée deux fois

Second symptôme du ticket : quand deux absences qui comptent se chevauchent (ex. ADEC validé + DEL gardés avec « Tout conserver »), le générateur créait une AINJ sur la plage commune.

Cause : le générateur ne « résolvait » une absence théorique par une saisie manuelle que s'il y avait exactement une saisie active à cet instant. Avec deux absences superposées, aucune résolution, donc AINJ.

Correctif : plusieurs saisies actives du même type (toutes des absences, ou toutes des présences) justifient ensemble l'absence, du début le plus tôt à la fin la plus tardive. Une absence et une présence superposées ne justifient toujours rien. Le chevauchement reste signalé par CONFLIMLTP.
