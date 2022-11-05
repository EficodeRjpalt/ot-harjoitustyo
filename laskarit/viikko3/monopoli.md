Monopolia pelataan käyttäen kahta noppaa. Pelaajia on vähintään 2 ja enintään 8. Peliä pelataan pelilaudalla joita on yksi. Pelilauta sisältää 40 ruutua. Kukin ruutu tietää, mikä on sitä seuraava ruutu pelilaudalla. Kullakin pelaajalla on yksi pelinappula. Pelinappula sijaitsee aina yhdessä ruudussa.

- Noppa x2
- Pelaajia 2 - 8
- 40 ruutua
    - Jokainen ruutu tietää mikä on sitä seuraava ruutu
- Pelinappula, ykis per pelaaja, pelinappula on aina ruudussa

```mermaid
 classDiagram
	  	 Pelaaja "2..8" <.. "2" Noppa
		  Pelilauta "1" <-- "40" Ruutu
		  Pelaaja "2..8" <-- "1" Pelinappula
		  Pelilauta "1" <-- "2..8" Pelinappula
		  Ruutu "1" <-- "2..8" Pelinappula
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
```