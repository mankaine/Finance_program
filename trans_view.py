# trans_view.py 
# Module to view attributes of Transactions, stylized.

import basecui as bc 

menu = """ 
VIEW MENU
=================================================================
    [yrr]    : View transactions made within a year
    [mth]    : View transactions made within a month
    [ymo]    : View transactions made within a year and month
    [cst]    : View transactions made within a custom time frame 
    [esc]    : Return to previous menu
"""

def main(ts: ["Transaction"]) -> None:
    """Requests user prompt to display information about Transactions
    """
    ts.sort(key=lambda x: (x.get_year(), x.get_month(), x.get_day()))
    viewing = True 
    while viewing: 
        print(menu)
        try: 
            choice = input("Your choice: ").rstrip()
            if choice == "yrr": 
                _by_year(ts) 
            elif choice == "mth": 
                _by_month(ts) 
            elif choice == "ymo": 
                _by_pair(ts) 
            elif choice == "cst":
                _by_custom(ts) 
            elif choice == "esc": 
                break 
            else: 
                print("Choice {} not an option. Try again.".format(choice))
        except Exception as e: 
            print("    An error occurred: " + str(e))
            break
        viewing = bc.binary_question("View more transactions? ([y]es or [n]o): ", "y", "n")


def _by_year(ts) -> None:
    """Prints transactions in a year based on user input 
    """
    print()
    y = bc.trans_timeframe(sorted(set(t.get_year() for t in ts)) + [-1])
    if y == -1:  
        return
    print("\n"+header()) 
    for t in (i for i in ts if i.get_year() == y): 
        print(view(t))
        

def _by_month(ts) -> None:
    """Prints transactions in a month based on user input 
    """
    s = (bc.months_abv(m) for m in sorted(set(t.get_month() for t in ts)))
    print()
    m = bc.trans_timeframe(list(s) + [-1])
    if m == -1: 
        return 
    print("\n"+header())
    for t in (i for i in ts if i.get_month() == bc.months_to_int[m]): 
        print(view(t)) 


def _by_pair(ts) -> None:
    """Prints transactions in a month and year based on user input
    """
    print()
    y = bc.trans_timeframe(sorted(set(t.get_year() for t in ts)) + [-1])
    if y == -1: 
        return 
    
    s = (bc.months_abv(m) for m in sorted(set(t.get_month() for t in ts)))
    print()
    m = bc.trans_timeframe(list(s) + [-1])
    if m == -1: 
        return 
    
    print("\n"+header())
    for t in (i for i in ts if i.get_month() == bc.months_to_int[m] and \
               i.get_year() == y): 
        print(view(t))


def _by_custom(ts) -> None:
    """Prints transactions in a series of months and years based on user input
    """
    def cond(y0,y1,m0,m1,t): return m0 <= t.get_month() <= m1 and y0 <= t.get_year() <= y1
    print()
    y0 = bc.trans_timeframe(sorted(set(t.get_year() for t in ts)) + [-1])
    if 0 == y0: 
        return
    s = (bc.months_abv(m) for m in sorted(set(t.get_month() for t in ts)))
    print()
    m0 = bc.trans_timeframe(list(s) + [-1])
    if 0 == m0: 
        return
    
    print()
    y1 = bc.trans_timeframe(sorted(set(t.get_year() for t in ts)) + [-1])
    if 0 == y1: 
        return
    s = (bc.months_abv(m) for m in sorted(set(t.get_month() for t in ts)))
    print()
    m1 = bc.trans_timeframe(list(s) + [-1])
    if 0 == m1: 
        return 
    
    print("\n"+header())
    for t in (i for i in ts if cond(
        y0,y1,bc.months_to_int[m0],bc.months_to_int[m1],i)): 
        print(view(t))    
    

def header(show_num=False) -> str:
    """Returns header string
    """ 
    f_header_str = "    {:4} {:2} {:2} {:<30} {:<30} {:<10} {:<10}".format(
        "Year", "Mo", "Dy", "Description", "Account", "Dr", "Cr")
    t_header_str ="{:3} {:4} {:2} {:2} {:<30} {:<30} {:<10} {:<10}".format(
        "Num", "Year", "Mo", "Dy", "Description", "Account", "Dr", "Cr")  
    return (t_header_str if show_num else f_header_str) + \
        "\n" + ("*"*len(t_header_str))   # Length irrelevant 


def view(t, num="") -> str:
    """Returns string representing a Transaction
    """
    return "{:>3}{} {:>4} {:>2} {:>2} {:<30} {:<30} {:>8.2f}\n{}{:<30} {:>8.2f}".format(
        num, "" if num == "" else ".", t.get_year()+1, t.get_month()+1, 
        t.get_day()+1,t.get_description(), t.get_dr_account(), 
        round(t.get_amount()/100, 2),  
        " "*55, t.get_cr_account(), round(t.get_amount()/100, 2))
      

# Testing
if __name__ == "__main__":
    # Construction
    from transaction import Transaction

    t1 = Transaction(2015, 11, 24, "Fast Food", "Cash", 'McDonald\'s', 300)
    t2 = Transaction(2015, 11, 24, "Fast Food", "Debit", "McDonald's", 200)
    t3 = Transaction(2015, 10, 24, "Fast Food", "Cash", "Wendy's", 500)
    t4 = Transaction(2015, 10, 23, "Fast Food", "Gifts", "Wendy's", 400)
    t5 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)

    print(header())    
    print(view(t1))
    print(view(t2))
    print(view(t3))
    print(view(t4))
    print(view(t5))
    
    main([t1,t2,t3,t4,t5])
