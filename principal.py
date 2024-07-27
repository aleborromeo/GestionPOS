import os
import sys
from tkinter import *
from tkinter import Tk, Frame
from container import Container
from ttkthemes import ThemedStyle
from PIL import Image, ImageTk

class Manager(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Sistema de punto de ventas")
        self.resizable(False, False)
        self.config(bg="#FBF8DD")
        self.geometry("800x400+120+40")
        
        ruta = self.rutas("logo.ico")
        self.iconbitmap(ruta)
        
        self.container = Frame(self, bg="#FBF8DD")
        self.container.pack(fill="both", expand=True)

        self.frames = {
            Container: None
        } #diccionario para guardar Frames
        self.load_frames()

        self.show_frame(Container)

        self.set_theme()
        
    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)

    def load_frames(self):
        for FrameClass in self.frames.keys():
            frame = FrameClass(self.container, self)
            self.frames[FrameClass] = frame

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def set_theme(self): #funcion para el tema
        style = ThemedStyle(self)
        style.set_theme("clearlooks")
        


def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()
