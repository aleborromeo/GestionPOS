import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sys
import os

class Inventario(tk.Frame):
    db_name = "basedatos.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.pack()
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.producto_id = None  # Para almacenar el ID del producto seleccionado
        self.widgets()
        
    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)
        
    def widgets(self): #clasificar los widgets
        frame1 = tk.Frame(self, bg="#E9C874", highlightbackground="#E0A75E", highlightthickness=5)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="INVENTARIO", bg="#E9C874", fg="#A34343", font=("Britannic Bold", 42), anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        frame2 = tk.Frame(self, bg="#FBF8DD", highlightbackground="#FBF8DD", highlightthickness=5)
        frame2.place(x=0, y=100, width=1100, height=550)



        labelframe = LabelFrame(frame2, text="Productos", bg="#FBF8DD", font=("Arial Black", 22))
        labelframe.place(x=20, y=30, width=400, height=500)

        lblnombre = Label(labelframe, text="Nombre: ", bg="#FBF8DD", font="sans 14 bold")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(labelframe, font="sans 14 bold") #cuadro de texto
        self.nombre.place(x=140, y=20, width=240, height=40)
        
        lblproveedor = Label(labelframe, text="Proveedor:", bg="#FBF8DD", font="sans 14 bold")
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Entry(labelframe, font="sans 14 bold") #cuadro de texto
        self.proveedor.place(x=140, y=80, width=240, height=40)

        lblprecio = Label(labelframe, text="Precio:", bg="#FBF8DD", font="sans 14 bold")
        lblprecio.place(x=10, y=140)
        self.precio = ttk.Entry(labelframe, font="sans 14 bold") #cuadro de texto
        self.precio.place(x=140, y=140, width=240, height=40)

        lblcosto = Label(labelframe, text="Costo:", bg="#FBF8DD", font="sans 14 bold") #precio de compra al distribuidor
        lblcosto.place(x=10, y=200)
        self.costo = ttk.Entry(labelframe, font="sans 14 bold") #cuadro de texto
        self.costo.place(x=140, y=200, width=240, height=40)

        lblstock = Label(labelframe, text="Stock:", bg="#FBF8DD", font="sans 14 bold")
        lblstock.place(x=10, y=260)
        self.stock = ttk.Entry(labelframe, font="sans 14 bold") #cuadro de texto
        self.stock.place(x=140, y=260, width=240, height=40) 



        boton_agregar = tk.Button(labelframe, text="Ingresar", font="sans 16 bold", fg="#FBF8DD", bg="#A34343", command=self.agregar_producto)
        boton_agregar.place(x=80, y=340, width=240, height=45)

        boton_editar = tk.Button(labelframe, text="Editar", font="sans 16 bold", fg="#FBF8DD", bg="#A34343", command=self.editar_producto)
        boton_editar.place(x=80, y=400, width=240, height=45)

        #tabla
        treFrame = Frame(frame2, bg="white")
        treFrame.place(x=440, y=70, width=620, height=400)

        #Barras de desplazamiento
        scrol_y = ttk.Scrollbar(treFrame) #vertical
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=("ID", "PRODUCTO", "PROVEEDOR", "PRECIO", "COSTO", "STOCK"), show="headings")
        #yscrollcommand=scrol_y.set ,,, el .set es para que pueda ejecutarse
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        #encabezados de las columnas de la tabla
        self.tre.heading("ID", text="ID")
        self.tre.heading("PRODUCTO", text="PRODUCTO")
        self.tre.heading("PROVEEDOR", text="PROVEEDOR")
        self.tre.heading("PRECIO", text="PRECIO")
        self.tre.heading("COSTO", text="COSTO")
        self.tre.heading("STOCK", text="STOCK")

        #Configuracion de tabla
        self.tre.column("ID", width=70, anchor="center")
        self.tre.column("PRODUCTO", width=100, anchor="center")
        self.tre.column("PROVEEDOR", width=100, anchor="center")
        self.tre.column("PRECIO", width=100, anchor="center")
        self.tre.column("COSTO", width=100, anchor="center")
        self.tre.column("STOCK", width=70, anchor="center")

        self.mostrar()

        # Evento para seleccionar un producto de la tabla
        #self.tre.bind("<Double-1>", self.seleccionar_producto)

    def eje_consulta(self, consulta, parametros=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(consulta, parametros)
            conn.commit()
        return result
    
    def validacion(self, nombre, prov, precio, costo, stock): #validacion de todas las celdas llenas
        if not (nombre and prov and precio and costo and stock):
            return False
        
        try:
            float(precio)
            float(costo)
            int(stock)
        except ValueError:
            return False
        
        return True
    
    def mostrar(self):
        consulta = "SELECT * FROM inventario ORDER BY id DESC"
        result = self.eje_consulta(consulta)

        # Limpiar la tabla antes de agregar los nuevos datos
        for item in self.tre.get_children():
            self.tre.delete(item)

        for elem in result:
            try:
                precio_s = "{:,.2f}".format(float(elem[3])) if elem[3] else ""
                costo_s = "{:,.2f}".format(float(elem[4])) if elem[4] else ""

            except ValueError:
                precio_s = elem[3]
                costo_s = elem[4]          

            self.tre.insert("", 0, text=elem[0], values=(elem[0], elem[1], elem[2], precio_s, costo_s, elem[5]))


    def agregar_producto(self):
        nombre = self.nombre.get()
        proveedor = self.proveedor.get()
        precio = self.precio.get()
        costo = self.costo.get()
        stock = self.stock.get()

        if self.validacion(nombre, proveedor, precio, costo, stock):
            consulta = "INSERT INTO inventario (nombre, proveedor, precio, costo, stock) VALUES (?, ?, ?, ?, ?)"
            parametros = (nombre, proveedor, precio, costo, stock)
            self.eje_consulta(consulta, parametros)
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.mostrar()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos correctamente")

    def editar_producto(self):
        seleccion = self.tre.selection()
        if not seleccion:
            messagebox.showwarning("Editar producto", "Seleccione un producto para editar.")
            return
        
        item_id = self.tre.item(seleccion)["text"]
        item_values = self.tre.item(seleccion)["values"]
        
        ventana_editar = Toplevel(self)
        ventana_editar.title("Editar producto")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#FBF8DD")
        
        lbl_nombre = Label(ventana_editar, text="Nombre:", font="sans 14 bold", bg="#FBF8DD")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10)
        entry_nombre = Entry(ventana_editar, font="sans 14 bold")
        entry_nombre.grid(row=0, column=1, padx=10, pady=10)
        entry_nombre.insert(0, item_values[1])
        
        lbl_proveedor = Label(ventana_editar, text="Proveedor:", font="sans 14 bold", bg="#FBF8DD")
        lbl_proveedor.grid(row=1, column=0, padx=10, pady=10)
        entry_proveedor = Entry(ventana_editar, font="sans 14 bold")
        entry_proveedor.grid(row=1, column=1, padx=10, pady=10)
        entry_proveedor.insert(0, item_values[2])
        
        lbl_precio = Label(ventana_editar, text="Precio:", font="sans 14 bold", bg="#FBF8DD")
        lbl_precio.grid(row=2, column=0, padx=10, pady=10)
        entry_precio = Entry(ventana_editar, font="sans 14 bold")
        entry_precio.grid(row=2, column=1, padx=10, pady=10)
        entry_precio.insert(0, item_values[3].replace(",", ""))
        
        lbl_costo = Label(ventana_editar, text="Costo:", font="sans 14 bold", bg="#FBF8DD")
        lbl_costo.grid(row=3, column=0, padx=10, pady=10)
        entry_costo = Entry(ventana_editar, font="sans 14 bold")
        entry_costo.grid(row=3, column=1, padx=10, pady=10)
        entry_costo.insert(0, item_values[4].replace(",", ""))
        
        lbl_stock = Label(ventana_editar, text="Stock:", font="sans 14 bold", bg="#FBF8DD")
        lbl_stock.grid(row=4, column=0, padx=10, pady=10)
        entry_stock = Entry(ventana_editar, font="sans 14 bold")
        entry_stock.grid(row=4, column=1, padx=10, pady=10)
        entry_stock.insert(0, item_values[5])
        
        #imagen
        ruta = self.rutas("img/editar.png")
        self.editar_producto_image = Image.open(ruta)
        self.editar_producto_image = self.editar_producto_image.resize((80, 80))
        self.editar_producto_image = ImageTk.PhotoImage(self.editar_producto_image)
        self.editar_producto_label = tk.Label(ventana_editar, image=self.editar_producto_image, bg="#FBF8DD")
        self.editar_producto_label.place(x=160, y=250)
        
        # Bloquear la ventana de editar_producto para que quede al frente
        ventana_editar.grab_set()
        ventana_editar.focus_set()
        
        def guardar_cambios():
            nombre = entry_nombre.get()
            proveedor = entry_proveedor.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()

            if not (nombre and proveedor and precio and costo and stock):
                messagebox.showwarning("Guardar cambios", "Rellene todos los campos.")
                return
            
            try:
                precio = float(precio)
                costo = float(costo)
            except ValueError:
                messagebox.showwarning("Guardar cambios", "Ingrese valores numericos validos para precio y costo.")
                return
            
            #Actualizar cambios en la base de datos
            consulta = "UPDATE inventario SET nombre=?, proveedor=?, precio=?, costo=?, stock=? WHERE id=?"
            parametros = (nombre, proveedor, precio, costo, stock, item_id)
            self.eje_consulta(consulta, parametros)
            
            self.mostrar()
            
            ventana_editar.destroy()
            
        btn_guardar = Button(ventana_editar, text="Guardar cambios", font="sans 14 bold", command=guardar_cambios, bg="#A34343", fg="#FBF8DD")
        btn_guardar.place(x=80, y=335, width=240, height=40)

    def limpiar_campos(self):
        self.nombre.delete(0, END)
        self.proveedor.delete(0, END)
        self.precio.delete(0, END)
        self.costo.delete(0, END)
        self.stock.delete(0, END)