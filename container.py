from tkinter import *
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from graficos import Graficos
from PIL import Image, ImageTk
import os
import sys

class Container(tk.Frame):
    def __init__(self, padre, controlador): #Constructor
        super().__init__(padre)
        self.controlador = controlador
        self.pack() #empaquetar para que se muestre en la ventana tienda_virtual
        self.place(x=0, y=0, width=800, height=400)
        self.config(bg="#FBF8DD")
        self.widgets()
        
    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def show_frames(self, container): #ventanas
        top_level = tk.Toplevel(self) #ventanas independientes
        frame = container(top_level)
        frame.config(bg="#FBF8DD")
        frame.pack(fill="both", expand=True)
        top_level.geometry("1100x650+120+40")
        top_level.resizable(False, False)
        ruta = self.rutas("logo.ico")
        top_level.iconbitmap(ruta)

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)
        
    def graficos(self):
        self.show_frames(Graficos)

    def widgets(self):
        frame1 = tk.Frame(self, bg="#FBF8DD", height=400)
        frame1.pack()
        frame1.place(x=0, y=0, width=800, height=400)
        
        #definir imagenes para botones
        ruta = self.rutas("img/ventas.png")
        ventas_pil = Image.open(ruta)
        ventas_resize = ventas_pil.resize((40, 40))
        ventas_tk = ImageTk.PhotoImage(ventas_resize)
        
        ruta = self.rutas("img/inventario.png")
        inventario_pil = Image.open(ruta)
        inventario_resize = inventario_pil.resize((40, 40))
        inventario_tk = ImageTk.PhotoImage(inventario_resize)
        
        ruta = self.rutas("img/graficos.png")
        graficos_pil = Image.open(ruta)
        graficos_resize = graficos_pil.resize((40, 40))
        graficos_tk = ImageTk.PhotoImage(graficos_resize)

        btnventas = Button(frame1, bg="#E9C874", fg="#A34343", font=("Britannic Bold", 24), text="Ventas", command=self.ventas)
        btnventas.config(image=ventas_tk, compound=LEFT, padx=10) #padx es oara un espaciado horizontal, pady es para el vertical
        btnventas.image = ventas_tk
        btnventas.place(x=70, y=50, width=240, height=60)

        btninventario = Button(frame1, bg="#E9C874", fg="#A34343", font=("Britannic Bold", 24), text="Inventario", command=self.inventario)
        btninventario.config(image=inventario_tk, compound=LEFT, padx=10)
        btninventario.image = inventario_tk
        btninventario.place(x=70, y=250, width=240, height=60)
        
        btngraficos = Button(frame1, bg="#E9C874", fg="#A34343", font=("Britannic Bold", 24), text="Graficos", command=self.graficos)
        btngraficos.config(image=graficos_tk, compound=LEFT, padx=10)
        btngraficos.image = graficos_tk
        btngraficos.place(x=70, y=150, width=240, height=60)
        
        #imagenes
        #cambiar ruta al momento de exportar
        ruta = self.rutas("img/loguito.png")
        self.logo_image = Image.open(ruta)
        self.logo_image = self.logo_image.resize((390, 390))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame1, image=self.logo_image, bg="#FBF8DD")
        self.logo_label.place(x=400, y=10)

        copyright_label = tk.Label(frame1, text="© 2024 ESTRUCTURA DE DATOS Y ALGORITMOS", bg="#FBF8DD", font=("arial", 8), fg="#8B322C")
        copyright_label.place(x=10, y=375)

    def show_frames(self, container): #bloqueo de ventana padre
        top_level = tk.Toplevel(self)
        frame = container(top_level)
        frame.config(bg="#F7F9F2")
        frame.pack(fill="both", expand=True)
        top_level.geometry("1100x650+120+20")
        top_level.resizable(False, False)

        top_level.transient(self.master)
        top_level.grab_set()
        top_level.focus_set()
        top_level.lift()


