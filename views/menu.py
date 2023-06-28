import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from fpdf import FPDF
import pandas as pd
from datetime import datetime
try:
    from controllers.controller import *
    import views.login as login
except ImportError:
    messagebox.showerror("Error", "Ingreso no autorizado")
class MainMenu:
    def __init__(self,login_window):
        if hasattr(login_window, "session_usuario") and login_window.session_usuario: 
            self.window = tk.Tk()
            self.window.title("Menú Principal")
            self.center_window(login_window)
                   
            # Crear un marco para la barra lateral izquierda
            self.sidebar_frame = tk.Frame(self.window, bg="lightgray", width=200)
            self.sidebar_frame.pack(side="left", fill="y")

            # Crear opciones del menú
            self.option1_button = tk.Button(self.sidebar_frame, text="Exportar como PDF", command=lambda:self.exportar_pdf(login_window))
            self.option1_button.pack(fill="x")

            self.option2_button = tk.Button(self.sidebar_frame, text="Exportar como Excel", command=lambda:self.exportar_excel(login_window))
            self.option2_button.pack(fill="x")

            if (login_window.session_nombre_rol =="administrador"):
                self.option3_button = tk.Button(self.sidebar_frame, text="Crear Categoria", command=lambda:self.crear_categoria(login_window))
                self.option3_button.pack(fill="x")

            # Espacio en blanco entre las opciones y el botón de cerrar sesión
            self.sidebar_space = tk.Frame(self.sidebar_frame, height=20, bg="lightgray")
            self.sidebar_space.pack(fill="x")

            # Botón de cerrar sesión
            self.logout_button = tk.Button(self.sidebar_frame, text="Cerrar Sesión", command=lambda:self.logout(login_window))
            self.logout_button.pack(side="bottom", fill="x")

            # Mostrar el mensaje de bienvenida
            self.welcome_label = tk.Label(self.window, text=f"Bienvenido {login_window.session_nombre} {login_window.session_apellido}", font=("Arial", 14))
            self.welcome_label.pack(anchor="nw", padx=10, pady=10)

            # Contenedor para los buscadores
            self.search_frame = tk.Frame(self.window)
            self.search_frame.pack(pady=10)

            # Campo de usuario
            self.producto_label = tk.Label(self.search_frame, text="Buscar Producto:")
            self.producto_label.pack(side="left", padx=5, pady=5)
            # Agregar un cuadro de entrada para el buscador
            self.search_entry_producto = tk.Entry(self.search_frame)
            # Cambiar el evento del botón de búsqueda al evento "<KeyRelease>"
            self.search_entry_producto.bind("<KeyRelease>", lambda event:self.search_productos(login_window))
            self.search_entry_producto.pack(side="left", padx=5, pady=5)

            #self.search_entry_categoria.bind("<KeyRelease>", lambda event:self.search_categoria(login_window))
            #self.search_entry_categoria.pack(side="left", padx=5, pady=5)
            
            # Agregar un botón de búsqueda
            #self.search_button = tk.Button(self.window, text="Buscar", command=lambda:self.search_productos(login_window))
            #self.search_button.pack()
            
            if (login_window.session_nombre_rol =="administrador"):
                self.table = ttk.Treeview(self.window, columns=("ID Producto", "Nombre", "Categoría", "Usuario"))
            else:
                self.table = ttk.Treeview(self.window, columns=("ID Producto", "Nombre", "Categoría"))
            self.table.heading("#0", text="")
            self.table.heading("ID Producto", text="ID Producto")
            self.table.heading("Nombre", text="Nombre")
            self.table.heading("Categoría", text="Categoría")
            if (login_window.session_nombre_rol =="administrador"):
                self.table.heading("Usuario", text="Usuario")

            self.table.column("#0", width=1)
            self.table.column("ID Producto", width=100)
            self.table.column("Nombre", width=150)
            self.table.column("Categoría", width=150)
            if (login_window.session_nombre_rol =="administrador"):
                self.table.column("Usuario", width=250)

            self.table.pack(pady=10)

            if (login_window.session_nombre_rol =="administrador"):
                # Configurar botones de acción
                self.table.bind("<Double-1>", self.editar_producto)  # Doble clic para editar
                self.table.bind("<Delete>", self.eliminar_producto)  # Tecla "Delete" para eliminar

                # Botón "Crear"
                self.create_button = tk.Button(self.window, text="Crear Producto", command=lambda:self.crear_producto(login_window))
                self.create_button.pack(pady=10)
            
            self.load_data(login_window)
            # Aplicar estilo para centrar valores por fila
            columns_to_center = ["ID Producto", "Nombre", "Categoría"]
            for column in columns_to_center:
                self.table.column(column, anchor="center")
            # Cargar datos de ejemplo
            self.window.mainloop()
        else:
            messagebox.showerror("Error", "No se ha iniciado sesión")
            self.window.destroy()
            #login.LoginWindow()
    
    def load_data(self,login_window):
        if (login_window.session_nombre_rol =="administrador"):
            products = [
                {
                    "id_producto": item[3],
                    "nombre": item[4],
                    "categoria": item[5],
                    "usuario": f"{item[0]}:{item[1]} {item[2]}"
                } for item in get_usuario_categoria_productos_all()]
            for product in products:
                self.table.insert("", tk.END, text="", values=(
                    product["id_producto"], product["nombre"], product["categoria"], product["usuario"]))
        else:   
            products = [
                {
                    "id_producto": item[3],
                    "nombre": item[4],
                    "categoria": item[5],
                    "usuario": f"{item[0]}:{item[1]} {item[2]}"
                } for item in get_usuario_categoria_productos(login_window.session_usuario)]
            for product in products:
                self.table.insert("", tk.END, text="", values=(
                        product["id_producto"], product["nombre"], product["categoria"]))
        
    def search_productos(self,login_window):
        # Obtener el término de búsqueda ingresado por el usuario
        query = self.search_entry_producto.get()

        # Verificar si el término de búsqueda está vacío
        if not query:
            self.limpiar_tabla()
            # Si está vacío, cargar todos los productos nuevamente
            self.load_data(login_window)
        else:
            # Realizar la búsqueda de productos en la base de datos
            # y actualizar la tabla con los resultados de la búsqueda
            if (login_window.session_nombre_rol =="administrador"):
                productos_encontrados = get_busqueda_producto_all(query)
                self.update_table(productos_encontrados,login_window)
            else:
                productos_encontrados = get_busqueda_producto(login_window.session_usuario,query)
                self.update_table(productos_encontrados,login_window)
                
    def limpiar_tabla(self):
        self.table.delete(*self.table.get_children())
    def update_table(self, search_encontrado,login_window):
        # Borrar todos los elementos de la tabla
        self.table.delete(*self.table.get_children())
        products = [
            {
                "id_producto": item[3],
                "nombre": item[4],
                "categoria": item[5],
                "usuario": f"{item[0]}:{item[1]} {item[2]}"
            } for item in search_encontrado]
        for product in products:
            if (login_window.session_nombre_rol =="administrador"):
                self.table.insert("", tk.END, values=(
                    product["id_producto"], product["nombre"], product["categoria"], product["usuario"]))
            else:
                self.table.insert("", tk.END, values=(
                    product["id_producto"], product["nombre"], product["categoria"]))
                
    def editar_producto(self, event):
        item = self.table.selection()
        if item:
            values = self.table.item(item)["values"]
            # Aquí puedes implementar la lógica para editar el producto con el ID seleccionado
            id_producto = values[0]
            nombre = values[1]
            categoria_name = values[2]
            #usuario = values[3]
            self.dialog = tk.Toplevel(self.window)
            self.dialog.title("Editar Producto")
            self.center_edit()
            nombre_label = tk.Label(self.dialog, text="Nombre:")
            nombre_label.pack()
            nombre_entry = tk.Entry(self.dialog)
            nombre_entry.insert(0, nombre)
            nombre_entry.pack()

            categoria_label = tk.Label(self.dialog, text="Categoría:")
            categoria_label.pack()
            categorias = get_categorias()
            combobox_categorias = ttk.Combobox(self.dialog, values=[categoria[1] for categoria in categorias])
            #combobox_categorias.set(categoria)
            for categoria in categorias:
                if categoria[1] == categoria_name:
                    combobox_categorias.set(categoria[1])
                    break
            combobox_categorias.pack()
            # Agregar un botón para guardar los cambios
            save_button = tk.Button(self.dialog, text="Guardar", command=lambda: self.guardar_cambios(item,id_producto ,nombre_entry.get(), combobox_categorias.get(),categorias, self.dialog))
            save_button.pack()
            print(f"Editar producto con ID: {id_producto}")

    def eliminar_producto(self, event):
        item = self.table.selection()
        if item:
            id_producto = self.table.item(item)["values"][0]
            confirmar = messagebox.askokcancel("Eliminado", f"¿Está seguro de eliminar el producto con ID {id_producto}?")
            if confirmar:
                data = delete_producto(id_producto)
                if data!=0:
                    messagebox.showinfo("Eliminación", "¡Dato eliminado con exito!")
                    self.table.delete(item)
                else:
                    messagebox.showinfo("Eliminación", "¡Hubo un error al eliminar!")

    def crear_producto(self,login_window):
        # Aquí puedes implementar la lógica para crear un nuevo producto
        self.dialog_create = tk.Toplevel(self.window)
        self.dialog_create.title("Crear Producto")
        self.center_create()

        nombre_label = tk.Label(self.dialog_create, text="Nombre:")
        nombre_label.pack()
        nombre_entry = tk.Entry(self.dialog_create)
        nombre_entry.pack()

        categoria_label = tk.Label(self.dialog_create, text="Categoría:")
        categoria_label.pack()
        categorias = get_categorias()
        combobox_categorias = ttk.Combobox(self.dialog_create, values=[categoria[1] for categoria in categorias])
        combobox_categorias.pack()

        # Agregar un botón para guardar el nuevo producto
        save_button = tk.Button(self.dialog_create, text="Guardar", command=lambda: self.guardar_nuevo_producto(nombre_entry.get(), combobox_categorias.get(), categorias, login_window))
        save_button.pack()
        print("Crear nuevo producto")
    def guardar_cambios(self, item_id,id_producto,nombre, categoria,categorias, dialog):
        # Actualizar los valores en la tabla
        if(len(nombre)!=0):
            for category in categorias:
                if category[1] == categoria:
                    data = update_producto(id_producto,nombre,category[0])
                    if data!=0:
                        messagebox.showinfo("Actualización", "¡Datos actualizados con exito!")
                        self.table.set(item_id, column="Nombre", value=nombre)
                        self.table.set(item_id, column="Categoría", value=categoria)
                    else:
                        messagebox.showinfo("Actualización", "¡Hubo un error al actualizar!")
                    break 
            # Cerrar el cuadro de diálogo
            self.dialog.destroy()
        else:
            messagebox.showinfo("Actualización", "No puede dejar campos vacios")
    def guardar_nuevo_producto(self, nombre, categoria, categorias, login_window):
        # Agrega aquí la lógica para guardar el nuevo producto en la base de datos
        # y actualizar la tabla
        # Obtener el ID de la categoría seleccionada
        categoria_id = None
        if(len(nombre)!=0 and len(categoria)!=0):
            for category in categorias:
                if category[1] == categoria:
                    categoria_id = category[0]
                    data = insert_producto(nombre,category[0])
                    if data == 0:
                        messagebox.showinfo("Creación", "¡Hubo un error al crear producto!")
                    elif data == -1:
                        messagebox.showinfo("Creación", "El producto ya existe")
                    else:
                        messagebox.showinfo("Creación", "¡Datos creados con exito!")
                        new_product_id = data  # Obtener el ID del nuevo producto creado (si es necesario)
                        if (login_window.session_nombre_rol =="administrador"):
                            self.table.insert("", tk.END, values=(new_product_id, nombre, categoria, f"{login_window.session_usuario}:{login_window.session_nombre} {login_window.session_apellido}"))
                        else:
                            self.table.insert("", tk.END, values=(new_product_id, nombre, categoria))
                    break       
            # Cerrar el cuadro de diálogo
            self.dialog_create.destroy()
        else:
            messagebox.showerror("Creación", "No puede dejar campos vacios")
    def center_edit(self):
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        window_width = 300
        window_height = 300
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
    def center_create(self):
        screen_width = self.dialog_create.winfo_screenwidth()
        screen_height = self.dialog_create.winfo_screenheight()
        window_width = 300
        window_height = 300
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.dialog_create.geometry(f"{window_width}x{window_height}+{x}+{y}")
    def center_categoria(self):
        screen_width = self.dialog_categoria.winfo_screenwidth()
        screen_height = self.dialog_categoria.winfo_screenheight()
        window_width = 300
        window_height = 300
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.dialog_categoria.geometry(f"{window_width}x{window_height}+{x}+{y}")
    def center_window(self,login_window):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        if (login_window.session_nombre_rol =="administrador"):
            window_width = 1000
        else:
            window_width = 600
        window_height = 400
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    def option1(self):
        print("Opción 1 seleccionada")

    def option2(self):
        print("Opción 2 seleccionada")

    def crear_categoria(self,login_window):
        self.dialog_categoria = tk.Toplevel(self.window)
        self.dialog_categoria.title("Crear Categoría")
        self.center_categoria()

        nombre_label = tk.Label(self.dialog_categoria, text="Nombre Categoria:")
        nombre_label.pack()
        nombre_entry = tk.Entry(self.dialog_categoria)
        nombre_entry.pack()

        usuario_label = tk.Label(self.dialog_categoria, text="Usuario Asignado:")
        usuario_label.pack()
        '''usuario_entry = tk.Entry(self.dialog_categoria)
        usuario_entry.pack()'''
        usuarios = get_usuario_all(login_window.session_nombre_rol)
        combobox_usuarios = ttk.Combobox(self.dialog_categoria, values=[f"{usuario[1]}: {usuario[2]} {usuario[3]}" for usuario in usuarios])
        combobox_usuarios.pack()

        # Agregar un botón para guardar la nueva categoría
        save_button = tk.Button(self.dialog_categoria, text="Guardar", command=lambda: self.guardar_nueva_categoria(nombre_entry.get(), combobox_usuarios.get(),usuarios, self.dialog_categoria))
        save_button.pack()

    def logout(self,login_window):
        if hasattr(login_window, "session_usuario"):
            del login_window.session_usuario
            del login_window.session_nombre
            del login_window.session_apellido
            del login_window.session_telefono
            del login_window.session_nombre_rol
        self.window.destroy()
        login.LoginWindow()
        # Agrega aquí el código para volver al inicio de sesión
    def guardar_nueva_categoria(self, nombre, usuario,usuarios, dialog):
        # Agrega aquí la lógica para guardar la nueva categoría en la base de datos
        # y actualizar la interfaz
        id_usuario = None
        # Verifica si los campos no están vacíos
        if len(nombre)!=0 and len(usuario)!=0:
            for user in usuarios:
                if f"{user[1]}: {user[2]} {user[3]}" == usuario:
                    id_usuario = user[0]
                    data = insert_categoria(nombre,id_usuario)
                    if data == 0:
                        messagebox.showinfo("Creación", "¡Hubo un error al crear la categoria!")
                    elif data == -1:
                        messagebox.showinfo("Creación", f"Categoria con nombre {nombre} ya existe.")
                    else:
                        messagebox.showinfo("Creación categoria", "¡Datos creados con exito!")
                    break
            self.dialog_categoria.destroy()
        else:
            messagebox.showerror("Error", "No puede dejar campos vacios")

    def exportar_pdf(self,login_window):
        # Crear el objeto PDF
        pdf = FPDF()

        # Configurar la página
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page(orientation="P")

        # Configurar la fuente y el tamaño
        pdf.set_font("Arial", size=12)

        # Agregar encabezados de columna
        if (login_window.session_nombre_rol == "administrador"):
            headers = ["ID Producto", "Nombre", "Categoría", "Usuario"]
        else:
            headers = ["ID Producto", "Nombre", "Categoría"]

        for header in headers[0:]:
            pdf.cell(40, 10, header, 1, 0, "C")

        pdf.ln()

        # Agregar filas de datos
        for item in self.table.get_children():
            for column in self.table["columns"][0:]:
                pdf.cell(40, 10, self.table.set(item, column), 1, 0, "C")
            pdf.ln()
        now = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        # Guardar el PDF
        pdf.output(f"resources/documents/tabla_{login_window.session_usuario}_{now}.pdf")

    # Función para exportar la tabla como Excel
    def exportar_excel(self,login_window):
        # Obtener los datos de la tabla
        data = []
        for item in self.table.get_children():
            values = []
            for column in self.table["columns"][0:]:
                values.append(self.table.set(item, column))
            data.append(values)

        # Crear un DataFrame de pandas con los datos
        if login_window.session_nombre_rol == "administrador":
            headers = ["ID Producto", "Nombre", "Categoría", "Usuario"]
        else:
            headers = ["ID Producto", "Nombre", "Categoría"]
        df = pd.DataFrame(data, columns=headers)
        now = datetime.now().strftime("%d.%m.%Y_%H.%M.%S")
        # Exportar el DataFrame como Excel
        df.to_excel(f"resources/documents/tabla_{login_window.session_usuario}_{now}.xlsx", index=False)