from tkinter import *
import tkinter
import views.login as login

class SplashScreen:
    def __init__(self):
        # create a tkinter window
        self.splash = Tk()
        self.splash.title("SplashScreen")
        ancho_ventana = 400
        alto_ventana = 300
        ancho_pantalla = self.splash.winfo_screenwidth()
        alto_pantalla = self.splash.winfo_screenheight()
        posicion_x = int((ancho_pantalla / 2) - (ancho_ventana / 2))
        posicion_y = int((alto_pantalla / 2) - (alto_ventana / 2))
        self.splash.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")
        etiqueta = tkinter.Label(self.splash,text="Bienvenido ...")
        etiqueta.pack(fill=tkinter.BOTH,expand=True)
        self.splash.after(3000, self.frame)
    def frame(self):
        self.splash.destroy()
        login.LoginWindow()
    def run(self):
        self.splash.mainloop()
if __name__ == "__main__":
    app = SplashScreen()
    app.run()