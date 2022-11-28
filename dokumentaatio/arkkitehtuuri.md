# Arkkitehtuurikuvaus #

## Rakenne ##
Ohjelman komponentit on jaettu kolmeen kategoriaan: entitites, services ja typing.

Entitites-kategorian komponentit mallintavat konkreettisia tietorakenteita kuten tässä tapauksessa Issueta ja Commentia.

Services-kategorian komponentit ovat ohjelman toiminnallisia komponentteja, jotka vastaavat ohjelman toimintalogiikasta.

Typing-kategorian komponentit tarjoavat tyypitustarkastamisen palveluita. Näitä käytetään esimerkiksi asetuksia varten, jotta palveluihin ei livahda väärän tyyppistä dataa.

Lisäksi ohjelmalla on kansio 'resources' joka sisältää ohjelman toimimiselle olennaisia resursseja.

## Käyttöliittymä ##
Sovellus on CLI-pohjainen. Kaikki asetukset säädetään config.cfg tai .env -tiedoston kautta.

## Käytetyt ulkoiset kirjastot ##
Sovellus hyödyntää seuraavia ulkopuolisia sovelluksia:
- Pandas
- Requests
- Typing
- Strongtyping

## Sovelluslogiikka ##
Sovelluksen bisneslogiikasta vastaavat seuraavat komponentit:
- JSONReader
- CSVServices
- DataFetcher
- Paginator
- Formatter

Lisäksi Formatter-luokka hyödyntää komponentteja Issue ja Comment, jotka ovat objekteja, joiden tarkoitus on mallintaa käsiteltäviä entiteettejä, eli issueita ja komponentteja.

Ohjelam alustaa suorituksensa siten, että JSONReader noutaa `mapping.json` -tiedostosta asetukset sille kuinka GitLabin issueiden kentät mäpätään Jiran vastaaviin kenttiin. Tämän jälkeen ohjelma parsii suoritusaikaiset asetukset config.cfg -tiedostosta configparserin avulla.
Seuraavaksi DataFetcher-oliolle annetaan noudettavan datan asetukset ja se kutsuu puolestaan Paginator-oliota, joka suorittaa varsinaiset HTTP-kyselyt, kyselyjen vastuasten sivuttamisen ja tulosten kokoamisen.
DataFetcher-olio palauttaa kootut tulokset dict-muodossa.
Formatter-olio käsittelee ensin palautetut tulokset muuttaen ne halutussa formaatissa oleviksi dicteiksi, jonka jälkeen em. dictit muutetaan Issue-luokan olioiksi, jotka palautetaan listana.
Lista annetaan Formatter-oliolle, joka poimii jokaisesta Issue-oliosta tiedon niihin liittyvien kommenttien URL:n sijainnista. Tieto annetaan DataFetcher-oliolle kautta Paginator-oliolle, joka hakee, sivuttaa ja kokoaa kaikki kommentit, jotka Formatter-olio liittää Issue-olioon.
Lopuksi ohjelma kirjoittaa pandas-kirjastoa hyödyntäen Issue-olioiden attribuutit CSV-tiedostoon.

## Luokkakaavio ##
```mermaid
 classDiagram
        JSONReader "1" -- "1" main
        CSVServices "1" -- "1" main
        DataFetcher "1" ..> "1" Paginator
        DataFetcher "1" -- "1" main
        Paginator "1" -- "1" main
        Formatter "1" ..> "1" DataFetcher
        Formatter "1" -- "1" main
        Formatter -- Issue
        Formatter -- Comment
        Issue "1" -- "*" Comment
        Pandas -- CSVServices
        Requests -- Paginator
		 
        class JSONReader{
        + read_json_to_dict(filepath: str)
        }
        
        class CSVServices {
        + write_issues_to_csv(issue_list: list, out_filepath: str, head_mappings: dict)
        }
        
        class DataFetcher {
            - pager
        + fetch_data(settings: dict, comment_endpoint:str, data_type=str)
        }
        
        class Paginator {
        + get_paginated_results(endpoint: str, params: dict, headers: dict)
        }
        
        class Formatter{
        + format_response_data_to_dict(response_data: list)
            + transform_dict_items_into_issues(dict_list: list)
            + add_comments_to_all_issues(issue_dict_list: list, settings: dict)
        }
        
        class Issue {
        - attributes
            - comments
            + issue_to_dict()
            + displaynaes_to_emails(domain_name: str)
            + timestamps_to_jira()
            + transform_name_to_email(name: str, domain_name: str)
            + transfrm_timestamp_to_jira(timestamp: str)
            + __repr__()
        }
        
        class Comment {
        - timestamp
            - actor
            - body
            + __repr__()
            + __str__()
        }
```

## Tietojen pysyväistallennus ##
Ohjelma hakee alkuun GitLabin REST API:sta halutun skoopin mukaisen datan ja ohjelman päätteeksi tuottaa artefaktina CSV-tiedoston, joka voidaan importoida Jiraan.

## Ohjelman rakenteelliset heikkoudet ##
- Issue-luokalle on delegoitu sellaisia vastuita, jotka saattaisivat paremmin kuulua Formatter-luokalle.
- Tyypityksen tarkastus on tällä hetkellä riittämätön.
- Testit Paginator.py:lle vaativat vielä hiomista, jotta ne nappaavat normaalit käyttötapaukset ja mahdolliset virhetapaukset.
- Noudetun datan muuntaminen HTTP-pyynnön palauttamasta datasta dictionaryksi on kovakoodattu Paginator.py'hyn. Kestävämpi ratkaisu olisi luoda erillinen tiedosto, johon voisi keskitetysti koota näidenkin asetukset.