# Issueiden GitLabista Jiraan Siirtäjä #
Yksinkertaisen CLI-sovelluksen avulla käyttäjän on mahdollista siirtää issuensa GitLabista Jiraan käyttämällä Jiran tarjoamaa Import Wizardia.

Ohjelma noutaa GitLabin REST API:sta haluttujen parametrien mukaisesti kaikki groupin tai projektin alle sijoittuvat issuet ja kirjoittaa ne CSV-tiedostoon muodossa, jossa Jira:n Import Wizard pysty lukemaan datan ja luomaan sen pohjalta uudet issuet Jiraan.

Noudettu data formatoidaan sellaiseen muotoon, jossa se voidaan saumattomasti importoida haluttuun Jira-instanssiin.

## Mitä dataa siirretään ##

Ohjelma siirtää tällä hetkellä GitLabin issueista seuraavat kentät:
- Title
- Description
- State
- Author
- Assigne (vain yksi, koska Jirassa vastaava kenttä sallii vain yhden käyttäjän)
- Due Date
- Created At
- Closed At
- Milestone
- Labels
- Time Estimate
- Time Spent
- Issue ID

Lisäksi issueen liittyvät kommentit liitetään mukaan listana. Mukana tuelvat kentät ja niiden mäppäykset löytyvät [mapping.json](src/resources/mapping.json)-tiedostosta.

## Huomioita Toteutuksestsa ##

Ideaalitapauksessa ohjelma lukisi datan GitLabin rajapinnasta ja kirjottaisi tiedon suoraan Jiran REST API:n kautta. On kuitenkin muutamia asiakasvaatimuksiin littyviä syitä, minkä takia CSV import on kannattavampi keino. Ohessa listattuna syitä:
- Kommentteja on mahdotonta migratoida REST API:n kautta. Kommentteja voi lisätä REST API:n kautta, mutta ne eivät säilytä alkuperäistä aikaleimaansa ja alkuperäistä kommentoijaansa. Sen sijaan niihin tulee kommentin luontiajan aikaleima ja kommentin luoneen henkilön nimi.
- Monilla tiimeillä on eri määritelmät eri kentissä käyttämilleen arvoille, josta johtuen CSV importterin tarjoama mäppäyvaihe tuo lisaa joustoa migraatioprosessiin. Ts. migraatiota suorittava henkilö voi vielä importaatiohetkellä suorittaa uudelleenmäppäyksiä asiakasvaatimusten mukaisesti koskematta ohjelman koodiin.

# Python -versiosta #

Projekti on testattu Python-versiolla 3.10. Tukea vanhempien versioiden kanssa ei taata.

# Ennakkovaatimukset #

1. Jotta ohjelmaa voi käyttää/testata, tarvitsee käyttäjällä olla pääsy johonkin GitLabin projektiin tai groupiin ja oikeudet katsoa kys. groupin tai projektin issueita.
2. Käyttäjällä tarvitsee olla luotu vaaditun groupin sisällä voimassa oleva Personal Access Token (ohjeet [täällä](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)).
3. Tokenilla tarvitsee olla skooppina `api` ja `read_api`.

# Dokumentaatio #

- Käyttöohje
- [Vaatimusmäärittely](dokumentaatio/vaatimukset.md)
- [Arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)
- Testausdokumentti
- [Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Changelog](dokumentaatio/changelog.md)

## Ulkoiset resurssit ##
- [GitLabin issueiden API-dokumentaatio](https://docs.gitlab.com/ee/api/issues.html)

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

[COMMON]
baseURL=https://gitlab.com/

[ISSUE]
state=all
per_page=100
scope_id=55156717

[COMMENT]
per_page=20
```
**FILEPATHS**

`input`: määrittää mistä ohjelam lähtee etsimään sille annettacaa CSV-tiedostoa, joka muunnetaan.
`input_short`: on yksikkötestien käyttämä kohde, jossa on lyhennetty datamäärä käytössä.output
`output`: määrittää minne lopputulos kirjoitetaan. Oletusarvoisesti kirjoitetun CSV-tiedoston nimi on `output.csv`.
`mapping.json`: sisältää kartoituksen siitä miten GitLabin issue fieldit mäpätään Jiran kenttiin.

**COMMON**

Sektiot COMMON, ISSUE ja COMMENT määrittävät issueiden ja kommenttien hakemiseen liittyvät HTTP-kyselyn parametrit.
`baseURL`: Määrittää GitLab-instanssin baseURL:n. Esim. https://gitlab.com/

**ISSUE**

`state`: Määrittää missä tilassa olevat issuet otetaan haun skooppiin. Vaihtoehdot ovat `opened`, `closed` tai `all`.
`per_page`: Kuinka monta tulosta yhdelle kyselylle halutaan palautettavan. Rajapinnan maksimiarvo on 100 issueta kerrallaan ja oletusarvo 20.
`scope_id`: Määrittää minkä skoopin sisältä issuet haetaan. Tarkempaa tietoa [täällä](https://docs.gitlab.com/ee/api/issues.html#list-project-issues). Huomaa, että käyttämällä id:tä haetaan aina _kaikki_ groupin alla olevat issuet jokaisesta sen alle sijoitetusta groupista ja projektista.

**Huom!** Helpoin tapa löytää ym. ID on suoraan GUI:n kautta menemällä projektin/groupin sivulle ja ottamalla ID projektin/groupin nimen alta. Esim: <img width="342" alt="image" src="https://user-images.githubusercontent.com/91126255/204075906-757a465d-8397-4fc4-a4dc-edf4714eae5c.png">

### Salaisuudet ###
Suoritusaikaiset salaisuudet löytyvät `.env`-tiedostosta. Tiedoston skeema löytyy repositorion juuressa olevasta tiedostosta sample.env.

`GL_PAT`: sisältää käyttäjän Personal Access Tokenin. Ks. ennakkovaatimukset kys. tokenin hankkimiseksi.


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
