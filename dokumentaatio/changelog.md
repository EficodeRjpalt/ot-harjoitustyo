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