# save_accounts.py 
# by mankaine
# September 13, 2016

# Executed when user decides to quit Finance Program. This module will pull 
# all Account data and save it to an external .txt file, which is what
# init_account calls during iniitalization to populate the Account list. 

from cashflow import CashFlow
from account import Account
from init_accounts import FILE_NAME
from save_cashflows import cf_str

EXPORT_LOCATION = FILE_NAME
OUTERDIV = "ACCOUNTx"


def main (accts: [Account]) -> None:                                            # Module's entry point
    '''Exports Account data to a .txt file
    '''
    export_data = _write_export_data(accts)
    file = open(EXPORT_LOCATION, 'w')
    try:
        file.write(export_data)
    finally:
        file.close()


def _write_export_data (accts: [Account]) -> str:
    '''Returns a string that will be exported
    '''
    export_str = ''                                                 
    
    for acct in accts:
        export_str += OUTERDIV + "{'budgets': {"                                # Dictionary on the Account level
        
        curr_year_ind = len(acct.budgets) - 1                                   # Dictionary exclusive to budgets
        for year in acct.budgets:                                               #      - on the year Level
            export_str += str(year) + ": {"
            
            curr_mo_ind = len(acct.budgets[year]) - 1                           # Dict exclusive to budgets - Month Level
            for month in acct.budgets[year]:
                export_str += str(month) + ": {"
                
                export_str += _str_budget_transxs(acct.budgets[year][month])    # Budget Values Level - called every time
                                                                                # for each transaction
                export_str += "}"               
                if curr_mo_ind > 0:
                    export_str += ', '                                          # Don't add a comma if it's the last key/pair 
                curr_mo_ind -= 1                                                # value in dict (i.e. value is 0)
                                                                                # Otherwise add comma and decrement value by 1                
            export_str += "}"                                                                                                                                   # otherwise add and decrement
            if curr_year_ind > 0:                               
                export_str += ', '
            curr_year_ind -= 1
        
        export_str += ('}, ' + _str_budget_name(
            acct.name) + _str_budget_sav(acct.is_saving) + '}')
    
    return export_str                                                           # Passed to main
    

def _str_budget_name(name: str) -> str:    
    '''Returns a string, formatted as a key/value pair, of an Account's name
    '''
    return '"name" : "' + name + '",'

def _str_budget_sav(is_sav: bool) -> str:
    '''Returns a string, formatted as a key/value pair, describing if an
    Account is a saving
    ''' 
    return '"is_sav" : ' + str(is_sav)
    
# Budget_Info is a tuple found in Account.
def _str_budget_transxs(data: 'Budget_Info') -> str:
    '''Returns a string of formatted budget information
    from the Budget_Info tuple 
    '''
    budget_info_str = ""
    
    budget_info_str += '"acct_transxs": ' + _str_transxs_data(                  # Account Transaction
        data.acct_transxs) + ',' 
    budget_info_str += '"budget" : ' + str(data.budget) + ', '                  # Budget 
    budget_info_str += '"reached" : ' + str(data.reached) + ', '                # Reached 
    budget_info_str += '"remain" : ' + str(data.remain) + ', '                  # Remain 
    budget_info_str += '"perc_remain" : ' + str(data.perc_remain) + ', '        # Percent Remaining  
    budget_info_str += '"perc_reached" : ' + str(data.perc_reached)             # Percent Reached
        
    return budget_info_str                                                      # Passed to _write_export_data


def _str_transxs_data(transxs: [CashFlow]) -> str:
    '''Returns a string of transactions, formatted for exporting
    '''
    str_transxs = "["
    
    transx_ind = len(transxs) - 1
    for transx in transxs:                                                      
        str_transxs += cf_str(transx)                                           # Creates transaction dict
        if transx_ind > 0:
            str_transxs += ', '
        transx_ind -= 1
    
    str_transxs += "]"
    
    return str_transxs
