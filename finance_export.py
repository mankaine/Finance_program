# finance_export
# By mankaine
# July 15, 2016

# Exports transactions entered to a .txt file specified by user.

import finance_view
import basic_view

import cashflow

from pathlib import Path

# handle_export_choice is called whenever a user wishes to export information to an 
# external .txt file. The net income, expense, and revenue values in finance_view 
# may not be calculated before files are exported, so handle+export_choice calls 
# these in order to maintain the values.
def handle_export_choice (
        pcf: cashflow.CashFlows, ncf: cashflow.CashFlows) -> str and '.txt':
    '''Exports transactions within a year and month to a .txt file
    '''     
    year_to_export = basic_view.view_years(
        pcf.cfs, ncf.cfs, "Years to export:")
    month_to_export = basic_view.view_months(
        year_to_export, pcf.cfs, ncf.cfs, "Months to export:")
     
    print("\nExporting {} {}".format(
        basic_view.MONTHS[month_to_export], year_to_export))
    
    setting_up_export = True
    while setting_up_export:
        file_location = file_to_export()
                
        pcf.update_cfs_total()
        ncf.update_cfs_total()

        finance_view.view_transxs(
            year_to_export, month_to_export, pcf.cfs, ncf.cfs)
        print("Net total: {:.2f} - {:.2f} = {:.2f}\n".format(
            pcf.total, ncf.total, pcf.total - ncf.total))
        
        export_to_file(pcf.cfs, ncf.cfs, file_location, 
            month_to_export, year_to_export, pcf.total, ncf.total)
        
        setting_up_export = basic_view.binary_choice(
            "Continue exporting? ", False, '')
    
    basic_view.print_loading_newline("RETURNING TO MAIN MENU")


# SELECTING MONTH/YEAR TO EXPORT ##############################################
# Handled by the basic_view

# SELECTING FILE TO EXPORT TO #################################################
# Like many other functions, file_to_export will loop through many queries 
# until a valid one is provided. It returns that value, allowing 
# handle_export_choice to pass it through to export_to_file as the name of the 
# file that is created/overwritten in exporting transactions.
def file_to_export () -> str:
    '''Prompts user for a file name until a valid one is provided
    '''
    file_searching = True
    while file_searching:
        file_name = input("\nSelect file to export: ").strip()
        print("Determining if file is available...".format(file_name))
        file_path = Path(file_name)
    
        if file_path.exists():
            while True:
                ask_to_overwrite = input(
                    ("\n{} already exists. Overwrite? ".format(
                    file_path))).strip().lower()
                if ask_to_overwrite == 'yes':
                    return file_name
                elif ask_to_overwrite == 'no':
                    break
                else:
                    print(
                    "\n{} not an option. Enter either 'yes' or 'no'".format(
                    ask_to_overwrite))
        else:
            print("File is available".format(file_name))

            file_searching = basic_view.binary_choice(
                "Continue looking for an export location? ", False, '')
            if not file_searching:
                return file_name

 
# VIEWING TRANSACTIONS TO EXPORT ##############################################
# Handled by finance_view.

# EXPORTING TRANSACTIONS TO EXPORT ############################################
# export_to_file opens up the file and calls write_transxs in order to 
# successfully export. 
# 
# write_transxs call various functions to write formatted lines of code into
# the specified .txt file: export_net_amount, titles_to_export, a
# attributes_to_export, and export_transx.
#
# export_transx follows the same protocol as viewing a list of transactions
# in finance_view and finance_edit; the first transaction contains the
# currency symbol and all else don't. 
def export_to_file (pcf: dict, ncf: dict, 
                    file_name: str, month_to_export: int, year_to_export: int, 
                    net_rev: float, net_xps: float) -> '.txt file':
    '''Exports transactions in the lists to a specified .txt file
    '''
    if basic_view.binary_choice("Export? ", False, ''): 
        try:
            export_file = open(file_name, 'w')
        except:
            print('{} not an acceptable file name. Try again.'.format(file_name))
        else:
            try:
                basic_view.print_loading("File successfully opened")
                basic_view.print_loading("Exporting Information")
                                
                write_transxs(
                    pcf, ncf, export_file, month_to_export, year_to_export, 
                    net_rev, net_xps)
            except Exception as e:
                export_file.close()
                basic_view.print_loading("An Error has occured")
                print(e)
                print()
            else:
                basic_view.print_loading("File successfully exported")
            finally:
                export_file.close()
                basic_view.print_loading("File successfully closed")
                print()


def write_transxs (pcf: dict, ncf: dict, export_file: 'file object', 
    month_to_export: int, year_to_export: int, net_rev: float, 
    net_xps: float) -> None:
    '''Writes data to a file
    '''
    export_file.write(
        titles_to_export(
        "{} {} Transactions".format(
        basic_view.MONTHS[month_to_export],year_to_export)))
    
    export_file.write(attribute_to_export("Revenues"))
    export_transx(pcf, year_to_export, month_to_export, export_file)
    export_net_amount(net_rev, "Revenues", export_file, '----------') 
    
    export_file.write('\n')
    
    export_file.write(attribute_to_export("Expenses"))
    export_transx(ncf, year_to_export, month_to_export, export_file)
    export_net_amount(net_xps, "Expenses", export_file, '----------')
    
    export_net_amount(net_rev - net_xps, "Income", export_file, "==========")


def export_net_amount(amt: float, 
        name: str, file_name: str, end_line: str) -> None:
    '''Writes information representing total name and its price to a file
    '''
    file_name.write('\nNet {} {} {:3}{:7.2f}\n{:>76}'.format(name, 
        '.' * ( 66 - len(name) - 7), basic_view.CURRENCY, amt, end_line))    


def titles_to_export(message: str) -> str:
    '''Returns the string necessary to export titles
    '''
    return "\n{:^80}\n{}".format(message, basic_view.LINE)


def attribute_to_export(message: str) -> str:
    '''Returns the string necessary to export attribute names
    '''
    return titles_to_export(message) + "\n{:10}{:30}{:25}{:10} {}\n{}".format(
        "Day", "Account", "Description", "Price", "Flow", basic_view.LINE)


def export_transx (dict_of_cfs: dict, year: int, month: int, 
                  file_object: 'file object') -> None:
    '''Writes a transaction to a file object
    '''
    if year in dict_of_cfs:
        if month in dict_of_cfs[year]:
            for transx in dict_of_cfs[year][month]:
                if dict_of_cfs[year][month][0] == transx:
                    file_object.write(_format_first_transx(transx))
                else:
                    file_object.write(_format_regular_transx(transx))
    else:
        file_object.write("\n\n{:^80}\n\n".format("No entries"))


def _format_first_transx (transx: cashflow.CashFlow) -> str:
    '''Returns the string representing the first transaction in a list
    '''
    return "\n{:2}        {:30}{:25}{:3}{:7.2f} {}".format(
        transx.day, transx.acct_name, transx.desc, 
        transx.currency, transx.price, 
        basic_view.CF_AS_STR[transx.pos_cash_flow])


def _format_regular_transx (transx: cashflow.CashFlow) -> str:
    '''Returns the string representing a transactions that is 
    not the first transaction in a list
    '''
    return "\n{:2}        {:30}{:25}{:10.2f} {}".format(
        transx.day, transx.acct_name, transx.desc, 
        transx.price, basic_view.CF_AS_STR[transx.pos_cash_flow])
