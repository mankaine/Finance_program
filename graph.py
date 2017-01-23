# Base class for AccountGraphCashFlow, AccountGraphRate, and 
# AccountGraphCompare.

from account import Account 
import tkinter as tk

class Graph:
    def __init__(self, a: Account, tf: [(int, int)], master=None):
        self._a     = a
        self._tf    = sorted(tf, key=lambda x: (x[0], x[1])) 

        self._t     = tk.Tk()
                
        self._canvas = tk.Canvas(master=self._t, height=1200, width=800)
        self._canvas.grid(row=0,column=0,sticky = tk.N + tk.S + tk.W + tk.E)
        self._canvas.bind('<Configure>', self._resize)
        
        self._t.rowconfigure(0, weight = 1)
        self._t.columnconfigure(0, weight = 1)    

    
    def reset(self) -> (int, int):
        """Returns current width and height of canvas, and deletes 
        all drawn material on canvas
        """
        self._canvas.delete(tk.ALL)
        h = self._canvas.winfo_height()
        w = self._canvas.winfo_width()
        return h,w 


    def draw_axes(self, h, w, order=0):
        """Draws to canvas axes 
        """
        if order == 0: 
            pass 
        elif order == 1: 
            self._canvas.create_line(0, h-30, w, h-30)  # x axis
            self._canvas.create_line(20, 0, 20, h)  # y-axis
        elif order == 2: 
            self._canvas.create_line(0, (h-40)/2, w, (h-40)/2) # x axis
            self._canvas.create_line(20, 0, 20, h) # y-axis


    def view(self):
        """Executes mainloop
        """
        self._t.mainloop()
    
