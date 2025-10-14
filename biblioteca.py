"""Módulo de lógica de negocio de la biblioteca"""
from datetime import datetime
from typing import List, Optional
from models import Libro, Usuario, Prestamo
from database import Database

class GestorBiblioteca:
    """Maneja la lógica de negocio de la biblioteca"""
    
    def __init__(self, db: Database):
        self.db = db
    
    # Gestión de Libros
    def agregar_libro(self, isbn: str, titulo: str, autor: str) -> bool:
        """Agrega un nuevo libro a la biblioteca"""
        if not isbn or not titulo or not autor:
            raise ValueError("Todos los campos son obligatorios")
        
        # Verificar que el ISBN no exista
        if self.db.buscar('libros', 'isbn', isbn):
            raise ValueError("El ISBN ya existe")
        
        libro = Libro(isbn, titulo, autor)
        return self.db.agregar('libros', libro.to_dict())
    
    def obtener_libros(self) -> List[Libro]:
        """Obtiene todos los libros"""
        libros_data = self.db.obtener_todos('libros')
        return [Libro.from_dict(l) for l in libros_data]
    
    def buscar_libro_por_isbn(self, isbn: str) -> Optional[Libro]:
        """Busca un libro por su ISBN"""
        resultados = self.db.buscar('libros', 'isbn', isbn)
        return Libro.from_dict(resultados[0]) if resultados else None
    
    # Gestión de Usuarios
    def registrar_usuario(self, id_usuario: str, nombre: str, email: str) -> bool:
        """Registra un nuevo usuario"""
        if not id_usuario or not nombre or not email:
            raise ValueError("Todos los campos son obligatorios")
        
        if '@' not in email:
            raise ValueError("Email inválido")
        
        if self.db.buscar('usuarios', 'id_usuario', id_usuario):
            raise ValueError("El ID de usuario ya existe")
        
        usuario = Usuario(id_usuario, nombre, email)
        return self.db.agregar('usuarios', usuario.to_dict())
    
    def obtener_usuarios(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        usuarios_data = self.db.obtener_todos('usuarios')
        return [Usuario.from_dict(u) for u in usuarios_data]
    
    def buscar_usuario_por_id(self, id_usuario: str) -> Optional[Usuario]:
        """Busca un usuario por su ID"""
        resultados = self.db.buscar('usuarios', 'id_usuario', id_usuario)
        return Usuario.from_dict(resultados[0]) if resultados else None
    
    # Gestión de Préstamos
    def prestar_libro(self, isbn: str, id_usuario: str) -> bool:
        """Registra un préstamo de libro"""
        libro = self.buscar_libro_por_isbn(isbn)
        if not libro:
            raise ValueError("Libro no encontrado")
        
        if not libro.disponible:
            raise ValueError("El libro no está disponible")
        
        usuario = self.buscar_usuario_por_id(id_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        if not usuario.activo:
            raise ValueError("Usuario inactivo")
        
        # Crear préstamo
        id_prestamo = f"P-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        prestamo = Prestamo(
            id_prestamo=id_prestamo,
            isbn_libro=isbn,
            id_usuario=id_usuario,
            fecha_prestamo=datetime.now().isoformat()
        )
        
        # Actualizar disponibilidad del libro
        self.db.actualizar('libros', 'isbn', isbn, {'disponible': False})
        
        return self.db.agregar('prestamos', prestamo.to_dict())
    
    def devolver_libro(self, isbn: str) -> bool:
        """Registra la devolución de un libro"""
        # Buscar préstamo activo
        prestamos = self.db.buscar('prestamos', 'isbn_libro', isbn)
        prestamo_activo = None
        
        for p in prestamos:
            if p.get('fecha_devolucion') is None:
                prestamo_activo = p
                break
        
        if not prestamo_activo:
            raise ValueError("No hay préstamo activo para este libro")
        
        # Actualizar préstamo
        self.db.actualizar(
            'prestamos', 
            'id_prestamo', 
            prestamo_activo['id_prestamo'],
            {'fecha_devolucion': datetime.now().isoformat()}
        )
        
        # Actualizar disponibilidad del libro
        return self.db.actualizar('libros', 'isbn', isbn, {'disponible': True})
    
    def obtener_prestamos_activos(self) -> List[Prestamo]:
        """Obtiene todos los préstamos activos"""
        prestamos_data = self.db.obtener_todos('prestamos')
        activos = [p for p in prestamos_data if p.get('fecha_devolucion') is None]
        return [Prestamo.from_dict(p) for p in activos]
