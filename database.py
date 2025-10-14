"""Módulo de persistencia de datos"""
import json
import os
from typing import List, Dict, Any

class Database:
    """Maneja la persistencia de datos en formato JSON"""
    
    def __init__(self, archivo: str = 'biblioteca.json'):
        self.archivo = archivo
        self.datos = self._cargar_datos()
    
    def _cargar_datos(self) -> Dict[str, List]:
        """Carga datos desde el archivo JSON"""
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {'libros': [], 'usuarios': [], 'prestamos': []}
        return {'libros': [], 'usuarios': [], 'prestamos': []}
    
    def guardar_datos(self) -> bool:
        """Guarda datos en el archivo JSON"""
        try:
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(self.datos, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
    
    def agregar(self, coleccion: str, elemento: Dict[str, Any]) -> bool:
        """Agrega un elemento a una colección"""
        if coleccion not in self.datos:
            self.datos[coleccion] = []
        self.datos[coleccion].append(elemento)
        return self.guardar_datos()
    
    def obtener_todos(self, coleccion: str) -> List[Dict]:
        """Obtiene todos los elementos de una colección"""
        return self.datos.get(coleccion, [])
    
    def buscar(self, coleccion: str, campo: str, valor: Any) -> List[Dict]:
        """Busca elementos por un campo específico"""
        elementos = self.datos.get(coleccion, [])
        return [e for e in elementos if e.get(campo) == valor]
    
    def actualizar(self, coleccion: str, campo: str, valor: Any, 
                   datos_nuevos: Dict[str, Any]) -> bool:
        """Actualiza un elemento en la colección"""
        elementos = self.datos.get(coleccion, [])
        for elemento in elementos:
            if elemento.get(campo) == valor:
                elemento.update(datos_nuevos)
                return self.guardar_datos()
        return False
