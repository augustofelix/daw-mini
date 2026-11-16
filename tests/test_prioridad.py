import sys, unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from tickettriage.tickets import crear_ticket

NO_VIP = "juan"


class TestPrioridad(unittest.TestCase):
    def test_ac01_todo_ticket_tiene_prioridad(self):
        """AC-01: todo ticket nuevo tiene prioridad en {alta, media, baja}."""
        t = crear_ticket("Consulta", "Hola", NO_VIP)
        self.assertIn(t.prioridad, {"alta", "media", "baja"})

    def test_ac02_titulo_caido_es_alta(self):
        """AC-02: título "Login caído" → alta."""
        t = crear_ticket("Login caído", "", NO_VIP)
        self.assertEqual(t.prioridad, "alta")

    def test_ac03_descripcion_urgente_es_alta(self):
        """AC-03: descripción "Es urgente, necesito ayuda" → alta."""
        t = crear_ticket("Problema", "Es urgente, necesito ayuda", NO_VIP)
        self.assertEqual(t.prioridad, "alta")

    def test_ac04_alta_gana_sobre_media(self):
        """AC-04: si matchean alta y media, gana alta."""
        t = crear_ticket("Problema", "El sistema anda lento y no funciona el login", NO_VIP)
        self.assertEqual(t.prioridad, "alta")

    def test_ac05_lenta_es_media_con_motivo(self):
        """AC-05: descripción "La página anda lenta" → media, motivo con 'lenta'."""
        t = crear_ticket("Problema", "La página anda lenta", NO_VIP)
        self.assertEqual(t.prioridad, "media")
        self.assertEqual(t.motivo, "media: matcheó 'lenta'")

    def test_ac06_error_es_media(self):
        """AC-06: descripción "Me tira error al guardar" → media."""
        t = crear_ticket("Problema", "Me tira error al guardar", NO_VIP)
        self.assertEqual(t.prioridad, "media")

    def test_ac07_sin_coincidencias_es_baja(self):
        """AC-07: sin coincidencias → baja, motivo "baja: sin coincidencias"."""
        t = crear_ticket("Cambiar mi email", "Quiero actualizar mis datos", NO_VIP)
        self.assertEqual(t.prioridad, "baja")
        self.assertEqual(t.motivo, "baja: sin coincidencias")

    def test_ac08_vip_sube_baja_a_media(self):
        """AC-08: cliente VIP "acme" sin coincidencias → media, +1 por VIP."""
        t = crear_ticket("Problema", "Quiero actualizar mis datos", "acme")
        self.assertEqual(t.prioridad, "media")
        self.assertEqual(t.motivo, "media: sin coincidencias; +1 por cliente VIP")

    def test_ac09_vip_ya_alta_queda_alta(self):
        """AC-09: cliente VIP "globex" con alta → alta, ya era alta."""
        t = crear_ticket("Login caído", "", "globex")
        self.assertEqual(t.prioridad, "alta")
        self.assertEqual(t.motivo, "alta: matcheó 'caído'; cliente VIP, ya era alta")

    def test_ac10_motivo_alta_no_vip(self):
        """AC-10: título "Login caído" no VIP → motivo "alta: matcheó 'caído'"."""
        t = crear_ticket("Login caído", "", NO_VIP)
        self.assertEqual(t.motivo, "alta: matcheó 'caído'")

    def test_ac11_ignora_mayusculas_y_tildes(self):
        """AC-11: título "SISTEMA CAIDO" → alta."""
        t = crear_ticket("SISTEMA CAIDO", "", NO_VIP)
        self.assertEqual(t.prioridad, "alta")

    def test_ac12_palabra_completa_terror_no_es_error(self):
        """AC-12: "terror" no matchea "error" → baja."""
        t = crear_ticket("Problema", "Fue un terror de día", NO_VIP)
        self.assertEqual(t.prioridad, "baja")

    def test_ac13_vip_con_espacios_y_mayusculas_sube_media_a_alta(self):
        """AC-13: cliente "  ACME " con error → alta, +1 por VIP."""
        t = crear_ticket("Problema", "Me tira error al guardar", "  ACME ")
        self.assertEqual(t.prioridad, "alta")
        self.assertEqual(t.motivo, "alta: matcheó 'error'; +1 por cliente VIP")

    def test_ac14_no_puedo_entrar_es_alta(self):
        """AC-14: "No puedo entrar a mi cuenta" → alta, motivo 'no puedo entrar'."""
        t = crear_ticket("Problema", "No puedo entrar a mi cuenta", NO_VIP)
        self.assertEqual(t.prioridad, "alta")
        self.assertEqual(t.motivo, "alta: matcheó 'no puedo entrar'")

    def test_ac15_tarda_es_media(self):
        """AC-15: "La carga tarda mucho" → media."""
        t = crear_ticket("Problema", "La carga tarda mucho", NO_VIP)
        self.assertEqual(t.prioridad, "media")


if __name__ == "__main__":
    unittest.main()
