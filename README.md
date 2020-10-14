# Kirjasto

[Sovellus Herokussa](http://tsoha-kirjasto.herokuapp.com/)

Herokussa sovellusta voi testata käyttäjätunnuksella *testi* ja salasanalla *kayttaja* niin kauan kunnes joku poistaa kyseisen tunnuksen. Näköjään tietojen muokkaamisen jälkeen myös sisäänkirjautuminen muuttuu ongelmalliseksi. Myös oman tunnuksen luominen onnistuu, sillä eri käyttäjätasoja ei ole vielä toteutettu.

Viimeisille päiville riittää vielä paljon tekemättömiä asioita, mutta näillä eväillä homma tässä vaiheessa kuitenkin jatkuu.

## Toiminnallisuuksia

* Kirjautumaton käyttäjä voi
    * tarkastella yleistietoja kirjaston aineistosta
    * katsella tekijöistä järjestelmään kirjattuja tietoja
    * rekisteröityä kirjaston asiakkaaksi (**käytössä**)
    * kirjautua sisään järjestelmään (**käytössä**)
* Asiakkaaksi kirjautuneena voi lisäksi
    * lainata ja palauttaa aineistoa (**käytössä**)
    * varata aineistoa, jos kaikki kappaleet ovat lainassa, tai perua varauksia
    * muokata omia tietoja (**käytössä**)
    * poistaa omat tiedot (**käytössä**)
* Pääkäyttäjänä voi 
    * lisätä järjestelmään uusia sisällöntuottajia (**käytössä**)
    * lisätä sisällöntuottajille uusia lainattavia tuotteita (**käytössä**)
    * muokata järjestelmässä olevia sisällöntuottajien ja lainattavien tuotteiden tietoja (**käytössä**)
    * poistaa järjestelmästä lainattavia tuotteita, sisällöntuottajia tai asiakkuuksia (**käytössä**)
    * nähdä lainassa olevan tuotteen tietojen yhteydessä myös senhetkisen lainaajan tiedot

Toistaiseksi kirjautuminen vaaditaan, jotta muihin toimintoihin pääsee tutustumaan. Rekisteröityminen ja tietojen tallentuminen tietokantaan toimii. Aineistoa voi lisätä vain olemassaolevien sisällöntuottajien kautta, ja lomakkeet toimivat oikein lähinnä oletusarvoisesti oikeilla syötteillä. Rekisteröitymisen yhteydessä käyttäjän tiedot tarkistetaan ikää lukuunottamatta. Jokaiseen kenttään pitää myös syöttää oikeantyyppinen tieto, jotta ohjelma toimisi oikein. Mitään tietoturvatarkistuksia ei ole vielä toteutettu, paitsi ehkä vahingossa.

