# Projektin Changelog #

## Viikko 3 ##
- 3.11. & 4.11.
    - Rakenteet
    - Poetry
    - .gitignore
    - configparser
    - pylint
    - pytest
    - Dependabot otettu käyttöön
    - Luotu pääohjelma, luokka/moduuli esittämään issueita, moduuli lukemaan CSV-tiedosto ja palauttamaan data dictinä
    - Testit luoduille moduuleille
    - Generoitu testidata, jolla voidaan testata CSV-lukijamoduulia

- 10.11.
    - Lisätty invoke, jolle käskyt: test (ajaa yksikkötestit), lint (suorittaa autopepin ja linttaa), autopep (suorittaa autopepin), coverage ja coverage-report (testikattavuus).
    - Työnkulkuun main.yml lisätty linttaus ja yksikkötestit.
    - CodeQL-työnkulku lisätty. Laitetty ajamaan vain, jos src-kansion tiedostoihin tulee muutoksia.
    - Muutettu Issue-luokkaa käyttämään konstruktorissa dictionarya, jotta konstruktoriin ei tule yli seitsemää parametria. Refaktoroitu yksikkötestit luokalle.

- 13.11.
    - Refaktoroitu paketin rakennetta vastaamaan esimerkkien rakennetta (services, entities, tests, resources)
    - Lisätty JSON-reader, joka hakee mäppäyksen GitLabin ja Jiran kenttien välillä
    - CSVReader muutettu tilalliseksi objektiksi, joka luomishetkellä ottaa attribuuteikseen CSV-tiedostojen sijainnit ja mäppäystiedoston sijainnin.
    - CSVReader suorittaa yhdellä käskyllä halutun GitLabista otetun eksport-tiedoston muutpksen Jiraan sopivaksi import CSV:ksi.

- 14.11. & 15.11.
    - Koodin refaktorointia: issue.py:n konstruktori muutettu käyttämään dictionarya, ettei lintteri herjaa
    - Lisätty lyhyt sample-csv testejä varten
    - Uudelleenkirjoitettu testit kaikille luokille
    - Lisätty json_reader.py käyttämään with'iä.
    - Lisätty varmistukset issue.py -luokkaan, etteivät instanssit koeta editoida tyhjiä käyttäjäkenttiä tai timestampeja

- 19.11. & 20.11.
    - Dokumentaatio kuntoon
    - Koodit CSV-lukijalle, koodikattavuus 100%

## Viikko 4 ##

- 22.11.
    - Toiminnallisuus, jolla kaikki data haetaan GitLabin tarjoaman REST APIn kautta
    - Konfiguraatioiden siirtäminen config.cfg ja .env
    - Comment-entiteetin luominen kuvaamaan kommenttia
    - Päivitetty mapping.json -tiedostoon uudet kentät (UID, URL ja muuta)

- 23.11.
    - Tuotetun CSV-tiedoston kirjoittaminen muutettu pandasilla tehtäväksi.
    - Tuotettu CSV sisältää nyt myös kaikki issueen liitetyt kommentit formaatissa "aika; tekijä; sisältö". Kaikki kommentit ovat flat listinä.
    - Linttaus 100%
    - Refaktoroitu pois GUI:sta haettavan eksportin lukemiseen tarkoitetut toiminnot
    - Korjattu testit refaktoroinnin jäljiltä.

- 24.11.
    - Yksikkötestit comment.py, issue.py ja paginator.py
    - Asetuksen tyypityksen validaation perusta luotu kansioon typing -> settings.py

- 25.11.
    - Arkkitehtuuri.md
    - Vaatimusmäärittelyn päivitys
    - README.md:n päivitys

- 27.11.
    - Refactor: created reconstructor.py to deconstruct label data and write each label into a separate colun in a csv

- 28.11.
    - Täydennetty ja korjattu CSVServicesin testit vastaamaan uusia toiminnallisuuksia
    - Refaktoroitu ja täydennetty luokkaa Comment ja päivitetty testit luokalle

- 29.11.
    - Refaaktoroitu reconstructor.py
    - Test coverage reconstructor.py ->s 75%

- 30.11.
    - Test coverage for reconstructor.py to 100%
    - Refaktoroituy reconstructor.py
    - Korvatty .copy() metodit deepcopylla
    - Refaktoroitu asetusten noutaminen: delegoitu settings_getter.py -moduulille

- 1.12.
    - Lisätty tuki sille, että issuet voidaan hakea joko groupin tai projektin tasolla. Aiemmin ohjelmassa oli puute: pystyi hakemaan vain groupille.
    - settings_getter.py -luokan testit
    - Refaktoroitu testit
    - CSV:n siistintä: Numeroidut kentät (Comments1, Comments2 jne.) muutetaan muotoon 'Comments'. Nopeuttaa CSV-tiedoston importtausta Jiraan huomattavasti.

- 2.12.
    - CSV_reader.py testit loppuun
    - Asetusten validaatio

- 3.12.
    - Dokumentaation päivitykset: README.md, tuntikirjanpidon tarkistus, changelogin tarkistus
    - Sekvenssikaavion raakaveersio arkkitehtuuri.md -tiedostoon

- 4.12.
    - Päivitetty luokkakaavio arkkitehtuuri.md'hen
    - SettingsValidatorin validointi lopuille ominaisuuksille, refaktorointi, testit

- 5.12.
    - Docstringit lisätty: settings.py, settings_getter.py, comment.py
    - GitHub Release viikolle 5

- 6.12.
    - Käyttäjänimien formatointi sähköposteiksi issuen assignee- ja reporter-kentille.
    - Käyttäjänimien formatointi sähköposteiksi comment-olioiden käyttäjänimille.
    - Käyttäjänimien formatointi sähköposteiksi watcher-kentän käyttäjänimille.

- 7.12.
    - Formatter.py refaktorointi ja yksikkötestit

- 8.12.
    - Formatter.py refaktorointi ja yksikkötestit
    - Issue.py refaktorointi ja yksikkötestien korjaus
    - SettingsValidator.py refaktorointi, päivitys ja testien päivitys

10.12.
    - Lisätty toiminnallisuus ,jossa etukäteen määritellyn konfiguraation mukaan voidaan purkaa projektissa käytetyt labelit omaan sarakkeeseensa tulkatulla arvolla. Esim. Prio 1 -label, voidaan tulkata olemaan Jiran kentän 'Priority' ja arvo 'Highest'
    - Lisätty validaatiota annettaville syötteille
    - Päivitetty asetuksien testejä.

11.12.
    - Lisätty validaatio tuki domaineille: doaminin nimessä voi esiintyä myös '-' merkki. Luotu testit.