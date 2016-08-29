# main_menu.py
# by mankaine
# July 12, 2016

# Implements main menu in shell user interface.
# See read_me.txt for example implementation.

import finance_entry
import finance_edit
import finance_view
import finance_export
import finance_import
import finance_budget_menu
import settings

import basic_view

import cashflow


MAIN_MENU = '''
MAIN MENU:
1. Enter Transactions
2. Edit Transactions
3. Import Transactions
4. Export Transactions
5. View Transactions
6. Budget Accounts
7. Settings
8. Access Settings
9. Exit
'''

# run_user_interface implements main_menu_input from the basic_view module
# and passes the value returned to _main_menu_options. If the value returned
# corresponds to the exit choice, the program breaks out of the loop. 
# 
# _main_menu_input processes and determines if the choice made is valid, and 
# prompts the user until a valid choice is made.


# _main_menu_options determines how the value _main_menu_input returns 
# should be processed. Its arguments, a Revenues object, an Expenses 
# object (accessed only by entering transactions), and a dictionary
# (passed into all choices), are updated every time a transaction
# is entered, edited, or imported. This event is coded in 
# run_user_interface. 
def _main_menu_options (choice: int, inflows: cashflow.CashFlows, 
        outflows: cashflow.CashFlows) -> None:
    '''Transfers control over to other menus from the main menu
    '''
    if choice == 1: 
        basic_view.print_loading_newline("ENTERING TRANSACTIONS")
        finance_entry.handle_entry_choice(inflows, outflows)
    
    elif choice == 2: 
        if inflows.cfs == {} and outflows.cfs == {}:
            print("\nINACESSABLE - No transactions entered")
        else:
            basic_view.print_loading_newline("EDITING TRANSACTIONS")
            finance_edit.handle_edit_choice(inflows, outflows)

    elif choice == 3:
        basic_view.print_loading_newline("MOVING TO IMPORT MENU")
        finance_import.handle_import_choice(inflows, outflows)

    elif choice == 4: 
        if inflows.cfs == {} and outflows.cfs == {}:
            print("\nINACESSABLE - No transactions entered")
        else:
            basic_view.print_loading_newline("EXPORTING TRANSACTIONS")
            finance_export.handle_export_choice(inflows, outflows)
     
    elif choice == 5: 
        if inflows.cfs == {} and outflows.cfs == {}:
            print("\nINACESSABLE - No transactions entered")
        else:
            basic_view.print_loading_newline("MOVING TO DISPLAY MENU")
            finance_view.handle_view_choice(inflows, outflows)
            
    elif choice == 6:
        if inflows.cfs == outflows.cfs:
            print("\nINACESSABLE - No transactions entered")
        else:
            basic_view.print_loading_newline("BUDGETING TRANSACTIONS")
            finance_budget_menu.handle_budget_choice(inflows, outflows)
  
    elif choice == 7:
        basic_view.print_loading_newline("GOING TO SETTINGS")
        basic_view.print_loading_newline("RETURNING TO MAIN MENU")        

    elif choice == 8:
        basic_view.print_loading_newline("ACESSING SETTINGS")
        settings.run_setting_interface()

    elif choice == 9:
        basic_view.print_loading_newline("EXITING PROGRAM")
        

# The model modules are designed to handle a large number of transactions, so 
# messages are constantly posted about the status of the program (which module
#  it's on, what it's loading, etc.). The program starts with a blank slate 
# Revenues, Expenses, and dict object and changes the values as the user enters 
# and edits. The final option is to exit the program, which is represented by 
# choosing '8' to break out of the while loop. 
def run_user_interface():
    '''Runs program
    '''
    basic_view.print_loading("FINANCE PROGRAM")
    
    inflows = cashflow.CashFlows() 
    outflows = cashflow.CashFlows() 
    
    using_program = True
    while using_program:
        choice = basic_view.menu_input(MAIN_MENU, 10)
        _main_menu_options(choice, inflows, outflows)
        if choice in [9, basic_view.KILL_PHRASE]:
            using_program = False
    basic_view.print_loading("PROGRAM EXITED")


if __name__ =='__main__':
    run_user_interface()
