# Kirjasto

[Sovellus Herokussa](http://tsoha-kirjasto.herokuapp.com/)

Herokussa sovellusta voi testata käyttäjätunnuksella *testi* ja salasanalla *testi* niin kauan kunnes joku poistaa kyseisen tunnuksen. Pääkäyttäjän ominaisuudet ovat käytettävissä tunnuksella *paakayttaja* ja salasanalla *admin*. Myös oman tunnuksen luominen onnistuu, mutta sillä pitäisi pystyä saavuttamaan ainoastaan peruskäyttäjälle tarjolla olevat toiminnallisuudet.


## Toiminnallisuuksia

* Kirjautumaton käyttäjä voi
    * tarkastella yleistietoja kirjaston aineistosta
    * katsella tekijöistä järjestelmään kirjattuja tietoja
    * rekisteröityä kirjaston asiakkaaksi (**käytössä**)
    * kirjautua sisään järjestelmään (**käytössä**)
* Asiakkaaksi kirjautuneena voi lisäksi
    * lainata ja palauttaa aineistoa (**käytössä**)
    * muokata omia tietoja (**käytössä**)
    * poistaa omat tiedot (**käytössä**)
* Pääkäyttäjänä voi 
    * lisätä järjestelmään uusia sisällöntuottajia (**käytössä**)
    * lisätä sisällöntuottajille uusia lainattavia tuotteita (**käytössä**)
    * muokata järjestelmässä olevia sisällöntuottajien ja lainattavien tuotteiden tietoja (**käytössä**)
    * poistaa järjestelmästä lainattavia tuotteita, sisällöntuottajia tai asiakkuuksia, kunhan tietokannalliset riippuvuudet on ensin poistettu (**käytössä**)
    * nähdä lainassa olevan tuotteen tietojen yhteydessä myös senhetkisen lainaajan tiedot

Toistaiseksi kirjautuminen vaaditaan, jotta muihin toimintoihin pääsee tutustumaan. Rekisteröityminen ja tietojen tallentuminen tietokantaan toimii. Aineistoa voi lisätä vain olemassaolevien sisällöntuottajien kautta, ja lomakkeet toimivat oikein lähinnä oletusarvoisesti oikeilla syötteillä. Rekisteröitymisen yhteydessä käyttäjän tiedot tarkistetaan. Jokaiseen kenttään pitää myös syöttää oikeantyyppinen tieto, jotta ohjelma toimisi oikein.

