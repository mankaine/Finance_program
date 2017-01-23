# basecui.py
# Basis display for Command Line Interface 

import calendar as cal 
from account import Account 

breakout_account = Account("Break Out", 0, [], {}) # Provide breakout option for Accounts

flow_as_str = {
    -1: "-", 
    1: "+"} 

str_as_flow = {
    "-": -1, 
    "+" : 1}

months_to_int = {
    "Jan":0,
    "Feb":1,
    "Mar":2,
    "Apr":3,
    "May":4,
    "Jun":5,
    "Jul":6,
    "Aug":7,
    "Sep":8,
    "Oct":9,
    "Nov":10,
    "Dec":11}

kind_to_str = {
    0: "Recurring Expenses",
    1: 'Variable Expenses',
    2: "Investments",
    3: 'Savings'} 
    

def months(m) -> str :
    """Returns the name of a month
    """
    return cal.month_name[m+1]

def months_abv(m) -> str:
    """Returns an abbreviated month
    """
    return cal.month_abbr[m+1]

def binary_question(question, true_if_this, false_if_this) -> bool: 
    """Returns boolean based on the conditions presented for a yes/no question
    """
    while True: 
        ans = input(question) 
        if ans == true_if_this: 
            return True 
        elif ans == false_if_this: 
            return False 
        else:
            print("Choice {} is not acceptable. Select either {} or {}".format(ans, true_if_this, false_if_this))
            

def trans_timeframe(it) -> int:
    """Returns an integer based off of viewing Transactions's timeframe 
    """
    while True: 
        print("Options\n" + ("="*40))
        for n, v in enumerate(it, 1): 
            print("{:>3}. {}".format(n, v+1 if type(v) == int else v))
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
        
def timeframe_from_accounts(accounts: ["Account"], a=None) -> ("Account",[(int, int)]):
    """Returns timeframe based off of user input. Available timeframes 
    generated through those of the Accounts 
    """
    def _in_timeframe(y,m): return \
        (y0, months_to_int[m0[:3]]) <= (y,m) <= (y1, months_to_int[m1[:3]])
    chosen_account = select_account(accounts)
    
    print("\nSelect Start Timeframe\n" + ("="*40))
    _unique_years0 = sorted(set(y for a in accounts for y in a.get_budgets())) 
    y0 = trans_timeframe(_unique_years0 + [-1]) 
    if y0 == -1: 
        return 

    print()    
    _unique_months0 = sorted(
        set(months(m) for a in accounts for m in a.get_budgets(y0)),
        key = lambda x: months_to_int[x])
    m0 = trans_timeframe(_unique_months0 + [-1])
    if m0 == -1: 
        return 
    
    print("\nSelect End Timeframe\n" + ("="*40))
    _unique_years1 = sorted(set(y for a in accounts for y in a.get_budgets())) 
    y1 = trans_timeframe(_unique_years1 + [-1]) 
    if y1 == -1: 
        return 

    print()    
    _unique_months1 = sorted(
        set(months(m) for a in accounts for m in a.get_budgets(y1)),
        key = lambda x: months_to_int[x])
    m1 = trans_timeframe(_unique_months1 + [-1])
    if m1 == -1: 
        return 

    return chosen_account, [
        (y,m) for y in a.get_budgets() for m in a.get_budgets(y) if \
        _in_timeframe(y,m)]


def timeframe_from_account(a: "Account") -> [(int, int)]:
    """Returns list covering start and end timeframe tuple based 
    on selected Account
    """

    def _in_timeframe(y,m): return \
        (y0, months_to_int[m0[:3]]) <= (y,m) <= (y1, months_to_int[m1[:3]])
    
    print("\nSelect Start Timeframe\n" + ("="*40))
    _unique_years0 = sorted(set(a.get_budgets().keys())) 
    y0 = trans_timeframe(_unique_years0 + [-1]) 
    if y0 == -1: 
        return [(-1,-1)]

    print()    
    _unique_months0 = sorted(
        set(months(m) for m in a.get_budgets(y0)),
        key = lambda x: months_to_int[x])
    m0 = trans_timeframe(_unique_months0 + [-1])
    if m0 == -1: 
        return [(-1,-1)]
    
    print("\nSelect End Timeframe\n" + ("="*40))
    _unique_years1 = sorted(set(a.get_budgets().keys())) 
    y1 = trans_timeframe(_unique_years1 + [-1]) 
    if y1 == -1: 
        return [(-1,-1)]

    print()    
    _unique_months1 = sorted(
        set(months(m) for m in a.get_budgets(y1)),
        key = lambda x: months_to_int[x])
    m1 = trans_timeframe(_unique_months1 + [-1])
    if m1 == -1: 
        return [(-1,-1)]

    return [
        (y,m) for y in a.get_budgets() for m in a.get_budgets(y) if \
        _in_timeframe(y,m)]



def select_account(it: [Account]) -> Account:
    """Returns Account selected from iterable it  
    """
    while True: 
        print("\nOptions\n" + ("="*40))
        for n, v in enumerate(it + [breakout_account], 1): 
            print("{:>3}. {}".format(n, v.get_name()))
        try: 
            choice = int(
                input("Select by number (select last to break out): ").rstrip())
            assert 1 <= choice <= len(list(it + [breakout_account]))
        except:
            print(
                "Choice is invalid. Must be an integer between 1 and {}".format(
                len([it]) + 1))
        else: 
            for n1, v1 in enumerate(it + [breakout_account], 1):
                if choice == n1:
                    return v1
            return -1
        

def remove_duplicates(ts: ["Transaction"]) -> ["Transaction"]:
    """Removes duplicates in a list of Transactions
    """
    iterated = list() 
    unique_ts= list() 
    for t in ts: 
        if t not in iterated: 
            unique_ts.append(t)
            iterated.append(t)
    return unique_ts