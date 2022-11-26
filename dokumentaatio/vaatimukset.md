# Migraatiotyökalu issueiden siirtämiselle GitLabista Jiraan #

## Toteutusteknologia ##

Sovellus toteutetaan pääosin Pythonilla, joskin markdown-formaattia Jiran markup-formaattiin muuttava kirjasto löytyy vain Javascriptille. Vaadittua skriptaa voidaan kutsua Python-ohjelman sisältä.

- [x] Ohjelma tuottaa artefaktina CSV-tiedoston, joka voidaan importoida Jiraan Jiran Import Wizardilla.

## Toiminnalliisuudet ##

- [x] Ohjelma pystyy hakemaan repositorio-kohtaisesti kaikki issuet halutusta GitLab-instanssista. Issuet voidaan noutaa joko kutsumalla instanssin REST APIa tai vaihtoehtoisesti ottamalla ohjelmasta CSV-eksportti.

- [x] Ohjelma pystyy täydentämään haettua dataa hakemalla jokaiseen issueen liittyvät kommentit.
- [ ] Kommentit siirretään Jira-instanssiin ja sidotaan siellä vastaavaan käyttäjään. 
- [ ] Issueiden description-kentän ja kommenttien teksti-kentän tulee olla muutettu markdown-formaatista Jiran omaan markup-syntaksiin.
- [ ] Ohjelman tulee tuoda mukana kaikki GitLabin skoopissa käytetyt labelit Jiraan
- [ ] Ohjelman tulee tuoda mukana myös tieto kaikista GitLabin issuessa mukana olleista participanteista Jiran Watcher-kenttään
- [ ] Ohjelma tarjoaa suorituksen aikaisen informatiivisen loggauksen ja sen lisäksi kirjoittaa jokaisesta suorituksesta login, josta löytyvät tiedot soritusaikana siirretystä datasta jne.
- [ ] Kun ohjelma on suorittanut eksportaation/importaation, ohjelma luo Google Sheetsiin raportin siirretystä datasta. Raportin tarkoitus on toimia projektin lokina, josta voidaan nopeasti tarkastaa mitä dataa kullakin operaatiolla on siirretty.
- [ ] gitLabista poistettujen käyttäjien kommentit ja toiminnot täytyy pystyä käsittelemään mielekkäällä tavalla. Tällä hetkellä ne ovat nimellä 'Ghost User.

## Siirrettävä data ##

- Asiakkaan kanssa on sovittava mikä data on siirrettävä ja kuinka se mäpätään Jiran päässä. Ohessa lista siirrettävistä kentistä ja niiden vastikekappaleista Jirassa.

## Käyttäjien hallinta ##

- GitLabin käyttäjät pyritään yhdistämään oikeisiin käyttäjiin Jirassa. Tätä varten on selvitettävä asiakkaan kanssa kuinka käyttäjiä hallitaan kummassakin päässä ja voidaanko käyttäjät liittää toisiinsa yksiselitteisen attribuutin avulla. Jira tunnistaa käyttäjän uniikista sähköpostiosoitteesta.

- Asiakkaan kanssa on määriteltävä mitä tehdä sellaisessa tapauksessa, jossa käyttäjä löytyy GitLabista, mutta ei Jirasta.

## Muuta ##
