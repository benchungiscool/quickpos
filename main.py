import tkinter as tk
from pointofsale import PointofSale
from meta import WindowManagement 


## Master class
class App(tk.Frame):
    def __init__(self, master=None):

        super().__init__(master)

        self.master = master
        self.pack()

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (MainMenu, PointofSale):

            page_name = F.__name__
            frame = F(self.master, self)
            self.frames[page_name] = frame

            #frame.grid(row=0, column=0, sticky="nsew")

        self.ShowFrame("MainMenu")
    
    def ShowFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

## Main menu class, navigate between elements of the program
class MainMenu(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.pack()
        self.CreateWidgets()

    def CreateWidgets(self):
        self.PointofSale = tk.Button(self)
        self.PointofSale["text"] = "Point of Sale"
        self.PointofSale["command"] = lambda:controller.ShowFrame(self,"PointOfSale")
        self.PointofSale.pack(side="left")
        

if __name__ == "__main__":
    master = tk.Tk()
    app = App(master=master)
    app.mainloop()
