# account_graph_rate.py 
# Contains a class to view rate of a selected Account's rate of spending/saving. 

import  tkinter  as tk  
from    account  import Account 
from    basecui  import months, months_abv, kind_to_str
from graph import Graph

standard_font = ("Helvetica", -10)

class AccountGraphRate(Graph): 
    def __init__(self, a: Account, tf: [(int, int)], master=None):
        Graph.__init__(self, a, tf, master)

        print(self._tf)
        min_year, min_month = self._tf[0][0]+1,  months(self._tf[0][1])
        max_year, max_month = self._tf[-1][0]+1, months(self._tf[-1][1])
        self._t.title(
            "Reached of Account "+ a.get_name()+" ({}) from {} {} to {} {}".format(
                kind_to_str[a.get_kind()],min_month, min_year, max_month, max_year))

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
        h,w = Graph.reset(self)
        w_spacing = w/len(self._tf)
        Graph.draw_axes(self, h, w, 1)
        self._draw_connections(h, w_spacing)
        self._draw_points(h, w_spacing)
        print("Graph Displayed")                                                # Confirmation

    
    
    def _draw_points(self, h, w_dist):
        """Draws to canvas points and their labels
        """
        largest = max(self._a.get_reached(y,m) for (y,m) in self._tf)
        for y,m in self._tf: 
            perc = 1 - (self._a.get_reached(y,m)/largest)
            y_point = 10+(perc*(h-10-20))
            radius = 2
            
            self._canvas.create_text(
                w_dist * self._tf.index((y,m)) + 25, h - 15, 
                text=months_abv(m)+"\n"+str(y), font=standard_font)             # Labels on the x-axis

            self._canvas.create_oval(
                w_dist * self._tf.index((y,m)) + 25 - radius, y_point-radius, 
                w_dist * self._tf.index((y,m)) + 25 + radius, y_point+radius,
                fill="#00f", outline="#00f")                                    # Points
            
            self._canvas.create_text(
                w_dist * self._tf.index((y,m)) + 25 - radius, y_point+10,
                text="{:.2f}".format(self._a.get_reached(y,m)/100, 2),
                font=standard_font)                                             # Values
            
            
    def _draw_connections(self, h, w_dist):
        """Draws onto canvas lines connecting from point to point
        """
        largest = max(self._a.get_reached(y,m) for (y,m) in self._tf)
        for i in range(len(self._tf) - 1): 
            y0, m0 = self._tf[i][0], self._tf[i][1]
            y1, m1 = self._tf[i+1][0], self._tf[i+1][1]
            
            perc0 = 1 - (self._a.get_reached(y0,m0)/largest)
            perc1 = 1 - (self._a.get_reached(y1,m1)/largest)
            
            y_point0 = 10+(perc0*(h-10-20))
            y_point1 = 10+(perc1*(h-10-20))

            self._canvas.create_line(
                w_dist * self._tf.index((y0,m0)) + 25, y_point0, 
                w_dist * self._tf.index((y1,m1)) + 25, y_point1,
                fill="#00f")
            
    def view(self):
        Graph.view(self)
            

# Testing 
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

    a2 = Account("Fast Food", 0, [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13], {})

    ag = AccountGraphRate(
        a2, 
        [(2016, 10), (2016, 11), (2015, 0), (2015, 1), (2015, 2), 
         (2015, 3), (2015, 4), (2015, 5), (2015, 6), (2015, 7),
        (2015, 8), (2015, 9), (2015, 10), (2015, 11)])
    ag.view()