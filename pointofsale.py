import tkinter as tk


class PointofSale(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

        print("PointofSale Function ran")
        
        self.CreateWidgets()
        
    def CreateWidgets(self):
        self.Button1 = tk.Button(self, text="MainMenu", 
                        command=lambda: self.controller.ShowFrame("Back"))
        self.Button1.grid(row=5, column=5)
       