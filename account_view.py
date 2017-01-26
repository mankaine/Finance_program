# account_view.py  
# Display accounts' attributes

from account import Account
from trans_view import view, header
import basecui as bc 

max_char = 100

menu = """
ACCOUNT VIEW MENU
===============================================================
    [ats]    : View all Transactions of an Account
    [cts]    : View an Account's transactions over a custom time period 
    [omy]    : View one Account for a month and year
    [oaa]    : View one Account for all months and years
    [ocst]   : View one Account over a custom timeframe
    [acst]   : View all Accounts over a custom timeframe
    [aaa]    : View all Accounts over all months and years
    [esc]    : Return to Account Menu
"""

def _um(a: Account, y: int) -> [int]:
    """Returns integers representing unique months of an Account and breakout integer
    """
    if y in a.get_budgets(): 
        return sorted(
        set(bc.months_abv(m) for m in a.get_budgets(y)), 
        key=lambda x: bc.months_to_int[x]) + [-1]
    return [-1]
    
        
def _uy(ats: [Account]) -> [int]:
    """Returns integers representing unique years and breakout integer
    """
    return sorted(set(y for a in ats for y in a.get_budgets())) + [-1]


def _um_ats(ats: "generator", y: int) -> [int]:
    """Returns integers represnting unique months of an Account collection
    and breakout integer
    """
    return sorted(
        set(bc.months_abv(m) for a in ats for m in a.get_budgets(y)), 
        key=lambda x: bc.months_to_int[x]) + [-1]


def main(ats: [Account]) -> None:
    while True: 
        assert len(ats) != 0, "No Account collection exists"
        for a in ats:
            a.remove_empty_budgets()
        print(menu)
        try: 
            choice = input("Your choice: ").rstrip()
            if choice == "esc":
                break
            try: 
                exec("_"+choice+"(ats)")
            except: 
                raise ValueError("Choice {} is not acceptable".format(choice))
        except ValueError as e:
            raise
            print("    An error has occurred: {}".format(e))
        except Exception as e:
            print("    An error has occurred: {}".format(e)) 


def _ats(ats: [Account]) -> None:
    """Executes choice to view all Transactions of an Account
    """
    a = bc.select_account(ats)
    print("\nDisplaying Transactions for {}\n".format(
        a.get_name())+_display_all_trans(a, bool))
    
    
def _cts(ats: [Account]) -> None:
    """Executes choice to view transactions of an Account over a custom time period
    """
    def _cond(t): return y0 <= t.get_year() <= y1 and \
        bc.months_to_int[m0] <= t.get_month() <= bc.months_to_int[m1]
    a = bc.select_account(ats)
    
    print("\nSelect Start Timeframe\n"+("="*40))            # Timeframe selection
    y0 = bc.trans_timeframe(_uy(ats))
    if y0 == -1: 
        return
    print()
    m0 = bc.trans_timeframe(_um(a, y0))
    if m0 == -1:
        return

    print("\nSelect End Timeframe\n"+("="*40))
    y1 = bc.trans_timeframe(_uy(ats))
    if y1 == -1: 
        return  
    print()
    m1 = bc.trans_timeframe(_um(a, y1))
    if m1 == -1:
        return

    print(
        "\nDisplaying Transactions for {} from {} {} to {} {}\n".format(
            a.get_name(), m0, y0, m1, y1))
    print(_display_all_trans(a, _cond))

 
def _omy(ats: [Account]) -> None: 
    """Executes choice to view one account for one year and one month
    """
    a = bc.select_account(ats)
    print()
    y0 = bc.trans_timeframe(_uy(ats))
    if y0 == -1: 
        return
    print()  
    m0 = bc.trans_timeframe(_um(a, y0))
    if m0 == -1:
        return
    print(_view_tf_budget(a, (y0, bc.months_to_int[m0] )))


def _oaa(ats: [Account]) -> None:
    """Executes choice to view one account for all years and months
    """
    a = bc.select_account(ats)
    print(_view_all_budgets(a, max_char))

    
def _ocst(ats: [Account]) -> None: 
    """Executes choice to view one account over a custom period
    """
    def _cond(y,m): return (y0,bc.months_to_int[m0]) <= (y,m) <= (y1,bc.months_to_int[m1])
    a = bc.select_account(ats)
    
    print("\nSelect Start Timeframe\n"+("="*40))             # Timeframe selection - copy in account analysis module
    y0 = bc.trans_timeframe(_uy(ats))
    if y0 == -1: 
        return
    print()
    m0 = bc.trans_timeframe(_um(a, y0))
    if m0 == -1:
        return

    print("\nSelect End Timeframe\n"+("="*40))
    y1 = bc.trans_timeframe(_uy(ats))
    if y1 == -1: 
        return  
    print()
    m1 = bc.trans_timeframe(_um(a, y1))
    if m1 == -1:
        return

    it = [(y,m) for y in a.get_budgets() \
          for m in a.get_budgets()[y] if _cond(y,m)]
    print(
        "\nDisplaying {} with Budgets from {} {} to {} {}".format(
            a.get_name(), m0, y0+1, m1, y1+1))
    print(_view_range_budget(
        a, sorted(it, key=lambda x: (x[0], x[1]), reverse=True), max_char))
    
    
def _acst(ats: [Account]) -> None:
    """Executes choice to view all accounts in a specific timeframe
    """
    def _cond1(y,m):
        return (y0,bc.months_to_int[m0]) <= (y,m) <= (y1,bc.months_to_int[m1])
    def _cond2(a):
        for y in range(y0,y1+1):
            for m in range(bc.months_to_int[m0],bc.months_to_int[m1]+1):
                if (y in a.get_budgets() and (m in a.get_budgets()[y])):
                    return True
        return False 
         
    print("\nSelect Start Timeframe\n"+("="*40))             # Timeframe selection
    y0 = bc.trans_timeframe(_uy(ats))
    if y0 == -1: 
        return
    print()
    m0 = bc.trans_timeframe(_um_ats(
        (a for a in ats if y0 in a.get_budgets()), y0))
    if m0 == -1:
        return

    print("\nSelect End Timeframe\n"+("="*40))
    y1 = bc.trans_timeframe(_uy(ats))
    if y1 == -1: 
        return  
    print()
    m1 = bc.trans_timeframe(_um_ats(
        (a for a in ats if y1 in a.get_budgets()), y1))
    if m1 == -1:
        return

    it = sorted(
        set(
        (y,m) for a in ats for y in a.get_budgets() for m in a.get_budgets(y) \
        if _cond1(y,m)), reverse=True)
    print("\nDisplaying All Accounts with Budgets from {} {} to {} {}".format(
        m0, y0+1, m1, y1+1))
    print(_view_range_budgets([a for a in ats if _cond2(a)], it, max_char))


def _aaa(ats: [Account]) -> None:
    it = sorted(
        set(
        (y,m) for a in ats for y in a.get_budgets() for m in a.get_budgets()[y]), 
                reverse=True)
    print("Displaying All Accounts for All Budgets")
    print(_view_range_budgets(ats, it, max_char))
                
        
def _display_all_trans(a: Account, f: "function") -> str:
    """Returns string of an Account's Transactions objects
    """
    ts = sorted((t for t in a.get_ts() if f(t)), 
                key=lambda x: (x.get_year(), x.get_month(), x.get_day()))
    return header(True) + "\n" + "\n".join(view(t, ts.index(t)+1) for t in ts)


def _display_budget_trans(a: Account, tf: (int, int)) -> str:
    """Returns string of account Transaction based on timeframe 
    """
    ts = sorted(
        (t for t in a.get_ts() if (t.get_year(), t.get_month()) == tf),
        key=lambda x: (x.get_year(), x.get_month(), x.get_day()))
    return header(True) + "\n" + "\n".join(view(t, ts.index(t)+1) for t in ts)


def _view_tf_budget(a: Account, tf: (int, int)) -> str:
    """Returns string of Account's budget tuple within timeframe
    """ 
    chosen_year, chosen_month = tf
    hd = "Account {} for {} {}\n".format(
        a.get_name(), chosen_year+1, bc.months(chosen_month)) 
    
    amt = "{:>.2f}".format(a.get_goal(chosen_year, chosen_month)/100)
    amt_full = "\tGoal........" + ("."*(10-len(amt))) + amt + "\n"

    rch = "{:>.2f}".format(a.get_reached(chosen_year, chosen_month)/100)
    reach_full = "\tReached....." + ("."*(10-len(rch))) + amt + "\n"
    
    rmn = "{:>.2f}".format(a.get_remain(chosen_year, chosen_month)/100)
    rem_full = "\tRemain......" + ("."*(10-len(rmn))) + amt + "\n"
    
    return "\n"+hd+("="*40)+"\n"+amt_full+reach_full+rem_full
    

def _view_all_budgets(a: Account, width: int) -> str:
    """Returns string of Account's budget tuple over all time periods.
    Prints out strings with the specified maximum width  
    """
    r = sorted(
        [(y,m) for y in a.get_budgets() for m in a.get_budgets(y)], 
        key=lambda x: (x[0], x[1]), reverse = True)
    return "\n"+_view_range_budget(a, r, width)
    
    
def _view_range_budget(a: Account, timeframe: [(int, int)], width: int) -> str:
    """Returns string of Account's budget tuple over a certain time period
    """
    bud_lim = ((width-10)//11)                                                  # How many budgets can be on one line
    it = len(timeframe)                                                         # How many budgets that will be displayed 
    set_lim = it//bud_lim + 1                                                   # How many sets to iterate through  
    set_apprch = 0; bud_apprch = 0; lines = list() 
        
    while set_apprch != set_lim: 
        set_apprch += 1
        title_sub_str = "Account {} for set {}".format(a.get_name(), set_apprch)
        hd          = "="*width + "\n"
        space_amt   = width//2-len(title_sub_str)
        title_str   = "{}{}{}".format(" "*space_amt, title_sub_str, " "*space_amt)
        attrib_str  = "Attribute|"
        goal_str    = "Goal.....|"
        reach_str   = 'Reached..|'
        remain_str  = "Remaining|"
                
        for y,m in timeframe[(set_apprch-1)*min(bud_lim, it):set_apprch*min(bud_lim, it)]:
            bud_apprch += 1

            attrib_str += "  {} {}|".format(bc.months_abv(m), y+1)
            
            g_str = "{:.2f}".format(a.get_goal(y,m)/100) 
            goal_str += "."*(10-len(g_str)) + g_str+"|"
            
            r_str = "{:.2f}".format(a.get_reached(y,m)/100)
            reach_str += "."*(10-len(r_str)) + r_str+"|"
            
            e_str = "{:.2f}".format(a.get_remain(y,m)/100)
            remain_str += "."*(10-len(e_str)) + e_str + "|"
        lines.append(title_str + "\n" + hd + attrib_str + "\n" + goal_str + "\n" + reach_str + "\n" + remain_str + "\n")
    return "\n".join(lines)


def _view_range_budgets(ats: [Account], timeframe: [(int, int)], width: int) -> str:
    """Returns string of multiple Accounts' budgets over a certain time period 
    """
    bud_lim = ((width-30)//11)                                                  # How many budgets can be on one line
    it = len(timeframe)                                                         # How many budgets that will be displayed 
    set_lim = it//bud_lim + 1                                                   # How many sets to iterate through  
    set_apprch = 0; bud_apprch = 0; lines = list() 

    while set_apprch != set_lim:
        set_apprch += 1
        title_sub_str = "Set {}".format(set_apprch)
        hd          = "="*width + "\n"
        space_amt   = width//2-len(title_sub_str)
        title_str   = "{}{}{}".format(" "*space_amt, title_sub_str, " "*space_amt)
        a_index     = 0
        lines.append(title_str + "\n" + hd)
        
        for a in sorted(ats, key=lambda x: x.get_name()):
            a_index     += 1
            a_str       = "{:>3}. {}".format(a_index, a.get_name())
            attrib_str  = a_str + (20-len(a_str)) * "." + "|Attribute|"
            goal_str    = " "*20+"|Goal.....|"
            reach_str   = " "*20+"|Reached..|"
            remain_str  = " "*20+"|Remaining|"
            
            for y,m in timeframe[(set_apprch-1)*min(bud_lim, it):set_apprch*min(bud_lim, it)]:
                bud_apprch += 1
                attrib_str += "  {} {}|".format(bc.months_abv(m), y+1)
                try: 
                    g_str = "{:.2f}".format(a.get_goal(y,m)/100) 
                    goal_str += "."*(10-len(g_str)) + g_str+"|"
                
                    r_str = "{:.2f}".format(a.get_reached(y,m)/100)
                    reach_str += "."*(10-len(r_str)) + r_str+"|"
                
                    e_str = "{:.2f}".format(a.get_remain(y,m)/100)
                    remain_str += "."*(10-len(e_str)) + e_str + "|"
                except:                 
                    goal_str    += "."*10 + "|"
                    reach_str   += "."*10 + "|"
                    remain_str  += "."*10 + "|"
            lines.append(attrib_str + "\n" + goal_str + "\n" + reach_str + "\n" + remain_str + "\n")
    return "\n".join(lines)


if __name__ == "__main__": 
    from transaction import Transaction 
    
    t0  = Transaction(2015, 0, 12, "Fast Food", "Cash", "In-n-Out", 100)
    t1  = Transaction(2015, 1, 24, "Fast Food", "Cash", 'McDonald\'s', 200)
    t2  = Transaction(2015, 2, 24, "Fast Food", "Debit", "McDonald's", 300)
    t3  = Transaction(2015, 3, 24, "Fast Food", "Cash", "Wendy's", 400)
    t4  = Transaction(2015, 4, 23, "Fast Food", "Gifts", "Wendy's", 500)
    t5  = Transaction(2015, 5, 22, "Fast Food", "Savings", "Coffee", 600)
    t6  = Transaction(2015, 6, 12, "Fast Food", "Cash", "In-n-Out", 700)
    t7  = Transaction(2015, 7, 24, "Fast Food", "Cash", 'McDonald\'s', 800)
    t8  = Transaction(2015, 8, 24, "Fast Food", "Debit", "McDonald's", 900)
    t9  = Transaction(2015, 9, 24, "Fast Food", "Cash", "Wendy's", 1000)
    t10 = Transaction(2015, 10, 23, "Fast Food", "Gifts", "Wendy's", 1100)
    t11 = Transaction(2015, 11, 22, "Fast Food", "Savings", "Coffee", 1200)
    t12 = Transaction(2016, 11, 22, "Fast Food", "Savings", "Coffee", 1300)
    t13 = Transaction(2016, 10, 22, "Fast Food", "Savings", "Coffee", 1300)
    t14 = Transaction(2016, 10, 22, "Drinks", "Savings", "Coffee", 1200)
    
    a1 = Account("Drinks", 0, [t14], {})
    a2 = Account("Fast Food", 0, [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13], {})
        
    print(_display_all_trans(a1, bool))
    print(_display_all_trans(a2, bool))
 
    print(_display_budget_trans(a1, (2015, 11)))
 
    print(_view_tf_budget(a1, (2016, 10)))
    print(_view_all_budgets(a1, 150))
    print(_view_all_budgets(a2, 150))

    main([a1, a2])
