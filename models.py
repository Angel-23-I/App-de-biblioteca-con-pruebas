"""Módulo de modelos de datos"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Libro:
    """Representa un libro en la biblioteca"""
    isbn: str
    titulo: str
    autor: str
    disponible: bool = True
    
    def to_dict(self):
        return {
            'isbn': self.isbn,
            'titulo': self.titulo,
            'autor': self.autor,
            'disponible': self.disponible
        }
    
    @staticmethod
    def from_dict(data):
        return Libro(**data)

@dataclass
class Usuario:
    """Representa un usuario de la biblioteca"""
    id_usuario: str
    nombre: str
    email: str
    activo: bool = True
    
    def to_dict(self):
        return {
            'id_usuario': self.id_usuario,
            'nombre': self.nombre,
            'email': self.email,
            'activo': self.activo
        }
    
    @staticmethod
    def from_dict(data):
        return Usuario(**data)

@dataclass
class Prestamo:
    """Representa un préstamo de libro"""
    id_prestamo: str
    isbn_libro: str
    id_usuario: str
    fecha_prestamo: str
    fecha_devolucion: Optional[str] = None
    
    def to_dict(self):
        return {
            'id_prestamo': self.id_prestamo,
            'isbn_libro': self.isbn_libro,
            'id_usuario': self.id_usuario,
            'fecha_prestamo': self.fecha_prestamo,
            'fecha_devolucion': self.fecha_devolucion
        }
    
    @staticmethod
    def from_dict(data):
        return Prestamo(**data)
