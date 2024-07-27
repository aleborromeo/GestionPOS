import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import datetime

class Ventas(tk.Frame):
    db_name = "basedatos.db"

    def __init__(self, parent):
        super().__init__(parent)
        self.numero_factura_actual = self.obtener_numero_factura_actual()
        self.widgets()
        self.mostrar_numero_factura()
        
    def rutas(self, ruta): #para que las rutas no se pierdan al pasarlo a exe
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def widgets(self): #clasificar los widgets

        #parte superior
        frame1 = tk.Frame(self, bg="#E9C874", highlightbackground="#E0A75E", highlightthickness=5)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="VENTAS", bg="#E9C874", fg="#A34343", font=("Britannic Bold", 42), anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
        

        #parte inferior
        frame2 = tk.Frame(self, bg="#FBF8DD", highlightbackground="#F8F6E3", highlightthickness=5)
        frame2.place(x=0, y=100, width=1100, height=550)

        lblframe = LabelFrame(frame2, text="Información de la venta", bg="#FBF8DD", font=("Arial Black", 14))
        lblframe.place(x=10, y=6, width=1060, height=80)

        label_numero_factura = tk.Label(lblframe, text="Número de \nfactura:", bg="#FBF8DD", font="sans 12 bold")
        label_numero_factura.place(x=10, y=1)
        

        #variable para el numero de factura automatico
        self.numero_factura = tk.StringVar()
        self.entry_numero_factura = ttk.Entry(lblframe, textvariable=self.numero_factura, state="readonly", font="sans 12 bold")
        self.entry_numero_factura.place(x=100, y=1, width=80)

        label_nombre = tk.Label(lblframe, text="Productos:", bg="#FBF8DD", font="sans 12 bold")
        label_nombre.place(x=200, y=5)
        self.entry_nombre = ttk.Combobox(lblframe, font="sans 12 bold", state="readonly") #para desplazar la lista de la base de datos, readonly = no poder escribir
        self.entry_nombre.place(x=290, y=5, width=180)
        

        #del combobox necesitamos que se ejecute
        self.cargar_productos()
        

        label_valor = tk.Label(lblframe, text="Precio: ", font="sans 12 bold", bg="#FBF8DD")
        label_valor.place(x=480, y=5)
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold", state="readonly")
        self.entry_valor.place(x=540, y=5, width=140)

        #para cargar el valor automaticamentee al seleccionar el producto
        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_precio_y_stock)

        label_cantidad = tk.Label(lblframe, text="Cantidad:", font="sans 12 bold", bg="#FBF8DD")
        label_cantidad.place(x=690, y=5)
        self.entry_cantidad = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x=770, y=5, width=110)
        
        label_stock= tk.Label(lblframe, text="Stock:", font="sans 12 bold", bg="#FBF8DD")
        label_stock.place(x=880, y=5)
        self.entry_stock = ttk.Entry(lblframe, font="sans 12 bold",  state="readonly")
        self.entry_stock.place(x=940, y=5, width=100)
        

        #tabla
        treFrame = tk.Frame(frame2, bg="#FBF8DD") #posicionado sobre el frame2
        treFrame.place(x=150, y=120, width=800, height=200)

        #barra de desplazamiento
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        

        #Creacion de tabla
        self.tree = ttk.Treeview(treFrame, columns=("Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)

        #encabezados
        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")

        #columnas
        self.tree.column("Producto", anchor="center")
        self.tree.column("Precio", anchor="center")
        self.tree.column("Cantidad", anchor="center")
        self.tree.column("Subtotal", anchor="center")

        self.tree.pack(expand=True, fill=BOTH)

        lblframe1 = LabelFrame(frame2, text="Opciones", font="sans 12 bold", bg="#F8F6E3")
        lblframe1.place(x=10, y=380, width=1060, height=100)
        
        #botones

        boton_agregar = tk.Button(lblframe1, text="Agregar artículo", font=("Berlin Sans FB", 16), fg="#FBF8DD", bg="#A34343", command=self.registrar)
        boton_agregar.place(x=50, y=10, width=200, height=50)

        boton_pagar = tk.Button(lblframe1, text="Pagar", font=("Berlin Sans FB", 16), fg="#FBF8DD", bg="#A34343", command=self.abrir_ventana_pago)
        boton_pagar.place(x=545, y=10, width=200, height=50)

        boton_factura = tk.Button(lblframe1, text="Ver Facturas", font=("Berlin Sans FB", 16), fg="#FBF8DD", bg="#A34343", command=self.abrir_ventana_factura)
        boton_factura.place(x=800, y=10, width=200, height=50)
        
        boton_eliminar = tk.Button(lblframe1, text="Eliminar artículo", font=("Berlin Sans FB", 16), fg="#FBF8DD", bg="#A34343", command=self.eliminar_producto)
        boton_eliminar.place(x=300, y=10, width=200, height=50)


        #suma automatica del los productos
        self.label_suma_total = tk.Label(frame2, text="Total a pagar: S/. 0 ", bg="#F8F6E3", font="sans 25 bold")
        self.label_suma_total.place(x=360, y=335)

    #funcion cargar productos
    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor() #cursor para cargar datos
            c.execute("SELECT nombre FROM inventario")
            productos = c.fetchall() #para obtener resultados
            self.entry_nombre["values"] = [producto[0] for producto in productos] #para seleccionar de una lista
            if not productos:
                print("No se encontraron productos en la base de datos.")
            conn.close()

        except sqlite3.Error as e:
            print("Error al cargar productos desde la base de datos.")

    def actualizar_precio_y_stock(self, event):
        nombre_producto = self.entry_nombre.get()
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            # Obtener el precio y el stock del producto seleccionado
            c.execute("SELECT precio, stock FROM inventario WHERE nombre = ?", (nombre_producto,))
            resultado = c.fetchone()
            if resultado:
                precio = resultado[0]
                stock = resultado[1]
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, f"{precio:.2f}")
                self.entry_valor.config(state="readonly")
                
                self.entry_stock.config(state="normal")
                self.entry_stock.delete(0, tk.END)
                self.entry_stock.insert(0, stock)
                self.entry_stock.config(state="readonly")
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "Precio no disponible")
                self.entry_valor.config(state="readonly")
                
                self.entry_stock.config(state="normal")
                self.entry_stock.delete(0, tk.END)
                self.entry_stock.insert(0, "Stock no disponible")
                self.entry_stock.config(state="readonly")
                
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el precio y stock: {e}")      
    
    def actualizar_total(self):
        total = 0.00
        for child in self.tree.get_children(): #son los datos que se ingresan a la tabla
            subtotal = float(self.tree.item(child, "values")[3]) #[3] = columna precio
            total += subtotal
        self.label_suma_total.config(text=f"Total a pagar: S/. {total:.2f}")

    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad: #verificar stock dentro de inventario
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto, cantidad):
                    messagebox.showerror("Error", "Stock insuficiente para el producto seleccionado")
                    return
                precio = float(precio)
                subtotal = cantidad * precio

                self.tree.insert("", "end", values=(producto, f"{precio:.2f}", cantidad, f"{subtotal:.2f}"))  #{precio:.2f} para dos decimales

                self.entry_nombre.set("")
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)

                self.actualizar_total()

            except ValueError:
                messagebox.showerror("Error", "Cantidad o precio no valido")

        else:
            messagebox.showerror("Error", "Debe completar todos los campos.")

    def verificar_stock(self, nombre_producto, cantidad):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM inventario WHERE nombre = ?", (nombre_producto,))
            stock = c.fetchone()

            if stock and stock[0] >= cantidad: #verificar si hay suficiente stock
                return True
            return False

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False
        
        finally:
            conn.close()

    def obtener_total(self):
        total = 0.0 
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        return total
    
    def abrir_ventana_pago(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", "No hay artículos para pagar")
            return
        
        ventana_pago = Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("500x400")
        ventana_pago.config(bg="#FBF8DD")
        ventana_pago.resizable(False, False)
        
        ventana_pago.grab_set()
        ventana_pago.focus_set()

        label_total = tk.Label(ventana_pago, bg="#FBF8DD", text=f"Total a pagar: S/. {self.obtener_total():.2f}",  font=("Arial Black", 22), anchor="center")
        label_total.place(x=50, y=30)
        
        ruta = self.rutas("img/pagar.png")
        self.pago_image = Image.open(ruta)
        self.pago_image = self.pago_image.resize((120, 120))
        self.pago_image = ImageTk.PhotoImage(self.pago_image)
        self.pago_label = tk.Label(ventana_pago, image=self.pago_image, bg="#FBF8DD")
        self.pago_label.place(x=180, y=135)

        label_cantidad_pagada = tk.Label(ventana_pago, bg="#FBF8DD", text="Cantidad pagada:", font="sans 14 bold", anchor="center")
        label_cantidad_pagada.place(x=160, y=90)
        entry_cantidad_pagada = ttk.Entry(ventana_pago, font="sans 12 bold")
        entry_cantidad_pagada.place(x=150, y=130)

        label_cambio = tk.Label(ventana_pago, bg="#FBF8DD", text="", font="sans 14 bold")
        label_cambio.place(x=100, y=190)

        def calcular_cambio():
            try:
                cantidad_pagada = float(entry_cantidad_pagada.get())
                total = self.obtener_total()
                cambio = cantidad_pagada - total
                if cambio < 0:
                    messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
                    return
                label_cambio.config(text=f"Vuelto: S/. {cambio:.2f}")
                label_cambio.place(x=165, y=180)
            
            except ValueError:
                messagebox.showerror("Error", "Cantidad pagada no válida")
            
        boton_calcular = tk.Button(ventana_pago, text="Calcular vuelto", bg="#A34343", fg="#FBF8DD", font=("Berlin Sans FB", 20), command=calcular_cambio)
        boton_calcular.place(x=120, y=260, width=240, height=50)

        boton_pagar = tk.Button(ventana_pago, text="Pagar", bg="#A34343", fg="#FBF8DD", font=("Berlin Sans FB", 20), command=lambda: self.pagar(ventana_pago, entry_cantidad_pagada, label_cambio))
        boton_pagar.place(x=120, y=320, width=240, height=50)
                

    def pagar(self, ventana_pago, entry_cantidad_pagada, label_cambio):
        
        try:
            cantidad_pagada = float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            
            if cambio < 0:
                messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
                return
            
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            try:
                productos = []
                for child in self.tree.get_children():
                    item = self.tree.item(child, "values")
                    producto = item[0]
                    precio = item[1]
                    cantidad_vendida = int(item[2])
                    subtotal = float(item[3])
                    productos.append([producto, precio, cantidad_vendida, subtotal])
                    
                    if not self.verificar_stock(producto, cantidad_vendida): #verificar
                        messagebox.showerror("Error", f"Stock insuficiente para el producto: {producto}")
                        return
                    
                    #para actualizar la tabla
                    c.execute("INSERT INTO ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal) VALUES (?, ?, ?, ?, ?)", (self.numero_factura_actual, producto, float(precio), cantidad_vendida, subtotal))

                    c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre = ?", (cantidad_vendida, producto))

                conn.commit()
                messagebox.showinfo("Éxito", "Venta registrada exitosamente")

                self.numero_factura_actual += 1
                self.mostrar_numero_factura()

                for child in self.tree.get_children():
                    self.tree.delete(child) #cuando se guarde la factura la tabla quedará en blanco para comenzar de nuevo
                self.label_suma_total.config(text="Total a pagar: S/. 0")

                ventana_pago.destroy()
                
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.generar_boleta_pdf(productos, total, self.numero_factura_actual - 1, fecha)

            except sqlite3.Error as e:
                conn.rollback() #para verificar que se guarde la factura
                messagebox.showerror("Error", "Error al registrar la venta")
            
            finally:
                conn.close()
        
        except ValueError:
            messagebox.showerror("Error", "Cantidad pagada no válida")
    
            
    def generar_boleta_pdf(self, productos, total, factura_numero, fecha):
        archivo_pdf = f"facturas/factura_{factura_numero}.pdf"
        
        c = canvas.Canvas(archivo_pdf, pagesize=letter)
        width, height = letter
        
        
        styles = getSampleStyleSheet()
        estilo_titulo = styles["Title"]
        estilo_normal = styles["Normal"]
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, f"Factura N°{factura_numero}")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, height - 70, f"Fecha: {fecha}")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, height - 100, "Información de la venta:")
        
        data = [["Producto", "Precio", "Cantidad", "Subtotal"]] + productos
        
        table = Table(data)
        table.wrapOn(c, width, height)
        table.drawOn(c, 100, height - 200)
        
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 250, f"Total a pagar: S/. {total:.2f}")
        
        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, height - 300, "Gracias por su compra, vuelva pronto.") 
        
        c.save()       
        
        messagebox.showinfo("Factura generada", f"La factura N°{factura_numero} ha sido creada exitosamente.")
        
        os.startfile(os.path.abspath(archivo_pdf))
        
        
    def obtener_numero_factura_actual(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT MAX(factura) FROM ventas")
            max_factura = c.fetchone()[0]

            if max_factura:
                return max_factura + 1
            else:
                return 1
            
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el número de factura: {e}")
            return 1
        finally:
            conn.close()
    
    def mostrar_numero_factura(self):
        self.numero_factura.set(self.numero_factura_actual)

    def abrir_ventana_factura(self):
        ventana_factura = Toplevel(self)
        ventana_factura.title("Factura")
        ventana_factura.geometry("800x500")
        ventana_factura.config(bg="#FBF8DD")
        ventana_factura.resizable(False, False)

        facturas = Label(ventana_factura, bg="#E9C874", text="Facturas registradas", fg="#A34343", font=("Britannic Bold", 30), anchor="center", highlightbackground="#E0A75E", highlightthickness=5)
        facturas.place(x=0, y=0, width=800, height=85)

        #tabla
        #almacenar tabla que crearemos
        treFrame = tk.Frame(ventana_factura, bg="#FBF8DD")
        treFrame.place(x=10, y=100, width=780, height=380)

        #barra de desplazamiento
        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        #Creacion de tabla
        tree_facturas = ttk.Treeview(treFrame, columns=("ID", "Factura", "Producto", "Precio", "Cantidad", "Subtotal"), show="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=tree_facturas.yview)
        scrol_x.config(command=tree_facturas.xview)

        #encabezados
        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#5", text="Cantidad")
        tree_facturas.heading("#6", text="Subtotal")

        #columnas
        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Producto", width=70, anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("Cantidad", width=130, anchor="center")
        tree_facturas.column("Subtotal", width=130, anchor="center")

        tree_facturas.pack(expand=True, fill=BOTH)

        self.cargar_facturas(tree_facturas)

    def cargar_facturas(self, tree):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            facturas = c.fetchall() #obtener datos de la consulta

            for factura in facturas:
                tree.insert("", "end", values=factura)
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar las facturas: {e}")
    
    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No hay ningún artículo seleccionado")
            return

        for item in selected_item:
            self.tree.delete(item)
        
        self.actualizar_total()