import tkinter as tk


class PointofSale(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        print("PointofSale Function ran")
        self.CreateWidgets()
        
    def CreateWidgets(self):
        self.Benj = tk.Label(self.master, text="Benj")
        self.Benj.pack() 

