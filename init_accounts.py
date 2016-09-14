# init_accounts.py 
# by mankaine
# September 12, 2016

# Executed during the initialization of the main_menu module. This module will open a file containing Account data and 
# populate a list of Accounts with the data saved to that file.  

from cashflow import CashFlow
from account import Account
from pathlib import Path
from basic_view import print_loading
from ast import literal_eval

class TransDocDNEError(Exception):
    pass

FILE_NAME = ''

# Module's entry point. Only public function.
def main(accts: [Account]) -> None:
    '''Executes main module of the function - imports a document 
    with info containing Accounts and then saves that info to memory
    '''
    accts = []                                                                  # Cleared to prevent duplications 
                                                                                # upon using Budget Analysis multiple times
    print_loading("Preparing Budget Analysis")
    try: 
        a = _valid_file(accts)
        print_loading("Ready")
        return a 
    except Exception as e:
        print(("An error occurred: {}. \n",                             
              "Your Account history during this session has been",
              "cleared").format(e))
        

def _valid_file(accts: [Account]) -> None:
    '''Determines if the FILE_NAME constant is a valid document to import
    Account history from
    '''
    filepath = Path(FILE_NAME)
    if (filepath.exists() and not filepath.is_dir() \
    and filepath.suffix == '.txt'):
        return _import_accts(filepath, accts)                                   # Passed to finance_budget_menu
                                                                                #     result combined with Account
    else:
        raise TransDocDNEError


def _import_accts(filepath: Path, accts: [Account]) -> None:
    '''Retrieves information from a 
    '''
    with filepath.open() as opened_file:
        acct_info = opened_file.read()                                          # Retrieve information
        new_accts = _create_accts(accts, acct_info)                             # Break imported data into data structures 
        opened_file.close()                                                     # Close
        
        return new_accts                                                        # Passed to _valid_file
        
def _create_accts(accts: [Account], acct_info: str) -> None:
    '''Sorts data 
    '''
    accts_list = acct_info.split("ACCOUNTx")
    del accts_list[0]
    for acct in accts:
        accts.append(_new_acct(acct))
    return accts                                                                # Passed to _import_accts
        
        
def _new_acct(acct: dict) -> Account:
    '''Returns a new Account object after parsing the dictionary parameter
    '''
    imp_acct = literal_eval(acct)                                               # Convert str to dict, then save as imported Account
    new_acct = Account()                                                        # New Account instance - will be populated
    
    new_acct.update_savings_value(imp_acct["is_sav"])
    new_acct.update_name(imp_acct["name"])
    
    new_transxs = []                                                            # To be filled by transactions
    for year in imp_acct["budgets"]:                                             
        for month in imp_acct["budgets"][year]:
            imp_acct_tf = imp_acct["budgets"][year][month]                      # For convenience - tf stands for timeframe
            
            for cf in imp_acct_tf["acct_transxs"]:
                new_transxs.append(_new_transx_from_dict(cf))

            new_acct_tf = new_acct.budgets[month][year]                         # Also for convenience
            
            new_acct.fill_transxs(new_transxs)                                  # Creates dictionaries of months 
            new_acct_tf.budget = imp_acct_tf["budget"]
            new_acct_tf.reached = imp_acct_tf["reached"] 
            new_acct_tf.remain = imp_acct_tf["remain"]
            new_acct_tf.perc_remain = imp_acct_tf["perc_remain"] 
            new_acct_tf.perc_reached = imp_acct_tf["perc_reached"]
    return new_acct                                                             # Passed to _create_accts
    
    
def _new_transx_from_dict(cf: dict) -> CashFlow:
    '''Returns new CashFlow object with information provided from dict argument
    '''
    new_cf = CashFlow()
    new_cf.update_year(cf["year"])
    new_cf.update_month(cf["month"])
    new_cf.update_day(cf["day"])
    new_cf.update_date()
    new_cf.update_acct(cf['acct_name'])
    new_cf.update_desc(cf['desc'])
    new_cf.update_cash_flow_direction(cf["is_sav"])
    new_cf.update_curr(cf['currency'])
    new_cf.update_price(cf['price'])
    return new_cf                                                               # Passed to _new_acct
