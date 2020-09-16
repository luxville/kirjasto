# Kirjasto

Tavoitteena on toteuttaa virtuaalinen kirjasto, josta asiakas voi lainata tai varata lainattavaa aineistoa. Yleistietoja lainattavista tuotteista voi tarkastella myös ilman että niitä lainaa tai varaa. Tarkoituksena on pitää järjestelmä yksinkertaisena, joten aineistoa voi aina lainata, kun sitä on saatavilla, ja mikäli kaikki kirjastossa olevat kappaleet ovat lainassa, voi sen varata. Varaaminen onnistuu ainoastaan siinä tapauksessa, että lainaajalla ei ole kyseistä aineistoa ennestään lainassa. Laina-aikoja ei ole, mutta samalla asiakkaalla samanaikaisesti lainassa olevien kappaleiden määrää on tarkoitus rajata, jotta kukaan ei voi vain lainata itselleen kaikkia kirjaston nimikkeitä, koska muuta pakkoa niiden palauttamiseen ei ole. Samoin varauksia voi olla samalla asiakkaalla kerrallaan vain rajallinen määrä. Aineistolle on mahdollista asettaa ikärajoja ja lainaajan ollessa alaikäinen tulee hänelle siitä lainaus- tai varausyrityksen yhteydessä ilmoitus, eikä lainaaminen tai varaaminen ole tällöin kyseisen henkilön toimesta mahdollista.

Ohjelman kehittyessä kirjautumaton käyttäjä voi katsella kirjastossa olevien lainattavien asioiden tietoja, joita voi rajata tekijän, julkaisuvuoden tai tyypin perusteella. Kirjautumattomana voi myös rekisteröityä ja hankkia näin itselleen lainausoikeuden kirjaston aineistoon. Kirjautuneena aineistoa voi lisäksi lainata ja varata sekä palauttaa ja perua varauksia. Myös omia tietoja voi muokata ja asiakkuuden poistaminenkin on mahdollista. Pääkäyttäjänä eli kirjaston edustajana kirjastoon voidaan luoda uutta aineistoa, vanhaa voidaan poistaa ja olemassaolevasta aineistosta nähdä, kenellä se on lainassa. Myös pääkäyttäjä voi lisätä ja poistaa asiakkuuksia.

## Toiminnallisuuksia
Toistaiseksi mitään toimintoja ei tosiasiallisesti ole piilotettu kirjautumisen taakse, eikä kaikkea ole myöskään toteutettu.
* Kirjautumaton käyttäjä voi
    * tarkastella yleistietoja kirjaston aineistosta
    * katsella tekijöistä järjestelmään kirjattuja tietoja
    * rekisteröityä kirjaston asiakkaaksi (*ei mahdollista asiakkaaksi kirjautuneena*)
    * kirjautua sisään järjestelmään
* Asiakkaaksi kirjautuneena voi lisäksi
    * lainata ja palauttaa aineistoa
    * varata aineistoa, jos kaikki kappaleet ovat lainassa, tai perua varauksia
    * muokata omia tietoja
    * poistaa omat tiedot
* Pääkäyttäjänä voi 
    * lisätä järjestelmään uusia sisällöntuottajia
    * lisätä sisällöntuottajille uusia lainattavia tuotteita
    * muokata järjestelmässä olevia asiakkaiden, sisällöntuottajien ja lainattavien tuotteiden tietoja
    * poistaa järjestelmästä lainattavia tuotteita, sisällöntuottajia tai asiakkuuksia
    * nähdä lainassa olevan tuotteen tietojen yhteydessä myös senhetkisen lainaajan tiedot

## Alustava tietokantarakenne

### Asiakas
* nimi
* käyttäjätunnus
* ikä
* salasana
* lainat
* varaukset

### Lainattava tuote
* nimi
* tekijä_id
* julkaisuvuosi
* määrä
* tyyppi
* ikäraja

### Tekijä
* etunimi
* sukunimi
* syntymävuosi
* kuolinvuosi
* lyhyt kuvaus

### Tyyppi
* kirja
* DVD-levy
* Blu-ray-levy
* CD-levy
* Lehti
* Muu

### Varatut tuotteet
* Varatun tuotteen id
* Asiakkaan id
