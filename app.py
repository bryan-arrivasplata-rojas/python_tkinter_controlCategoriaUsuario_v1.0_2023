from tkinter import ttk,Label,Tk
import tkinter as tk
import views.login as login
from PIL import ImageTk, Image

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
        color_background = "#800404"

        self.splash.config(bg=color_background)
        self.splash.overrideredirect(True)
        label = Label(self.splash, text="¡Bienvenido!", fg="white", bg=color_background, font=("Arial", 18))
        label.pack(pady=10)

        self.logo_image = Image.open("resources/images/logo_blanco.png")
        self.logo_image = self.logo_image.resize((150, 175), Image.ANTIALIAS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        self.logo_label = tk.Label(self.splash, image=self.logo_photo,bg=color_background)
        self.logo_label.pack(pady=10)

        self.progress_label = Label(self.splash,text="Loading...",font=("Trebuchet Hs",13,"bold"),fg="#FFFFFF", bg=color_background)
        self.progress_label.pack()

        #Barra aumento
        progress = ttk.Style()
        progress.theme_use('clam')
        progress.configure("Custom.Horizontal.TProgressbar",background=color_background)
        self.progres = ttk.Progressbar(self.splash,orient="horizontal",length=400,mode="determinate",style="Custom.Horizontal.TProgressbar")
        self.progres.pack()
        self.i = 0
        self.load()
        #self.splash.after(3000, self.frame)
    def frame(self):
        self.splash.destroy()
        login.LoginWindow()
    def run(self):
        self.splash.mainloop()
    
    def load(self):
        if self.i<=4:
            txt ='Loading... '+(str(25*self.i)+'%')
            self.progress_label.config(text=txt)
            self.progress_label.after(600,self.load)
            self.progres['value']=25*self.i
            self.i += 1
        else:
            self.frame()
            
if __name__ == "__main__":
    app = SplashScreen()
    app.run()