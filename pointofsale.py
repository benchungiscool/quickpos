import tkinter as tk


class PointofSale(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.pack()
        self.CreateWidgets()

    def CreateWidgets(self):
        self.Text = tk.Label(self.master, text="Benj")
        self.Text.pack() 
