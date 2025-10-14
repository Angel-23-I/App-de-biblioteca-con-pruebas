"""Interfaz gráfica de usuario con Tkinter"""
import tkinter as tk
from tkinter import ttk, messagebox
from biblioteca import GestorBiblioteca
from database import Database

class BibliotecaGUI:
    """Interfaz gráfica para el sistema de biblioteca"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Biblioteca")
        self.root.geometry("800x600")
        
        self.db = Database()
        self.gestor = GestorBiblioteca(self.db)
        
        self.crear_widgets()
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestañas
        self.tab_libros = ttk.Frame(self.notebook)
        self.tab_usuarios = ttk.Frame(self.notebook)
        self.tab_prestamos = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_libros, text='Libros')
        self.notebook.add(self.tab_usuarios, text='Usuarios')
        self.notebook.add(self.tab_prestamos, text='Préstamos')
        
        self.crear_tab_libros()
        self.crear_tab_usuarios()
        self.crear_tab_prestamos()
    
    def crear_tab_libros(self):
        """Crea la pestaña de gestión de libros"""
        frame_form = ttk.LabelFrame(self.tab_libros, text="Agregar Libro", padding=10)
        frame_form.pack(fill='x', padx=10, pady=10)
        
        # Campos
        ttk.Label(frame_form, text="ISBN:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_isbn = ttk.Entry(frame_form, width=30)
        self.entry_isbn.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Título:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_titulo = ttk.Entry(frame_form, width=30)
        self.entry_titulo.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame_form, text="Autor:").grid(row=2, column=0, sticky='w', pady=5)
        self.entry_autor = ttk.Entry(frame_form, width=30)
        self.entry_autor.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame_form, text="Agregar", command=self.agregar_libro).grid(
            row=3, column=0, columnspan=2, pady=10)
        
        # Lista de libros
        frame_lista = ttk.LabelFrame(self.tab_libros, text="Libros Registrados", padding=10)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree_libros = ttk.Treeview(
            frame_lista, 
            columns=('ISBN', 'Título', 'Autor', 'Disponible'),
            show='headings'
        )
        self.tree_libros.heading('ISBN', text='ISBN')
        self.tree_libros.heading('Título', text='Título')
        self.tree_libros.heading('Autor', text='Autor')
        self.tree_libros.heading('Disponible', text='Disponible')
        self.tree_libros.pack(fill='both', expand=True)
        
        ttk.Button(frame_lista, text="Actualizar Lista", 
                   command=self.actualizar_lista_libros).pack(pady=5)
        
        self.actualizar_lista_libros()
    
    def crear_tab_usuarios(self):
        """Crea la pestaña de gestión de usuarios"""
        frame_form = ttk.LabelFrame(self.tab_usuarios, text="Registrar Usuario", padding=10)
        frame_form.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_form, text="ID Usuario:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_id_usuario = ttk.Entry(frame_form, width=30)
        self.entry_id_usuario.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_nombre = ttk.Entry(frame_form, width=30)
        self.entry_nombre.grid(row=1, column=1, pady=5)
        
        ttk.Label(frame_form, text="Email:").grid(row=2, column=0, sticky='w', pady=5)
        self.entry_email = ttk.Entry(frame_form, width=30)
        self.entry_email.grid(row=2, column=1, pady=5)
        
        ttk.Button(frame_form, text="Registrar", command=self.registrar_usuario).grid(
            row=3, column=0, columnspan=2, pady=10)
        
        # Lista de usuarios
        frame_lista = ttk.LabelFrame(self.tab_usuarios, text="Usuarios Registrados", padding=10)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree_usuarios = ttk.Treeview(
            frame_lista,
            columns=('ID', 'Nombre', 'Email', 'Activo'),
            show='headings'
        )
        self.tree_usuarios.heading('ID', text='ID')
        self.tree_usuarios.heading('Nombre', text='Nombre')
        self.tree_usuarios.heading('Email', text='Email')
        self.tree_usuarios.heading('Activo', text='Activo')
        self.tree_usuarios.pack(fill='both', expand=True)
        
        ttk.Button(frame_lista, text="Actualizar Lista",
                   command=self.actualizar_lista_usuarios).pack(pady=5)
        
        self.actualizar_lista_usuarios()
    
    def crear_tab_prestamos(self):
        """Crea la pestaña de gestión de préstamos"""
        frame_prestar = ttk.LabelFrame(self.tab_prestamos, text="Prestar Libro", padding=10)
        frame_prestar.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_prestar, text="ISBN Libro:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_isbn_prestamo = ttk.Entry(frame_prestar, width=30)
        self.entry_isbn_prestamo.grid(row=0, column=1, pady=5)
        
        ttk.Label(frame_prestar, text="ID Usuario:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_id_prestamo = ttk.Entry(frame_prestar, width=30)
        self.entry_id_prestamo.grid(row=1, column=1, pady=5)
        
        ttk.Button(frame_prestar, text="Prestar", command=self.prestar_libro).grid(
            row=2, column=0, columnspan=2, pady=10)
        
        # Devolución
        frame_devolver = ttk.LabelFrame(self.tab_prestamos, text="Devolver Libro", padding=10)
        frame_devolver.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_devolver, text="ISBN Libro:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_isbn_devolucion = ttk.Entry(frame_devolver, width=30)
        self.entry_isbn_devolucion.grid(row=0, column=1, pady=5)
        
        ttk.Button(frame_devolver, text="Devolver", command=self.devolver_libro).grid(
            row=1, column=0, columnspan=2, pady=10)
        
        # Lista de préstamos activos
        frame_lista = ttk.LabelFrame(self.tab_prestamos, text="Préstamos Activos", padding=10)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.tree_prestamos = ttk.Treeview(
            frame_lista,
            columns=('ID Préstamo', 'ISBN', 'ID Usuario', 'Fecha'),
            show='headings'
        )
        self.tree_prestamos.heading('ID Préstamo', text='ID Préstamo')
        self.tree_prestamos.heading('ISBN', text='ISBN')
        self.tree_prestamos.heading('ID Usuario', text='ID Usuario')
        self.tree_prestamos.heading('Fecha', text='Fecha Préstamo')
        self.tree_prestamos.pack(fill='both', expand=True)
        
        ttk.Button(frame_lista, text="Actualizar Lista",
                   command=self.actualizar_lista_prestamos).pack(pady=5)
        
        self.actualizar_lista_prestamos()
    
    def agregar_libro(self):
        """Agrega un libro al sistema"""
        try:
            isbn = self.entry_isbn.get().strip()
            titulo = self.entry_titulo.get().strip()
            autor = self.entry_autor.get().strip()
            
            self.gestor.agregar_libro(isbn, titulo, autor)
            messagebox.showinfo("Éxito", "Libro agregado correctamente")
            
            self.entry_isbn.delete(0, tk.END)
            self.entry_titulo.delete(0, tk.END)
            self.entry_autor.delete(0, tk.END)
            
            self.actualizar_lista_libros()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def registrar_usuario(self):
        """Registra un usuario en el sistema"""
        try:
            id_usuario = self.entry_id_usuario.get().strip()
            nombre = self.entry_nombre.get().strip()
            email = self.entry_email.get().strip()
            
            self.gestor.registrar_usuario(id_usuario, nombre, email)
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            
            self.entry_id_usuario.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.entry_email.delete(0, tk.END)
            
            self.actualizar_lista_usuarios()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def prestar_libro(self):
        """Registra un préstamo de libro"""
        try:
            isbn = self.entry_isbn_prestamo.get().strip()
            id_usuario = self.entry_id_prestamo.get().strip()
            
            self.gestor.prestar_libro(isbn, id_usuario)
            messagebox.showinfo("Éxito", "Préstamo registrado correctamente")
            
            self.entry_isbn_prestamo.delete(0, tk.END)
            self.entry_id_prestamo.delete(0, tk.END)
            
            self.actualizar_lista_libros()
            self.actualizar_lista_prestamos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def devolver_libro(self):
        """Registra la devolución de un libro"""
        try:
            isbn = self.entry_isbn_devolucion.get().strip()
            
            self.gestor.devolver_libro(isbn)
            messagebox.showinfo("Éxito", "Devolución registrada correctamente")
            
            self.entry_isbn_devolucion.delete(0, tk.END)
            
            self.actualizar_lista_libros()
            self.actualizar_lista_prestamos()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def actualizar_lista_libros(self):
        """Actualiza la lista de libros en la interfaz"""
        for item in self.tree_libros.get_children():
            self.tree_libros.delete(item)
        
        libros = self.gestor.obtener_libros()
        for libro in libros:
            self.tree_libros.insert('', 'end', values=(
                libro.isbn, libro.titulo, libro.autor,
                'Sí' if libro.disponible else 'No'
            ))
    
    def actualizar_lista_usuarios(self):
        """Actualiza la lista de usuarios en la interfaz"""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        usuarios = self.gestor.obtener_usuarios()
        for usuario in usuarios:
            self.tree_usuarios.insert('', 'end', values=(
                usuario.id_usuario, usuario.nombre, usuario.email,
                'Sí' if usuario.activo else 'No'
            ))
    
    def actualizar_lista_prestamos(self):
        """Actualiza la lista de préstamos en la interfaz"""
        for item in self.tree_prestamos.get_children():
            self.tree_prestamos.delete(item)
        
        prestamos = self.gestor.obtener_prestamos_activos()
        for prestamo in prestamos:
            fecha = prestamo.fecha_prestamo.split('T')[0]
            self.tree_prestamos.insert('', 'end', values=(
                prestamo.id_prestamo, prestamo.isbn_libro,
                prestamo.id_usuario, fecha
            ))

def main():
    """Función principal para ejecutar la aplicación"""
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
