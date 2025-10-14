import unittest
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import Database
from biblioteca import GestorBiblioteca

class TestIntegracion(unittest.TestCase):
    """Pruebas de integración entre Database y GestorBiblioteca"""
    
    def setUp(self):
        """Configuración antes de cada prueba"""
        self.archivo_test = 'test_biblioteca.json'
        self.db = Database(self.archivo_test)
        self.gestor = GestorBiblioteca(self.db)
    
    def tearDown(self):
        """Limpieza después de cada prueba"""
        if os.path.exists(self.archivo_test):
            os.remove(self.archivo_test)
    
    def test_agregar_y_buscar_libro(self):
        """Prueba agregar un libro y buscarlo en la base de datos"""
        isbn = '978-001'
        self.gestor.agregar_libro(isbn, 'Libro Test', 'Autor Test')
        
        libro = self.gestor.buscar_libro_por_isbn(isbn)
        self.assertIsNotNone(libro)
        self.assertEqual(libro.isbn, isbn)
        self.assertEqual(libro.titulo, 'Libro Test')
    
    def test_registrar_y_buscar_usuario(self):
        """Prueba registrar un usuario y buscarlo"""
        id_usuario = 'U-TEST-001'
        self.gestor.registrar_usuario(id_usuario, 'Usuario Test', 'test@email.com')
        
        usuario = self.gestor.buscar_usuario_por_id(id_usuario)
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.id_usuario, id_usuario)
        self.assertEqual(usuario.email, 'test@email.com')
    
    def test_flujo_prestamo_completo(self):
        """Prueba el flujo completo de préstamo y devolución"""
        # Agregar libro y usuario
        isbn = '978-002'
        id_usuario = 'U-TEST-002'
        self.gestor.agregar_libro(isbn, 'Libro Préstamo', 'Autor Préstamo')
        self.gestor.registrar_usuario(id_usuario, 'Usuario Préstamo', 'prestamo@email.com')
        
        # Verificar que el libro esté disponible
        libro = self.gestor.buscar_libro_por_isbn(isbn)
        self.assertTrue(libro.disponible)
        
        # Prestar el libro
        self.gestor.prestar_libro(isbn, id_usuario)
        
        # Verificar que el libro no esté disponible
        libro = self.gestor.buscar_libro_por_isbn(isbn)
        self.assertFalse(libro.disponible)
        
        # Devolver el libro
        self.gestor.devolver_libro(isbn)
        
        # Verificar que el libro esté disponible nuevamente
        libro = self.gestor.buscar_libro_por_isbn(isbn)
        self.assertTrue(libro.disponible)
    
    def test_validacion_isbn_duplicado(self):
        """Prueba que no se pueda agregar un libro con ISBN duplicado"""
        isbn = '978-003'
        self.gestor.agregar_libro(isbn, 'Libro 1', 'Autor 1')
        
        with self.assertRaises(ValueError) as context:
            self.gestor.agregar_libro(isbn, 'Libro 2', 'Autor 2')
        
        self.assertIn('ISBN ya existe', str(context.exception))
    
    def test_validacion_email(self):
        """Prueba la validación de email al registrar usuario"""
        with self.assertRaises(ValueError) as context:
            self.gestor.registrar_usuario('U-TEST', 'Usuario Test', 'email_invalido')
        
        self.assertIn('Email inválido', str(context.exception))

if __name__ == '__main__':
    unittest.main()
