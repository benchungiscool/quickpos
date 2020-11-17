import tkinter as tk


class PointofSale(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller      
        self.CreateWidgets()
        
    def CreateWidgets(self):
        self.Button1 = tk.Button(self, text="Back", 
                        command=lambda: self.controller.ShowFrame("MainMenu"))
        self.Button1.grid(row=5, column=5)
       
