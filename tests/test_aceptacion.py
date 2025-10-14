import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database
from biblioteca import GestorBiblioteca

class TestAceptacion(unittest.TestCase):
    """Pruebas de aceptación basadas en historias de usuario"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.archivo_test = 'test_aceptacion.json'
        self.db = Database(self.archivo_test)
        self.gestor = GestorBiblioteca(self.db)
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)
    
    def test_historia_usuario_nuevo_miembro(self):
        """
        Historia de usuario: Como nuevo miembro de la biblioteca,
        quiero registrarme en el sistema para poder pedir libros prestados.
        """
        # Criterio de aceptación 1: El usuario puede registrarse con datos válidos
        resultado = self.gestor.registrar_usuario(
            'U-NEW-001',
            'Pedro Martínez',
            'pedro.martinez@email.com'
        )
        self.assertTrue(resultado)
        
        # Criterio de aceptación 2: El usuario queda registrado en el sistema
        usuario = self.gestor.buscar_usuario_por_id('U-NEW-001')
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nombre, 'Pedro Martínez')
        
        # Criterio de aceptación 3: El usuario está activo por defecto
        self.assertTrue(usuario.activo)
    
    def test_historia_bibliotecario_agregar_libro(self):
        """
        Historia de usuario: Como bibliotecario,
        quiero agregar nuevos libros al catálogo para ampliar la colección.
        """
        # Criterio de aceptación 1: Puedo agregar un libro con toda su información
        resultado = self.gestor.agregar_libro(
            '978-84-9804-654-0',
            'Cien años de soledad',
            'Gabriel García Márquez'
        )
        self.assertTrue(resultado)
        
        # Criterio de aceptación 2: El libro aparece en el catálogo
        libros = self.gestor.obtener_libros()
        self.assertEqual(len(libros), 1)
        
        # Criterio de aceptación 3: El libro está disponible inicialmente
        libro = self.gestor.buscar_libro_por_isbn('978-84-9804-654-0')
        self.assertTrue(libro.disponible)
    
    def test_historia_usuario_pedir_prestamo(self):
        """
        Historia de usuario: Como usuario registrado,
        quiero pedir un libro prestado para poder leerlo en casa.
        """
        # Preparación: agregar libro y registrar usuario
        self.gestor.agregar_libro('978-1234', 'El Quijote', 'Miguel de Cervantes')
        self.gestor.registrar_usuario('U-READER-001', 'Ana Lector', 'ana@email.com')
        
        # Criterio de aceptación 1: Puedo solicitar un préstamo
        resultado = self.gestor.prestar_libro('978-1234', 'U-READER-001')
        self.assertTrue(resultado)
        
        # Criterio de aceptación 2: El préstamo queda registrado
        prestamos = self.gestor.obtener_prestamos_activos()
        self.assertEqual(len(prestamos), 1)
        self.assertEqual(prestamos[0].isbn_libro, '978-1234')
        
        # Criterio de aceptación 3: El libro ya no está disponible
        libro = self.gestor.buscar_libro_por_isbn('978-1234')
        self.assertFalse(libro.disponible)
    
    def test_historia_usuario_devolver_libro(self):
        """
        Historia de usuario: Como usuario con un libro prestado,
        quiero devolver el libro para que otros puedan usarlo.
        """
        # Preparación: hacer un préstamo
        self.gestor.agregar_libro('978-5678', 'La Odisea', 'Homero')
        self.gestor.registrar_usuario('U-READER-002', 'Carlos Lector', 'carlos@email.com')
        self.gestor.prestar_libro('978-5678', 'U-READER-002')
        
        # Criterio de aceptación 1: Puedo devolver el libro
        resultado = self.gestor.devolver_libro('978-5678')
        self.assertTrue(resultado)
        
        # Criterio de aceptación 2: El libro vuelve a estar disponible
        libro = self.gestor.buscar_libro_por_isbn('978-5678')
        self.assertTrue(libro.disponible)
        
        # Criterio de aceptación 3: El préstamo ya no está activo
        prestamos = self.gestor.obtener_prestamos_activos()
        self.assertEqual(len(prestamos), 0)
    
    def test_historia_bibliotecario_consultar_prestamos(self):
        """
        Historia de usuario: Como bibliotecario,
        quiero ver todos los préstamos activos para hacer seguimiento.
        """
        # Preparación: crear varios préstamos
        self.gestor.agregar_libro('978-AAA', 'Libro A', 'Autor A')
        self.gestor.agregar_libro('978-BBB', 'Libro B', 'Autor B')
        self.gestor.agregar_libro('978-CCC', 'Libro C', 'Autor C')
        
        self.gestor.registrar_usuario('U-001', 'Usuario 1', 'u1@email.com')
        self.gestor.registrar_usuario('U-002', 'Usuario 2', 'u2@email.com')
        
        self.gestor.prestar_libro('978-AAA', 'U-001')
        self.gestor.prestar_libro('978-BBB', 'U-002')
        
        # Criterio de aceptación 1: Puedo ver todos los préstamos activos
        prestamos = self.gestor.obtener_prestamos_activos()
        self.assertEqual(len(prestamos), 2)
        
        # Criterio de aceptación 2: Los préstamos contienen información completa
        for prestamo in prestamos:
            self.assertIsNotNone(prestamo.id_prestamo)
            self.assertIsNotNone(prestamo.isbn_libro)
            self.assertIsNotNone(prestamo.id_usuario)
            self.assertIsNotNone(prestamo.fecha_prestamo)
            self.assertIsNone(prestamo.fecha_devolucion)

if __name__ == '__main__':
    unittest.main()
