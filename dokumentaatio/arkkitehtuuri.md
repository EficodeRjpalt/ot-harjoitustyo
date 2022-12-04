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
Sovellus hyödyntää seuraavia ulkopuolisia kirjastoja:
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
- Reconstructor
- SettingsGetter

Formatter-luokka hyödyntää komponentteja Issue ja Comment, jotka ovat objekteja, joiden tarkoitus on mallintaa käsiteltäviä entiteettejä, eli issueita ja komponentteja. Pakkauksen hakemistossa 'typesets' löytyvät ohjelman käyttävät tyypityksen validaattori, SettingsValidator, jolla pyritään varmistamaan, että ohjelmalle annetaan oikeassa muodossa oikean tyyppistä dataa suoritusta varten.

Ohjelam alustaa suorituksensa siten, että JSONReader noutaa `mapping.json` -tiedostosta asetukset sille kuinka GitLabin issueiden kentät mäpätään Jiran vastaaviin kenttiin.
Ohjelman suorituksen konfiguraatiot ovat config.cfg -tiedostossa. Ohjelman alkuun SettingsGetter-olio purkaa konfiguraatiotiedoston konfiguraatiot dictionary-formaattiin. SettingsValidator-moduuli vastaa asetusten validoinnista: asetuksien tyypitys tarkastetaan ja merkkijonomuotoiset syötteet tarkastetaan regexp-lausekkeita vasten. Jos syötteet ovat virheellisiä, nostaa validaatori errorin.
Seuraavaksi DataFetcher-oliolle annetaan noudettavan datan asetukset ja se kutsuu puolestaan Paginator-oliota, joka suorittaa varsinaiset HTTP-kyselyt, kyselyjen vastuasten sivuttamisen ja tulosten kokoamisen.
DataFetcher-olio palauttaa kootut tulokset dict-muodossa.
Formatter-olio käsittelee ensin palautetut tulokset muuttaen ne halutussa formaatissa oleviksi dicteiksi, jonka jälkeen em. dictit muutetaan Issue-luokan olioiksi, jotka palautetaan listana.
Lista annetaan Formatter-oliolle, joka poimii jokaisesta Issue-oliosta tiedon niihin liittyvien kommenttien URL:n sijainnista. Tieto annetaan DataFetcher-oliolle kautta Paginator-oliolle, joka hakee, sivuttaa ja kokoaa kaikki kommentit, jotka Formatter-olio liittää Issue-olioon.
Ennen tietojen kirjoittamista CSV-tiedostoon Reconstructor-olio purkaa määritellyt attribuutit (Labels, Comments ja/tai Watchers) niin, että jokaisen attribuutin listna alkiot siirretään omiin sarakkeisiinsa. Sarakkeet foramtoidaan niin, että niillä on kaikilla sama nimi.
Lopuksi ohjelma kirjoittaa pandas-kirjastoa hyödyntäen Issue-olioiden attribuutit CSV-tiedostoon.

## Luokkakaavio ##
```mermaid
 classDiagram
        JSONReader "1" -- "1" main
	SettignsGetter "1" -- "1" main
	SettingsValidator "1" -- "1" SettingsGetter
        CSVServices "1" -- "1" main
        DataFetcher "1" ..> "1" Paginator
        DataFetcher "1" -- "1" main
        Paginator "1" -- "1" main
        Formatter "1" ..> "1" DataFetcher
        Formatter "1" -- "1" main
        Formatter -- Issue
        Formatter -- Comment
        Issue "1" -- "*" Comment
	Reconstructor "1" -- "1" main
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
	
	class Reconstructor {
	    + reconstruct_all_issue_dict_attributes(header_mappings: dict, issue_dict_list: list, deconst_attributes: list)
	    + reformat_tmp_issue(tmp_issue: Issue, deconst_attribute: str)
	    + get_max_count(list_of_issues: list, attribue_name: str)
	    + generate_list_appendix(max_labels: int, attribute_type: str)
	    + check_spaces_from_attr (check_type: str, attribute: str)
	    + update_headers(header_mappings: dict, header_appendix: list)
	}
	
	class SettingsGetter {
	    - config (ConfigParser)
	    + get_http_request_settings()
	    + get_header_mappings()
	    + create_endpoint(scope: str)
	    + get_deconstruction_attributes()
	}
	
	class SettingsValidator {
	    + validate_http_settings (settings: dict)
	    + validate_url (url: str)
	    + validate_domain_name (domain_name: str)
	    + validate_gl_pat (gl_pat: str)
	    + validate_scope_type (scope_type: str)
	    + validate_scope_id (scope_id: str)
	}
```

## Ohjelman sekvenssikaavio ##

```mermaid
sequenceDiagram
	autonumber
	participant main
	main ->> DataFetcher: init
	DataFetcher ->> Paginator: init
	main ->> SettingsGetter: get http request settings
	activate SettingsGetter
	SettingsGetter ->> ConfigParser: parse configs
	activate ConfigParser
	ConfigParser ->> SettingsGetter: return configs
	deactivate ConfigParser
	SettingsGetter ->> SettingsValidator: validate/invalidate settings
	activate SettingsValidator
	SettingsValidator ->> settingsGetter: validate / raise exception
	deactivate SettingsValidator
	SettingsGetter ->> main: return http settings
	deactivate SettingsGetter
    main ->> SettingsGetter: get header mappings
	activate SettingsGetter
	SettingsGetter ->> JSONReader: get header mappings
	activate JSONReader
	JSONReader ->> SettingsGetter: header mappings (dict)
	SettingsGetter ->> main: header mappings
	deactivate SettingsGetter
	main ->> SettingsGetter: get deconst attributes
	activate SettingsGetter
	SettingsGetter ->> ConfigParser: parse configs
	activate ConfigParser
	ConfigParser ->> SettingsGetter: return configs
	deactivate ConfigParser
	SettingsGetter ->> SettingsValidator: validate/invalidate settings
	activate SettingsValidator
	SettingsValidator ->> settingsGetter: validate / raise exception
	deactivate SettingsValidator
	SettingsGetter ->> main: return deconstruction attributes (list)
	deactivate SettingsGetter
	main ->> DataFetcher: fetch data
	activate DataFetcher
	DataFetcher ->> Paginator: get paginated results
	activate Paginator
	Paginator ->> DataFetcher: return collected results
	deactivate Paginator
	DataFetcher ->> main: return fetched issue data
	deactivate DataFetcher
	main ->> Formatter: format fetched issues
	activate Formatter
	Formatter ->> main: return formatted issues
	Formatter ->> Issue: turn dicts into Issue objects
	activate Issue
	Issue ->> Formatter: return Issue object
	deactivate Issue
	Formatter ->> Comment: fetch comment data
	activate Comment
	Comment ->> DataFetcher: get comment data
	activate DataFetcher
	DataFetcher ->> Paginator: get paginated results
    activate Paginator
    Paginator ->> DataFetcher: return collected results
    deactivate Paginator
    DataFetcher ->> Comment: return collected comment data
    deactivate DataFetcher
    Comment ->> Formatter: 
    Formatter ->> Issue: append Comments to issue
    Formatter ->> DataFetcher: get participant info
    activate DataFetcher
    DataFetcher ->> Paginator: get participant information
    activate Paginator
    Paginator ->> DataFetcher: return participant information
    deactivate Paginator
    DataFetcher ->> Formatter: return participant information
    deactivate DataFetcher
    Formatter ->> Issue: append participant data to issue
	deactivate Formatter
	main ->> Reconstructor: reconstruct all issues
	activate Reconstructor
	Reconstructor ->> main: return reconstructed issues
	deactivate Reconstructor
	main ->> CSVTool: write issues into CSV
```

## Tietojen pysyväistallennus ##
Ohjelma hakee alkuun GitLabin REST API:sta halutun skoopin mukaisen datan ja ohjelman päätteeksi tuottaa artefaktina CSV-tiedoston, joka voidaan importoida Jiraan.

## Ohjelman rakenteelliset heikkoudet ##
- Issue-luokalle on delegoitu sellaisia vastuita, jotka saattaisivat paremmin kuulua Formatter-luokalle.
- Tyypityksen tarkastus on tällä hetkellä riittämätön.
- Testit Paginator.py:lle vaativat vielä hiomista, jotta ne nappaavat normaalit käyttötapaukset ja mahdolliset virhetapaukset.
- Noudetun datan muuntaminen HTTP-pyynnön palauttamasta datasta dictionaryksi on kovakoodattu Paginator.py'hyn. Kestävämpi ratkaisu olisi luoda erillinen tiedosto, johon voisi keskitetysti koota näidenkin asetukset.
