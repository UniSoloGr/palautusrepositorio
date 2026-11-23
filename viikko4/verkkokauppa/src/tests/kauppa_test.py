import unittest
from unittest.mock import Mock, ANY, call
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

        self.pankki_mock.tilisiirto.assert_called()

    def test_maksaessa_ostos_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        asiakas = "pekka"
        tilinro = "12345"
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
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu(asiakas, tilinro)

        self.pankki_mock.tilisiirto.assert_called_with(asiakas, 42, tilinro, "33333-44455", 7)

    def test_maksaessa_kahta_samaa_tuotetta_pankin_metodia_tilisiirto_kutsutaan_oikeilla_parametreilla(self):
        asiakas = "pekka"
        tilinro = "12345"
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
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu(asiakas, tilinro)

        self.pankki_mock.tilisiirto.assert_called_with(asiakas, 42, tilinro, "33333-44455", 5)

    def test_aloita_asiointi_nollaa_edellisen_ostoksen_tiedot(self):
        asiakas = "pekka"
        tilinro = "12345"
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu(asiakas, tilinro)

        asiakas = "joki"
        tilinro = "54321"
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu(asiakas, tilinro)

        self.assertEqual(
            self.pankki_mock.tilisiirto.call_args_list,
            [
                call(ANY, ANY, ANY, ANY, 10),
                call(ANY, ANY, ANY, ANY, 15)
            ]
        )

    def test_kauppa_pyytää_uuden_tilinumeron(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("asiakas1", "001")

        self.viitegeneraattori_mock.uusi.return_value = 43
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("asiakas2", "002")

        self.assertEqual(
            self.pankki_mock.tilisiirto.call_args_list,
            [
                call(ANY, 42, ANY, ANY, ANY),
                call(ANY, 43, ANY, ANY, ANY)
            ]
        )
    
    def test_kauppa_poistaa_tuotteen_korista(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)
        self.kauppa.tilimaksu("asiakas1", "001")

        self.pankki_mock.tilisiirto.assert_called_with("asiakas1", 42, "001", "33333-44455", 0)