# trans_edit.py 
# Edits transactions 

from transaction    import Transaction
from account        import Account  
from trans_view     import view, header
import basecui      as bc

as_attrib = {
    "yrr": "year", 
    "mth": "month",
    "day": "day",
    "dsc": "description",
    "dac": "dr_account",
    "cac": "cr_account",
    "crr": "currency",
    "amt": "amount",
    "esc": "esc",
    "del": "delete"}

_menu =  """
EDIT TRANSACTION MENU
================================================================================
    [yrr]    : Edit year - must be an integer between 0 and 9999
    [mth]    : Edit month - must be an integer between 1 and 12
    [day]    : Edit day of the month  
    [dsc]    : Edit description
    [dac]    : Edit debit account name
    [cac]    : Edit credit account name
    [crr]    : Edit currency symbol no longer than 3 characters 
    [amt]    : Edit a positive floating or integer number
    [del]    : Delete transaction
    [esc]    : Return to previous menu""" 


def main(ts: [Transaction], ats: [Account]) -> None:
    """Revises Transaction from a Transaction collection, based on 
    user input 
    """
    editing = True 
    while editing: 
        t = _select_trans(ts)
        if isinstance(t, Transaction): 
            menu(ts, ts.index(t), ats)
        editing = bc.binary_question("Edit another transaction ([y]es or [n]o): ", "y", "n")


def _select_trans(ts) -> Transaction or None:
    """Returns transaction selected based on iteration
    """
    def _cond(y,m,t): return t["year"] == y and t["month"] == bc.months_to_int[m]
    
    print("Unique Years\n"+("=" * 40))
    y = bc.trans_timeframe(sorted(set(t["year"] for t in ts)) + [-1])
    if y == -1: 
        return 
    
    print("\nUnique Months\n"+("=" * 40))
    s = (bc.months_abv(m) for m in sorted(set(t["month"] for t in ts)))
    m = bc.trans_timeframe(list(s) + [-1])
    ts_tf = sorted((t for t in ts if _cond(y,m,t)), key = lambda x: x["day"])
    if m == -1: 
        return 
    
    while True:     
        try: 
            print("\n"+header(True))
            for n0,t in enumerate(ts_tf, 1):
                print(view(t,n0))        
            n = int(input("Select transaction number: ").rstrip())
            for n1, v in enumerate(ts_tf, 1):
                if n == n1:
                    return v 
        except Exception as e: 
            print("    An error has occurred: " + str(e))
             
    
def menu(ts, i, ats) -> None:
    """Revises Transaction object based on user input 
    """ 
    attribs = ("yrr", "mth", "day", "dsc", "dac", "cac", "crr", "flw", "amt",
               "prc", "del", "esc")
    while True:
        print(_menu+"\n\nSelected Transaction:\n" + header()) 
        print(view(ts[i])) 
        try:
            choice = input("Your choice: ").rstrip()
            assert choice in attribs, "{} not an option.".format(choice)
            if choice == "esc": break
            _new_input(ts, i, as_attrib[choice], ats)
            break
        except Exception as e: 
            print("    An error occured: transedit.main: {}".format(e))
            
            
def _new_input(ts: [Transaction], trans_index: int, attrib: str, ats: [Account]) -> None:
    """Mutates a transaction based on user input
    """
    while True: 
        try: 
            if attrib in ("day", "month", "year"):
                choice = input("Enter new value (previous: {}): ".format(ts[trans_index][attrib] + 1)) 
                ts[trans_index][attrib] = int(eval(choice) - 1)
            elif attrib in ("description", "dr_account", "cr_account", "currency"):
                choice = input("Enter new value (previous: {}): ".format(ts[trans_index][attrib])) 
                ts[trans_index][attrib] = choice  
            elif attrib in ("amount"): 
                choice = input("Enter new value (previous: {}): ".format(ts[trans_index][attrib]))
                ts[trans_index][attrib] = int(eval(choice) * 100)
            elif attrib in ("delete"):
                if bc.binary_question(
                    "Are you sure you want to delete this transaction ([y]es or [n]o): ", 
                    "y", "n"):
                    ts.remove(ts[trans_index])
                    for a in ats: 
                        if ts[trans_index] in a: 
                            a.remove(ts[trans_index])
                    print("Transaction Successfully Deleted")
                    break
        except Exception as e: 
            print("    An error has occurred: " + str(e))
        else: 
            print("Transaction Successfully Updated")
            break 
        
        
if __name__ == "__main__":
    t0 = Transaction(2015, 11, 24, "Fast Food", "Cash", 'McDonald\'s', 400)
    t1 = Transaction(2015, 11, 24, "Fast Food", "Cash", 'McDonald\'s', 300)
    t2 = Transaction(2015, 11, 24, "Fast Food", "Debit", "McDonald's", 200)
    t3 = Transaction(2015, 10, 24, "Fast Food", "Cash", "Wendy's", 500)
    t4 = Transaction(2015, 10, 23, "Fast Food", "Gifts", "Wendy's", 400)
    t5 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)

#    menu(t0)
#     def check_new_input(t, a):
#         """function to check _new_input the output of methods
#         """
#         print("Checking " + a)
#         print("Previous:", t[a])
#         _new_input(t, a)
#         print("New     :",t[a])
#         print()
#      
#     check_new_input(t0, "day")
#     check_new_input(t0, "month")
#     check_new_input(t0, "year")
#     
#     check_new_input(t0, "description")
#     check_new_input(t0, "dr_account")
#     check_new_input(t0, "cr_account")
#     
#     check_new_input(t0, "amount")
#     check_new_input(t0, "currency")

    main([t0,t1,t2,t3,t4,t5])