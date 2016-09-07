# finance_export.py
# by mankaine
# July 15, 2016

# Exports transactions entered to a .txt file specified by user.

import basic_view

import cashflow

from pathlib import Path

# handle_export_choice is called whenever a user wishes to export information to an 
# external .txt file. The net income, expense, and revenue values in finance_view 
# may not be calculated before files are exported, so handle+export_choice calls 
# these in order to maintain the values.
def handle_export_choice (
    inflows: cashflow.CashFlows, outflows: cashflow.CashFlows) -> None:
    '''Exports transactions within a year and month to a .txt file
    '''
    year, month = choose_timeframe(inflows, outflows)   
    if month == 0:
        basic_view.print_loading_newline("RETURNING TO MAIN MENU")
        return
      
    print("\nExporting {} {}".format(basic_view.MONTHS[month], year))
    
    setting_up_export = True
    while setting_up_export:
        file_location = file_to_export()
        prepare_export_view(inflows, outflows)
        view_export(inflows, outflows, year, month)
        export_to_file(inflows, outflows, file_location, month, year)
        setting_up_export = basic_view.binary_choice(
            "Continue exporting? ", False, '')
    
    basic_view.print_loading_newline("RETURNING TO MAIN MENU")

# Called in handle_export_choice. Returns the transactions within the integers
# that are returned (year and month, respectively)
def choose_timeframe (inflows: cashflow.CashFlows,
                      outflows: cashflow.CashFlows) -> (int, int):
    year = basic_view.view_years(
        inflows.cfs, outflows.cfs, "Years to export:")
    month = basic_view.view_months(
        year, inflows.cfs, outflows.cfs, "Months to export:")
    return year, month


# Prepares export
def prepare_export_view (inflows: cashflow.CashFlows, 
                        outflows: cashflow.CashFlows) -> None:
    '''Updates CashFlows object total
    '''
    inflows.update_cfs_total()
    outflows.update_cfs_total()
    
# Displays to user everything that will be exported
def view_export (
    inflows: cashflow.CashFlows, outflows: cashflow.CashFlows, year: int,
    month: int) -> str:
    '''Prints transaction and subtotals that will be exported
    '''
    net_in = inflows.return_total(year, month)
    net_out = outflows.return_total(year, month)

    _print_titles_to_export("{} {} Transactions".format(
    basic_view.MONTHS[month],year))
    
    _print_attribute_to_export("Savings")
    _print_transxs_to_export(inflows.cfs, year, month)
    _print_net_amt_to_export(net_in, "Revenues", '----------')
        
    _print_attribute_to_export("Spendings")
    _print_transxs_to_export(outflows.cfs, year, month)
    _print_net_amt_to_export(net_out, "Expenses", '----------')
    
    _print_net_amt_to_export(net_in - net_out, "Income", "==========")


def _print_titles_to_export(message: str) -> str:
    '''Returns the string necessary to export titles
    '''
    print("{:^80}\n{}".format(message, basic_view.LINE))


def _print_attribute_to_export(message: str) -> str:
    '''Returns the string necessary to export attribute names
    '''
    print(titles_to_export(message) + "\n{:10}{:30}{:25}{:10} {}\n{}".format(
        "Day", "Account", "Description", "Price", "Flow", basic_view.LINE))


def _print_net_amt_to_export (amt: float, name: str, end_line: str) -> str:
    '''Writes information representing total name and its price to a file
    '''
    print('Net {} {} {:3}{:7.2f}\n{:>76}'.format(name, 
        '.' * ( 66 - len(name) - 7), basic_view.CURRENCY, amt, end_line))    


def _print_transxs_to_export (cf_dict: dict, year: int, month: int) -> str:
    '''Displays all transactions to be exported
    '''
    if year in cf_dict:
        if month in cf_dict[year]:
            for transx in cf_dict[year][month]:
                if cf_dict[year][month][0]==transx:
                    _print_first_transx_to_export(transx)
                else:
                    _print_transx_to_export(transx)
    else:
        print("\n\n{:^80}\n\n".format("No entries"))


def _print_first_transx_to_export (transx: cashflow.CashFlow) -> str:
    print("{:2}        {:30}{:25}{:3}{:7.2f} {}".format(
        transx.day, transx.acct_name, transx.desc, 
        transx.currency, transx.price, 
        basic_view.CF_AS_STR[transx.is_sav]))


def _print_transx_to_export (transx: cashflow.CashFlow) -> str:
    '''Returns the string representing a transactions that is 
    not the first transaction in a list
    '''
    print("{:2}        {:30}{:25}{:10.2f} {}".format(
        transx.day, transx.acct_name, transx.desc, 
        transx.price, basic_view.CF_AS_STR[transx.is_sav]))


# SELECTING MONTH/YEAR TO EXPORT ##############################################
# Handled by basic_view.py

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
def export_to_file (inflows: cashflow.CashFlows, outflows: cashflow.CashFlows, 
                    file_name: str, month_to_export: int, year_to_export: int
                    ) -> '.txt file':
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
                inflows, outflows, export_file, month_to_export, year_to_export)
            except Exception as e:
                basic_view.print_loading("An Error has occurred")
                print(e, "\n")
            else:
                basic_view.print_loading("File successfully exported")
            finally:
                export_file.close()
                basic_view.print_loading("File successfully closed")
                print()


def write_transxs (inflows: cashflow.CashFlows, outflows: cashflow.CashFlows,
    export_file: 'file object', month_to_export: int, year_to_export: int) -> None:
    '''Writes data to a file
    '''
    net_in = inflows.return_total(year_to_export, month_to_export)
    net_out = outflows.return_total(year_to_export, month_to_export)
    
    export_file.write(titles_to_export("{} {} Transactions".format(
    basic_view.MONTHS[month_to_export],year_to_export)))
    
    export_file.write(attribute_to_export("Savings"))
    export_transxs(inflows.cfs, year_to_export, month_to_export, export_file)
    export_file.write(net_amt_to_export(net_in, "Revenues", '----------')) 
    
    export_file.write('\n')
    
    export_file.write(attribute_to_export("Spendings"))
    export_transxs(outflows.cfs, year_to_export, month_to_export, export_file)
    export_file.write(net_amt_to_export(net_out, "Expenses", '----------'))
    
    export_file.write(net_amt_to_export(
    net_in - net_out, "Income", "=========="))


def net_amt_to_export (amt: float, name: str, end_line: str) -> None:
    '''Writes information representing total name and its price to a file
    '''
    return '\nNet {} {} {:3}{:7.2f}\n{:>76}'.format(name, 
        '.' * ( 66 - len(name) - 7), basic_view.CURRENCY, amt, end_line)    


def titles_to_export(message: str) -> str:
    '''Returns the string necessary to export titles
    '''
    return "\n{:^80}\n{}".format(message, basic_view.LINE)


def attribute_to_export(message: str) -> str:
    '''Returns the string necessary to export attribute names
    '''
    return titles_to_export(message) + "\n{:10}{:30}{:25}{:10} {}\n{}".format(
        "Day", "Account", "Description", "Price", "Flow", basic_view.LINE)


def export_transxs (dict_cfs: dict, year: int, month: int, 
                    filename: 'file object') -> None:
    '''Writes a transaction to a file object
    '''
    if year in dict_cfs:
        if month in dict_cfs[year]:
            for transx in dict_cfs[year][month]:
                if dict_cfs[year][month][0] == transx:
                    filename.write(_format_first_transx(transx))
                else:
                    filename.write(_format_regular_transx(transx))
        else:
            filename.write("\n\n{:^80}\n\n".format("No entries"))
    else:
        filename.write("\n\n{:^80}\n\n".format("No entries"))


def _format_first_transx (transx: cashflow.CashFlow) -> str:
    '''Returns the string representing the first transaction in a list
    '''
    return "\n{:2}        {:30}{:25}{:3}{:7.2f} {}".format(
        transx.day, transx.acct_name, transx.desc, 
        transx.currency, transx.price, 
        basic_view.CF_AS_STR[transx.is_sav])


def _format_regular_transx (transx: cashflow.CashFlow) -> str:
    '''Returns the string representing a transactions that is 
    not the first transaction in a list
    '''
    return "\n{:2}        {:30}{:25}{:10.2f} {}".format(
        transx.day, transx.acct_name, transx.desc, 
        transx.price, basic_view.CF_AS_STR[transx.is_sav])
