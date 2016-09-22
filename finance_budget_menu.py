# finance_budget_menu.py
# by mankaine  
# August 11, 2016

# Menu module of budget option, selected from main menu


import finance_budget_edit
import finance_budget_view_one_month
import finance_budget_view_all_months
from account import Account, Budget_Info
import basic_view
from cashflow import CashFlows
import pprint
import init_accounts
import save_accounts


budget_menu = '''BUDGET MENU:
1. Edit account budgets
2. View budget of one month
3. Compare budgets of multiple months
4. Return to main menu
'''


def handle_budget_choice(inflows: CashFlows, outflows: CashFlows) -> None:      # Called from main_menu module.
    '''Handles user's decision to view and edit budgets
    '''    
    budgeting = True
    
    accts_coll = _create_acct_coll(inflows, outflows)
    
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


def _create_acct_coll(inflows: CashFlows, outflows: CashFlows) -> [Account]:
    '''Returns a list of Accounts
    '''
    sorted_in = _separate_by_name(inflows) 
    sorted_out = _separate_by_name(outflows)
    unique_sort = _sort_cfs(sorted_in, sorted_out)                              # Merge duplicates
    ntrd_accts = _create_acct_list(unique_sort)
    imptd_accts = init_accounts.main()                                          
    return _merge_acct_lists(ntrd_accts, imptd_accts)                           # Merge duplicates
                                                                                #     Value passed to handle_budget_choice as 
                                                                                #     accts_coll
def _separate_by_name (cfs: CashFlows) -> dict:
    '''Returns a dict of unique Account names
    '''
    dict_accts = {}
    for year in cfs.cfs:
        for month in cfs.cfs[year]:
            for cf in cfs.cfs[year][month]:
                if cf.acct_name not in dict_accts:
                    dict_accts[cf.acct_name] = [cf]
                else:
                    dict_accts[cf.acct_name].append(cf)
    return dict_accts                                                           # Keys: Account names
                                                                                #     Values: CashFlows with acct_name = Key
                                                                                #     Passed to _merge_acct_dicts         
def _sort_cfs (acct_data1: dict, acct_data2: dict) -> dict:
    '''Merges those accounts which have the same name
    '''
    merged_data = {}
    
    for acct_name in acct_data1:                                                # inflows = acct_data1, outflows = acct_data2
        if acct_name in acct_data2:                                             # Prevents duplicate accounts
            acct_data1[acct_name].extend(acct_data2[acct_name])
        merged_data[acct_name] = acct_data1[acct_name]                          # Account name is unique to inflows
        
    for acct_name in acct_data2:                                                # First loop does not include uniquely outflow
        if acct_name not in merged_data:                                        #     accounts
            merged_data[acct_name] = acct_data2[acct_name]
        
    return merged_data                                                          # Passed to _create_acct_list


def _create_acct_list (acct_transxs: dict) -> [Account]:                        # Called in handle_budget_choice
    '''Creates a list of Accounts, containing sorted transactions and 
    names
    '''
    if acct_transxs != {}:                                                      # Check if transactions entered
        accts = []                      
        for acct_name in acct_transxs:
            acct = Account()
            acct.update_name(acct_name)
            if acct_transxs[acct_name] != None:                                 # Prevents TypeError when calling acct.fill_transxs
                acct.fill_transxs(acct_transxs[acct_name]) 
            accts.append(acct)
        return accts                                                            # Passed to menu options as ntrd_accts
    else:
        return []


def _merge_acct_lists (accts1: [Account], accts2: [Account]) -> [Account]:
    '''Returns a list of Accounts that have been merged
    '''
    merged_accts = []                                                           # Start clean; this is the structure to be returned
    for acct in accts2:                                                         # accts2 is more likely to be larger (more sessions)
        acct_or_none = _find_duplicate(acct.name, accts1)                       #     - it will catch more duplicates 
        if type(acct_or_none) == Account:                                       
            merged_accts.append(_merge_transx_dicts(acct, acct_or_none))        
        else:
            merged_accts.append(acct)
    merged_accts.extend(accts1)                                                 # Above loop doesn't include new transactions
    return merged_accts
            
    
def _find_duplicate (acct_name: str, acct_coll: [Account]) -> Account or None:
    '''Returns the Account that has the same name as another, or None if no 
    case of this occurs 
    '''
    result = None
    for acct in acct_coll:
        if acct_name.strip() == acct.name.strip(): 
            result = acct                                                       # Either return value passed in _merge_acct_lists
    return result                                                               # Indicates that all accounts are unique      


def _merge_transx_dicts (acct1: Account, acct2: Account) -> Account:
    '''Merges transactions of both Accounts, and returns them in a 
    single Account object
    '''
    new_acct = Account()
    new_acct.name = acct2.name
    new_acct.budgets = acct2.budgets                                            # Populate with Account 2 data
            
    for year in acct1.budgets:                                                  # Populate with Account 1 data
        if year not in new_acct.budgets:
            new_acct.budgets[year] = {}
            for month in acct1.budgets[year]:
                if month not in new_acct.budgets[year]:
                    new_acct.budgets[year][month] = Budget_Info(
                        acct1.budgets[year][month].acct_transxs)
                else:
                    new_acct.budgets[year][month].budgets.extend(
                        acct1.budgets[year][month].acct_transxs)
    return new_acct
