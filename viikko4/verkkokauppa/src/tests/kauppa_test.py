import unittest
from unittest.mock import Mock
from kauppa import Kauppa
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()
        self.tuote1 = Tuote(1, "maito", 5)
        self.tuote2 = Tuote(2, "omena", 2)

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 2

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return self.tuote1
            if tuote_id == 2:
                return self.tuote2

        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        self.kauppa = Kauppa(
            self.varasto_mock,
            self.pankki_mock,
            self.viitegeneraattori_mock
        )

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):

        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksaessa_ostos_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        asiakas = "pekka"
        tilinro = "12345"
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu(asiakas, tilinro)

        self.pankki_mock.tilisiirto.assert_called_with(
            asiakas,
            42,
            tilinro,
            "33333-44455",
            self.tuote1.hinta
        )

    def test_maksaessa_ostoksia_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        asiakas = "pekka"
        tilinro = "12345"
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu(asiakas, tilinro)

        self.pankki_mock.tilisiirto.assert_called_with(asiakas, 42, tilinro, "33333-44455", 7)

    def test_maksaessa_kahta_samaa_tuotetta_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        asiakas = "pekka"
        tilinro = "12345"
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu(asiakas, tilinro)

        self.pankki_mock.tilisiirto.assert_called_with(asiakas, 42, tilinro, "33333-44455", 10)

    def test_maksaessa_ostoksia_joista_toinen_on_loppu_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0

        self.varasto_mock.saldo.side_effect = varasto_saldo

        asiakas = "pekka"
        tilinro = "12345"
        # tehdään ostokset
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu(asiakas, tilinro)

        self.pankki_mock.tilisiirto.assert_called_with(asiakas, 42, tilinro, "33333-44455", 5)
