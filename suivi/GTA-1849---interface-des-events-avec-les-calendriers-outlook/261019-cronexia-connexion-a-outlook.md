# GTA-1849 — Synchronisation des événements vers les calendriers Microsoft Outlook

ARTE France utilise Microsoft 365 pour la messagerie et les calendriers de ses collaborateurs. Le calendrier affiché dans Outlook et celui affiché dans Teams sont le même calendrier Exchange Online.

Cronexia y reporte les événements de gestion des temps. La création, la mise à jour et la suppression se font directement dans le calendrier de la personne concernée. Aucune invitation n'est envoyée, et le collaborateur n'a rien à accepter.

L'échange repose sur Microsoft Graph, l'interface standard de Microsoft 365 pour les calendriers Exchange Online. Il a lieu au moins une fois par jour. Il peut aussi être relancé depuis Cronexia, par un bouton du planning ou de la page calendrier. Dans les deux cas, la personne reste dans Cronexia.

---

## Partie 1 — Fonctionnement envisagé

### 1.1 Actions possibles

Les événements issus de Cronexia sont créés, modifiés ou retirés du calendrier Microsoft. Les rendez-vous saisis par le collaborateur dans Outlook ou Teams restent en dehors de cet échange.

Chaque type d'événement (télétravail, absence, astreinte, et les autres types gérés par la GTA) a un libellé et une disponibilité, définis pour ARTE. Exemples de rendu :

- Le télétravail apparaît avec son libellé. Les collègues voient « Travaille ailleurs ».
- Une absence sensible, une maladie par exemple, est privée. Le collaborateur voit le motif. Une personne qui ouvre son calendrier voit « Rendez-vous privé », avec le statut Absent. Le motif n'est pas exposé.
- L'astreinte suit le libellé et la disponibilité choisis pour ce type.

La période couverte est paramétrable. Un fonctionnement de référence allait d'un mois dans le passé à cinq mois dans le futur. Les bornes exactes, ainsi que le catalogue des libellés, seront fixés en phase d'analyse.

Les demandes suivent un circuit de validation. Leur présence dans le calendrier dépend de l'état :

- Brouillon : rien n'est envoyé.
- En attente de validation : l'événement est créé comme provisoire. La plage apparaît hachurée, et la disponibilité affichée est « Provisoire ».
- En attente de justificatif : l'événement est envoyé, avec une couleur de catégorie qui le distingue d'un événement validé.
- Validé : l'événement prend la disponibilité normale de son type (absent, travaille ailleurs ou occupé).
- Refusé ou annulé : l'événement est retiré du calendrier.

Outlook peut afficher le libellé, une couleur parmi vingt-cinq couleurs prédéfinies, le hachurage du provisoire, et le cadenas des événements privés. Le cadenas est l'icône standard d'Outlook pour un événement privé. Note : Le bloc d'agenda d'outlook ne permet pas d'afficher les icônes choisies par Cronexia et affichées dans la GTA.

### 1.2 Gestion des droits

L'accès est accordé une seule fois, par un administrateur Microsoft Entra ID d'ARTE, à l'application Cronexia. Il couvre les calendriers du périmètre retenu, et peut être limité aux seules boîtes concernées.

Le collaborateur ne donne pas son accord, ni au premier échange, ni à chacun des suivants. L'autorisation reste valable jusqu'à ce qu'un administrateur la retire. Elle n'a pas besoin d'être renouvelée.

Ce mode est celui prévu par Microsoft pour les boîtes professionnelles d'un tenant Microsoft 365 : l'application lit et écrit les calendriers sans utilisateur connecté.

Prérequis côté ARTE :

- Microsoft 365, avec des boîtes Exchange Online.
- Un administrateur du tenant, pour l'accord unique.
- L'adresse de la boîte Microsoft de chaque collaborateur du périmètre.

Cette adresse peut différer de l'e-mail du compte Cronexia. Un réglage du site indique si les deux sont identiques. S'ils diffèrent, l'adresse Microsoft est portée par un champ du dossier collaborateur, renseigné par les ressources humaines ou par un import. Si l'adresse est absente, ou inconnue dans le tenant, la personne est signalée et son calendrier n'est pas modifié.

### 1.3 Pages Cronexia concernées

- La page de connexion reste celle de Cronexia. Elle identifie le compte Cronexia, et ne demande pas d'identifiants Microsoft.
- Aucune page, fenêtre intégrée ou formulaire de mot de passe Microsoft n'est ajouté.
- Lorsque le réglage indique que l'adresse du calendrier diffère de l'e-mail du compte, cette adresse se saisit dans le dossier du collaborateur.
- Un bouton d'échange avec le calendrier est prévu sur le planning individuel, le planning collectif, le planning d'équipe et la page calendrier du collaborateur.
- L'écran d'administration des calendriers de jours (jours fériés, types de jours) ne porte pas cet échange.

---

## Partie 2 — Repères techniques

### Principe

Le front SvelteKit appelle l'API Cronexia. Le backend NestJS est le seul à appeler Microsoft Graph v1.0 (`https://graph.microsoft.com/v1.0`). Les écritures passent par `POST`, `PATCH` et `DELETE` sur `/users/{adresse}/events`. Les événements sont posés dans le calendrier. Le flux n'envoie pas d'invitation : la liste des participants n'est pas utilisée pour cet échange.

Le calendrier Teams et le calendrier Outlook sont la même boîte Exchange Online.

### Droits

La permission d'accès aux calendriers se nomme `Calendars.ReadWrite`, en permission d'application.

Références :

- Présentation de Microsoft Graph : https://learn.microsoft.com/fr-fr/graph/overview
- Accès sans utilisateur : https://learn.microsoft.com/en-us/graph/auth-v2-service
- Référence des permissions : https://learn.microsoft.com/en-us/graph/permissions-reference

Mise en place :

- Inscription d'une application dans Microsoft Entra ID. Secret ou certificat stocké côté backend.
- Permission d'application `Calendars.ReadWrite`, avec consentement administrateur.
- Stratégie d'accès applicative Exchange, pour limiter les boîtes à un groupe du périmètre.
- Pour les couleurs de catégorie, permission d'application `MailboxSettings.ReadWrite`. Les catégories sont créées dans la liste maître de la boîte (`POST /users/{id}/outlook/masterCategories`), avec une couleur `preset0` à `preset24`. Le nom de la catégorie est ensuite posé sur `event.categories`.
- Jeton de type client credentials, environ une heure, renouvelé par le serveur. Le consentement administrateur demeure jusqu'à révocation. Documentation des jetons : https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens
- Le mode délégué existe : chaque salarié consent une fois (`Calendars.ReadWrite` et `offline_access`), puis un jeton de rafraîchissement couvre les appels suivants. Ce jeton expire après 90 jours sans usage, et se renouvelle à chaque usage. Ce mode est écarté, parce qu'il demande une action du collaborateur, ce que le besoin exclut.

### Adresse de la boîte

Réglage global dans la table `Config` :

- code `IS_CALENDAR_EMAIL_SAME_AS_USER_EMAIL`
- type `Boolean`
- valeur de seed proposée : `true`

Lorsque la valeur est `true`, l'adresse envoyée à Graph est `User.email`.

Lorsque la valeur est `false`, l'adresse est le champ de dossier « e-mail du calendrier » : un `ResourceField` de type `String`, valeur dans `ResourceStrVal`. Il n'y a pas de repli sur `User.email`. Champ vide, ou boîte introuvable dans le tenant : la ressource est ignorée et signalée.

Le champ est porté par la ressource, pas par la session de la personne connectée. Un gestionnaire peut valider une demande pendant que le collaborateur est absent. Le traitement quotidien tourne sans utilisateur connecté. La cible est la ressource du planning, y compris lorsqu'elle n'a pas de compte de connexion Cronexia.

### Déclenchement

- Traitement quotidien `@Cron`. `@nestjs/schedule` est déjà en place.
- Le même service est appelé par un bouton sur les plannings individuel, collectif et d'équipe, et sur la page calendrier collaborateur (`/calendar`).
- Pas de bouton sur l'administration des calendriers de jours (`/admin/calendar`).

### Contenu synchronisé

Périmètre de la réponse à l'appel d'offres : de la GTA vers le calendrier.

- Seuls les événements créés par Cronexia sont mis à jour ou supprimés. Chacun est marqué par une propriété étendue (identifiant Cronexia), et l'identifiant Graph est mémorisé.
- Le traitement réconcilie une fenêtre de dates paramétrable : création, mise à jour, suppression.
- La correspondance part du type d'événement (`Event`, `EventTypeEnum`, indicateurs télétravail et astreinte) : sujet, `showAs` (`free`, `tentative`, `busy`, `oof`, `workingElsewhere`), `sensitivity` (`normal` ou `private`), journée entière ou horaires.

Les demandes de workflow visent un événement via `Workflow.targetEventForTypeEventRangeOnResource`. Effet de `WorkflowStateEnum` :

- Brouillon / `draft` : pas d'envoi.
  - Ou possibilité d'envoi avec une couleur dédiée, par exemple bleu ciel, pour le calendrier de l'utilisateur uniquement.
- En attente / `pending` :
  - Propriété du calendrier d'Outlook : `showAs = tentative`.
  - Affichage avec une couleur orangée.
- `awaitingAttachements` : événement envoyé.
  - Affichage avec une couleur orangée.
- `validated` :
  - Propriété du calendrier d'Outlook : `showAs` du type d'événement.
  - Affichage avec une couleur verte ou neutre.
- `refused` et `cancelled` : suppression de l'événement Graph.
  - Ou possibilité d'envoi avec une couleur dédiée, par exemple rouge et/ou hachurée.

Pour les évènements "sensibles", la propriété du calendrier d'Outlook `sensitivity = private` affiche le cadenas et masque le sujet aux personnes qui ouvrent le calendrier (« Absence »). La disponibilité (`showAs`) reste visible.

L'import, du calendrier vers Cronexia, peut être porté par le même bouton. Il est hors de l'engagement de l'appel d'offres. Si mis en place, les évènements externes seront identifiés via une propriété dédiée du côté Cronexia.

### Points laissés à l'analyse et la configuration ultérieure

Fenêtre de dates, catalogue des libellés et des couleurs par type et par statut, boîtes hybrides, passage éventuel à une fréquence horaire, règles précises de l'import.
