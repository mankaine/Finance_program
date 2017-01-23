# trans_entry.py 
# Entering and Initializing Transactions 

from transaction import Transaction
import basecui as bc 
import trans_edit
from trans_view import view, header 
import valid

_menu = """ 
TRANSACTION MENU:
======================================
    [ind]    : Enter individually
    [moo]    : Enter by month
    [esc]    : Return to Main Menu
"""

def main() -> [Transaction]:
    """Runs menu to create transactions. Returns a list of 
    Transactions created from user input 
    """
    ts = list()
    while True: 
        print(_menu)
        choice = input("Your choice: ").rstrip()
        try: 
            if choice == "ind":
                print("\nEntering one Transaction")
                ts.append(_enter()) 
            elif choice == "moo":
                print("\nEntering multiple transactions")
                ts += _enter_block() 
            elif choice == "esc":
                print("\nReturning to main menu")
                return ts
            else: 
                print("Choice {} not an option. Try again.".format(choice))
        except Exception as e: 
            print("    An error has occurred: " + str(e))
            return ts 


def _enter(y=-1, m=-1) -> Transaction:
    """Returns a transaction constructed from user input, with 
    second iteration to edit 
    """
    print("Entering transaction\n" + ("="*40))
    if y < 0: # All ints representing months are non-negative
        y = _prompt_year()
    if m < 0:
        m = _prompt_month()
    d = _prompt_day(y,m) 
    dr = _prompt_dr_account()
    cr = _prompt_cr_account()
    e = _prompt_description()
    a = _prompt_amount()
    c = _prompt_currency()
    
    t = Transaction(y,m,d,dr,cr,e,a) if c == "" else Transaction(y,m,d,dr,cr,e,a,c)
    print("\nEntered Transaction:\n" + header())
    print(view(t))
    
    return _opt_edit(t) 


def _opt_edit(t: Transaction) -> Transaction:
    """Prompts user to edit a Transaction
    """
    if bc.binary_question("Edit transaction ([y]es or [n]o): ", "y", "n"): 
        trans_edit.menu(t)         
    return t


def _enter_block():
    """Loop to enter transactions under a specific month and year
    """
    ts = list()
    print("Entering year and month\n" + ("="*40))
    y = _prompt_year()
    if y == -1: 
        return ts 
    
    m = _prompt_month()
    if m == -1:
        return ts
    
    entering = True 
    while entering:
        try:  
            ts.append(_enter(y,m))
        except Exception as e: 
            print("    An error has occurred: " + str(e)) 
        else: 
            entering = bc.binary_question("Enter another question ([y]es or [n]o): ", "y", "n")
    return ts 


def _prompt_year() -> int:
    """Returns integer representing year, based off of user input and 
    zero based indexing 
    """
    while True: 
        choice = input("Enter year            : ").rstrip() 
        try: 
            choice_int = int(eval(choice)) - 1
            valid.year(choice_int)
        except Exception as e: 
            print(
                "    An error has occurred: transentry._prompt_year: " + \
                "{} is not an option because {} Try again".format(choice, e)) 
        else: 
            return choice_int
        

def _prompt_month() -> int:
    """Returns integer representing year, based off of user input and 
    zero based indexing 
    """
    while True: 
        choice = input("Enter month number (e.g. January is 1): ").rstrip() 
        try: 
            choice_int = int(eval(choice)) - 1
            valid.month(choice_int)
        except Exception as e: 
            print("    An error has occurred: transentry._prompt_month: " +\
                  "{} is not an option because {} Try again".format(choice, e)) 
        else: 
            return choice_int
        
        
def _prompt_day(y: int, m: int) -> int:
    """Returns integer representing day, absed off of user input and 
    zero based indexing 
    """
    while True: 
        choice = input("Enter day             : ").rstrip() 
        try: 
            choice_int = int(eval(choice))
            valid.day(y,m,choice_int)
        except Exception as e: 
            print("    An error has occurred: transentry._prompt_day: " + \
                  "{} is not an option because {} Try again".format(choice, e)) 
        else: 
            return choice_int - 1


def _prompt_dr_account() -> str:
    """Returns string of Account Debit name
    """
    while True: 
        choice = input("Enter account (debit) : ").rstrip() 
        try: 
            valid.dr_account(choice)
        except Exception as e: 
            print("    An error has occurred: transentry._prompt_dr_account:"+\
            " {} is not an option because {} Try again".format(choice, e)) 
        else: 
            return choice


def _prompt_cr_account() -> str:
    """Returns string of Account Credit name
    """
    while True: 
        choice = input("Enter account (credit): ").rstrip() 
        try: 
            valid.cr_account(choice)
        except Exception as e: 
            print("    An error has occurred: transentry._prompt_cr_account:" +\
                  " {} is not an option because {} Try again".format(choice, e)) 
        else: 
            return choice 


def _prompt_description() -> str:
    """Returns string of Transaction description
    """
    while True: 
        choice = input("Enter description     : ").rstrip() 
        try: 
            valid.cr_account(choice)
        except Exception as e: 
            print("    An error has occurred: transentry._prompt_description:"+\
                  " {} is not an option because {} Try again".format(choice, e)) 
        else: 
            return choice 


def _prompt_currency() -> str:
    """Returns string of Transaction currency
    """
    while True: 
        choice = input("Enter currency        : ").rstrip() 
        try: 
            valid.currency(choice)
        except Exception as e: 
            print("    An error has occurred: transentry._prompt_currency:"+\
                  " {} is not an option because {} Try again".format(choice, e)) 
        else: 
            return choice 


def _prompt_amount() -> int:
    """Returns integer representing amount
    """
    while True: 
        choice = input("Enter amount          : ").rstrip()
        int_choice = int(eval(choice)*100)
        try: 
            valid.amount(int_choice)
        except Exception as e: 
            print("    An error has occurred: transentry._prompt_amount:" +\
                  " {} is not an option because {} Try again".format(choice, e)) 
        else: 
            return int_choice 

    
if __name__ == "__main__": 
    # Testing an Individual Input
    t0 = _enter()
    print("Resulting transaction: " + repr(t0))
    
    # Testing the main module 
    print(main())