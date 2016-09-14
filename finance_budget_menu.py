# finance_budget_menu
# By mankaine
# August 11, 2016

# Menu module of budget option, selected from main menu


import finance_budget_edit
import finance_budget_view_one_month
import finance_budget_view_all_months
import account
import basic_view
import cashflow

import init_accounts
import save_accounts


budget_menu = '''BUDGET MENU:
1. Edit account budgets
2. View budget of one month
3. Compare budgets of multiple months
4. Return to main menu
'''

# Called from main_menu module.
def handle_budget_choice(
    inflows: cashflow.CashFlows, outflows: cashflow.CashFlows) -> None:
    '''Handles user's decision to view and edit budgets
    '''    
    budgeting = True
    
    accts_coll = _create_acct_list(_separate_by_name(inflows, {}))
    accts_coll.extend(_create_acct_list(_separate_by_name(outflows, {})))
    accts_coll.extend(init_accounts.main(accts_coll))
    
    while budgeting:
        int_choice = basic_view.menu_input(budget_menu, 5)
        if int_choice == 1:
            basic_view.print_loading_newline("Editing account budgets")
            accts_coll = finance_budget_edit.edit_acct_budgets(
                        inflows, outflows, accts_coll)
        elif int_choice == 2:
            basic_view.print_loading_newline("Viewing budget of one month")
            finance_budget_view_one_month.view_acct_by_months(
                                        inflows, outflows, accts_coll)
        elif int_choice == 3:
            basic_view.print_loading_newline("Comparing budgets across time")
            finance_budget_view_all_months.view_acct_all_months(
                                        inflows, outflows, accts_coll)
        elif int_choice == 4:
            save_accounts.main(accts_coll)
            budgeting = False
    basic_view.print_loading_newline("RETURING TO MAIN MENU")


def _separate_by_name (cfs: cashflow.CashFlows, dict_accts: dict) -> dict:
    for year in cfs.cfs:
        for month in cfs.cfs[year]:
            for cf in cfs.cfs[year][month]:
                if cf.acct_name not in dict_accts:
                    dict_accts[cf.acct_name] = [cf]
                else:
                    dict_accts[cf.acct_name].append(cf)
    return dict_accts                                                           # Keys: Transaction name accounts
                                                                                # Values: Transactions with those account names
                                                                                # Passed to _create_acct_list         
    

def _create_acct_list (acct_transxs: dict) -> [account.Account]:                # Called in handle_budget_choice
    '''Creates a list of Accounts, containing sorted transactions and names
    '''
    accts = []                      
    for acct_name in acct_transxs:
        acct = account.Account()
        acct.update_name(acct_name)
        acct.fill_transxs(acct_transxs[acct_name]) 
        accts.append(acct)
    return accts            
