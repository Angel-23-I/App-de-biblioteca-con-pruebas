"""Pruebas de sistema - Prueban el sistema completo end-to-end"""
import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database
from biblioteca import GestorBiblioteca

class TestSistema(unittest.TestCase):
    """Pruebas de sistema que verifican el funcionamiento completo"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.archivo_test = 'test_sistema.json'
        self.db = Database(self.archivo_test)
        self.gestor = GestorBiblioteca(self.db)
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)
    
    def test_escenario_biblioteca_completo(self):
        """Prueba un escenario completo de uso de la biblioteca"""
        # 1. Agregar múltiples libros
        self.gestor.agregar_libro('978-101', 'Python para todos', 'Autor A')
        self.gestor.agregar_libro('978-102', 'JavaScript Moderno', 'Autor B')
        self.gestor.agregar_libro('978-103', 'Base de Datos', 'Autor C')
        
        # 2. Registrar múltiples usuarios
        self.gestor.registrar_usuario('U001', 'Juan Pérez', 'juan@email.com')
        self.gestor.registrar_usuario('U002', 'María García', 'maria@email.com')
        
        # 3. Verificar que hay 3 libros y 2 usuarios
        libros = self.gestor.obtener_libros()
        usuarios = self.gestor.obtener_usuarios()
        self.assertEqual(len(libros), 3)
        self.assertEqual(len(usuarios), 2)
        
        # 4. Realizar múltiples préstamos
        self.gestor.prestar_libro('978-101', 'U001')
        self.gestor.prestar_libro('978-102', 'U002')
        
        # 5. Verificar préstamos activos
        prestamos = self.gestor.obtener_prestamos_activos()
        self.assertEqual(len(prestamos), 2)
        
        # 6. Intentar prestar un libro ya prestado (debe fallar)
        with self.assertRaises(ValueError):
            self.gestor.prestar_libro('978-101', 'U002')
        
        # 7. Devolver un libro
        self.gestor.devolver_libro('978-101')
        
        # 8. Verificar que ahora hay 1 préstamo activo
        prestamos = self.gestor.obtener_prestamos_activos()
        self.assertEqual(len(prestamos), 1)
        
        # 9. Verificar que el libro devuelto está disponible
        libro = self.gestor.buscar_libro_por_isbn('978-101')
        self.assertTrue(libro.disponible)
    
    def test_persistencia_datos(self):
        """Prueba que los datos persistan correctamente"""
        # Agregar datos
        self.gestor.agregar_libro('978-201', 'Libro Persistente', 'Autor Persistente')
        self.gestor.registrar_usuario('U-PERSIST', 'Usuario Persistente', 'persist@email.com')
        
        # Crear nueva instancia de base de datos (simula reinicio)
        db_nueva = Database(self.archivo_test)
        gestor_nuevo = GestorBiblioteca(db_nueva)
        
        # Verificar que los datos persisten
        libro = gestor_nuevo.buscar_libro_por_isbn('978-201')
        usuario = gestor_nuevo.buscar_usuario_por_id('U-PERSIST')
        
        self.assertIsNotNone(libro)
        self.assertIsNotNone(usuario)
        self.assertEqual(libro.titulo, 'Libro Persistente')
        self.assertEqual(usuario.nombre, 'Usuario Persistente')
    
    def test_manejo_errores_sistema(self):
        """Prueba el manejo de errores en todo el sistema"""
        # Error: prestar libro inexistente
        with self.assertRaises(ValueError):
            self.gestor.prestar_libro('ISBN-FALSO', 'U001')
        
        # Error: prestar a usuario inexistente
        self.gestor.agregar_libro('978-301', 'Libro Test', 'Autor Test')
        with self.assertRaises(ValueError):
            self.gestor.prestar_libro('978-301', 'USUARIO-FALSO')
        
        # Error: devolver libro no prestado
        with self.assertRaises(ValueError):
            self.gestor.devolver_libro('978-301')

if __name__ == '__main__':
    unittest.main()
