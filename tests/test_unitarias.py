import unittest
import sys
import os

# Agregar el directorio padre al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Libro, Usuario, Prestamo

class TestModels(unittest.TestCase):
    """Pruebas unitarias para los modelos de datos"""
    
    def test_crear_libro(self):
        """Prueba la creación de un libro"""
        libro = Libro('978-123', 'Python Avanzado', 'Juan Pérez')
        self.assertEqual(libro.isbn, '978-123')
        self.assertEqual(libro.titulo, 'Python Avanzado')
        self.assertEqual(libro.autor, 'Juan Pérez')
        self.assertTrue(libro.disponible)
    
    def test_libro_from_dict(self):
        """Prueba la creación de libro desde diccionario"""
        data = {
            'isbn': '978-789',
            'titulo': 'Django Web',
            'autor': 'Carlos Ruiz',
            'disponible': True
        }
        libro = Libro.from_dict(data)
        self.assertEqual(libro.isbn, '978-789')
        self.assertEqual(libro.titulo, 'Django Web')
    
    def test_crear_usuario(self):
        """Prueba la creación de un usuario"""
        usuario = Usuario('U001', 'María López', 'maria@email.com')
        self.assertEqual(usuario.id_usuario, 'U001')
        self.assertEqual(usuario.nombre, 'María López')
        self.assertEqual(usuario.email, 'maria@email.com')
        self.assertTrue(usuario.activo)
    
    
    def test_crear_prestamo(self):
        """Prueba la creación de un préstamo"""
        prestamo = Prestamo('P001', '978-123', 'U001', '2025-10-12')
        self.assertEqual(prestamo.id_prestamo, 'P001')
        self.assertEqual(prestamo.isbn_libro, '978-123')
        self.assertIsNone(prestamo.fecha_devolucion)

if __name__ == '__main__':
    unittest.main()
