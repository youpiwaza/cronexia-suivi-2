$ playwright test conflict-modes-admin

Running 4 tests using 1 worker

  ✓  1 [chromium] › e2e/conflict-modes-admin.flow.spec.ts:27:3 › Administration — réaction au conflit par profil › liste les profils avec leur mode et rappelle l’effet de chacun (3.1s)
  ✓  2 [chromium] › e2e/conflict-modes-admin.flow.spec.ts:42:3 › Administration — réaction au conflit par profil › les modes du seed sont ceux attendus par profil (867ms)
  ✓  3 [chromium] › e2e/conflict-modes-admin.flow.spec.ts:84:3 › Administration — réaction au conflit par profil › annuler depuis la toolbar revient à la valeur enregistrée (1.6s)
  ✓  4 [chromium] › e2e/conflict-modes-admin.flow.spec.ts:98:3 › Administration — réaction au conflit par profil › enregistrer depuis la toolbar persiste, puis on restaure (2.4s)

  4 passed (8.9s)
❯ bun run test:e2e

$ playwright test

Running 22 tests using 8 workers

  -   1 [chromium] › e2e/absence-conflict-replacement.flow.spec.ts:58:8 › Absences — remplacement d'un chevauchement › recouvrement total : l'existant est supprimé
  -   2 [chromium] › e2e/absence-conflict-replacement.flow.spec.ts:66:8 › Absences — remplacement d'un chevauchement › recouvrement par la fin : l'existant est raccourci
  -   3 [chromium] › e2e/absence-conflict-replacement.flow.spec.ts:71:8 › Absences — remplacement d'un chevauchement › recouvrement au milieu : l'existant est scindé en deux
  -   4 [chromium] › e2e/absence-conflict-replacement.flow.spec.ts:77:8 › Absences — remplacement d'un chevauchement › demi-journée : l'existant garde son matin
  -   5 [chromium] › e2e/absence-conflict-replacement.flow.spec.ts:82:8 › Absences — remplacement d'un chevauchement › « Tout conserver » laisse les deux events en place
  -   6 [chromium] › e2e/absence-conflict-replacement.flow.spec.ts:87:8 › Absences — remplacement d'un chevauchement › fermer la fenêtre n'écrit rien
  -   7 [chromium] › e2e/absence-conflict-replacement.flow.spec.ts:94:8 › Absences — une absence issue d'une demande est verrouillée › ni modifiable ni supprimable, et le tooltip le dit
  ✓   8 [chromium] › e2e/conflict-arbitration.smoke.spec.ts:76:3 › Conflit d'événements — actions proposées selon le mode du profil › Acceptable : le choix est laissé (8.6s)
  ✓   9 …hromium] › e2e/absence-conflict-replacement.flow.spec.ts:41:3 › Absences — remplacement d'un chevauchement › le tableau des absences en jours est accessible et la toolbar y répond (11.3s)  ✓  10 [chromium] › e2e/conflict-arbitration.smoke.spec.ts:96:3 › Conflit d'événements — actions proposées selon le mode du profil › la fenêtre liste le conflit et nomme le collaborateur (8.5s)
  ✓  11 [chromium] › e2e/color.smoke.spec.ts:10:1 › color showcase page loads (10.1s)
  ✓  12 … e2e/conflict-arbitration.smoke.spec.ts:83:3 › Conflit d'événements — actions proposées selon le mode du profil › Évité + événement non remplaçable : « Tout conserver » est rouvert (9.9s)  ✓  13 [chromium] › e2e/conflict-arbitration.smoke.spec.ts:49:3 › Conflit d'événements — actions proposées selon le mode du profil › Interdit : la saisie est rejetée, aucun arbitrage (9.3s)
  ✓  14 … › e2e/conflict-arbitration.smoke.spec.ts:57:3 › Conflit d'événements — actions proposées selon le mode du profil › Interdit : aucun motif de blocage, seulement les chevauchements (10.0s)  ✓  15 [chromium] › e2e/conflict-arbitration.smoke.spec.ts:68:3 › Conflit d'événements — actions proposées selon le mode du profil › Évité : le remplacement est imposé (9.9s)
  ✘  16 …dgets.flow.spec.ts:42:3 › Accueil collaborateur — widgets calendrier des absences / emploi du temps › navigation mois précédent/suivant met à jour le libellé et le bouton "retour" (23.1s)  ✘  17 …m] › e2e/home-employee-calendar-widgets.flow.spec.ts:33:3 › Accueil collaborateur — widgets calendrier des absences / emploi du temps › affiche les 2 widgets avec le mois en cours (23.1s)  ✓  18 …ome-employee-calendar-widgets.flow.spec.ts:61:3 › Accueil collaborateur — widgets calendrier des absences / emploi du temps › le lien "Voir mon calendrier annuel" mène à /calendar (24.6s)  ✓  19 [chromium] › e2e/login.flow.spec.ts:7:1 › logs in from / and reaches Super Admin home (5.1s)
  ✓  20 …ployee-calendar-widgets.flow.spec.ts:67:3 › Accueil collaborateur — widgets calendrier des absences / emploi du temps › le lien "Voir mon emploi du temps annuel" mène à /timetable (24.9s)  ✓  21 [chromium] › e2e/login.smoke.spec.ts:3:1 › login page renders form landmarks (1.2s)
  ✓  22 …2e/planning-palette-conflict.flow.spec.ts:54:3 › Planning collectif — barre de raccourcis › deux pastilles superposées ouvrent l’arbitrage à l’enregistrement, Annuler n’écrit rien (25.1s)

  1) [chromium] › e2e/home-employee-calendar-widgets.flow.spec.ts:33:3 › Accueil collaborateur — widgets calendrier des absences / emploi du temps › affiche les 2 widgets avec le mois en cours

    Error: expect(locator).toBeVisible() failed

    Locator: getByRole('heading', { name: 'Espace collaborateur' })
    Expected: visible
    Timeout: 15000ms
    Error: element(s) not found

    Call log:
      - Expect "toBeVisible" with timeout 15000ms
      - waiting for getByRole('heading', { name: 'Espace collaborateur' })


      28 |     }
      29 |
    > 30 |     await expect(employeeHome).toBeVisible({ timeout: 15_000 });
         |                                ^
      31 |   });
      32 |
      33 |   test('affiche les 2 widgets avec le mois en cours', async ({ page }) => {
        at /home/youpiwaza/code/cronexia-gta-front-v2/app/e2e/home-employee-calendar-widgets.flow.spec.ts:30:32

    Error Context: test-results/home-employee-calendar-wid-d6539-dgets-avec-le-mois-en-cours-chromium/error-context.md

  2) [chromium] › e2e/home-employee-calendar-widgets.flow.spec.ts:42:3 › Accueil collaborateur — widgets calendrier des absences / emploi du temps › navigation mois précédent/suivant met à jour le libellé et le bouton "retour"

    Error: expect(locator).toBeVisible() failed

    Locator: getByRole('heading', { name: 'Espace collaborateur' })
    Expected: visible
    Timeout: 15000ms
    Error: element(s) not found

    Call log:
      - Expect "toBeVisible" with timeout 15000ms
      - waiting for getByRole('heading', { name: 'Espace collaborateur' })


      28 |     }
      29 |
    > 30 |     await expect(employeeHome).toBeVisible({ timeout: 15_000 });
         |                                ^
      31 |   });
      32 |
      33 |   test('affiche les 2 widgets avec le mois en cours', async ({ page }) => {
        at /home/youpiwaza/code/cronexia-gta-front-v2/app/e2e/home-employee-calendar-widgets.flow.spec.ts:30:32

    Error Context: test-results/home-employee-calendar-wid-a4150-ibellé-et-le-bouton-retour--chromium/error-context.md

  2 failed
    [chromium] › e2e/home-employee-calendar-widgets.flow.spec.ts:33:3 › Accueil collaborateur — widgets calendrier des absences / emploi du temps › affiche les 2 widgets avec le mois en cours
    [chromium] › e2e/home-employee-calendar-widgets.flow.spec.ts:42:3 › Accueil collaborateur — widgets calendrier des absences / emploi du temps › navigation mois précédent/suivant met à jour le libellé et le bouton "retour"
  7 skipped
  13 passed (36.6s)
error: script "test:e2e" exited with code 1
