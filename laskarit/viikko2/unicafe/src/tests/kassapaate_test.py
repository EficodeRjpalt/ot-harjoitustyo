import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)
        self.huono_kortti = Maksukortti(100)

    def test_kassassa_alussa_tonni(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassassa_alussa_myynti_nolla_edullisille(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_kassassa_alussa_myynti_nolla_maukkaat(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_voi_syoda_edullisesti_kateisella(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(palautus, 260)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000 + 240)

    def test_kateisella_maksu_kasvattaa_syotyja_lounaita(self):
        self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_liian_pieni_maksu_palauttaa_rahat_eika_lisaa_kassaan_edullinen(self):
        palautus = self.kassapaate.syo_edullisesti_kateisella(230)

        self.assertEqual(palautus, 230)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_maksu_maukas_kateinen_kassa_jamyynnit_kasvavat(self):
        self.kassapaate.syo_maukkaasti_kateisella(400)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000 + 400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_liian_pieni_maksu_palauttaa_rahat_eika_lisaa_kassaan_maukas(self):
        palautus = self.kassapaate.syo_maukkaasti_kateisella(390)

        self.assertEqual(palautus, 390)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_voi_ostaa_kortilla_edullisen(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)

        self.assertEqual(self.kortti.saldo, 1000 - 240)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_onnistunut_korttiosto_kasvattaa_edullisten_myyntia(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.kortti), True)

        self.assertEqual(self.kassapaate.edulliset, 1)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_liian_pienella_saldolla_ei_edullista(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.huono_kortti), False)

        self.assertEqual(self.huono_kortti.saldo, 100)

        self.assertEqual(self.kassapaate.edulliset, 0)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_voi_ostaa_kortilla_maukkaan(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)

        self.assertEqual(self.kortti.saldo, 1000 - 400)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)


    def test_onnistunut_korttiosto_kasvattaa_maukkaitten_myyntia(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.kortti), True)

        self.assertEqual(self.kassapaate.maukkaat, 1)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_liian_pienella_saldolla_ei_maukasta(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.huono_kortti), False)

        self.assertEqual(self.huono_kortti.saldo, 100)

        self.assertEqual(self.kassapaate.maukkaat, 0)

        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)


    def test_korttia_voi_ladata(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, 500)

        self.assertEqual(self.kortti.saldo, 1500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000 + 500)

    def test_korttia_ei_voi_ladata_anti_rahalla(self):
        self.kassapaate.lataa_rahaa_kortille(self.kortti, -100)

        self.assertEqual(self.kortti.saldo, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)