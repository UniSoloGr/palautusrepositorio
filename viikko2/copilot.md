## Kuinka hyödyllisiksi koit koodin täydennyksen ehdotukset?

Tässä tapauksessa täydennys toimi täydellisesti ja oli hyödyksi siksi, koska funktiolle oli valmiiksi kirjoitettu puhdas doc-stringi. Kuitenkin perinteisessä näpyttely ohjelmoinnissa jatkuvat ehdotukset pikemminkin häiritsevät ajattelua, sillä Copilot pyrkii ennakoimaan funktiota doc-stringin puuttuessa pelkän sen nimen avulla (ja muun koodin), mikä ei aina tuota oikeaa tulosta, mutta vaatii yhä uudelleen syötteen analysointia.

## Pitikö Copilotin selitys Pylint-varoituksesta paikkansa?

Kyllä, se antoi täsmällisen vastauksen, joka muistutti paljon pylint:in omaa dokumentaatiota, jolla se olikin varmasti treenattu.

## Tekikö agentti toimivan ratkaisun, ja testit?

Kyllä, niin ratkaisu kuin testienkin luonti onnistui täydellisesti ensimmäisellä kerralla.

## Eroaako testeissä joku siitä miten testejä tehtiin edellisellä viikolla?

Tekoäly toteutti yksikkötestit pelkällä assert -komennolla ilman unittestin importtaamista testitiedostoon. Käsitykseni mukaan se on myös toimiva ratkaisu, koska assert vertaa yhtä lailla kaksi oliota keskenään kuin unittestin assert -metodikin.

## Löysikö Pylint agentin koodista virheitä?

Ei, agentti tuotti heti koodia, joka seurasi pylintin omaa projektikonfiguraatiota.

## Mitä muuta opit?

Opin välittämään remoten portteja ssh-tunnelin kautta omalle koneelleni. En saanut auki coveragen luomaa html sivua VS Coden Remote -tilassa, joten laitoin sen pyörimään hostin porttiin ja välitin sen VS Coden Ports -valikosta läppärin selaimeen.
