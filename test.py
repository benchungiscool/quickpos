import tkinter as tk
from tkinter import font as tkfont
from pointofsale import PointofSale

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {"MainMenu", "PointofSale"}
        for F in (MainMenu, PointofSale):
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenu(tk.Frame):
    def __init__(self, master=None, controller=None):
        super().__init__(master)
        self.controller = controller
        self.master = master
        self.CreateWidgets()

    def CreateWidgets(self):
        self.Button1 = tk.Button(self, text="Point of Sale", 
                        command=lambda: self.controller.show_frame("PointofSale"))
        self.Button1.pack(side="left")


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
