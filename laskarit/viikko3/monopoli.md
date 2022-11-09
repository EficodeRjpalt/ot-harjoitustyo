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
		Pelilauta "1" -- "40" Ruutu
		Pelaaja "2..8" -- "1" Pelinappula
		Pelilauta "1" -- "2..8" Pelinappula
		Ruutu "1" <-- "2..8" Pelinappula
	class Noppa {
		silmäluku
	}
	class Pelaaja {
		nimi
	}
	class Pelilauta {
		      
	}
	class Ruutu {
		Järjestysluku
		Seuraavan järjestysluku
	}
	class Pelinappula {
		väri
	}
```

## Tehtävä 2 ##

### Vaatimukset ###

Aloitusruutu 1
Vankila 1
Sattuma ja yhteismaa 6
Asemat ja laitokset 6
Normaalit kadut (joihin liittyy nimi) 22
Muut (2x ver, vapaa pysäköinti, mene vankilaan) 4
Monopolipelin täytyy tuntea sekä aloitusruudun että vankilan sijainti.

Jokaiseen ruutuun liittyy jokin toiminto.

Sattuma- ja yhteismaaruutuihin liittyy kortteja, joihin kuhunkin liittyy joku toiminto.

Toimintoja on useanlaisia. Ei ole vielä tarvetta tarkentaa toiminnon laatua.

Normaaleille kaduille voi rakentaa korkeintaan 4 taloa tai yhden hotellin. Kadun voi omistaa joku pelaajista. Pelaajilla on rahaa.

- [x] Tee luokasta ruutu abstrakti ruutu, jonka ominaisuudet periytyvät ym. listalle ruutuja (perintäsuhde)
- [x] Ruudulla on oltava toiminto, järjestysluku, tieto seuraavan ruudun luvusta
- [x] Tee luokka Kortti, jolla on aina attribuuttina luokan Toiminto instanssi
- [x] Kadun voi omistaa joku pelaaja
- [x] Kadulla sijaitsee 0 - 4 taloa tai yksi hotelli
- [x] Pelaaja-luokka on tilallinen: sillä on aina tietty määrä rahaa taskussa

```mermaid
 classDiagram
		Pelaaja "2..8" <.. "2" Noppa
		Pelaaja "2..8" -- "1" Pelinappula
		Pelilauta "1" -- "2..8" Pelinappula
		Aloitsuruutu --|> Ruutu
		Vankila --|> Ruutu
		Sattuma ja Yhteismaa --|> Ruutu
		Asemat ja laitokset --|> Ruutu
		Katu --|> Ruutu
		Muu --|> Ruutu
		Sattuma ja Yhteismaa "1" -- "*" Kortti
		Pelilauta "1" -- "1" Aloitusruutu
		Pelilauta "1" -- "1" Vankila
		Pelilauta "1" -- "6" Sattuma ja yhteismaa
		Pelilauta "1" -- "6" Asemat ja laitokset
		Pelilauta "1" -- "22" Katu
		Pelilauta "1" -- "4" Muu
		Kortti "1" -- "1" Toiminto
	class Noppa {
		+ silmäluku
	}
	class Pelaaja {
		+ nimi: string
		+ balanssi: int
		+ kayta_rahaa(summa: int)
		+ tienaa_rahaa(summa: int)
	}
	class Pelilauta{
		+ aloitusruudun järj.nro.: int
		+ vankilan järj.nro: int
	}
	class Ruutu{
		+ Järjestysluku: int
		+ Seuraavan ruudun järjestysluku: int
		+ toiminto()
	}
	class Aloitusruutu {
		  
	}
	class Vankila{
		  
	}
	class Sattuma ja Yhteismaa {
		  
	}
	class Asemat ja laitokset{
		  
	}
	class Katu {
		+ omistaja: Pelaaja
		+ talojen_lkm: int
		+ hotellien_lkm: int
		+ aseta_omistaja(pelaaja: Pelaaja)
	}
	class Muu {
		  
	}
	class Pelinappula{
		+ väri: string
		+ sijainti: int
	}
	class Kortti {

	}
	class Toiminto {
		+ toiminto()
	}
```

# Sekvenssikaaviot #

## Tehtävä 3 ##

- [x] 1: Main-metodi luo Machine-instanssin
- [x] 2: Machine-instanssin konstruktori luo FuelTankin
- [x] 3: Kutsutaan luodun FuelTankin metodia fill arvolla 40
- [x] 4: Luodaan Engine-instanssi, jolle annetaan äsken luotu ja täytetty tankki
- [x] 5: Palautetaan kontrolli main-metodiin
- [x] 6: Kutsutaan Machinen metodia drive()
- [x] 7: Machine kutsuu luokan Engine metodia start() 
- [x] 8: Tämä trigeröi consumen FuelTankille arvolla 5
- [x] 9: Palautetaan kontrolli Machine-luokalle
- [x] 10: Machine kutsuu Engine-luokan metodia s_running()
- [x] 11: Engine tarkastaa FuelTankilta bensamäärän (fuel_contents)
- [x] 12: FuelTank palauttaa attribuutin fuel_contents arvon kokonaislukuna
- [x] 13: Engine evaluoi palautuksesta onko tankissa yli 0l. Jos (ja tässä tapauksessa kun) ehto on tosi, palautetaan arvo true
- [x] 14: Machine kutsuu Enginen metodia use_energy()
- [x] 15: Engine kutsuu FuelTankin metodia consume arvolla 10
- [x] 16: Engine palauttaa kontrollin Machinelle
- [x] 17: Machine palauttaa kontrollin main-metodille, johon ohjelma päättyy

```mermaid
sequenceDiagram
	autonumber
	participant main
	main ->> Machine: init
	activate Machine
	Machine ->> FuelTank: init
	Machine ->> FuelTank: fill(40)
	Machine ->> Engine: init(self._tank)
	Machine -->> main: 
	deactivate Machine
	main ->> Machine: drive()
	activate Machine
	Machine ->> Engine: start()
	activate Engine
	Engine ->> FuelTank: consume(5)
	Engine -->> Machine: 
	deactivate Engine
	Machine ->> Engine: is_running()
	activate Engine
	Engine ->> FuelTank: fuel_contents
	activate FuelTank
	FuelTank -->> Engine: int
	deactivate FuelTank
	Engine -->> Machine: true
	deactivate Engine
	Machine ->> Engine: use_energy()
	activate Engine
	Engine ->> FuelTank: consume(10)
	Engine -->> Machine: 
	deactivate Engine
	Machine -->> main: 
	deactivate Machine
```

## Tehtävä 4 ##

```mermaid
sequenceDiagram
	autonumber
	participant main
	activate main
	main ->> laitehallinto: HKLLaitehallinto()
	main ->> rautatietori: Lataajalaite()
	main ->> ratikka6: Lukijalaite()
	main ->> bussi244: Lukijalaite()
	laitehallinto ->> rautatietori: lisaa_lataaja(rautatietori)
	laitehallinto ->> ratikka6: lisaa_lukija(ratikka6)
	laitehallinto ->> bussi244: lisaa_lukija(bussi244)
	main ->> lippu_luukku: Kioski()
	main ->> lippu_luukku: osta_matkakortti("Kalle")
		activate lippu_luukku
	lippu_luukku -> Matkakortti: Matkakortti("Kalle")
	Matkakortti -->> lippu_luukku: uusi_kortti
	lippu_luukku -->> kallen_kortti: uusi_kortti
	deactivate lippu_luukku
	lippu_luukku -->> main: 
	main ->> rautatietori: lataa_arvoa(kallen_kortti, 3)
		activate rautatietori
	rautatietori -->> kallen_kortti: kasvata_arvoa(3)
	kallen_kortti -->> rautatietori: 
	rautatietori -->> main: 
	deactivate rautatietori
	main ->> ratikka6: osta_lippu(kallen_kortti, 0)
		activate ratikka6
	ratikka6 ->> kallen_kortti: arvo
	kallen_kortti -->> ratikka6: 3
	ratikka6 ->> kallen_kortti: vahenna_arvoa(1.5)
	kallen_kortti --> ratikka6: 
	ratikka6 -->> main: True
	deactivate ratikka6
	main ->> bussi244: osta_lippu(kallen_kortti, 2)
		activate bussi244
	bussi244 ->> kallen_kortti: arvo
	kallen_kortti -->> bussi244: 1.5
	bussi244 -->> main: False
	deactivate bussi244
	deactivate main
```
- [x] 1: Luodaan HKLLaitehallinto-olio nimellä 'laitehallinto' 
- [x] 2: Luodaan Lataajalaite-olio nimellä 'rautatietori'
- [x] 3: Luodaan Lukijalaite-olio nimellä 'ratikka6'
- [x] 4: Luodaan Lukijalaite-olio nimellä 'bussi244'
- [x] 5: Lisätään rautatietori laitehallintoon metodilla lisaa_lataaja
- [x] 6: Lisätään lukija ratikka6 laitehallintoon metodilla lisaa_lukija()
- [x] 7: Lisätään lukija bussi244 laitehallintoon metodilla lisaa_lukija()
- [x] 8: Luodaan Kioski-olio nimellä lippu_luukku
- [x] 9: Main-metodista kutsutaan lippu_luukun metodia osta_matkakortti arvolla "Kalle"
- [x] 10: lippu_luukku kutsuu oliota Matkakortti luodakseen uuden instanssin oliosta nimellä uusi_kortti ja omistajana "Kalle"
- [x] 11: Matkakortti-luokka palauttaa uuden olion, "uusi_kortti"
- [x] 12: lippu_luukku palauttaa uuden Matkakortti-instanssin muuttujaan 'kallen_kortti'
- [x] 13: Kontrolli palautetaan main-metodiin
- [x] 14: main-metodi kutsuu rautatietorin metodia lataa_arvoa antaen parametreiksi kallen_kortin ja kokonaisluvun 3
- [x] 15: rautatietori kutsuu kallen_kortin metodia kasvata_arvoa arvonaan kokonaisluku 3
- [x] 16: kallen_kortti ei palauta mitään arvoa, vain kontrollin
- [x] 17: Kontrolli palautetaan main-metodiin
- [x] 18: main-metodi kutsuu ratikka6:n metodia osta_lippu antaen parametreinä kallen kortin ja kokonaisluvun 0
- [x] 19: ratikka6 hakee kallen_kortin attribuutin 'arvo'
- [x] 20: kallen_kortti palauttaa arvonsa (3)
- [x] 21: (Arvo evaluoituu lipun hintaa suuremmaksi) ratikka6 kutsuu kallen_kortin metodia vahenna_arvoa arvolla 1.5
- [x] 22: kallen_kortti ei palauta mitään, mutta vähentää arvo-attribuutistansa 1.5
- [x] 23: ratikka6 palauttaa kontrollin ja arvon True main-metodille
- [x] 24: main-metodi kutsuu bussi244:n metodia osta_lippu parametreinään kallen_kortti ja 2
- [x] 25: bussi244 hakee kallen_kortin attribuutin arvo
- [x] 26: kallen_kortti palauttaa arvon 1.5.
- [x] 27: Arvo evaluoituu pienemmäksi kuin lipun hinta, jolloin kontrolli ja arvo False palautetaan main-metodille