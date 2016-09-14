# save_cashflows.py 
# by William Khaine
# September 12, 2016

# Executed with the close of the program. Exports all data to a txt file with the information regarding Accounts and CashFlows.

from cashflow import CashFlow, CashFlows
from init_cashflows import FILE_NAME

IMPORT_LOCATION = FILE_NAME
OUTERDIV = 'CFSOx'                                                              # Divider between CashFlows
INNERDIV = "SPLTHR"                                                             # Divider between CashFlow attributes    


def main (inflows: CashFlows, outflows: CashFlows) -> None:                     # called in main_menu.py
    '''Combines CashFlow information into one string, then exports it
    '''
    in_cfs_str = _cfs_str(inflows.cfs)
    in_net_str = _net_str(inflows.total)
    out_cfs_str = _cfs_str(outflows.cfs)
    out_net_str = _net_str(outflows.total)
    export_str = in_cfs_str + in_net_str + out_cfs_str + out_net_str
    
    export_file = open(IMPORT_LOCATION, "w")
    try:
        export_file.write(export_str)
    except Exception as e:
        print("This happened:{}. Nothing was saved.\n\ngg\n".format(e))
    else:
        print("Your session has been saved.")
    finally:
        export_file.close()
    

def _cfs_str (transxs: 'CashFlows.cfs') -> str:                                 # Called by main
    '''Returns the string necessary for initializer to consider a CashFlows's
    cfs attribute
    '''
    export_str = OUTERDIV + INNERDIV + '{'
    year_num = len(transxs) - 1
   
    for year in transxs:                                                        # Year Level 
        export_str += (str(year) + ": {")
        
        month_num = len(transxs[year]) - 1                                      # Month Level
        for month in transxs[year]:
            export_str += (str(month) + ": [")
            
            cf_num = len(transxs[year][month]) - 1                              # Transaction Level
            for cf in transxs[year][month]:
                export_str += cf_str(cf)
                if cf_num > 0:                                                  # same meter pattern used as in save_accounts
                    export_str += ','
                cf_num -= 1
            
            export_str += ']'
            if month_num > 0:
                export_str += ','
            month_num -= 1
            
        export_str += '}'
        if year_num > 0:
            export_str += ','
        year_num -= 1
        
    export_str += '}'
    return export_str
    

def cf_str(transx: CashFlow) -> str:
    '''Returns the string necessary for initializer to consider a CashFlow 
    object
    '''
    timeframe = '"year":{},"month":{},"day":{},'.format(
        transx.year, transx.month, transx.day)
    desc_and_acct = '"acct_name":"{}","desc":"{}","is_sav":{},'.format(
        transx.acct_name, transx.desc, transx.is_sav)
    curr_and_price = '"currency":"{}","price":{}'.format(
        transx.currency, transx.price)
    return '{' + timeframe + desc_and_acct + curr_and_price + '}' 
    

def _net_str (total: 'CashFlows.total') -> str:                                 # Called by main
    '''Returns the string necessary for initializer to consider a net total
    of a CashFlows object 
    '''
    return "{}{:.2f}".format(INNERDIV, total)
