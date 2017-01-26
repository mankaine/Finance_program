# account_edit.py 
# Module to edit Accounts 

from account import Account
import basecui as bc
import valid

# This module edits three of the attributes of an Account class; the name, 
# the kind, and the budget specific to each month. Each public function will
# implement the user interface to edit it.

# Menu to select what to edit 

menu = """
BUDGET ANALYSIS MENU
========================================
    [nam]    : Edit Account name
    [knd]    : Edit Account kind  
    [gll]    : Edit Account goal
    [esc]    : Return to main menu
"""

def main(ats: [Account]) -> None:
    """Provides menu/user input to edit accounts
    """
    while True: 
        for a in ats: 
            a.remove_empty_budgets()
        try: 
            print(menu)
            choice = input("Your Choice: ").rstrip()
            if choice == "nam":
                edit_name(ats)
            elif choice == "knd":
                edit_kind(ats)
            elif choice == "gll":
                edit_goal(ats)
            elif choice == "esc":
                break
            else:
                raise ValueError("Choice {} not acceptable".format(choice))
        except Exception as e: 
            print("    An error has occurred: {}".format(e))


# Edit name
def edit_name(ats: Account) -> None:
    """Prompts user for a new value for Account name
    """
    print("\nEditing Name\n" + ("="*40))
    while True: 
        a = bc.select_account(ats)
        if a == bc.breakout_account: 
            break
        while True: 
            print("\nInput New Name\n" + ("="*40))
            choice = input("New name (Current name: " + a.get_name() + "): ")
            if bc.binary_question("Confirm new name is " + choice + " ([y]es [n]o): ", "y", "n"): 
                a.set_name(choice)
            if not bc.binary_question("Enter a new name ([y]es or [n]o): ", "y", "n"):
                break
        if not bc.binary_question("Edit another Account's name ([y]es or [n]o): ", "y", "n"):
            break


# Edit type 
def edit_kind(ats: Account) -> None:
    """Prompts user for a new value for Account name
    """
    print("\nEditing Kind\n" + ("="*40))
    while True: 
        a = bc.select_account(ats)
        if a == bc.breakout_account:
            break
        while True: 
            print("\nInput New Kind\n" + ("="*40))
            try :
                for k,v in bc.kind_to_str.items(): 
                    print("{:>3}.".format(k + 1), v)
                choice_str = input("Select new name by number (Current kind: " + bc.kind_to_str[a.get_kind()] + "): ")
                choice = int(choice_str) - 1
                valid.kind(choice) 
                if bc.binary_question("Confirm new kind is " + bc.kind_to_str[choice] + " ([y]es [n]o): ", "y", "n"): 
                    a.set_kind(choice)
                if not bc.binary_question("Enter a new kind ([y]es or [n]o): ", "y", "n"):
                    break
            except Exception as e: 
                print("    An error has occurred: " + str(e))
        if not bc.binary_question("Edit another Account's kind ([y]es or [n]o): ", "y", "n"):
            break
    
    
# Edit goal for each month
def edit_goal(ats: Account) -> None: 
    """Mutates the goal of the selected Account and timeframe. 
    Provides user interface for mutating this information
    """
    print("\nEditing Goal\n" + ("="*40))
    while True: 
        a = bc.select_account(ats)
        if a == bc.breakout_account: 
            break
        while True: 
            print()
            y = bc.trans_timeframe(a.get_budgets())
            print()
            m = bc.months_to_int[bc.trans_timeframe([bc.months(i) for i in a.get_budgets(y)] + [-1])[:3]]
            while True: 
                print("\nInput New Goal\n" + ("="*40))
                try:
                    choice_str = input("Enter new goal (Current goal: {:.2f}): ".format(a.get_goal(y,m)/100))
                    choice = int(choice_str) * 100
                    valid.amount(choice) 
                    if bc.binary_question("Confirm new goal is {:.2f}".format(choice/100) + " ([y]es [n]o): ", "y", "n"): 
                        a.set_goal(y, m, choice)
                        break
                except Exception as e: 
                    print("    An error has occurred: " + str(e))
            if not bc.binary_question("Enter goals for other months ([y]es or [n]o): ", "y", "n"):
                break
        if not bc.binary_question("Edit a goal for another Account ([y]es or [n]o): ", "y", "n"):
            break


# Testing
if __name__ == "__main__":
    from account import Budget 
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
    
    a1 = Account("Drinks", 0, [t14], {2016: {10: Budget(1500, 1200, 1)}})
    a2 = Account("Fast Food", 0, [t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13], {})
    
    ats = [a1, a2]
    
    # Testing edit_name
    print("Previous value for a1.name" + a1.get_name())
    print("Previous value for a2.name" + a2.get_name())
 
    edit_name(ats)
     
    print("New value for a1.name" + a1.get_name())
    print("New value for a2.name" + a2.get_name())


    # Testing edit_kind
    print("Previous value for a1.kind {}".format(a1.get_kind()))
    print("Previous value for a2.kind {}".format(a2.get_kind()))
 
    edit_kind(ats)
     
    print("New value for a1.kind {}".format(a1.get_kind()))
    print("New value for a2.kind {}".format(a2.get_kind()))

    # Testing edit_goal 
    import pprint 
    pprint.pprint(a1.get_budgets())
    pprint.pprint(a2.get_budgets())

    edit_goal(ats)
    
    pprint.pprint(a1.get_budgets())
    pprint.pprint(a2.get_budgets())

