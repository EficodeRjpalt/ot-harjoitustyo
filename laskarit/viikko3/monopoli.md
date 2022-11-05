# Monopolin UML-mallinnus #

## Tehtävä 1 ##

### Vaatimukset ##
Monopolia pelataan käyttäen kahta noppaa. Pelaajia on vähintään 2 ja enintään 8. Peliä pelataan pelilaudalla joita on yksi. Pelilauta sisältää 40 ruutua. Kukin ruutu tietää, mikä on sitä seuraava ruutu pelilaudalla. Kullakin pelaajalla on yksi pelinappula. Pelinappula sijaitsee aina yhdessä ruudussa.

- [x] Noppa x2
- [x] Pelaajia 2 - 8
- [x] 40 ruutua
- [x] Jokainen ruutu tietää mikä on sitä seuraava ruutu (Katso huomiot tehtävän alla)
- [x] Pelinappula, yksi per pelaaja, pelinappula on aina ruudussa

```mermaid
 classDiagram
	  	 Pelaaja "2..8" <.. "2" Noppa
		  Pelilauta "1" <-- "40" Ruutu
		  Pelaaja "2..8" <-- "1" Pelinappula
		  Pelilauta "1" <-- "2..8" Pelinappula
		  Ruutu "1" <-- "2..8" Pelinappula
		  Ruutu "1" <-- "1" SeuraavaRuutu
      class Noppa {
          silmäluku
      }
      class Pelaaja {
	  	   nimi
      }
	    class Pelilauta{
		      
		  }
		  class Ruutu{
		    
		  }
		  class Pelinappula{
		    väri
		  }
		  class SeuraavaRuutu{
		  
		  }
```

***

**Huomioita**
- Ruutujen välinen suhde (ne tietävät aina mikä on seuraava ruutu), kuuluisi oikeasti ilmaista UML:n syntaksilla 'self association', mutta mermaid ei tällä hetkellä tue kyseistä syntaksia, jonka takia tässä kaaviossa olen käyttänyt ns. huonoa käytänneettä, eli mallintanut luokan instanssien suhdetta luomalla käsitteen 'SeuraavaRuutu'. Tosiasiassa luokat saisivat luotaessa aina referenssin siihen ruutuun, joka tulee niiden jälkeen.

## Tehtävä 2 ##

### Vaatimukset ###

Aloitusruutu
Vankila
Sattuma ja yhteismaa
Asemat ja laitokset
Normaalit kadut (joihin liittyy nimi)
Monopolipelin täytyy tuntea sekä aloitusruudun että vankilan sijainti.

Jokaiseen ruutuun liittyy jokin toiminto.

Sattuma- ja yhteismaaruutuihin liittyy kortteja, joihin kuhunkin liittyy joku toiminto.

Toimintoja on useanlaisia. Ei ole vielä tarvetta tarkentaa toiminnon laatua.

Normaaleille kaduille voi rakentaa korkeintaan 4 taloa tai yhden hotellin. Kadun voi omistaa joku pelaajista. Pelaajilla on rahaa.

- [] Tee luokasta ruutu abstrakti ruutu, jonka ominaisuudet periytyvät ym. listalle ruutuja (perintäsuhde)
- [] Tee luokka Kortti, jolla on aina attribuuttina luokan Toiminto instanssi
- [] Tee luokat Talo ja  Hotelli
- [] Kadulla voi olla 4 taloa TAI 1 hotelli
- [] Kadun VOI omistaa joku pelaaja
- [] Pelaaja-luokka on tilallinen: sillä on aina tietty määrä rahaa taskussa