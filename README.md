# Kirjasto

[Sovellus Herokussa](http://tsoha-kirjasto.herokuapp.com/)

Herokussa sovellusta voi testata käyttäjätunnuksella *testi* ja salasanalla *testi*. Pääkäyttäjän ominaisuudet ovat käytettävissä tunnuksella *paakayttaja* ja salasanalla *admin*. Myös oman tunnuksen luominen onnistuu, mutta sillä pitäisi pystyä saavuttamaan ainoastaan peruskäyttäjälle tarjolla olevat toiminnallisuudet.


## Toiminnallisuuksia

* Kirjautumaton käyttäjä voi
    * tarkastella yleistietoja kirjaston aineistosta,
    * katsella tekijöistä järjestelmään kirjattuja tietoja,
    * rekisteröityä kirjaston asiakkaaksi ja
    * kirjautua sisään järjestelmään.
* Asiakkaaksi kirjautuneena voi lisäksi
    * lainata ja palauttaa aineistoa
    * muokata omia tietoja,
    * vaihtaa oman salasanan ja
    * poistaa omat tiedot järjestelmästä.
* Pääkäyttäjänä voi 
    * lisätä järjestelmään uusia sisällöntuottajia,
    * lisätä sisällöntuottajille uusia lainattavia tuotteita,
    * muokata järjestelmässä olevia sisällöntuottajien ja lainattavien tuotteiden tietoja ja
    * poistaa järjestelmästä lainattavia tuotteita, sisällöntuottajia tai asiakkuuksia, kunhan tietokannalliset riippuvuudet on ensin poistettu.


## Käyttöohje

Herokussa on mahdollista tutustua kirjaston tarjontaan sekä lainattavien tuotteiden että sisällöntuottajien osalta nimettyjen linkkien kautta. Heti etusivulla on mahdollisuus kirjautumiseen ja siinä näkyy myös viisi eniten lainauskertoja saanutta lainattavaa tuotetta. Yläreunan linkkipalkista valittaessa *Lainattavat tuotteet* päädytään sivulle, jolla tuotteet voi järjestellä nimen, tekijän tai tyypin mukaan aakkosjärjestykseen tai julkaisuajankohdan mukaan uusimmasta vanhimpaan. *Sisällöntuottajat*-sivulla järjestelmään lisätyt kirjailijat, elokuvaohjaajat, muusikot ja muut on järjestelty aakkosjärjestykseen. Kaikilla käyttäjätasoilla vasemman yläkulman Kirjasto-linkin kautta pääsee takaisin etusivulle. 

Kirjautuneena sisältöön tutustumisen lisäksi on mahdollista lainata tuotteita ja muokata itsestään antamiaan tietoja tietyin rajauksin. Salasanan vaihtaminen on rekisteröitymisen ja sisäänkirjautumisen lisäksi ainoa toimenpide, jonka suorittamiseen vaaditaan salasanaa. Omalla sivulla on nähtävillä senhetkiset lainat ja oma lainaushistoria. Mikäli omat tietonsa poistaa järjestelmästä, häviää samalla kyseisen lainaajan lainaushistoria ja kaikki kyseisellä käyttäjällä olevat lainat palautuvat automaattisesti muiden lainattaviksi. Istuntonsa voi päättää kirjautumalla ulos.

Pääkäyttäjänä *Sisällöntuottajat*-sivulta on mahdollista lisätä uusia sisällöntuottajia järjestelmään. Sisällöntuottajan kautta voi puolestaan lisätä kirjastoon uusia lainattavia tuotteita, joita voi sitten muokata pääkäyttäjänä niiden omilta sivuilta. *Tilastoja*-sivulta löytyy listaus kaikesta tietokantojen sisällöstä kevyesti pureskeltuna. Käyttäjätietoihin kuuluu mahdollisuus nollata kenen tahansa perustason käyttäjän salasana niin, että se on jatkossa sama kuin käyttäjätunnus. Pääkäyttäjä ei voi palauttaa peruskäyttäjän lainoja, mutta voi poistaa hänen käyttäjätilinsä kokonaan. Ohjelman käyttö tässä vaiheessa perustuu luottamukseen, ettei pääkäyttäjä lähtökohtaisesti ole vihamielinen peruskäyttäjiä kohtaan.

Skaalautuvuus suurille tietomäärille jäi toteuttamatta, joten aktiivisella käytöllä systeemit saa helposti tukkoon ja selaimen hakutoiminnoille saattaa hyvinkin olla käyttöä. Ulkoisesti sivusto on mitä sattuu, mutta ainakin suurimpaan osaan virheellisistä syötteistä pitäisi olla jonkinlainen varasuunnitelma. Luultavasti jokin tai joitakin on silti päässyt jäämään toteutukseen. Muutama muukin ajatus jäi lopulta haaveeksi ja jokunen funktio vielä käyttämättä. Todellisuus iski, ja tässä on lopputulos.

