import tkinter as tk
from pointofsale import PointofSale
from meta import WindowManagement 

## Main menu class, navigate between elements of the program
class MainMenu(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = WindowManagement.Clear(self, self.master)
        self.pack()
        self.CreateWidgets()

    def CreateWidgets(self):
        self.PointofSale = tk.Button(self)
        self.PointofSale["text"] = "Point of Sale"
        self.PointofSale["command"] = self.ShowPointofSale
        self.PointofSale.pack(side="left")

    def ShowPointofSale(self):
        self.master = WindowManagement.Clear(self, self.master)
        app = PointofSale()
        

if __name__ == "__main__":
    master = tk.Tk()
    app = MainMenu(master=master)
    app.mainloop()
