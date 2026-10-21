![Logo
Cronexia](media/image3.png "Logo Cronexia"){width="2.3622047244094486in"
height="2.0407983377077867in"}

**Spécification fonctionnelle**

  -----------------------------------------------------------------------
  **Source**        Fichier « Absences avec droits V2 » (Excel, 10
                    onglets)
  ----------------- -----------------------------------------------------
  **Date du         12 octobre 2026
  document**        

  **Contenu**       Besoin général, paramétrage d'un droit, règles de
                    gestion, données par ressource, fonctionnalités
                    attendues, exemples détaillés
  -----------------------------------------------------------------------

## Sommaire

1\. Objet et vocabulaire

2\. Le besoin : principes généraux

3\. Paramétrage d'un droit

4\. Règles de gestion

5\. Données à gérer par ressource

6\. Ce que les informations doivent permettre de faire

7\. Exemples détaillés

8\. Points d'attention et éléments à clarifier

# 1. Objet et vocabulaire

Ce document met en forme le besoin fonctionnel de gestion des **absences
avec droits** : des absences (congés payés, RTT, repos compensateur...)
dont la pose est conditionnée par un volume de droits qui s'acquiert, se
consomme, peut être reporté, puis est perdu ou payé. Il reprend
l'intégralité du contenu du fichier Excel source, réorganisé par thème.

Le fichier Excel comprend : un onglet de principes généraux, un onglet
décrivant les informations à gérer, un onglet de quatre exemples de
paramétrage, et six onglets détaillant les mouvements de ces exemples
pour une ressource donnée (matricule 123456A).

## 1.1 Vocabulaire

  ---------------------------------------------------------------------------
  **Terme**        **Signification dans le fichier**               **Géré**
  ---------------- ----------------------------------------------- ----------
  **Droit**        Ensemble de paramètres décrivant comment des    
                   droits à absence sont acquis, consommés,        
                   reportés puis perdus ou payés (ex. DCP, DRTT,   
                   DRC).                                           

  **Event**        Type d'absence posé par la ressource (ex. CP,   
                   RTT, RC). Plusieurs droits peuvent alimenter un 
                   même event.                                     

  **Ressource**    Personne dont on gère les droits, identifiée    
                   par son matricule.                              

  **Population**   Groupe de ressources (ex. Tous, Cadres, Non     
                   cadres) servant à définir l'éligibilité à un    
                   droit.                                          

  **Exercice**     Une période d'acquisition associée à une        
                   période de prise (relation un pour un). Un      
                   droit peut ne pas être géré par exercice.       

  **En cours**     Droits en cours d'acquisition sur l'exercice.   

  **Acquis**       Droits acquis. Lorsque la période d'acquisition 
                   est égale à la période de prise, il n'y a que   
                   des acquis.                                     

  **Report**       Droits normalement perdus ou payés, conservés   
                   pendant un délai de report avec un délai de     
                   prise avant perte définitive.                   

  **Perdus /       Droits neutralisés : non pris à l'issue de la   
  payés**          période de prise ou de report.                  

  **Compteur**     Valeur calculée, référencée par son code,       
                   utilisable comme valeur d'acquisition, plafond  
                   de report, minoration, majoration ou contrôle   
                   de pose.                                        

  **Mouvement**    Ligne de trace d'une opération sur un droit :   
                   acquisition, prise, transfert, perte,           
                   ajustement...                                   
  ---------------------------------------------------------------------------

# 2. Le besoin : principes généraux

Le système doit être en mesure de **calculer des droits à absence** en
fonction des critères ci-dessous. A compléter : la colonne « Géré » (oui
ou non) en fonction de ce qui a déjà est développé à ce jour dans
l'outil.

## 2.1 Populations et volumes

  --------------------------------------------------------------------------------
  **Réf.**    **Exigence**                      **Exemple / précision** **Géré**
  ----------- --------------------------------- ----------------------- ----------
  **PG-01**   Calculer des droits uniquement    Les RTT ne concernent   
              pour certaines populations ou     généralement pas tout   
              pour tout le monde.               le monde.               

  **PG-09**   Associer, pour des populations    CP gérés du 01/01 au    
              différentes, un droit différent à 31/12 pour certaines    
              un même event.                    populations et du 01/06 
                                                au 31/05 pour d'autres  
                                                ; dans les deux cas     
                                                l'event posé est CP.    

  **PG-13**   Gérer des droits en jours ou en                           
              heures.                                                   

  **PG-14**   Définir un volume de droits       Cadres dirigeants : 3   
              acquis différent par population.  jours par mois ; cadres 
                                                : 2,5 jours par mois.   
  --------------------------------------------------------------------------------

## 2.2 Acquisition et exercices

  --------------------------------------------------------------------------------
  **Réf.**    **Exigence**                      **Exemple / précision** **Géré**
  ----------- --------------------------------- ----------------------- ----------
  **PG-02**   Définir, ou non, une date de                              
              début et une date de fin                                  
              d'acquisition des droits.                                 

  **PG-04**   Gérer, ou non, différents         1 exercice = 1 période  
              exercices.                        d'acquisition + 1       
                                                période de prise.       

  **PG-10**   Permettre d'utiliser tous les                             
              droits dès le début de la                                 
              période, ou seulement selon les                           
              droits réellement acquis.                                 

  **PG-11**   Faire varier le volume de droits                          
              acquis selon certaines absences                           
              minorantes.                                               

  **PG-12**   Calculer des droits au prorata    Tenir compte des dates  
              via un compteur : taux d'emploi,  d'entrée et de sortie   
              entrée ou sortie en cours de      des ressources : aucun  
              période, sortie de la population  calcul de droits en     
              éligible en cours de période.     dehors de ces périodes. 

  **PG-19**   Remettre les droits à zéro en cas Au lendemain de la date 
              de sortie.                        de sortie, ou à la date 
                                                de ré-entrée en cas de  
                                                retour dans la société  
                                                si c'est plus simple.   
  --------------------------------------------------------------------------------

## 2.3 Prise et contrôles

  --------------------------------------------------------------------------------
  **Réf.**    **Exigence**                      **Exemple / précision** **Géré**
  ----------- --------------------------------- ----------------------- ----------
  **PG-03**   Définir, ou non, une date de                              
              début et une date de fin de prise                         
              pour les droits acquis.                                   

  **PG-05**   Hiérarchiser les prises selon les                         
              différents exercices, lorsqu'ils                          
              existent.                                                 

  **PG-07**   Associer, pour une même           Congés payés alimentés  
              population, plusieurs droits à un par les droits à congés 
              seul event de prise.              normaux et les droits à 
                                                congés d'ancienneté.    

  **PG-08**   Hiérarchiser les différents       Un event CP décrémente  
              droits associés à un event lors   d'abord les droits à    
              de sa prise.                      congés d'ancienneté,    
                                                puis les droits à       
                                                congés normaux.         

  **PG-15**   Définir un délai de consommation                          
              du droit à partir de sa date                              
              d'acquisition.                                            

  **PG-22**   Limiter le volume des prises sur  Pas plus de 2 jours de  
              une période donnée.               RTT par mois.           

  **PG-23**   Limiter le nombre de jours de     3 jours consécutifs     
              prise consécutifs.                maximum.                
  --------------------------------------------------------------------------------

## 2.4 Report et perte

  --------------------------------------------------------------------------------
  **Réf.**    **Exigence**                      **Exemple / précision** **Géré**
  ----------- --------------------------------- ----------------------- ----------
  **PG-06**   Reporter des droits normalement                           
              perdus, en tout ou partie, avec                           
              un délai de prise avant perte                             
              définitive.                                               

  **PG-21**   Générer des alertes lorsque des                           
              droits sont sur le point d'être                           
              perdus.                                                   
  --------------------------------------------------------------------------------

## 2.5 Ajustements et transferts

  --------------------------------------------------------------------------------
  **Réf.**    **Exigence**                      **Exemple / précision** **Géré**
  ----------- --------------------------------- ----------------------- ----------
  **PG-16**   Modifier manuellement les droits                          
              acquis d'une ressource donnée.                            

  **PG-17**   Transférer des droits d'une       Le transfert doit se    
              ressource vers une autre.         faire vers une          
                                                ressource appartenant à 
                                                une population donnée.  
  --------------------------------------------------------------------------------

## 2.6 Soldes et restitution

  --------------------------------------------------------------------------------
  **Réf.**    **Exigence**                      **Exemple / précision** **Géré**
  ----------- --------------------------------- ----------------------- ----------
  **PG-18**   Calculer des soldes à la date du                          
              jour et en prévisionnel.                                  

  **PG-20**   Récupérer dans des compteurs les  Voir les exemples pour  
              valeurs d'un droit donné : droits les informations à      
              acquis, pris et soldes à la date  récupérer.              
              du jour, à une date passée en                             
              paramètre et en prévisionnel,                             
              valeur des reports, des droits                            
              perdus, etc.                                              
  --------------------------------------------------------------------------------

# 3. Paramétrage d'un droit

Un droit est défini par les paramètres suivants. Les tableaux indiquent
pour chacun les valeurs possibles, sa règle de renseignement, son
**applicabilité** (code couleur du fichier source) et sa
**modifiabilité**.

### Légende

  -----------------------------------------------------------------------
  **Tous droits**       Information à renseigner dans tous les cas (noir
                        dans le fichier).
  --------------------- -------------------------------------------------
  **Droit géré par un   Information à renseigner uniquement pour les
  exercice**            droits gérés par un exercice (bleu).

  **Droit non géré par  Information à renseigner uniquement pour les
  un exercice**         droits non gérés par un exercice (orange).

  **Non modifiable**    Lié au droit et non modifiable une fois des
                        droits calculés.

  **Modifiable**        Lié au droit et modifiable.

  **Modifiable, lié aux Lié aux populations et modifiable.
  populations**         
  -----------------------------------------------------------------------

## 3.1 Identification

+-----------+---------+---------------------------+----------+-------+
| **Pa      | **      | **Règle et commentaire**  | **       | **G   |
| ramètre** | Valeurs |                           | Statut** | éré** |
|           | poss    |                           |          |       |
|           | ibles** |                           |          |       |
+===========+=========+===========================+==========+=======+
| **Code du | Texte   | Identifie le droit.       | **Tous   |       |
| droit**   |         |                           | droits** |       |
|           |         |                           |          |       |
|           |         |                           | Non      |       |
|           |         |                           | mo       |       |
|           |         |                           | difiable |       |
|           |         |                           | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **Libellé | Texte   |                           | **Tous   |       |
| court**   |         |                           | droits** |       |
|           |         |                           |          |       |
|           |         |                           | Mo       |       |
|           |         |                           | difiable |       |
+-----------+---------+---------------------------+----------+-------+
| **Libellé | Texte   |                           | **Tous   |       |
| long**    |         |                           | droits** |       |
|           |         |                           |          |       |
|           |         |                           | Mo       |       |
|           |         |                           | difiable |       |
+-----------+---------+---------------------------+----------+-------+

## 3.2 Gestion, population et acquisition

+-----------+---------+---------------------------+----------+-------+
| **Pa      | **      | **Règle et commentaire**  | **       | **G   |
| ramètre** | Valeurs |                           | Statut** | éré** |
|           | poss    |                           |          |       |
|           | ibles** |                           |          |       |
+===========+=========+===========================+==========+=======+
| **Mode de | En      | Obligatoire. En jours,    | **Tous   |       |
| gestion** | jours / | l'unité du droit est la   | droits** |       |
|           | En      | journée ; en heures,      |          |       |
|           | heures  | c'est l'heure.            | Non      |       |
|           |         |                           | mo       |       |
|           |         |                           | difiable |       |
|           |         |                           | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **P       | Pop     | Obligatoire. Les          | **Tous   |       |
| opulation | ulation | ressources de la          | droits** |       |
| cible**   |         | population sont éligibles |          |       |
|           |         | à ce droit.               | Mo       |       |
|           |         |                           | difiable |       |
+-----------+---------+---------------------------+----------+-------+
| **Remise  | Oui /   | Obligatoire (booléen). Si | **Tous   |       |
| à zéro    | Non     | oui, une ressource qui    | droits** |       |
| des       |         | sort de la population     |          |       |
| droits à  |         | cible à une date donnée   | Mo       |       |
| la sortie |         | perd ses droits restants  | difiable |       |
| de la     |         | à cette date. Si non, les |          |       |
| p         |         | droits acquis sont        |          |       |
| opulation |         | conservés.                |          |       |
| cible**   |         |                           |          |       |
+-----------+---------+---------------------------+----------+-------+
| **Valeur  | Co      | Obligatoire, donnée       | **Tous   |       |
| d'acqu    | nstante | historisée. Constante :   | droits** |       |
| isition** | /       | valeur entière ou         |          |       |
|           | C       | décimale, la périodicité  | Mod      |       |
|           | ompteur | d'acquisition est alors   | ifiable, |       |
|           |         | obligatoire. Compteur :   | lié aux  |       |
|           |         | sa valeur donne la valeur | pop      |       |
|           |         | du droit.                 | ulations |       |
+-----------+---------+---------------------------+----------+-------+
| **Pé      | N       | Obligatoire uniquement si | **Tous   |       |
| riodicité | ombre + | la valeur d'acquisition   | droits** |       |
| d'ac      | unité   | est une constante. Grisé  |          |       |
| quisition | (jours, | si la valeur est un       | Non      |       |
| du        | mois,   | compteur, car c'est alors | mo       |       |
| droit**   | année)  | la périodicité du         | difiable |       |
|           |         | compteur qui s'applique.  | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **Event   | Choix   | Obligatoire. Plusieurs    | **Tous   |       |
| associé** | d'un    | droits peuvent être       | droits** |       |
|           | event   | associés à un même event  |          |       |
|           |         | ; il faut alors           | Non      |       |
|           |         | hiérarchiser le décompte  | mo       |       |
|           |         | des différents droits.    | difiable |       |
|           |         |                           | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+

## 3.3 Exercice et dates

+-----------+---------+---------------------------+----------+-------+
| **Pa      | **      | **Règle et commentaire**  | **       | **G   |
| ramètre** | Valeurs |                           | Statut** | éré** |
|           | poss    |                           |          |       |
|           | ibles** |                           |          |       |
+===========+=========+===========================+==========+=======+
| **Droit   | Oui /   | Obligatoire (booléen). Si | **Tous   |       |
| géré par  | Non     | oui, les dates de début   | droits** |       |
| un        |         | et de fin d'acquisition   |          |       |
| e         |         | et de début et de fin de  | Non      |       |
| xercice** |         | prise sont obligatoires.  | mo       |       |
|           |         |                           | difiable |       |
|           |         |                           | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **Date de | JJ/MM + | Obligatoire si droit géré | **Droit  |       |
| début     | année   | par un exercice (grisé    | géré par |       |
| d'acqu    | N-1, N  | sinon). Jour et mois,     | un       |       |
| isition** | ou N+1  | relatifs ou non, plus     | ex       |       |
|           |         | année relative. Exemples  | ercice** |       |
|           |         | : 01/06/Année N-1,        |          |       |
|           |         | 01/Mois M/Année N.        | Non      |       |
|           |         |                           | mo       |       |
|           |         |                           | difiable |       |
|           |         |                           | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **Date de | JJ/MM + | Obligatoire si droit géré | **Droit  |       |
| fin       | année   | par un exercice.          | géré par |       |
| d'acqu    | N-1, N  | Obligatoirement           | un       |       |
| isition** | ou N+1  | supérieure ou égale à la  | ex       |       |
|           |         | date de début             | ercice** |       |
|           |         | d'acquisition. Exemples : |          |       |
|           |         | 31/05/Année N, 31/Mois    | Non      |       |
|           |         | M/Année N.                | mo       |       |
|           |         |                           | difiable |       |
|           |         |                           | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **Date de | JJ/MM + | Obligatoire si droit géré | **Droit  |       |
| début de  | année   | par un exercice. Jour et  | géré par |       |
| prise**   | N-1, N  | mois, relatifs ou non,    | un       |       |
|           | ou N+1  | plus année relative.      | ex       |       |
|           |         |                           | ercice** |       |
|           |         |                           |          |       |
|           |         |                           | Non      |       |
|           |         |                           | mo       |       |
|           |         |                           | difiable |       |
|           |         |                           | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **Date de | JJ/MM + | Obligatoire si droit géré | **Droit  |       |
| fin de    | année   | par un exercice.          | géré par |       |
| prise**   | N-1, N  | Obligatoirement           | un       |       |
|           | ou N+1  | supérieure ou égale à la  | ex       |       |
|           |         | date de début de prise.   | ercice** |       |
|           |         |                           |          |       |
|           |         |                           | Non      |       |
|           |         |                           | mo       |       |
|           |         |                           | difiable |       |
|           |         |                           | une fois |       |
|           |         |                           | les      |       |
|           |         |                           | droits   |       |
|           |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **Aut     | Oui /   | Obligatoire si droit géré | **Droit  |       |
| orisation | Non     | par un exercice.          | géré par |       |
| de        |         | Possibilité de poser des  | un       |       |
| prendre   |         | droits en cours sur la    | ex       |       |
| par       |         | période d'acquisition.    | ercice** |       |
| ant       |         |                           |          |       |
| icipation |         |                           | Non      |       |
| les       |         |                           | mo       |       |
| droits en |         |                           | difiable |       |
| cours     |         |                           | une fois |       |
| cumulés à |         |                           | les      |       |
| la date   |         |                           | droits   |       |
| du jour** |         |                           | calculés |       |
+-----------+---------+---------------------------+----------+-------+
| **Aut     | Oui /   | Obligatoire si droit géré | **Droit  |       |
| orisation | Non     | par un exercice.          | géré par |       |
| de        |         | Possibilité de poser des  | un       |       |
| prendre   |         | droits en cours pendant   | ex       |       |
| par       |         | leur période              | ercice** |       |
| ant       |         | d'acquisition, au-delà de |          |       |
| icipation |         | la date du jour (droits   | Non      |       |
| les       |         | prévisionnels) et jusqu'à | mo       |       |
| droits en |         | la fin de l'exercice.     | difiable |       |
| cours non |         |                           | une fois |       |
| encore    |         |                           | les      |       |
| cumulés   |         |                           | droits   |       |
| (au-delà  |         |                           | calculés |       |
| de la     |         |                           |          |       |
| date du   |         |                           |          |       |
| jour)**   |         |                           |          |       |
+-----------+---------+---------------------------+----------+-------+
| **Date    | JJ/MM + | Facultatif. Paramètre     | **Droit  |       |
| d'        | année   | indisponible (grisé) si   | géré par |       |
| ouverture | N-1, N  | la prise par anticipation | un       |       |
| du        | ou N+1  | des droits en cours non   | ex       |       |
| droit**   |         | encore cumulés n'est pas  | ercice** |       |
|           |         | autorisée. La date doit   |          |       |
|           |         | être antérieure ou égale  | Mo       |       |
|           |         | à la date de début de     | difiable |       |
|           |         | l'exercice d'acquisition. |          |       |
|           |         | Sans date, le droit est   |          |       |
|           |         | ouvert à la date de début |          |       |
|           |         | de l'exercice             |          |       |
|           |         | d'acquisition.            |          |       |
+-----------+---------+---------------------------+----------+-------+
| **Délai   | N       | Grisé si le droit est     | **Droit  |       |
| de prise  | ombre + | géré par un exercice,     | non géré |       |
| à compter | unité   | facultatif sinon. Sans    | par un   |       |
| de la     | (jours, | valeur et sans exercice,  | ex       |       |
| date      | mois,   | le droit court            | ercice** |       |
| d'acqu    | année)  | indéfiniment (jusqu'à la  |          |       |
| isition** |         | sortie du salarié).       | Mod      |       |
|           |         |                           | ifiable, |       |
|           |         |                           | lié aux  |       |
|           |         |                           | pop      |       |
|           |         |                           | ulations |       |
+-----------+---------+---------------------------+----------+-------+

## 3.4 Prise et contrôles

+-----------+---------+---------------------------+----------+-------+
| **Pa      | **      | **Règle et commentaire**  | **       | **G   |
| ramètre** | Valeurs |                           | Statut** | éré** |
|           | poss    |                           |          |       |
|           | ibles** |                           |          |       |
+===========+=========+===========================+==========+=======+
| **Vér     | Oui /   | Obligatoire (booléen). Si | **Tous   |       |
| ification | Non     | oui, la validation de la  | droits** |       |
| de        |         | prise est aussi           |          |       |
| l'app     |         | conditionnée par          | Non      |       |
| artenance |         | l'appartenance de la      | précisé  |       |
| à la      |         | ressource à la population |          |       |
| p         |         | cible sur toute la        |          |       |
| opulation |         | période de prise.         |          |       |
| cible à   |         |                           |          |       |
| la date   |         |                           |          |       |
| de        |         |                           |          |       |
| prise**   |         |                           |          |       |
+-----------+---------+---------------------------+----------+-------+
| **Solde   | Nombre  | Solde minimum applicable  | **Tous   |       |
| minimum   | (jours  | par défaut. Peut être     | droits** |       |
| a         | si      | outrepassé si les droits  |          |       |
| utorisé** | droits  | de l'utilisateur le       | Mod      |       |
|           | en      | permettent : le solde     | ifiable, |       |
|           | jours,  | minimum qu'un             | lié aux  |       |
|           | durée   | collaborateur peut        | pop      |       |
|           | si      | générer n'est pas le même | ulations |       |
|           | droits  | que pour un gestionnaire  |          |       |
|           | en      | RH.                       |          |       |
|           | heures) |                           |          |       |
+-----------+---------+---------------------------+----------+-------+
| **P       | Pop     | Facultatif. Sans valeur,  | **Tous   |       |
| opulation | ulation | aucun transfert n'est     | droits** |       |
| autorisée |         | autorisé. Avec valeur, un |          |       |
| pour      |         | écran de saisie (non      | Mod      |       |
| transfert |         | encore développé, pour    | ifiable, |       |
| de        |         | plus tard) permettra de   | lié aux  |       |
| solde**   |         | transférer tout ou partie | pop      |       |
|           |         | du solde vers les droits  | ulations |       |
|           |         | d'une ressource de cette  |          |       |
|           |         | population. Développement |          |       |
|           |         | futur.                    |          |       |
+-----------+---------+---------------------------+----------+-------+

## 3.5 Report

+-----------+---------+---------------------------+----------+-------+
| **Pa      | **      | **Règle et commentaire**  | **       | **G   |
| ramètre** | Valeurs |                           | Statut** | éré** |
|           | poss    |                           |          |       |
|           | ibles** |                           |          |       |
+===========+=========+===========================+==========+=======+
| **Délai   | N       | Obligatoire. Égal à zéro  | **Tous   |       |
| de        | ombre + | : pas de report. Délai    | droits** |       |
| report**  | unité   | pendant lequel des droits |          |       |
|           | (jours, | normalement perdus ou     | Mod      |       |
|           | mois,   | payés peuvent être        | ifiable, |       |
|           | année)  | reportés ; il court au    | lié aux  |       |
|           |         | lendemain de la date de   | pop      |       |
|           |         | fin de prise normalement  | ulations |       |
|           |         | prévue.                   |          |       |
+-----------+---------+---------------------------+----------+-------+
| **Plafond | Co      | Facultatif. Sans plafond, | **Tous   |       |
| de        | nstante | tous les droits restants  | droits** |       |
| report**  | (entier | peuvent être reportés.    |          |       |
|           | ou      | Avec une valeur ou un     | Mod      |       |
|           | d       | compteur, le droit        | ifiable, |       |
|           | écimal) | reporté est plafonné et   | lié aux  |       |
|           | /       | le reliquat est perdu ou  | pop      |       |
|           | C       | payé.                     | ulations |       |
|           | ompteur |                           |          |       |
+-----------+---------+---------------------------+----------+-------+
| **Report  | Oui /   | Obligatoire (booléen).    | **Tous   |       |
| auto      | Non     | Automatique : report mis  | droits** |       |
| matique** |         | en œuvre au lendemain de  |          |       |
|           |         | la date de fin de prise   | Mod      |       |
|           |         | pour toute la population  | ifiable, |       |
|           |         | concernée. Non            | lié aux  |       |
|           |         | automatique : déclenché   | pop      |       |
|           |         | manuellement par un       | ulations |       |
|           |         | utilisateur habilité,     |          |       |
|           |         | pour tout ou partie de la |          |       |
|           |         | population ; le plafond   |          |       |
|           |         | et le délai du droit      |          |       |
|           |         | s'appliquent par défaut   |          |       |
|           |         | mais peuvent être         |          |       |
|           |         | surchargés sans impact    |          |       |
|           |         | sur le droit. Le report   |          |       |
|           |         | manuel fera l'objet d'un  |          |       |
|           |         | descriptif séparé.        |          |       |
+-----------+---------+---------------------------+----------+-------+

## 3.6 Compteurs et ajustements manuels

+-----------+---------+---------------------------+----------+-------+
| **Pa      | **      | **Règle et commentaire**  | **       | **G   |
| ramètre** | Valeurs |                           | Statut** | éré** |
|           | poss    |                           |          |       |
|           | ibles** |                           |          |       |
+===========+=========+===========================+==========+=======+
| *         | Choix   | Facultatif. Code du       | **Tous   |       |
| *Compteur | d'un    | compteur permettant       | droits** |       |
| de        | c       | d'impacter négativement   |          |       |
| m         | ompteur | la valeur d'un droit.     | Mo       |       |
| inoration |         |                           | difiable |       |
| / prorata |         |                           |          |       |
| des       |         |                           |          |       |
| droits**  |         |                           |          |       |
+-----------+---------+---------------------------+----------+-------+
| *         | Choix   | Facultatif. Code du       | **Tous   |       |
| *Compteur | d'un    | compteur permettant       | droits** |       |
| de        | c       | d'impacter positivement   |          |       |
| maj       | ompteur | la valeur d'un droit.     | Mo       |       |
| oration** |         |                           | difiable |       |
+-----------+---------+---------------------------+----------+-------+
| *         | Choix   | Facultatif. Sans          | **Tous   |       |
| *Compteur | d'un    | compteur, les contrôles   | droits** |       |
| de        | c       | habituels sont effectués. |          |       |
| contrôle  | ompteur | Avec compteur, on vérifie | Mo       |       |
| per       |         | en plus sa valeur de      | difiable |       |
| sonnalisé |         | retour : vrai, pas de     |          |       |
| des       |         | blocage de la prise ;     |          |       |
| prises**  |         | faux, rejet de la prise   |          |       |
|           |         | (reste à définir comment  |          |       |
|           |         | transmettre le message    |          |       |
|           |         | justifiant le rejet).     |          |       |
+-----------+---------+---------------------------+----------+-------+
| **A       | ---     | Fonctionnalité à mettre   | **Droit  |       |
| justement |         | en place dans un deuxième | géré par |       |
| manuel    |         | temps.                    | un       |       |
| des       |         |                           | ex       |       |
| droits en |         |                           | ercice** |       |
| cours**   |         |                           |          |       |
|           |         |                           | Non      |       |
|           |         |                           | précisé  |       |
+-----------+---------+---------------------------+----------+-------+
| **A       | ---     | Fonctionnalité à mettre   | **Tous   |       |
| justement |         | en place dans un deuxième | droits** |       |
| manuel    |         | temps.                    |          |       |
| des       |         |                           | Non      |       |
| droits    |         |                           | précisé  |       |
| acquis**  |         |                           |          |       |
+-----------+---------+---------------------------+----------+-------+
| **A       | ---     | Fonctionnalité à mettre   | **Tous   |       |
| justement |         | en place dans un deuxième | droits** |       |
| manuel de |         | temps.                    |          |       |
| report**  |         |                           | Non      |       |
|           |         |                           | précisé  |       |
+-----------+---------+---------------------------+----------+-------+

# 4. Règles de gestion

## 4.1 Cycle de vie et ordre de décompte des droits

-   Si la période d'acquisition d'un droit est égale à la période de
    prise, il n'y a pas lieu de distinguer « En cours » et « Acquis » :
    il n'y a que des acquis.

-   Lorsque « En cours », « Acquis » et « Report » sont distingués, les
    prises décrémentent **d'abord le report** jusqu'à épuisement, **puis
    les acquis**, et enfin les **droits en cours** si au moins l'un des
    paramètres « Autorisation de prise par anticipation » du droit est
    vrai.

-   Si un délai de report existe, à l'issue de la période de report les
    droits reportés et non pris sont perdus ou payés (neutralisés).

-   Si aucun délai de report n'existe, à l'issue de la période de prise
    les droits acquis et non pris sont perdus ou payés (neutralisés).

-   Tous les mouvements (acquisition, prise, transfert d'en cours vers
    acquis, perte des droits restants...) doivent être tracés. Un
    énuméré regroupant tous les types de mouvement est à prévoir (voir
    §5.3).

## 4.2 Validation d'une pose

Pour vérifier qu'une pose peut être acceptée, le système doit :

1.  prendre en compte les droits à la date retenue pour la vérification
    ;

2.  prendre en compte les prises déjà effectuées jusqu'à la date de fin
    de prise de l'exercice associé ;

3.  vérifier que le solde (droits moins prises) est supérieur ou égal au
    solde minimum autorisé.

La date et la nature des droits pris en compte dépendent du paramétrage
:

  --------------------------------------------------------------------------
  **Cas d'exemple**   **Date retenue pour   **Droits pris en      **Géré**
                      les droits**          compte**              
  ------------------- --------------------- --------------------- ----------
  **Exemple 1 : CP,   Date du jour de la    Reports + acquis + en 
  période légale**    pose (et non la date  cours                 
                      d'effet de la pose)                         

  **Exemple 2 : CP,   Date de fin           Reports + acquis      
  année civile, tous  d'exercice                                  
  droits utilisables                                              
  dès le début**                                                  

  **Exemple 3 : RTT** Date du jour de la    Reports + acquis      
                      pose (et non la date                        
                      d'effet de la pose)                         
  --------------------------------------------------------------------------

Par ailleurs, le système doit vérifier l'existence d'un droit avant
d'accepter la prise et, selon les droits du profil de l'utilisateur,
rejeter une demande en cas de droits insuffisants ; il doit aussi
vérifier que les droits d'un exercice donné sont posés sur une période
cohérente avec la période de prise autorisée associée.

## 4.3 Historisation et calcul des soldes

-   Il ne peut y avoir qu'**une seule ligne** avec la même date d'effet
    et le même code droit.

-   Il faut pouvoir déterminer le solde à une date donnée (par exemple
    la date du jour) ainsi que le solde tenant compte de l'ensemble des
    absences prévisionnelles déjà posées mais pas encore prises.

-   La validation des poses s'appuie sur le **solde prévisionnel**
    (droits à date moins poses prévisionnelles) et non sur le solde à
    date (droits à date moins poses à date).

-   Pour connaître le **solde prévisionnel** à une date donnée, on
    s'appuie sur les **dates de mise à jour**. Pour connaître le **solde
    à date**, on s'appuie sur la **date d'effet**. Dans les deux cas, on
    récupère la valeur dont la date est inférieure ou égale à la date
    passée en paramètre.

-   Une prise postérieure à l'exercice en cours est **provisionnée** sur
    les droits en cours, avec contrôle des soldes à la date de pose ; à
    l'ouverture de l'exercice suivant, ces provisions sont transformées
    en report ou en acquis selon les droits.

# 5. Données à gérer par ressource

Les droits d'une ressource sont suivis sous forme de mouvements datés,
auxquels sont associés des cumuls et des soldes par exercice.

## 5.1 Informations d'un mouvement

  -------------------------------------------------------------------------
  **Champ**          **Description**                             **Géré**
  ------------------ ------------------------------------------- ----------
  **Matricule**      Identifiant de la ressource.                

  **Date de création Dates de création et de dernière mise à     
  / Date de mise à   jour du mouvement.                          
  jour**                                                         

  **Code droit**     Code du droit concerné.                     

  **Date d'effet du  Date à laquelle le mouvement produit son    
  mouvement**        effet.                                      

  **Date             Facultatif, pour les droits non gérés par   
  d'expiration du    un exercice.                                
  droit**                                                        

  **Nature du        Voir la liste au §5.3.                      
  mouvement**                                                    

  **Référence de     Période de début et de fin d'acquisition de 
  l'exercice**       référence, associée à une période de prise  
                     en relation un pour un. Nulle si le droit   
                     n'est associé à aucun exercice.             

  **Référence        Référence de l'event dans EventByDay        
  instance event**   (absences en heures) ou EventRangeByDay     
                     (absences en jours). Renseignée uniquement  
                     pour les mouvements de prise.               

  **Date de fin de   Uniquement pour les droits non associés à   
  validité du        un exercice.                                
  droit**                                                        

  **Droits en        Nombre en cours d'acquisition.              
  cours**                                                        

  **Droits acquis**  Nombre acquis.                              

  **Droits reports** Nombre reporté.                             

  **Droits perdus /  Nombre perdu ou payé.                       
  payés**                                                        

  **Pris sur en      Nombre pris sur les droits en cours         
  cours**            d'acquisition.                              

  **Pris sur         Nombre pris sur les acquis.                 
  acquis**                                                       

  **Pris sur         Nombre pris sur le report.                  
  report**                                                       
  -------------------------------------------------------------------------

## 5.2 Cumuls et soldes sur l'exercice

  -------------------------------------------------------------------------
  **Champ**          **Description**                             **Géré**
  ------------------ ------------------------------------------- ----------
  **Cumul droits     Nombre de droits reportés.                  
  report sur                                                     
  l'exercice**                                                   

  **Cumul droits     Nombre de droits reportés perdus.           
  report perdus /                                                
  payés sur                                                      
  l'exercice**                                                   

  **Cumul pris       Nombre pris sur report.                     
  report sur                                                     
  l'exercice**                                                   

  **Cumul droits     Nombre de droits acquis.                    
  acquis sur                                                     
  l'exercice**                                                   

  **Cumul droits     Nombre de droits acquis perdus.             
  acquis perdus /                                                
  payés sur                                                      
  l'exercice**                                                   

  **Cumul pris       Nombre pris sur acquis.                     
  acquis sur                                                     
  l'exercice**                                                   

  **Cumul en cours   Nombre de droits en cours.                  
  sur l'exercice**                                               

  **Cumul pris en    Nombre pris sur les droits en cours.        
  cours sur                                                      
  l'exercice**                                                   

  **Cumul provision  Nombre de droits en cours provisionnés      
  en cours sur       (prises sur l'exercice suivant).            
  l'exercice**                                                   

  **Solde report sur Droits report − Pris report − Perdus        
  l'exercice**       report.                                     

  **Solde acquis sur Droits acquis − Pris acquis − Perdus        
  l'exercice**       acquis.                                     

  **Solde en cours   Droits en cours − Pris en cours (les        
  sur l'exercice**   exemples déduisent aussi la provision en    
                     cours).                                     
  -------------------------------------------------------------------------

## 5.3 Liste des natures de mouvement

  ------------------------------------------------------------------------------
  **N°**   **Nature du mouvement** **Précision**                      **Géré**
  -------- ----------------------- ---------------------------------- ----------
  **1**    Ajout d'en cours                                           

  **2**    Prise d'en cours sur                                       
           exercice courant                                           

  **3**    Prise d'en cours sur                                       
           exercice suivant                                           

  **4**    Transfert en cours vers Au lendemain de la date de fin     
           acquis                  d'acquisition, les « En cours »    
                                   deviennent des « Acquis ».         

  **5**    Prise d'acquis                                             

  **6**    Perte d'acquis                                             

  **7**    Paiement d'acquis                                          

  **8**    Transfert acquis vers                                      
           report                                                     

  **9**    Prise de report                                            

  **10**   Perte de report                                            

  **11**   Paiement de report                                         

  **12**   Ajustement manuel d'en                                     
           cours                                                      

  **13**   Ajustement manuel                                          
           d'acquis                                                   

  **14**   Ajustement manuel de                                       
           report                                                     
  ------------------------------------------------------------------------------

> La liste du fichier ne contient pas toutes les natures utilisées dans
> les exemples (voir §8).

# 6. Ce que les informations doivent permettre de faire

1.  Déterminer les soldes d'une ressource pour un droit donné à une date
    donnée, en particulier à la date du jour ou à une date future en
    tenant compte des prises prévisionnelles.

2.  Fournir les éléments expliquant la valeur des droits restants (les
    soldes) à n'importe quelle date.

3.  Opérer la bascule « en cours » vers « acquis » à la date appropriée.

4.  Opérer la bascule « acquis » vers « report » à la date appropriée
    (si report automatique).

5.  Opérer la bascule « acquis » vers « perdu / payé » à la date
    appropriée.

6.  Distinguer les droits en fonction des exercices.

7.  Vérifier l'existence d'un droit avant d'accepter la prise et, selon
    les droits du profil utilisateur, rejeter une demande en cas de
    droits insuffisants.

8.  Vérifier que les droits d'un exercice donné sont posés sur une
    période cohérente avec la période de prise autorisée associée.
