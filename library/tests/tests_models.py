from django.test import TestCase

from library.models import LibraryEntry

class DemoTest(TestCase):
    def test_demo(self):
        # Comprueba que dos valores son exactamente iguales.
        self.assertEqual(4, 2+2)
        # Comprueba si una condición se cumple o no.
        self.assertTrue(4 == 4)
        self.assertFalse(5 == 4)
        # Permiten distinguir entre None y otros valores como cadenas vacías o ceros.
        self.assertIsNone(None)
        # Comprueba que una acción provoca un error concreto.
        with self.assertRaises(ZeroDivisionError):
            # Codigo que lanza la excepcion
            4/0

class LibraryEntryExternalIdLengthTests(TestCase):
    def test_external_id_length_counts_regular_string(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 3)

    def test_external_id_length_counts_empty_string_as_zero(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 0)

    def test_external_id_length_counts_whitespace(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="   ")

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 3)

    def test_external_id_length_counts_max_length_boundary_100(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id="x" * 100)

        # Llamada
        longitud = entry.external_id_length()

        # Comprobaciones
        self.assertEqual(longitud, 100)

    def test_external_id_length_raises_type_error_if_not_string_or_none(self):
        # Caso anómalo: asignación indebida en memoria.
        # Precondiciones
        entry = LibraryEntry(external_game_id=123)

        # Llamada
        # Comprobaciones
        with self.assertRaises(TypeError):
            entry.external_id_length()

#------------------------------------------------------------------#
#metodo para comprobar external_id_upper() 
class LibraryEntryExternalIdUpperTests(TestCase):
    
    #metodo para comprobar que convierte a mayusculas correctamente
    def test_external_id_upper_converts_to_uppercase(self):
        
        # Precondiciones
        entry = LibraryEntry(external_game_id="abc123")

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "ABC123")
    
    #metodo para comprobar cadena vacia
    def test_external_id_upper_returns_empty_string_if_external_game_id_is_none(self):
        # Precondiciones
        entry = LibraryEntry(external_game_id=None)

        # Llamada
        resultado = entry.external_id_upper()

        # Comprobaciones
        self.assertEqual(resultado, "")

class LibraryEntryHoursPlayedLabelTests(TestCase):    
    #metodo para comprobar que hours_played devuelve un entero
    def test_hours_played_label_none_when_hours_played_is_zero(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=0)

        # Llamada
        resultado = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(resultado, "none")
        
    #metodo para comprobar que hours_played devuelve low
    def test_hours_played_label_low_when_hours_played_is_less_than_10(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=5)

        # Llamada
        resultado = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(resultado, "low")
        
    #metodo para comprobar que hours_played devuelve high
    def test_hours_played_label_high_when_hours_played_is_10_or_more(self):
        # Precondiciones
        entry = LibraryEntry(hours_played=10)

        # Llamada
        resultado = entry.hours_played_label()

        # Comprobaciones
        self.assertEqual(resultado, "high")
        
class LibraryEntryStatusValueTests(TestCase):
    def test_status_value_returns_zero_for_wishlist(self):
        # Precondiciones
        entry = LibraryEntry(status=LibraryEntry.STATUS_WISHLIST)

        # Llamada
        resultado = entry.status_value()

        # Comprobaciones
        self.assertEqual(resultado, 0)
    
    def test_status_value_playing(self):
        # Precondiciones
        entry = LibraryEntry(status=LibraryEntry.STATUS_PLAYING)

        # Llamada
        resultado = entry.status_value()

        # Comprobaciones
        self.assertEqual(resultado, 1)
    
    def test_status_value_completed(self):
        # Precondiciones
        entry = LibraryEntry(status=LibraryEntry.STATUS_COMPLETED)

        # Llamada
        resultado = entry.status_value()

        # Comprobaciones
        self.assertEqual(resultado, 2)
    
    def test_status_value_dropped(self):
        # Precondiciones
        entry = LibraryEntry(status=LibraryEntry.STATUS_DROPPED)

        # Llamada
        resultado = entry.status_value()

        # Comprobaciones
        self.assertEqual(resultado, 3)
    
    def test_status_value_invalid_status(self):
        # Precondiciones
        entry = LibraryEntry(status="invalid_status")

        # Llamada
        resultado = entry.status_value()

        # Comprobaciones
        self.assertEqual(resultado, -1)
    
    