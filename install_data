# init_cashflows.py 
# by mankaine
# September 12, 2016

# Executed during the initialization of the main_menu module. This module will pull from all the data created from previous 
# transactions, and populate the Finance Program with Account and CashFlow data. 

from cashflow import CashFlow, CashFlows
from pathlib import Path
from basic_view import print_loading
from ast import literal_eval

class TransDocDNEError(Exception):
    pass

FILE_NAME = ''

def main(inflows: CashFlows, outflows: CashFlows) -> None:                      # Called in main_menu.py.
    '''Imports transactions 
    '''
    print_loading("Initializing")           
    try:
        _populate_cfs(inflows, outflows, FILE_NAME)                             # CashFlows are otherwise empty 
    except TransDocDNEError:
        print("Initialization document missing.\n",
              "Transaction history will begin as",
              "empty upon completed initialization")
    print_loading("Initialization Complete")


# Calls _execute_import, containing a list 
def _populate_cfs (
    inflows: CashFlows, outflows: CashFlows, file_name: str) -> None:
    '''Populates CashFlow objects with transactions, but raises 
    Exceptions upon error
    '''
    file_path = Path(file_name)
    if (file_path.exists() and not file_path.is_dir() \
        and file_path.suffix == '.txt'):                                        # Import only works for .txt files
        try: 
            in_t, in_n, out_t, out_n = _execute_import(file_path)
            _update_cfs(inflows, in_t, in_n)
            _update_cfs(outflows, out_t, out_n)
        except Exception as e:
            print("An error occured during initialization\n" + str(e),
                  "\nTransaction history will begin as",
                  "empty upon completed initialization")
    else:
        raise TransDocDNEError()
    

# Passes value to be used in _populate_import
def _execute_import (file_path: Path) -> [dict, float, dict, float]:
    '''Imports data and converts it to appropriate data types
    '''
    # Import
    with file_path.open() as opened_file: 
        cf_info = opened_file.readlines()                                       # Retrieve information
        opened_file.close()
        
        result = ''                                                             # Join information
        in_t_str, in_net_str, out_t_str, out_net_str = _sort_import_doc(
            result.join(cf_info))
        
        in_transxs = literal_eval(in_t_str)                                     # Creating elements
        in_net = literal_eval(in_net_str)
        out_transxs = literal_eval(out_t_str)
        out_net = literal_eval(out_net_str)
        return in_transxs, in_net, out_transxs, out_net                         # Passed to _popualte_cfs
                

def _sort_import_doc (cf_info: str) -> [str]:
    '''Splits imported text according to CashFlows and its attributes
    '''
    imported_split = (cf_info.split("CFSOx"))                                   # Indicates new CashFlows object
    inf_data, outf_data = imported_split[1], imported_split[2]
    in_t, in_net = _remove_empty_elem(inf_data.split("SPLTHR"))                 # Indicates new CashFlow attribtue
    out_t, out_net = _remove_empty_elem(outf_data.split("SPLTHR"))              # Above was for inflow, this for outflow
    return in_t, in_net, out_t, out_net                                         # Passed to _execute_import


def _remove_empty_elem (str_list: [str]) -> [str]:
    '''Removes all strings which are empty
    '''
    result = []
    for elem in str_list:
        if elem != '':
            result.append(elem)
    return result                                                               


def _update_cfs(CFS: CashFlows, transxs: dict, total: float) -> None:
    '''Updates a CashFlows' attributes with newly imported data
    '''
    CFS.update_total(total)                                                     # Initialize Total

    for year in transxs:                                                        # Initialize Transactions
        CFS.cfs[year] = {}                                                      # Sets up append to CFS in _update_cf
        for month in transxs[year]:
            CFS.cfs[year][month] = []                                           # Sets up append to CFS in _update_cf
            for cf in transxs[year][month]:
                _update_cf(CFS, cf, year, month)
                

def _update_cf (
    CFS: CashFlows, cf: 'dict value', year: int, month: int) -> None:
    '''Initializes Cash Flow
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
    CFS.cfs[year][month].append(new_cf)
