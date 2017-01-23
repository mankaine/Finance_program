# account_analysis.py 
# conducts and presents analysis of budgets 

from account                    import Account
from transaction                import Transaction
from account_graph_rate         import AccountGraphRate
from account_graph_compare      import AccountGraphCompare
from account_graph_cash_flow    import AccountGraphCashFlow
from calendar                   import monthrange
from datetime                   import date 
import basecui                  as bc 

menu = """
BUDGET ANALYSIS MENU
========================================
    [rsp]    : Rate of spending/saving for an Account
    [css]    : Compare rate of spending to rate of saving  
    [cfs]    : Analyze cash flows
    [bkd]    : Breakdown totals by Accounts
    [pce]    : Track rate of transactions
    [esc]    : Return to Main Menu
"""

def main(ats: [Account]) -> None:
    """Main menu for Budget Analysis. Prompts user for a choice
    """
    while True:
        if len(ats) == 0: print("No Account exists"); break
        print(menu)
        try: 
            choice = input("Your choice: ").rstrip()
            if choice == "rsp":
                _rate_of_reach(ats)
            elif choice == "css":
                _compare_goal_to_reach(ats)
            elif choice == "cfs":
                _compare_cash_flows(ats)
            elif choice == "bkd":
                _breakdown(ats)
            elif choice == "pce":
                _accounts_pace(ats)
            elif choice == "esc":
                break
            else:
                raise ValueError("Choice {} is not acceptable".format(choice))
        except ValueError as e:
            print("    An error has occurred: {}".format(e))
        except Exception as e:
            print("    An error has occurred: {}".format(e)) 
            

def _rate_of_reach(ats: [Account]) -> None:
    """Executes choice to view rate of spending or saving, depending on 
    the type of the Account
    """
    a = bc.select_account(ats)
    if a == bc.breakout_account:
        return 
    it = bc.timeframe_from_account(a)
    if it == [(-1,-1)]: 
        return 

    try: 
        print("Displaying graph of rate of spending")
        AccountGraphRate(a, it).view()
    except Exception as e: 
        print("    An error has occurred: {}".format(e))
    else:
        print("Graph closed")


def _compare_goal_to_reach(ats: [Account]) -> None:
    """Executes choice to view the goals of an Account against 
    its reached attributes
    """
    a = bc.select_account(ats)
    if a == bc.breakout_account:
        return 
    it = bc.timeframe_from_account(a)
    if it == [(-1,-1)]: 
        return 
    
    try: 
        print("Displaying graph comparing spending to goals")
        AccountGraphCompare(a, it).view()
    except Exception as e: 
        print("    An error has occurred: {}".format(e))
    else:
        print("Graph closed")


def _compare_cash_flows(ats: [Account]) -> None:
    """Executes choice to view the cash flows of an Account 
    """
    a = bc.select_account(ats)
    if a == bc.breakout_account:
        return 
    it = bc.timeframe_from_account(a)
    if it == [(-1,-1)]:
        return 

    try: 
        print("Displaying graph of cash flows")
        AccountGraphCashFlow(a, it).view()
    except Exception as e: 
        print("    An error has occurred: {}".format(e))
    else:
        print("Graph closed")


def _breakdown(ats: [Account]) -> None:
    """Executes choice to view the breakdown of transactions 
    of Accounts
    """
    def _um(a: Account, y: int) -> [int]:
        """Returns integers representing unique months of an Account and breakout integer
        """
        return sorted(
        set(bc.months_abv(m) for m in a.get_budgets(y)), 
        key=lambda x: bc.months_to_int[x]) + [-1]

        
    def _uy(a: Account or [Account]) -> [int]:
        """Returns integers representing unique years and breakout integer
        """
        if type(a) == Account: 
            return sorted(set(y for y in a.get_budgets())) + [-1]
        return sorted(set(y for act in a for y in act.get_budgets())) + [-1]
    
    def _cond1(y,m): return (y0, bc.months_to_int[m0_str[:3]]) \
        <= (y,m) <= (y1, bc.months_to_int[m1_str[:3]])
    
    def _um_ats(ats: "generator", y: int) -> [int]:
        """Returns integers represnting unique months of an Account collection
        and breakout integer
        """
        months = set() 
        for a in ats:
            if y in a.get_budgets():
                for m in a.get_budgets(y):
                    months.add(bc.months(m))
        return sorted(months, key=lambda x: bc.months_to_int[x[:3]]) + [-1]
                            
    print("\nSelect Start Timeframe\n"+("="*40))
    
    y0 = bc.trans_timeframe(_uy(ats))               # basecui.py selects timeframe based off of one account 
    if y0 == -1: 
        return
    print()
    
    m0_str = bc.trans_timeframe(_um_ats(ats, y0))
    if m0_str == -1:
        return

    print("\nSelect End Timeframe\n"+("="*40))
    y1 = bc.trans_timeframe(_uy(ats))
    if y1 == -1: 
        return  
    print()
    m1_str = bc.trans_timeframe(_um_ats(ats, y1))
    if m1_str == -1:
        return
    
    k = _select_kind(ats)
    
    k_ats = [a for a in ats if a.get_kind() == k]
    total = round(sum(t.get_amount() for a in k_ats for t in a.get_ts())/100, 2)
    line = "{:>3}. {:30} {:>10.2f} ({:>6.2f}%)"
    
    print("\nBreakdown of " + bc.kind_to_str[k] + " by Account")
    print("{:4} {:32} {:>8} {:>5}".format("Num", "Account Name", "Amount", "Percent"))
    print("="*55)
    print(line.format(1, "TOTAL", total, 100))
    
    ats.sort(key=lambda x: x.get_name())
    for n, a in enumerate(k_ats, 2):
        print(_breakdown_str(n, a, 
        [(y,m) for y in a.get_budgets() for m in a.get_budgets(y) if _cond1(y,m)],
        total, line))
        

def _breakdown_str(i: int, a: Account, tf: [(int, int)], net: float, line: str) -> str:
    """Returns string indicating the breakdown of an Account 
    """
    tf_amount   = round(
        sum(t.get_amount() for t in a.get_ts() \
            if (t.get_year(), t.get_month()) in tf)/100, 2)
    tf_perc     = round((tf_amount/net)*100, 2)
    return line.format(i, a.get_name(), tf_amount, tf_perc)


def _select_kind(ats: [Account]) -> int:
    """Returns kind according to user prompt
    """
    print("\nSelect Kind\n"+("="*40))
    it = sorted(set(a.get_kind() for a in ats))
    while True: 
        print("Options\n" + ("="*40))
        for n, v in enumerate(it, 1): 
            print("{:>3}. {}".format(n, bc.kind_to_str[v]))
        try: 
            choice = int(input("Select by number (select last to break out): ").rstrip())
            assert 1 <= choice <= len(list(it))
        except:
            print("Choice is invalid. Must be an integer between 1 and {}".format(len([it])))
        else: 
            for n1, v in enumerate(it, 1):
                if choice == n1:
                    return v
            return -1
    

def _accounts_pace(ats: [Account]) -> None:
    """Executes choice to view the pacing of reaching goals of 
    Account budgets
    """
    tf = [(y,m) for a in ats for y in a.get_budgets() for m in a.get_budgets(y)]
    start_year, start_month = tf[0][0], tf[0][1]
    end_year, end_month = tf[-1][0], tf[-1][1]
    
    print("\nShowing Daily Budgeting of Transactions")
    print("="*40)
    print("Start:", bc.months(start_month), start_year)
    print("End  :", bc.months(end_month), end_year)
    print("Today:", date.today().strftime("%B %d %Y"))
    print("{:>3}  {:20} {:65} {:8} {:8} {:8} {:8}".format(
        "No.", "Account Name", "", "Reached", "Goal", "Remain", 
        "Rate to remain on task"))
    for n, a in enumerate(ats, 1): 
        print(_pce_str(n, a, tf))
            
     
def _budget_total(a: Account, s: str, tf: [(int, int)]) -> int:
    """Returns sum of Account's attribute over specified timeframe
    """
    _sum = 0
    for y,m in tf: 
        if y in a.get_budgets():
            if m in a.get_budgets(y):
                method_str = "a.get_" + s + "(" + str(y)+ "," + str(m) + ")"
                _sum += eval(method_str)
    return _sum


def _calculate_pace_placement(tf: [(int, int)], bar_max: int) -> int:
    """Returns integer representing placement for pace string
    """
    today = date.today()
    number_of_days = 0
    number_of_days_before_today = 0
    
    for y,m in tf: 
        if (y,m) <= (today.year, today.month):
            number_of_days_before_today += monthrange(y+1,m+1)[1] 
        number_of_days += monthrange(y+1,m+1)[1]
    return bar_max*(number_of_days_before_today/number_of_days)


def _days_remaining(tf: [(int, int)]):
    """Returns integer indicating how many days remain in a timeframe  
    """
    today = date.today()
    days = 0 
    
    for y,m in tf: 
        if (today.year+1, today.month+1) < (y,m):
            days += monthrange(y+1, m+1)[1]
    return days


def _pce_str(i: int, a: Account, tf: [(int, int)]) -> str: 
    """Returns string indicating pacing of how goals have been reaching transaction 
    """    
    bar_len = 60                                            # space in between brackets
    budget_total  = _budget_total(a, "goal", tf)            # used to place | 
    reached_total = _budget_total(a, "reached", tf)         # used to place -
    days_left = _days_remaining(tf)

    reach_int       = round((reached_total/budget_total)*60)
    pace_int        = _calculate_pace_placement(tf, bar_len)
    remain_total    = (budget_total - reached_total)
    ideal_pace      = (budget_total - reached_total)
    if days_left != 0:                                      # Account for division by zero error
        ideal_pace /= days_left
    else: 
        ideal_pace = days_left
        
    bar_str = "["
    for n in range(bar_len): 
        if n == pace_int: 
            bar_str += "|"
        elif n < reach_int: 
            bar_str += "-"
        else:
            bar_str += " "
    bar_str += '|]' if "|" not in bar_str else "]"
            
    return "{:>3}. {:20} {:65} {:8.2f} {:8.2f} {:8.2f} {:8.2f}/day".format(
        i, a.get_name(), bar_str, reached_total/100, budget_total/100, 
        remain_total/100, ideal_pace/100)


# Testing
if __name__ == "__main__":
    from account import Budget 
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
    
    a1 = Account("Drinks", 0, [t14], {2016: {10: Budget(1500, 1200, 1)}})
    a2 = Account("Fast Food", 0, [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13], {})

    main([a1,a2])
