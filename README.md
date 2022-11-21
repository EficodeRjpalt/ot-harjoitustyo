# Issueiden GitLabista Jiraan Siirtäjä #
Yksinkertaisen CLI-sovelluksen avulla käyttäjän on mahdollista siirtää issuensa GitLabista Jiraan käyttämällä Jiran tarjoamaa Import Wizardia.

Toistaiseksi ohjelma on toteutettu niin, että issuet haetaan projekti- tai ryhmäkohtaisesti ottamalla issueista CSV-eksportti GitLabin graafisesta käyttöliittymstä. Pidemmällä aikavälillä ohjelman on tarkoitus lukea projekti- tai ryhmäkohtainen data suoraan GitLabin API:sta.

Noudettu data formatoidaan sellaiseen muotoon, jossa se voidaan saumattomasti importoida haluttuun Jira-instanssiin.

## Huomioita Toteutuksestsa ##

Ideaalitapauksessa ohjelma lukisi datan GitLabin rajapinnasta ja kirjottaisi tiedon suoraan Jiran REST API:n kautta. On kuitenkin muutamia asiakasvaatimuksiin littyviä syitä, minkä takia CSV import on kannattavampi keino. Ohessa listattuna syitä:
- Kommentteja on mahdotonta migratoida REST API:n kautta. Kommentteja voi lisätä REST API:n kautta, mutta ne eivät säilytä alkuperäistä aikaleimaansa ja alkuperäistä kommentoijaansa. Sen sijaan niihin tulee kommentin luontiajan aikaleima ja kommentin luoneen henkilön nimi.
- Monilla tiimeillä on eri määritelmät eri kentissä käyttämilleen arvoille, josta johtuen CSV importterin tarjoama mäppäyvaihe tuo lisaa joustoa migraatioprosessiin. Ts. migraatiota suorittava henkilö voi vielä importaatiohetkellä suorittaa uudelleenmäppäyksiä asiakasvaatimusten mukaisesti koskematta ohjelman koodiin.

# Python -versiosta #

Projekti on testattu Python-versiolla 3.10. Tukea vanhempien versioiden kanssa ei taata.

# Dokumentaatio #

- Käyttöohje
- [Vaatimusmäärittely](dokumentaatio/vaatimukset.md)
- Arkkitehtuurikuvaus
- Testausdokumentti
- [Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Changelog](dokumentaatio/changelog.md)

# Asennus #

1. Riippuvuudet asenetaan komennolla `poetry install`
2. Ohjelma suoritetaan komennolla `poetry run invoke start`

# Käyttöohjeet #

## Asetukset##
Ohjelman asetukset löytyvät osoitteesta `/src/config.cfg`:
```
[FILEPATHS]
input=src/resources/sample.csv
input_short=src/resources/sample_short.csv
output=src/resources/
mapping=src/resources/mapping.json
```
`input` määrittää mistä ohjelam lähtee etsimään sille annettacaa CSV-tiedostoa, joka muunnetaan.
`input_short` on yksikkötestien käyttämä kohde, jossa on lyhennetty datamäärä käytössä.output
`output` määrittää minne lopputulos kirjoitetaan. Oletusarvoisesti kirjoitetun CSV-tiedoston nimi on `output.csv`.
`mapping.json` sisältää kartoituksen siitä miten GitLabin issue fieldit mäpätään Jiran kenttiin.

## Datan hakeminen GitLabista ##
Tällä hetkellä ohjelma tukee GitLabin graafisen käyttöliittymän kautta haetun export-tiedoston lukemista. Voit hakea uuden tiedoston mistä tahansa GitLabin groupsita tai projektista ja korvata sillä nykyisen `sample.csv` -tiedoston. Ohjeet exportin ottamiseen löytyvät [täältä](https://docs.gitlab.com/ee/user/project/issues/csv_export.html).

# Komentorivitoiminnot #

## Ohjelman suorittaminen ##
Ohjelma suoritetaan komennolla:
`poetry run invoke start`

## Testaus ##
Testit suoritetaan komennolla:
`poetry run invoke test`

## Autopep ja Pylint ##
Autopep ja pylint ajetaan samalla komennolla:
`poetry run invoke lint`

Ajatuksena on, että turha lintata, jos ei ole autopep ajettuna.

## Testikattavuus ##
Testit ja testikattavuusraportti ajetaan komennolla:
`poetry run invoke coverage`
