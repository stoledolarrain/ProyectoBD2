import tkinter as tk
from tkinter import Toplevel, messagebox
from tkcalendar import Calendar
import psycopg2


class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Polideportivo")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        self.usuario_logueado = None  # Variable para el usuario logueado
        self.boton_cerrar_sesion = None  # Referencia al botón "Cerrar Sesión"

        # Conexión a la base de datos
        self.conectar_base_datos()

        # Crear el marco superior para el título
        self.frame_titulo = tk.Frame(self.root, bg="#0073e6", height=80)
        self.frame_titulo.pack(fill=tk.X)

        # Título principal
        self.label_titulo = tk.Label(
            self.frame_titulo,
            text="Sistema de Polideportivo",
            font=("Helvetica", 20, "bold"),
            bg="#0073e6",
            fg="white"
        )
        self.label_titulo.pack(side=tk.LEFT, pady=20, padx=10)

        # Botón de "Iniciar Sesión" en el marco superior
        self.boton_sesion = tk.Button(
            self.frame_titulo,
            text="Iniciar Sesión",
            font=("Helvetica", 12),
            bg="#004080",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            activebackground="#0059b3",
            command=self.mostrar_login
        )
        self.boton_sesion.pack(side=tk.RIGHT, pady=20, padx=20)

        # Crear el menú lateral
        self.frame_menu = tk.Frame(self.root, bg="#004080", width=250)
        self.frame_menu.pack(side=tk.LEFT, fill=tk.Y)

        # Opciones del menú lateral
        self.menu_items = ["Inicio", "Eventos", "Jugadores", "Calendario", "Estadísticas"]
        self.botones_menu = []

        for item in self.menu_items:
            boton = tk.Button(
                self.frame_menu,
                text=item,
                font=("Helvetica", 12),
                bg="#0059b3",
                fg="white",
                bd=0,
                relief=tk.FLAT,
                activebackground="#0073e6",
                activeforeground="white",
                command=lambda opcion=item: self.navegar(opcion)
            )
            boton.pack(fill=tk.X, pady=5, padx=10)
            self.botones_menu.append(boton)

        # Crear el área principal de contenido
        self.frame_contenido = tk.Frame(self.root, bg="white")
        self.frame_contenido.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        # Etiqueta de contenido inicial
        self.label_contenido = tk.Label(
            self.frame_contenido,
            text="Bienvenido al Sistema de Polideportivo",
            font=("Helvetica", 16),
            bg="white",
            fg="#333"
        )
        self.label_contenido.pack(pady=20)

    def conectar_base_datos(self):
        """Conecta a la base de datos PostgreSQL."""
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                database="boliviasport",
                user="postgres",
                password="root",
                port=5501
            )
            print("Conexión exitosa a la base de datos.")
        except psycopg2.Error as e:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {e}")
            self.connection = None

    def navegar(self, opcion):
        """Función para manejar la navegación del menú."""
        # Limpiar el área de contenido antes de mostrar algo nuevo
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        if opcion == "Calendario":
            self.mostrar_calendario()
        else:
            self.label_contenido = tk.Label(
                self.frame_contenido,
                text=f"Has seleccionado: {opcion}",
                font=("Helvetica", 16),
                bg="white",
                fg="#333"
            )
            self.label_contenido.pack(pady=20)

    def mostrar_calendario(self):
        """Muestra un calendario en el área principal."""
        cal = Calendar(
            self.frame_contenido,
            selectmode="day",
            year=2024,
            month=11,
            day=1,
            font=("Helvetica", 16),
            width=25,
            height=10
        )
        cal.pack(pady=20, padx=20)

        def mostrar_fecha():
            fecha_seleccionada = cal.get_date()
            messagebox.showinfo("Fecha Seleccionada", f"Has seleccionado: {fecha_seleccionada}")

        boton_fecha = tk.Button(
            self.frame_contenido,
            text="Mostrar Fecha Seleccionada",
            font=("Helvetica", 12),
            bg="#004080",
            fg="white",
            command=mostrar_fecha
        )
        boton_fecha.pack(pady=10)

    def mostrar_login(self):
        """Ventana de inicio de sesión."""
        ventana_login = Toplevel(self.root)
        ventana_login.title("Iniciar Sesión")
        ventana_login.geometry("400x300")
        ventana_login.configure(bg="#f0f0f0")

        tk.Label(ventana_login, text="Usuario:", font=("Helvetica", 12)).pack(pady=10)
        usuario_entry = tk.Entry(ventana_login, font=("Helvetica", 12))
        usuario_entry.pack(pady=5)

        tk.Label(ventana_login, text="Contraseña:", font=("Helvetica", 12)).pack(pady=10)
        contrasena_entry = tk.Entry(ventana_login, show="*", font=("Helvetica", 12))
        contrasena_entry.pack(pady=5)

        def iniciar_sesion():
            usuario = usuario_entry.get()
            contrasena = contrasena_entry.get()
            if not self.connection:
                messagebox.showerror("Error", "No hay conexión a la base de datos.")
                return

            consulta = "SELECT nombre FROM Usuarios WHERE username = %s AND contrasena = %s"
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(consulta, (usuario, contrasena))
                    resultado = cursor.fetchone()
                    if resultado:
                        self.usuario_logueado = resultado[0]
                        messagebox.showinfo("Login", f"Bienvenido: {self.usuario_logueado}")
                        ventana_login.destroy()
                        self.actualizar_interfaz_usuario()
                    else:
                        messagebox.showerror("Error", "Credenciales incorrectas.")
            except psycopg2.Error as e:
                messagebox.showerror("Error de Consulta", f"Error al ejecutar la consulta: {e}")

        def registrar():
            ventana_login.destroy()
            self.mostrar_registro()

        tk.Button(ventana_login, text="Iniciar Sesión", font=("Helvetica", 12),
                  command=iniciar_sesion, bg="#004080", fg="white").pack(pady=10)

        tk.Button(ventana_login, text="Registrar", font=("Helvetica", 12),
                  command=registrar, bg="#0059b3", fg="white").pack(pady=10)

    def mostrar_registro(self):
        """Ventana de registro."""
        ventana_registro = Toplevel(self.root)
        ventana_registro.title("Registrarse")
        ventana_registro.geometry("400x500")
        ventana_registro.configure(bg="#f0f0f0")

        tk.Label(ventana_registro, text="Nombre:", font=("Helvetica", 12)).pack(pady=5)
        nombre_entry = tk.Entry(ventana_registro, font=("Helvetica", 12))
        nombre_entry.pack(pady=5)

        tk.Label(ventana_registro, text="Apellido:", font=("Helvetica", 12)).pack(pady=5)
        apellido_entry = tk.Entry(ventana_registro, font=("Helvetica", 12))
        apellido_entry.pack(pady=5)

        tk.Label(ventana_registro, text="Correo:", font=("Helvetica", 12)).pack(pady=5)
        correo_entry = tk.Entry(ventana_registro, font=("Helvetica", 12))
        correo_entry.pack(pady=5)

        tk.Label(ventana_registro, text="Teléfono:", font=("Helvetica", 12)).pack(pady=5)
        telefono_entry = tk.Entry(ventana_registro, font=("Helvetica", 12))
        telefono_entry.pack(pady=5)

        tk.Label(ventana_registro, text="Fecha de Nacimiento (YYYY-MM-DD):", font=("Helvetica", 12)).pack(pady=5)
        fecha_nacimiento_entry = tk.Entry(ventana_registro, font=("Helvetica", 12))
        fecha_nacimiento_entry.pack(pady=5)

        tk.Label(ventana_registro, text="Usuario:", font=("Helvetica", 12)).pack(pady=5)
        usuario_entry = tk.Entry(ventana_registro, font=("Helvetica", 12))
        usuario_entry.pack(pady=5)

        tk.Label(ventana_registro, text="Contraseña:", font=("Helvetica", 12)).pack(pady=5)
        contrasena_entry = tk.Entry(ventana_registro, show="*", font=("Helvetica", 12))
        contrasena_entry.pack(pady=5)

        def registrar_usuario():
            nombre = nombre_entry.get()
            apellido = apellido_entry.get()
            correo = correo_entry.get()
            telefono = telefono_entry.get()
            fecha_nacimiento = fecha_nacimiento_entry.get()
            usuario = usuario_entry.get()
            contrasena = contrasena_entry.get()

            if not (nombre and apellido and correo and fecha_nacimiento and usuario and contrasena):
                messagebox.showerror("Error", "Todos los campos son obligatorios.")
                return

            if not self.connection:
                messagebox.showerror("Error", "No hay conexión a la base de datos.")
                return

            consulta = """
            INSERT INTO Usuarios (nombre, apellido, correo, telefono, fecha_nacimiento, username, contrasena)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(consulta, (nombre, apellido, correo, telefono, fecha_nacimiento, usuario, contrasena))
                    self.connection.commit()
                    messagebox.showinfo("Registro", f"Usuario {usuario} registrado correctamente.")
                    ventana_registro.destroy()
            except psycopg2.Error as e:
                messagebox.showerror("Error de Registro", f"Error al registrar el usuario: {e}")

        tk.Button(ventana_registro, text="Registrar", font=("Helvetica", 12),
                  command=registrar_usuario, bg="#004080", fg="white").pack(pady=20)

    def actualizar_interfaz_usuario(self):
        """Actualiza la interfaz gráfica para mostrar al usuario logueado."""
        if self.usuario_logueado:
            self.boton_sesion.destroy()
            self.label_usuario = tk.Label(
                self.frame_titulo,
                text=f"Usuario: {self.usuario_logueado}",
                font=("Helvetica", 12),
                bg="#0073e6",
                fg="white"
            )
            self.label_usuario.pack(side=tk.RIGHT, pady=20, padx=20)

            # Agregar botón "Cerrar Sesión" al menú lateral
            self.boton_cerrar_sesion = tk.Button(
                self.frame_menu,
                text="Cerrar Sesión",
                font=("Helvetica", 12),
                bg="#FF4C4C",
                fg="white",
                bd=0,
                relief=tk.FLAT,
                activebackground="#FF6B6B",
                activeforeground="white",
                command=self.cerrar_sesion
            )
            self.boton_cerrar_sesion.pack(fill=tk.X, pady=5, padx=10)

    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual."""
        self.usuario_logueado = None

        # Restaurar el botón "Iniciar Sesión" en el encabezado
        self.label_usuario.destroy()
        self.boton_sesion = tk.Button(
            self.frame_titulo,
            text="Iniciar Sesión",
            font=("Helvetica", 12),
            bg="#004080",
            fg="white",
            bd=0,
            relief=tk.FLAT,
            activebackground="#0059b3",
            command=self.mostrar_login
        )
        self.boton_sesion.pack(side=tk.RIGHT, pady=20, padx=20)

        # Eliminar el botón "Cerrar Sesión" del menú lateral
        if self.boton_cerrar_sesion:
            self.boton_cerrar_sesion.destroy()

        # Restaurar el área de contenido al mensaje de bienvenida
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

        self.label_contenido = tk.Label(
            self.frame_contenido,
            text="Bienvenido al Sistema de Polideportivo",
            font=("Helvetica", 16),
            bg="white",
            fg="#333"
        )
        self.label_contenido.pack(pady=20)

        messagebox.showinfo("Cerrar Sesión", "Se ha cerrado la sesión.")

    def __del__(self):
        """Cierra la conexión al salir."""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")

# Crear la ventana principal y ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)
    root.mainloop()