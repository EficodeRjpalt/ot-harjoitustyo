# Migraatiotyökalu issueiden siirtämiselle GitLabista Jiraan #

## Toteutusteknologia ##

Sovellus toteutetaan pääosin Pythonilla, joskin markdown-formaattia Jiran markup-formaattiin muuttava kirjasto löytyy vain Javascriptille. Vaadittua skriptaa voidaan kutsua Python-ohjelman sisältä.

- [x] Ohjelma tuottaa artefaktina CSV-tiedoston, joka voidaan importoida Jiraan Jiran Import Wizardilla.

## Toiminnalliisuudet ##

- [x] Ohjelma pystyy hakemaan repositorio-kohtaisesti kaikki issuet halutusta GitLab-instanssista. Issuet voidaan noutaa joko kutsumalla instanssin REST APIa tai vaihtoehtoisesti ottamalla ohjelmasta CSV-eksportti.

- [x] Ohjelma pystyy täydentämään haettua dataa hakemalla jokaiseen issueen liittyvät kommentit.
- [x] Ohjelmaan on mahdollista konfiguroida confif.cfg -tiedostoon jokaisen ajon aikaiset konfiguraatiot.
- [x] Ohjelman tulee tuoda mukana kaikki GitLabin skoopissa käytetyt labelit Jiraan
- [x] Ohjelman tulee tuoda mukana myös tieto kaikista GitLabin issuessa mukana olleista participanteista Jiran Watcher-kenttään
- [x] Ohjelman tuottama CSV-tiedosto on formatoitu niin, että se on mahdollisimman helppoa ajaa sisään Jira-instanssiin.
    - [x] Kentät, joilla on useampi arvo Jirassa, on oltava purettu CSV'hen muodossa, jossa jokaisen uniikin arvon kolumnin nimi on sama. (Watcher, Watcher, Watcher eikä Watcher1, Watcher2, Watcher3)
- [ ] Ohjelman tulee antaa mielekkäät virheilmoitukset sille tuleien syötteiden suhteen.
    - [x] Suoritukselle annettavat konfiguraatiot tulee validoida.
    - [ ] GitLabin rajapinnan vastaukset tulee käsitellä ja tarkastaa. Minimissään ohjelman tulee antaa mielekästä palautetta, jos HTTP-pyyntöön vastataan jollain muulla kuin koodilla 200.
- [x] Kommentit siirretään Jira-instanssiin ja sidotaan siellä vastaavaan käyttäjään. Tämä tapahtuu muuttamalla käyttäjän nimi haluttuun sähköpostiosoitteeseen (käyttäjien uniikki nimi Jira Cloudissa on sähköposti)
    - [x] Käyttäjällä tulee olla mahdollisuus antaa ohjelmalle lista, jossa on mäppäykset nimien ja sähköpostien välillä. Jos nimi ei löydy listalta, ohjelma rakentaa käyttäjäniemestä sähköpostiosoitteen, joka voidaan vielä validoida importatessa.
    - [x] gitLabista poistettujen käyttäjien kommentit ja toiminnot täytyy pystyä käsittelemään mielekkäällä tavalla. Tällä hetkellä ne ovat nimellä 'Ghost User.
- [x] Käyttäjän tulee pystyä antamaan ohjelmalle konfiguraatio siitä kuinka labeleissa oleva tieto tulee purkaa. Esimerkiksi label 'In Progress' pitää voida purkaa niin, että kun issue siirretään Jiraan, sille asetetaan kenttään Status arvo 'In Progress'. Mäppäys tapahtuu luomalla konfiguraatiot ennen ajoa määrättyy nkonfiguraatiotiedostoon.
- [ ] Ohjelma tarjoaa suorituksen aikaisen informatiivisen loggauksen ja sen lisäksi kirjoittaa jokaisesta suorituksesta login, josta löytyvät tiedot soritusaikana siirretystä datasta jne.
- [ ] Issueiden description-kentän ja kommenttien teksti-kentän tulee olla muutettu markdown-formaatista Jiran omaan markup-syntaksiin.
- [ ] Ohjelman tulee tarjota käyttäjälle mahdollisuus käyttää GitLabissa olevia käyttäjien sähköpostiosotteita käyttäjämäppäyksen ja nimen pohjalta rakennetun sähköpostiosoitteen sijaan.

## Siirrettävä data ##

- Asiakkaan kanssa on sovittava mikä data on siirrettävä ja kuinka se mäpätään Jiran päässä. Ohessa lista siirrettävistä kentistä ja niiden vastikekappaleista Jirassa.

## Käyttäjien hallinta ##

- GitLabin käyttäjät pyritään yhdistämään oikeisiin käyttäjiin Jirassa. Tätä varten on selvitettävä asiakkaan kanssa kuinka käyttäjiä hallitaan kummassakin päässä ja voidaanko käyttäjät liittää toisiinsa yksiselitteisen attribuutin avulla. Jira tunnistaa käyttäjän uniikista sähköpostiosoitteesta.

- Asiakkaan kanssa on määriteltävä mitä tehdä sellaisessa tapauksessa, jossa käyttäjä löytyy GitLabista, mutta ei Jirasta.

## Muuta ##
