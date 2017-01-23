# accountgraphcompare.py 
# A class to compare a chosen Account's rate of spending to saving.

from account import Account, Budget
from basecui import months_abv, kind_to_str
import tkinter as tk 

standard_font = ("Helvetica", -10)

class AccountGraphCompare:
    def __init__(self, a: Account, it: [(int, int)], master=None):
        self._a     = a
        self._it    = sorted(it, key=lambda x: (x[0], x[1])) 
    
        self._t     = tk.Tk()
            
        min_year, min_month = self._it[0][0]+1,  months_abv(self._it[0][1])
        max_year, max_month = self._it[-1][0]+1, months_abv(self._it[-1][1])
        self._t.title(
            "Goals vs. Reached of Account "+ a["name"]+" ({}) from {} {} to {} {}".format(
                kind_to_str[a["kind"]],min_month, min_year, max_month, max_year))
            
        self._canvas = tk.Canvas(master=self._t, height=1200, width=800)
        self._canvas.grid(row=0,column=0,sticky = tk.N + tk.S + tk.W + tk.E)
        self._canvas.bind('<Configure>', self._resize)
            
        self._t.rowconfigure(0, weight = 1)
        self._t.columnconfigure(0, weight = 1)
        
        
    def _resize(self, event):
        """Method that is called when canvas is resized. Deletes the current 
        drawing of the canvas and redraws it to fit the current size of the 
        canvas
        """
        self._canvas.delete(tk.ALL)
        h = self._canvas.winfo_height()
        w = self._canvas.winfo_width()
        w_spacing = w/len(self._it)
        self._draw_axes(h, w)
        self._draw_connections(h, w_spacing) 
        self._draw_points(h, w_spacing)
        print("Graph Displayed")                                                # Confirmation
        
        
    def _draw_axes(self, h, w):
        """Draws the axes of a graph 
        """
        self._canvas.create_line(0, h-30, w, h-30)                              # x axis
        self._canvas.create_line(20, 0, 20, h)                                  # y-axis

    
    def _draw_connections(self, h, w_dist):
        """Draws the lines between points on a graph. The lines are from 
        goal point to goal point and reached point to reached point.
        """
        largest = max(
            max(self._a[("reached", y, m)] for (y,m) in self._it),
            max(self._a[("goal", y, m)] for (y,m) in self._it))
        for i in range(len(self._it) - 1): 
            y0, m0 = self._it[i][0], self._it[i][1]
            y1, m1 = self._it[i+1][0], self._it[i+1][1]
            
            perc0r = 1 - (self._a[("reached", y0, m0)]/largest)                 # Reached
            perc1r = 1 - (self._a[("reached", y1, m1)]/largest)
                        
            y_point0r = 10+(perc0r*(h-10-20))
            y_point1r = 10+(perc1r*(h-10-20))
            
            self._canvas.create_line(
                w_dist * self._it.index((y0,m0)) + 25, y_point0r, 
                w_dist * self._it.index((y1,m1)) + 25, y_point1r,
                fill="#f00")

            perc0g = 1 - (self._a[("goal", y0, m0)]/largest)                    # Goal
            perc1g = 1 - (self._a[("goal", y1, m1)]/largest)

            y_point0g = 10+(perc0g*(h-10-20))
            y_point1g = 10+(perc1g*(h-10-20))
            
            self._canvas.create_line(
                w_dist * self._it.index((y0,m0)) + 25, y_point0g, 
                w_dist * self._it.index((y1,m1)) + 25, y_point1g,
                fill="#00f")
    
    
    def _draw_points(self, h, w_dist):
        """Draws on a graph the goal and reached attributes of an Account's 
        budgets 
        """
        largest = max(
            max(self._a[("reached", y, m)] for (y,m) in self._it),
            max(self._a[("goal", y, m)] for (y,m) in self._it))
        for y,m in self._it: 
            perc_r = 1 - (self._a[("reached", y, m)]/largest)
            y_point_r = 10+(perc_r*(h-10-20))
            
            perc_g = 1 - (self._a[("goal", y, m)]/largest)
            y_point_g = 10+(perc_g*(h-10-20))
            radius = 2
            
            self._canvas.create_text(
                w_dist * self._it.index((y,m)) + 25, h - 15, 
                text=months_abv(m)+"\n"+str(y), font=standard_font)             # Labels on the x-axis

            self._canvas.create_oval(
                w_dist * self._it.index((y,m)) + 25 - radius, y_point_r-radius, 
                w_dist * self._it.index((y,m)) + 25 + radius, y_point_r+radius,
                fill="#f00", outline="#f00")                                    # Points of reached
            
            self._canvas.create_text(
                w_dist * self._it.index((y,m)) + 25 - radius, y_point_r+10,
                text="{:.2f}".format(self._a[("reached", y, m)]/100, 2),
                font=standard_font, fill="#f00")                                # Values of reached

            self._canvas.create_oval(
                w_dist * self._it.index((y,m)) + 25 - radius, y_point_g-radius, 
                w_dist * self._it.index((y,m)) + 25 + radius, y_point_g+radius,
                fill="#00f", outline="#00f")                                    # Points of goal
            
            self._canvas.create_text(
                w_dist * self._it.index((y,m)) + 25 - radius, y_point_g+10,
                text="{:.2f}".format(self._a[("goal", y, m)]/100, 2),
                font=standard_font, fill="#00f")                                # Values of goal
            
            
    def view(self):
        self._t.mainloop()


if __name__ == "__main__": 
    from transaction import Transaction
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

    ag = AccountGraphCompare(
        a2, 
        [(2016, 10), (2016, 11), (2015, 0), (2015, 1), (2015, 2), 
         (2015, 3), (2015, 4), (2015, 5), (2015, 6), (2015, 7),
         (2015, 8), (2015, 9), (2015, 10), (2015, 11)])
    ag.view()