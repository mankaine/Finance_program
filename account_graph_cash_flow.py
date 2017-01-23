# account_graph_cash_flow.py 
# Contains a class to view a graph of Cash Flow over a period of time.

from account import Account 
from basecui import months_abv, kind_to_str 
import tkinter as tk
from graph import Graph

standard_font = ("Helvetica", -10)

class AccountGraphCashFlow(Graph):
    def __init__(self, a: Account, tf: [(int, int)], master=None):
        Graph.__init__(self, a, tf, master)
            
        min_year, min_month = self._tf[0][0]+1,  months_abv(self._tf[0][1])
        max_year, max_month = self._tf[-1][0]+1, months_abv(self._tf[-1][1])
        self._t.title(
            "Cash Flow of Account "+ a.get_name()+" ({}) from {} {} to {} {}".format(
                kind_to_str[a.get_kind()],min_month, min_year, max_month, max_year))
            
        self._canvas = tk.Canvas(master=self._t, height=1200, width=800)
        self._canvas.grid(row=0,column=0,sticky = tk.N + tk.S + tk.W + tk.E)
        self._canvas.bind('<Configure>', self._resize)
            
        self._t.rowconfigure(0, weight = 1)
        self._t.columnconfigure(0, weight = 1)


    def _resize(self, event): 
        """Executes when canvas is resized. Deletes the current drawing of 
        the canvas and redraws the axes, labels, points, and lines that 
        constitute the graph.
        """
        h,w = Graph.reset(self)
                
        w_spacing = w/len(self._tf)
        Graph.draw_axes(self, h, w)
        self._draw_connections(h, w_spacing) 
        self._draw_points(h, w_spacing)
        print("Graph Displayed")                                                # Confirmation

    
    def _draw_connections(self, h, w_dist):
        """Draws the lines between points on a graph
        """
        largest = max(abs(self._a.get_remain(y,m)) for (y,m) in self._tf)
        for i in range(len(self._tf) - 1): 
            y0, m0 = self._tf[i][0], self._tf[i][1]
            perc0r = (1 - ((self._a.get_remain(y0,m0)/largest) if largest != 0 else 1)) / 2
            y_point0r = (h-40)*(perc0r) if perc0r != 0 else (h/2)-20

            y1, m1 = self._tf[i+1][0], self._tf[i+1][1]            
            perc1r = (1 - ((self._a.get_remain(y1,m1)/largest) if largest != 0 else 1)) / 2
            y_point1r = (h-40)*(perc1r) if perc1r != 0 else (h/2)-20
            
            self._canvas.create_line(
                w_dist * self._tf.index((y0,m0)) + 25, y_point0r, 
                w_dist * self._tf.index((y1,m1)) + 25, y_point1r,
                fill="#4B8A08" if (y_point0r-y_point1r >= 0) else "#f00")

    
    def _draw_points(self, h, w_dist):
        """Draws points indicating net cash flows on the canvas 
        """
        largest = max(abs(self._a.get_remain(y,m)) for (y,m) in self._tf)
        for y,m in self._tf: 
            perc_r = (1 - ((self._a.get_remain(y,m)/largest) if largest != 0 else 1)) / 2
            y_point_r = (h-40)*(perc_r) if perc_r != 0 else (h/2)-20
                                    
            radius = 2
            
            self._canvas.create_text(
                w_dist * self._tf.index((y,m)) + 25, h - 15, 
                text=months_abv(m)+"\n"+str(y), font=standard_font)             # Labels on the x-axis

            self._canvas.create_oval(
                w_dist * self._tf.index((y,m)) + 25 - radius, y_point_r-radius, 
                w_dist * self._tf.index((y,m)) + 25 + radius, y_point_r+radius,
                fill="#4B8A08" if self._a.get_remain(y,m) >= 0 else "#f00",
                outline="#4B8A08" if self._a.get_remain(y,m) >= 0 else "#f00")    # Points of reached
            
            self._canvas.create_text(
                w_dist * self._tf.index((y,m)) + 25 - radius, y_point_r+10,
                text="{:.2f}".format(self._a.get_remain(y,m)/100, 2),
                font=standard_font, 
                fill="#4B8A08" if self._a.get_remain(y,m) >= 0 else "#f00")   # Values of reached

            
    def view(self):
        Graph.view(self)


# Testing
if __name__ == "__main__": 
    from transaction import Transaction
    from account import Budget 
    t0  = Transaction(2015, 0, 12, "Fast Food", "Cash", "In-n-Out", 100)
    t1  = Transaction(2015, 1, 24, "Fast Food", "Cash", 'McDonald\'s', 200)
    t2  = Transaction(2015, 2, 24, "Fast Food", "Debit", "McDonald's", 300)
    t3  = Transaction(2015, 3, 24, "Fast Food", "Cash", "Wendy's", 400)
    t4  = Transaction(2015, 4, 23, "Fast Food", "Gifts", "Wendy's", 600)
    t5  = Transaction(2015, 5, 22, "Fast Food", "Savings", "Coffee", 100)
    t6  = Transaction(2015, 6, 12, "Fast Food", "Cash", "In-n-Out", 700)
    t7  = Transaction(2015, 7, 24, "Fast Food", "Cash", 'McDonald\'s', 400)
    t8  = Transaction(2015, 8, 24, "Fast Food", "Debit", "McDonald's", 900)
    t9  = Transaction(2015, 9, 24, "Fast Food", "Cash", "Wendy's", 1000)
    t10 = Transaction(2015, 10, 23, "Fast Food", "Gifts", "Wendy's", 1100)
    t11 = Transaction(2015, 11, 22, "Fast Food", "Savings", "Coffee", 1200)
    t12 = Transaction(2016, 11, 22, "Fast Food", "Savings", "Coffee", 1300)
    t13 = Transaction(2016, 10, 22, "Fast Food", "Savings", "Coffee", 1300)
    t14 = Transaction(2016, 10, 22, "Drinks", "Savings", "Coffee", 1200)

    a2 = Account(
        "Fast Food", 0, 
        [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13], 
        {2015: {3: Budget(goal=100, reached=200, ts_amt=1)}})

    ag = AccountGraphCashFlow(
        a2, 
        [(2016, 10), (2016, 11), (2015, 0), (2015, 1), (2015, 2), 
         (2015, 3), (2015, 4), (2015, 5), (2015, 6), (2015, 7),
         (2015, 8), (2015, 9), (2015, 10), (2015, 11)])
    ag.view()