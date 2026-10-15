❯ docker compose exec -T db mariadb \
  -uasqatasunDatabaseUserLogin -pasqatasunDatabaseUserP4ssword asqatasun <<'SQL'
SELECT * FROM SCENARIO\G
SHOW CREATE TABLE SCENARIO;
SQL
*************************** 1. row ***************************
         Id_Scenario: 1
    Date_Of_Creation: 2026-10-15 15:46:50
               Label: Test des pages en tant que gestionnaire RH
             Content: {
  "id": "91dbb395-d61f-41ce-8e66-de8db835f543",
  "version": "2.0",
  "name": "Cronexia se connecter en tant que pierre-olivier.courtois et acceder au planning",
  "url": "http://host.docker.internal:4173",
  "tests": [{
    "id": "be244ad7-a20a-4693-80f9-159a22cd35b9",
    "name": "Test 1",
    "commands": [{
      "id": "6ad2a850-f76b-42a2-99f3-31c16f713f22",
      "comment": "",
      "command": "open",
      "target": "/login",
      "targets": [],
      "value": ""
    }, {
      "id": "a61750b9-f536-40e8-9663-e65fb8bc1c0a",
      "comment": "",
      "command": "executeScript",
      "target": "const login = document.querySelector(\"md-outlined-text-field[name='login']\"); const password = document.querySelector(\"md-outlined-text-field[name='password']\"); login.value = 'pierre-olivier.courtois'; password.value = 'P!zz@&T@c0$#FTW'; login.dispatchEvent(new Event('input', { bubbles: true })); password.dispatchEvent(new Event('input', { bubbles: true }));",
      "targets": [],
      "value": ""
    }, {
      "id": "dad8388b-a68c-4421-8ec7-f641895ac123",
      "comment": "",
      "command": "click",
      "target": "xpath=//md-filled-button[contains(.,'Se connecter')]",
      "targets": [],
      "value": ""
    }, {
      "id": "50736359-7a7e-4c6f-9e08-a9a98c2c3005",
      "comment": "",
      "command": "waitForElementNotPresent",
      "target": "css=.auth-form__submit",
      "targets": [],
      "value": "15000"
    }, {
      "id": "e152ddd5-0050-4226-85c7-71c05171cadd",
      "comment": "",
      "command": "open",
      "target": "/collective-schedule/population/All_Resources/resource/all/dateStart/2024-04-01/dateEnd/2024-04-14",
      "targets": [],
      "value": ""
    }, {
      "id": "b7c1d2e3-f4a5-6789-abcd-ef0123456789",
      "comment": "",
      "command": "pause",
      "target": "3000",
      "targets": [],
      "value": ""
    }]
  }],
  "suites": [{
    "id": "8ff689b3-98d2-40d7-ab17-bbcd2c9808ed",
    "name": "Default Suite",
    "persistSession": false,
    "parallel": false,
    "timeout": 300,
    "tests": ["be244ad7-a20a-4693-80f9-159a22cd35b9"]
  }],
  "urls": ["http://host.docker.internal:4173/"],
  "plugins": []
}

         Description: NULL
CONTRACT_Id_Contract: 2
Table   Create Table
SCENARIO        CREATE TABLE `SCENARIO` (\n  `Id_Scenario` bigint(20) NOT NULL AUTO_INCREMENT,\n  `Date_Of_Creation` datetime NOT NULL,\n  `Label` varchar(255) NOT NULL,\n  `Content` mediumtext NOT NULL,\n  `Description` varchar(255) DEFAULT NULL,\n  `CONTRACT_Id_Contract` bigint(20) NOT NULL,\n  PRIMARY KEY (`Id_Scenario`),\n  KEY `INDEX_TGSI_SCENARIO_CONTRACT_Id_Contract` (`CONTRACT_Id_Contract`),\n  CONSTRAINT `FK_TGSI_SCENARIO_TGSI_CONTRACT` FOREIGN KEY (`CONTRACT_Id_Contract`) REFERENCES `CONTRACT` (`Id_Contract`) ON DELETE CASCADE ON UPDATE CASCADE\n) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci
