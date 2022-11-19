# Issueiden GitLabist Jiraan Siirtäjä #
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
- Vaatimusmäärittely
- Arkkitehtuurikuvaus
- Testausdokumentti
- Työaikakirjanpito
- [Changelog](dokumentaatio/changelog.md)

## Viikko 2 ##


## Viikon 3 ##

### Ohjelmistotyön Backlog ###
Ohjelmistotyön [backlogi](https://github.com/EficodeRjpalt/ot-harjoitustyo/milestone/1) viikolle 3. Viikon 3 tavoitteena on saada MVP-tason toiminnallisuus, jolla GitLabin issuet voidaan muuntaa CSV-tiedostoksi, joka voidaan importata helposti Jiraan. Lisäksi tavoitteena on, että importattujen tiedostojen Description-kenttä formatoidaan käyttämään Jiran markup languagea.
