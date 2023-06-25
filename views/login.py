import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
try:
    from controllers.controller import get_login,get_usuario,register_usuario
    import views.menu as menu
except ImportError:
    messagebox.showerror("Error", "Ingreso no autorizado")

class LoginWindow:
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("Login")
        self.center_window()
        # Configurar el contenido de la ventana de login
        # Logo
        self.logo_image = Image.open("resources/images/logo.png")
        self.logo_image = self.logo_image.resize((150, 175), Image.ANTIALIAS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = tk.Label(self.win, image=self.logo_photo)
        self.logo_label.pack(pady=20)

        # Campo de usuario
        self.username_label = tk.Label(self.win, text="Usuario:")
        self.username_label.pack()

        self.etusername = tk.Entry(self.win)
        self.etusername.pack(pady=5)

        # Campo de contraseña
        self.password_label = tk.Label(self.win, text="Contraseña:")
        self.password_label.pack()

        self.etpassword = tk.Entry(self.win, show="*")
        self.etpassword.pack(pady=5)
        self.etpassword.bind("<Return>", lambda event: self.login())

        # Botón de inicio de sesión
        self.login_button = tk.Button(self.win, text="Iniciar sesión", command=self.login)
        self.login_button.pack(pady=10)


        self.bottom_frame = tk.Frame(self.win)
        self.bottom_frame.pack(side=tk.BOTTOM, pady=10)

        self.register_label = tk.Label(self.bottom_frame, text="No tengo usuario, click aqui.", fg="blue", cursor="hand2")
        self.register_label.pack(side=tk.BOTTOM)
        self.register_label.bind("<Button-1>", lambda event: self.register())

        self.win.mainloop()

    def center_window(self):
        screen_width = self.win.winfo_screenwidth()
        screen_height = self.win.winfo_screenheight()
        window_width = 300
        window_height = 500
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.win.geometry(f"{window_width}x{window_height}+{x}+{y}")
    def center_window_register(self):
        screen_width = self.register_window.winfo_screenwidth()
        screen_height = self.register_window.winfo_screenheight()
        window_width = 300
        window_height = 500
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.register_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    def login(self):
        username = self.etusername.get()
        password = self.etpassword.get()
        if(len(username)!=0 and len(password)!=0):
            self.verificar_sesion = get_login(username,password)
            if len(self.verificar_sesion)!=0:
                self.data = get_usuario (username)
                for tupla in self.data:
                    self.session_usuario = tupla[0]
                    self.session_nombre = tupla[1]
                    self.session_apellido = tupla[2]
                    self.session_telefono = tupla[3]
                    self.session_nombre_rol = tupla[4]
                messagebox.showinfo("Inicio de sesión", "¡Inicio de sesión exitoso!")
                self.win.destroy()
                menu.MainMenu(self)
            else:
                messagebox.showerror("Inicio de sesión", "Credenciales inválidas")
        else:
            messagebox.showerror("Inicio de sesión", "No puede dejar campos vacios")
    def register(self):
        self.register_window = tk.Toplevel(self.win)
        self.register_window.title("Registro")
        self.center_window_register()
        # Etiqueta y campo de usuario
        username_label = tk.Label(self.register_window, text="Usuario:")
        username_label.pack()

        et_username = tk.Entry(self.register_window)
        et_username.pack()

        # Etiqueta y campo de contraseña
        password_label = tk.Label(self.register_window, text="Contraseña:")
        password_label.pack()

        et_password = tk.Entry(self.register_window, show="*")
        et_password.pack()

        # Etiqueta y campo de nombre
        nombre_label = tk.Label(self.register_window, text="Nombre:")
        nombre_label.pack()

        et_nombre = tk.Entry(self.register_window)
        et_nombre.pack()

        # Etiqueta y campo de apellido
        apellido_label = tk.Label(self.register_window, text="Apellido:")
        apellido_label.pack()

        et_apellido = tk.Entry(self.register_window)
        et_apellido.pack()

        # Etiqueta y campo de dirección
        direccion_label = tk.Label(self.register_window, text="Dirección:")
        direccion_label.pack()

        et_direccion = tk.Entry(self.register_window)
        et_direccion.pack()

        # Etiqueta y campo de teléfono
        telefono_label = tk.Label(self.register_window, text="Teléfono:")
        telefono_label.pack()

        et_telefono = tk.Entry(self.register_window)
        et_telefono.pack()

        # Botón de registro
        register_button = tk.Button(self.register_window, text="Registrar", command=lambda: self.register_user(et_username.get(), et_password.get(), et_nombre.get(), et_apellido.get(), et_direccion.get(), et_telefono.get()))
        register_button.pack(pady=10)

    def register_user(self, username, password, nombre, apellido, direccion, telefono):
        # Aquí puedes implementar la lógica para registrar al usuario
        # Puedes usar los datos ingresados en los campos del formulario
        # Utiliza los valores de las variables username, password, nombre, apellido, direccion, telefono
        if(len(username)!=0 and len(password)!=0 and len(nombre)!=0 and len(apellido)!=0 and len(direccion)!=0 and len(telefono)!=0):
            self.verificar_register = register_usuario(username, password, nombre, apellido, direccion, telefono)
            if self.verificar_register>0:
                messagebox.showinfo("Registro de usuario", "¡Registro exitoso!")
                self.register_window.destroy()
                #menu.MainMenu(self)
            else:
                messagebox.showerror("Registro de usuario", "Sucedio un error al registrar, pruebe nuevamente")
        else:
            messagebox.showerror("Registro de usuario", "No puede dejar campos vacios")
        # Una vez realizado el registro, puedes cerrar la ventana register_window
        