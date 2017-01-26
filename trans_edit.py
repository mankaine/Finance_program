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
    def _cond(y,m,t): return t.get_year() == y and t.get_month() == bc.months_to_int[m]
    
    print("Unique Years\n"+("=" * 40))
    y = bc.trans_timeframe(sorted(set(t.get_year() for t in ts)) + [-1])
    if y == -1: 
        return 
    
    print("\nUnique Months\n"+("=" * 40))
    s = (bc.months_abv(m) for m in sorted(set(t.get_month() for t in ts if t.get_year() == y)))
    m = bc.trans_timeframe(list(s) + [-1])
    if m == -1: 
        return 

    ts_tf = sorted((t for t in ts if _cond(y,m,t)), key = lambda x: x.get_day())
    
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
    editing = True 
    while editing:
        print(_menu+"\n\nSelected Transaction:\n" + header()) 
        if len(ts) == 0:
            print("    No Transactions to edit")
            break
        try:
            # Placing this in try statement prevents exception from being raised
            # when Transaction is deleted
            try: 
                print(view(ts[i])) 
            except: 
                print("{:^100}".format("Transaction No Longer Available: It Was Deleted"))
                break 
            choice = input("Your choice: ").rstrip()
            assert choice in attribs, "{} not an option.".format(choice)
            if choice == "esc":
                break
            _new_input(ts, i, as_attrib[choice], ats)
            editing = bc.binary_question("Continue editing ([y]es or [n]o): ", "y", 'n')
        except Exception as e: 
            print("    An error occured: transedit.main: {}".format(e))
            
            
def _new_input(ts: [Transaction], trans_index: int, attrib: str, ats: [Account]) -> None:
    """Mutates a transaction based on user input
    """
    trans_to_edit = ts[trans_index]
    while True: 
        try: 
            if attrib == "day":
                choice = input("Enter new day (previous: {}): ".format(
                    trans_to_edit.get_day() + 1))
                trans_to_edit.set_day(int(eval(choice) - 1))
                break
            elif attrib == "month":
                choice = input("Enter new month (previous: {}): ".format(
                    trans_to_edit.get_month() + 1))
                trans_to_edit.set_month(int(eval(choice) - 1))
                break
            elif attrib == "year":
                choice = input("Enter new year (previous: {}): ".format(
                    trans_to_edit.get_year() + 1)) 
                trans_to_edit.set_year(int(eval(choice) - 1))
                break
            elif attrib == "description":
                choice = input("Enter new description (previous: {}): ".format(
                    trans_to_edit.get_description())) 
                trans_to_edit.set_description(choice)
                break
            elif attrib == "dr_account":
                choice = input("Enter new account (previous: {}): ".format(
                    trans_to_edit.get_dr_account())) 
                trans_to_edit.set_dr_account(choice)
                break
            elif attrib == "cr_account":
                choice = input("Enter new account (previous: {}): ".format(
                    trans_to_edit.get_cr_account())) 
                trans_to_edit.set_cr_account(choice)
                break
            elif attrib == "description":
                choice = input("Enter new description (previous: {}): ".format(
                    trans_to_edit.get_currency())) 
                trans_to_edit.set_currency(choice)
                break
            elif attrib == "amount": 
                choice = input("Enter new amount (previous: {:.2f}): ".format(
                    round(trans_to_edit.get_amount()/100, 2) ))
                trans_to_edit.set_amount(eval(choice)*100)
                break
            elif attrib in ("delete"):
                if bc.binary_question(
                    "Are you sure you want to delete this transaction ([y]es or [n]o): ", 
                    "y", "n"):
                    for a in ats: 
                        if ts[trans_index] in a: 
                            a.remove(ts[trans_index])
                    ts.remove(ts[trans_index])
                    print("Transaction Successfully Deleted")
                    break
                else:
                    break
        except Exception as e: 
            print("    An error has occurred: " + str(e))
        else: 
            print("Transaction Successfully Updated")
        
        
if __name__ == "__main__":
    t0 = Transaction(2015, 11, 24, "Fast Food", "Cash", 'McDonald\'s', 400)
    t1 = Transaction(2015, 11, 24, "Fast Food", "Cash", 'McDonald\'s', 300)
    t2 = Transaction(2015, 11, 24, "Fast Food", "Debit", "McDonald's", 200)
    t3 = Transaction(2015, 10, 24, "Fast Food", "Cash", "Wendy's", 500)
    t4 = Transaction(2015, 10, 23, "Fast Food", "Gifts", "Wendy's", 400)
    t5 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)

    a0 = Account("Fast Food", 0, [t0,t1,t2,t3,t4], {})
    a1 = Account("Drinks", 0, [t5], {})
    main([t0,t1,t2,t3,t4,t5], [a0, a1])
