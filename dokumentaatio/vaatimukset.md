# Migraatiotyökalu issueiden siirtämiselle GitLabista Jiraan #

## Toteutusteknologia ##

Sovellus toteutetaan pääson Pythonilla, joskin markdown-formaattia Jiran markup-formaattiin muuttava kirjasto löytyy vain Javascriptille. Vaadittua skriptaa voidaan kutsua Python-ohjelman sisältä.

## Toiminnalliisuudet ##

- Ohjelma pystyy hakemaan repositorio-kohtaisesti kaikki issuet halutusta GitLab-instanssista. Issuet voidaan noutaa joko kutsumalla instanssin REST APIa tai vaihtoehtoisesti ottamalla ohjelmasta CSV-eksportti.

- Ohjelma pystyy täydentämään haettua dataa hakemalla jokaiseen issueen liittyvät kommentit. Kommentteja ei voida datansiirrossa liittää niiden alkuperäisiin kirjoittajiin. On selvitettävä riittääkö, että kommentit otetaan tekstikenttänä 

- Issueiden description-kentän ja kommenttien teksti-kentän tulee olla muutettu markdown-formaatista Jiran omaan markup-syntaksiin.

## Siirrettävä data ##

- Asiakkaan kanssa on sovittava mikä data on siirrettävä ja kuinka se mäpätään Jiran päässä. Ohessa lista siirrettävistä kentistä ja niiden vastikekappaleista Jirassa.

## Käyttäjien hallinta ##

- GitLabin käyttäjät pyritään yhdistämään oikeisiin käyttäjiin Jirassa. Tätä varten on selvitettävä asiakkaan kanssa kuinka käyttäjiä hallitaan kummassakin päässä ja voidaanko käyttäjät liittää toisiinsa yksiselitteisen attribuutin avulla.

- Asiakkaan kanssa on määriteltävä mitä tehdä sellaisessa tapauksessa, jossa käyttäjä löytyy GitLabista, mutta ei Jirasta.

## Muuta ##