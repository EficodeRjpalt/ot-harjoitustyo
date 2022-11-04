# Projektin Changelog #

## Viikko 3 ##
- Projektin setuppaaminen
    - Rakenteet
    - Poetry
    - .gitignore
    - configparser
- Luotu pääohjelma, luokka/moduuli esittämään issueita, moduuli lukemaan CSV-tiedosto ja palauttamaan data dictinä
- Testit luoduille moduuleille
- Generoitu testidata, jolla voidaan testata CSV-lukijamoduulia

Tavoite:
- Pystyä lukemaan CSV:stä tiedot ja tulostamana ulos formatoidun CSV-tiedoston
    - Markdown-kentät pitää muuttaa Jiran markupiksi
        - Tätä varten tarvitsee olla erillinen js-skripta, joka käsittelee datan
    - Ulostettavien kenttien tulee vastata Jiran kenttien nimiä
    - Tässä vaiheessa ei tarvitse olla mukana vielä kommentteja (Vasta seuraavalla viikolla kommentit)