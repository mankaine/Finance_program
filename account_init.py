# account_init.py
# module to create Accounts 

from transaction import Transaction 
from account     import Account 
from collections import defaultdict

# Create Accounts automatically from Transactions. Call only when creating 
# new Account objects to prevent duplication of Account object and loss of 
# customized budgets   
def create_from(ts: [Transaction]) -> [Account]:
    """Returns list of Account objects from Transaction objects 
    """
    accts = defaultdict(list)
    for t in ts: 
        accts[t.get_dr_account()].append(t)
        accts[t.get_cr_account()].append(t)
        
    results = list()
    for a in accts: 
        results.append(Account(a, 0, accts[a], {}))
    return results 


# Create account 
def create(ts: [Transaction]) -> Account:
    """Returns Account based on user interface preferences
    """
    n = _get_name(ts)
    print()        
    tx = _get_ts(n)
    print()
    t = _get_type()
    return Account(n, t, tx, {})


def merge_accounts(ats: [Account]) -> [Account]:
    """Returns Accounts that have been merged
    """
    merged_accounts  = list() 
    grouped_accounts = defaultdict(list)
    for a in ats: grouped_accounts[a.get_name()].append(a)
    for _,v in grouped_accounts.items():
        merged_accounts.append( v[0].merge(v[1:]) )
    return merged_accounts


def _get_name(ts: [Transaction]) -> str:
    """Returns name user indicates as the title of Account, based on 
    user input 
    """
    while True: 
        names_duplicates = [t.get_dr_account() for t in ts] + [t.get_cr_account() for t in ts]
        names = sorted(set(names_duplicates))
        try: 
            print("Choosing Account Name\n" + ("="*40))
            for n0, v0 in enumerate(names, 1): 
                print("{:>3}. {}".format(n0, v0))
            choice = int(input("Enter name of Account (number): ").rstrip())
            assert choice in range(1, len(names) + 1), "Choice {} not in the range 1 to {}".format(choice, len(names))
        except Exception as e: 
            print("    An error occurred: {}".format(e))
        else: 
            for n1, v1 in enumerate(names, 1):
                if n1 == choice: 
                    return v1
                

def _get_type() -> int:
    """Returns type of Account based on user input
    """
    types = {
        0: "Recurring Expenses", 1: "Variable Expenses", 
        2: "Investments", 3: "Savings"}
    t_keys = list(types.keys()); lo = min(t_keys) + 1; hi = max(t_keys) + 2 
    options =  "Choosing Account Type\n" + ("="*40) + "\n" + "\n".join(
        "{:>3}. {}".format(k+1, v) for (k, v) in types.items())

    while True:  
        try: 
            print(options)
            choice = int(input("Choose by number: ").rstrip())
            assert choice in range(lo, hi), "Choice not in the range {} to {}".format(lo, hi-1)
        except Exception as e:  
            print("    An error has occurred: {}".format(e))
        else: 
            return choice - 1
        
        
def _get_ts(name: str) -> [Transaction]:
    """Returns Transactions that contain an account name with the specified value
    """ 
    return [t for t in ts if name in (t.get_dr_account(), t.get_cr_account())]        


# Testing
if __name__ == "__main__":
    t0 = Transaction(2015, 11, 24, "Cash", "Accounts Recievable", "Job", 400)
    t1 = Transaction(2015, 11, 24, "Fast Food", "Cash", 'McDonald\'s', 300)
    t2 = Transaction(2015, 11, 24, "Fast Food", "Debit", "McDonald's", 200)
    t3 = Transaction(2015, 10, 24, "Fast Food", "Cash", "Wendy's", 500)
    t4 = Transaction(2015, 10, 23, "Fast Food", "Gifts", "Wendy's", 400)
    t5 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)
    t6 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)
    t7 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)
    t8 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)
    
    ts = [t0, t1,t2,t3,t4,t5]

    a0,a1=create_from([t5,t6])
    a2,a3=create_from([t7,t8])
    for a in create_from(ts):
        print(a)
     
    n = _get_name(ts)    
    print("Obtained name   : ", n)
     
    tx = _get_ts(n)
    print("Transactions    : ", tx)
     
    t = _get_type()
    print("Type            :", t)

    a = create(ts)
    print(a)
    import pprint 

    for i in merge_accounts([a0,a1,a2,a3]):
        pprint.pprint(i)
        print(len(i.get_ts()))
    
    