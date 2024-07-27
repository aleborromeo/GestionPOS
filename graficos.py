import sqlite3
import tkinter as tk
from tkinter import *
import sys
import os
import pandas as pd
from matplotlib.figure import Figure
import matplotlib.animation as anim
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import datetime
from PIL import Image, ImageTk

class Graficos(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.grafica_1 = False
        self.grafica_2 = False
        
        self.widgets()
        
    def rutas(self, ruta): 
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)
    
    def animate(self, i): 
        
        if self.grafica_1:
            self.ax.clear()
            
            try:
                self.ax.bar(self.grafx, self.grafy, color="#E90074", label="Ventas")
                self.ax.grid(True)
                self.ax.legend()
                self.figura.autofmt_xdate(rotation=30)
                self.cvs.draw()  # Update the canvas
            except Exception as e:
                print(f"Error en animate (grafica_1): {e}")
        
        elif self.grafica_2:
            self.ax.clear()
            
            try:
                self.ax.bar(self.grafx, self.grafy_2, color="yellow", label="Venta Total")
                self.ax.bar(self.grafx, self.grafy_1, color="orange", label="Costo Total")
                self.ax.grid(True)
                rects = self.ax.patches
                labels = self.grafy_2 + self.grafy_1
                
                for rect, label in zip(rects, labels):
                    height = rect.get_height()
                    self.ax.text(rect.get_x() + rect.get_width()/2, height, f'{label}', ha="center", va="bottom")
                
                self.ax.legend()
                self.figura.autofmt_xdate(rotation=30)
                self.cvs.draw()  # Update the canvas
            except Exception as e:
                print(f"Error en animate (grafica_2): {e}")
            
        self.ani.event_source.stop()
        
    def representar_1(self):
        with sqlite3.connect("basedatos.db") as conn:
            df = pd.read_sql("SELECT * FROM VENTAS", conn)
        
        try:
            self.grafica_1 = True
            self.grafica_2 = False
            
            datos_1 = df[["nombre_articulo", "cantidad"]]
            self.data_1 = datos_1.groupby(["nombre_articulo"]).sum()
            self.grafx = list(self.data_1.index)
            self.grafy = list(self.data_1["cantidad"])
        except Exception as e:
            print(f"Error en representar_1: {e}")
        
        self.ani.event_source.start()
    
    def representar_2(self):
        with sqlite3.connect("basedatos.db") as conn:
            df = pd.read_sql("SELECT * FROM VENTAS", conn)
        
        try:
            self.grafica_2 = True
            self.grafica_1 = False
            
            datos_2 = df[["nombre_articulo", "cantidad", "valor_articulo", "subtotal"]]
            costo_T = datos_2["cantidad"] * datos_2["valor_articulo"]
            venta_T = datos_2["subtotal"]
            
            self.datos_2 = datos_2.assign(CostoT=costo_T, VentaT=venta_T)
            self.data_2 = self.datos_2
            self.grafx = list(self.data_2["nombre_articulo"])
            self.grafy_1 = list(self.data_2["CostoT"])
            self.grafy_2 = list(self.data_2["VentaT"])
        
        except Exception as e:
            print(f"Error en representar_2: {e}")
        
        self.ani.event_source.start()
    
    def widgets(self): 
        frame1 = tk.Frame(self, bg="#E9C874", highlightbackground="#E0A75E", highlightthickness=5)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)

        titulo = tk.Label(self, text="GRÁFICOS", bg="#E9C874", fg="#A34343", font=("Britannic Bold", 42), anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)
        

        frame2 = tk.Frame(self, bg="#FBF8DD", highlightbackground="#F8F6E3", highlightthickness=5)
        frame2.place(x=0, y=100, width=1100, height=550)
        
        self.figura = Figure()
        self.ax = self.figura.add_subplot(111)
        self.cvs = FigureCanvasTkAgg(self.figura, frame2) 
        self.cvs.draw()
        self.cvs.get_tk_widget().pack()
        
        tlb = NavigationToolbar2Tk(self.cvs, frame2)
        tlb.update()
        
        self.ani = anim.FuncAnimation(self.figura, self.animate, interval=100, save_count=50)
        
        ruta = self.rutas("img/graficosf.png")
        self.logo_image = Image.open(ruta)
        self.logo_image = self.logo_image.resize((200, 200))
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(frame2, image=self.logo_image, bg="#FBF8DD")
        self.logo_label.place(x=880, y=100)
        
        boton_productos_vendidos = tk.Button(frame2, text="Productos\nvendidos", bg="#E9C874", fg="#A34343", font=("Britannic Bold", 24), command=self.representar_1)
        boton_productos_vendidos.place(x=10, y=70, width=200, height=78)
        
        boton_costos = tk.Button(frame2, text="Costos/\nVenta", bg="#E9C874", fg="#A34343", font=("Britannic Bold", 24), command=self.representar_2)
        boton_costos.place(x=10, y=180, width=200, height=78)
        
        try:
            self.representar_1()
        except Exception as e:
            print(f"Error en widgets: {e}")

