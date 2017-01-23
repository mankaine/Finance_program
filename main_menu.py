# main_menu.py
# Script to execute Finance Program in Command Line.  

import trans_entry
import trans_view
import trans_edit
import account_init
import account_edit 
import account_view
import account_analysis
import initialize
import save 
import basecui as bc
import os 

# Initialiation of variables 
data_file_str="data.txt"
menu = """
MAIN MENU
========================================
    [ntr]    : Enter Transactions
    [edt]    : Edit Transactions  
    [vts]    : View Transactions
    [eda]    : Edit Accounts
    [vwa]    : View Accounts
    [ana]    : Analyze Accounts 
    [esc]    : Exit menu
"""

# Script
# Ensure file exists
if not os.path.isfile(data_file_str): 
    data_file = open(data_file_str, "w")
    data_file.close()  
variables, accounts, transactions_dirty=initialize.main(data_file_str)
transactions = bc.remove_duplicates(transactions_dirty) # Remove impure Transactions (duplicates)

# Menu looping 
while True: 
    print(menu)
    try: 
        choice = input("Your choice: ").rstrip()
        if choice == "ntr":
            transactions += trans_entry.main()
            # Add data to Account objects
            accounts_t=(account_init.create_from(transactions))
            # Account for duplicate Accounts created from Transactions 
            accounts=account_init.merge_accounts(accounts_t + accounts)
        elif choice == "edt":
            trans_edit.main(transactions, accounts)
            # Many Accounts may be updated
            for a in accounts: 
                a.update_all_reached()
        elif choice == "vts":
            trans_view.main(transactions)
        elif choice == "eda":
            account_edit.main(accounts)
        elif choice == "vwa":
            account_view.main(accounts)
        elif choice == "ana":
            account_analysis.main(accounts)
        elif choice == "esc":
            break
        else:
            raise ValueError("Choice {} unacceptable. Try again.".format(choice))
    except ValueError as e:
        print("    An error has occurred: {}".format(e))
    except Exception as e:
        print("    Fatal Error: {}".format(e)) 

# Saving Data 
save.main(transactions, accounts, variables, data_file_str)