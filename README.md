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
- Time Estimate
- Time Spent
- Issue ID
- Participants
- Labels

Lisäksi issueen liittyvät kommentit (**poislukien liitetiedostot**) liitetään mukaan. Mukana tuelvat kentät ja niiden mäppäykset löytyvät [mapping.json](src/resources/mapping.json)-tiedostosta.

### Labelsien tulkkaus Jiran kentiksi ###
Viikon 6 releasesta lähtien ohjelma osaa tulkata GitLabissa käytetyt labelit Jiran kentiksi ja antaa niille arvon. Esimerkiksi jos projektissa on käytössä label 'Priority 1', ohjelman voi konfiguroida tulkitsemaan kyseisen labelin olevan Jiran kenttä 'Priority', jolle annetaan arvo 'Highest'. Konfiguraation luomisesta lisää alempana.

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

# Käyttöohjeet #

1. Ohjelma suoritetaan komennolla `poetry run invoke start`
2. Suorituksen jälkeen ohjelma tuottaa juurihakemistoonsa CSV-tiedoston, jonka nimi on formaatissa `<jira_project_key>_dd-MM-yyyy-hh:mm:ss.csv`. Eli sisältää kohdeprojektin avaimen ja aikaleiman.

## Asetukset ##
Ohjelman asetukset löytyvät osoitteesta `/src/config.cfg`:
```
[FILEPATHS]
input=src/resources/sample.csv
input_short=src/resources/sample_short.csv
output=src/resources/
mapping=src/resources/mapping.json
user_mappings=src/resources/user_mapping.csv
label_configs=src/resources/label_configs.json

[COMMON]
baseURL=https://gitlab.com/
domain_name=eficode.com
scope_id=55156717
scope_type=group

[ENDPOINTS]
group=api/v4/groups/
project=api/v4/projects/

[ISSUE]
state=all
per_page=100

[COMMENT]
per_page=20

[WATCHER]
per_page=20

[DECONSTRUCT]
allowed=Comments,Labels,Watchers

[JIRA]
project_key=XYZ
```
**FILEPATHS**

`input`: määrittää mistä ohjelam lähtee etsimään sille annettacaa CSV-tiedostoa, joka muunnetaan.
`input_short`: on yksikkötestien käyttämä kohde, jossa on lyhennetty datamäärä käytössä.output
`output`: määrittää minne lopputulos kirjoitetaan. Oletusarvoisesti kirjoitetun CSV-tiedoston nimi on `output.csv`.
`mapping.json`: sisältää kartoituksen siitä miten GitLabin issue fieldit mäpätään Jiran kenttiin.

**COMMON**

Sektiot COMMON, ISSUE ja COMMENT määrittävät issueiden ja kommenttien hakemiseen liittyvät HTTP-kyselyn parametrit.
`baseURL`: Määrittää GitLab-instanssin baseURL:n. Esim. https://gitlab.com/
`domain_name`: Sähköpostien perään laitettava domain name. Esimerkiksi test.com.
`scope_id`: GitLabin groupille tai projektille annettava uniikki ID, jolla ohjelma osaa hakea oikeaan skooppiin kuuluvat issuet. Tarkempaa tietoa [täällä](https://docs.gitlab.com/ee/api/issues.html#list-project-issues). Huomaa, että käyttämällä id:tä haetaan aina _kaikki_ groupin alla olevat issuet jokaisesta sen alle sijoitetusta groupista ja projektista.
`scope_type`: määrittelee onko yllä annetty ID groupin vai projektin ID. Mahdolliset arvot: "group" ja "project". Riippuen onko kyseessä group vai project, endpoint datan hakemiselle on eri.

**Huom!** Helpoin tapa löytää ym. ID on suoraan GUI:n kautta menemällä projektin/groupin sivulle ja ottamalla ID projektin/groupin nimen alta. Esim: <img width="342" alt="image" src="https://user-images.githubusercontent.com/91126255/204075906-757a465d-8397-4fc4-a4dc-edf4714eae5c.png">

**ENDPOINTS**
Etukäteen määritellyt API:n endpointit group-tason ja project-tason issueiden hakemiselle.

**ISSUE**

`state`: Määrittää missä tilassa olevat issuet otetaan haun skooppiin. Vaihtoehdot ovat `opened`, `closed` tai `all`.
`per_page`: Kuinka monta tulosta yhdelle kyselylle halutaan palautettavan. Rajapinnan maksimiarvo on 100 issueta kerrallaan ja oletusarvo 20.

**COMMENT**

`per_page`: Kuinka monta tulosta yhdelle kyselylle halutaan palautettavan. Rajapinnan maksimiarvo on 100 issueta kerrallaan ja oletusarvo 20.

**WATCHER**

`per_page`: Kuinka monta tulosta yhdelle kyselylle halutaan palautettavan. Rajapinnan maksimiarvo on 100 issueta kerrallaan ja oletusarvo 20.

**DECONSTRUCT**

`allowed`: Määrittää mitkä kentät halutaan "purkaa" useampaan sarakkeeseen CSV-tiedotoon. Jos Jiraan importoidaan CSV:llä issueita, täytyy sellaiset kentät, joissa on useampi arvo (esim. yli 1 label) purkaa useampaan sarakkeeseen. Ks. [täältä](https://support.atlassian.com/jira-cloud-administration/docs/import-data-from-a-csv-file/) lisää tietoa.

**JIRA**

`project_key`: Projektin avain Jirassa. Tietoa käytetään ohjelman tuottaman CSV-tiedoston nimessä: se laitetaan tiedoston etuliitteeksi, jotta käyttäjän on helpompi paikantaa luomansa tiedosto.

### Salaisuudet ###
Suoritusaikaiset salaisuudet löytyvät `.env`-tiedostosta. Tiedoston skeema löytyy repositorion juuressa olevasta tiedostosta sample.env.

`GL_PAT`: sisältää käyttäjän Personal Access Tokenin. Ks. ennakkovaatimukset kys. tokenin hankkimiseksi.

## Asetukset labelien tulkkaamista varten ##
Labelien dekoodaamisen asetukset luodaan kohteeseen [src/resources/label_configs.json](src/resources/label_configs.json). Tiedoston skeema on seuraava:
```
{
    "headers": {
        "Priority": "Normal",
        "Issue Type": "Task",
        "Status": ""
    },
    "labels": {
        "labelname": {
            "field": "Jira Field Name",
            "value": "Jira Field Value"
        }
        
        ...
}
```
Avaimen "labels" alle sijoitetaan kaikki labelit, jotka halutaan tulkata arvollisiksi kentiksi Jirassa. Jokainen label on avain objektille joka sisältää "field" kentässä tiedon siitä minkä kentän nimen labelin arvo saa Jirassa ja "value" kentän, joka sisältää tiedon mikä arvo tuolle kentäle annetaan. Ajon päätteeksi ohjelma käy läpi tuotetun pandas dataframen läpi parsien label-tiedot ja luoden vaadittavat sarakkeet ja niiden tiedot lopulliseen CSV'hen.

## Käyttäjätietojen mäppäys GitLabin ja Jiran välillä ##
Ohjelmalle voi antaa myös listauksen käyttäjistä ja heidän sähköposteistaan Jirassa. Mäppäyksen tekemistä suositellaan kaikissa tapauksissa, jos suinkin mäppäys on saatavilla. Jirassa käyttäjätunnukset on sidottu käyttäjien sähköpostiosotteisiin, joten jos ei ole takeita, että käyttäjillä on käytössä samat sähköpostiosoitteet GitLabissa kuin Jirassa, täytyy suorittaa nimistä erikseen mäppäys. Tällä hetkellä ohjelmalle voi antaa edellä mainitun tiedoston, joka sisältää mäppäyksen. Jos käyttäjä ei löydy tiedostosta, ohjelma generoi käyttäjän sähköpostin muotoon `etunimi.muutnimetjasukunimi@domain.com`.

**Huom!** Tällä hetkellä ohjelma oletusarvoisesti suorittaa käyttäjänimien mäppäyksen. Taustalla on asiakastapauksesta johtuva priorisointi, jossa _EI_ voida käyttää asiakkaan GitLabissa olevia sähköposteja. Projektin backlogilla on lisättynä [feature](#63), jossa mahdollistetaan asetus, jolla voidaan määritellä että kyätetäänkö käyttäjien mäppäystä ja sähköpostin "arvausta" vai haetaanko suoraan käyttäjän sähköposti GitLabista.

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
