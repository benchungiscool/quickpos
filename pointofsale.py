import tkinter as tk
from meta import WindowManagement 


class PointofSale(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.CreateWidgets()

    def CreateWidgets(self):
        self.Text = tk.Text(self.master)
        self.Text.pack()
        self.Text.insert(tk.END, "Benj")
        
        
