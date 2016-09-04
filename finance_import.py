# finance_import.py
# by mankaine
# August 2, 2016

# User interface module that allows the user to import a .txt file containing 
# information about transactions and record them into the collections 
# of transactions.

# When a user chooses the option to import transactions from the main_menu, 
# command is given to handle_import_choice. It prompts the user to enter a 
# .txt file location to import, and prompts so until a valid one is provided.
# The user will enter information as to whether to edit, and will be shown
# the transactions to confirm. The user can then import another file,
# repeating the procedure, or return to the main menu. 
import cashflow
import basic_view
import finance_view
import finance_edit

import io
from pathlib import Path

MONTH_NAMES_TO_NUMBS = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12}


def handle_import_choice(
    inflows: cashflow.CashFlows, outflows: cashflow.CashFlows) -> None:
    '''Runs import section of Finance Program
    '''
    importing = True
    while importing:
        file_name = file_to_import() 
        if file_name == basic_view.KILL_PHRASE:
            break 
        elif basic_view.binary_choice("Import file? ", False, ''):
            year, month_name, temp_inflows, temp_outflows = _import_transxs(
            file_name)
            # temp_inflows and temp_outflows are directly imported from the .txt
            # file. They are added to inflows and outflows when all edits are 
            # complete.
            
            # View imported transactions
            finance_view.view_transxs(
                int(year), MONTH_NAMES_TO_NUMBS[month_name], temp_inflows.cfs, 
                temp_outflows.cfs) 
            if basic_view.binary_choice("\nEdit a transaction? ", False, ''):
 
                # Edit and display newly imported transactions
                temp_inflows, temp_outflows, _year_choice, _month_choice = edit_imported_transxs(
                    temp_inflows, temp_outflows)
            
            # Integrate temp_flows into permanent flows
            update_dicts(inflows, temp_inflows)
            update_dicts(outflows, temp_outflows) 
            
            importing = basic_view.binary_choice(
                    "Return to main menu? ", True, '')
        
        else:
            importing = basic_view.binary_choice(
                    "Return to main menu? ", True, '')
    basic_view.print_loading("RETURNING TO MAIN MENU")


# update_dicts is preferable to dict.update(dict) because the former preserves 
# both dictionary's values. While it returns nothing, it updates the original
# CashFlows objects that will be used by the rest of the Finance Program. It is 
# called after all transactions have been edited.
def update_dicts (
    orig_cfs: cashflow.CashFlows, temp_cfs: cashflow.CashFlows) -> None: ###***###
    '''Updates the first parameter dictionary with the second so that the 
    first parameter contains the transactions of the second
    '''
    if orig_cfs.cfs == {}:
        orig_cfs.cfs = temp_cfs.cfs
    elif temp_cfs.cfs == {}:
        return
    else:
        temp_year = list(temp_cfs.cfs.keys())[0]
        temp_month = list(temp_cfs.cfs[temp_year].keys())[0]
        
        for year in orig_cfs.cfs:
            if temp_year not in orig_cfs.cfs:
                orig_cfs.cfs[year] = {}
            if temp_month not in orig_cfs.cfs[temp_year]:
                orig_cfs.cfs[year][temp_month] = temp_cfs.cfs[year][temp_month]
            else:
                orig_cfs.cfs[year][temp_month].extend(
                temp_cfs.cfs[year][temp_month])
                    

# handle_import_choice calls edit_imported_transxs in order to edit, display, 
# and confirm transactions. The nature of this function bears strong 
# similarities to finance_edit's handle_edit_choice, meaning that 
# edit_imported_transxs calls multiple finance_edit functions. The significant 
# difference is that _year_choice and _month_choice are provided not by 
# prompting the user, but instead by the imported document, implemented by 
# define_year_and_month.
def edit_imported_transxs(
    temp_inflows: cashflow.CashFlows, temp_outflows: cashflow.CashFlows
    ) -> (cashflow.CashFlows, cashflow.CashFlows):
    '''Edits imported transactions and returns the CashFlows objects
    containing all imported transactions
    '''
    _year_choice, _month_choice = define_year_and_month(
    temp_inflows.cfs, temp_outflows.cfs)
    finance_edit.view_transxs(
    _year_choice, _month_choice, temp_inflows.cfs, temp_outflows.cfs)
    
    editing_transx = True
    while editing_transx:
        _inflow_len, _num_choice = finance_edit.select_transx_index(
            temp_inflows.cfs, temp_outflows.cfs, _year_choice, _month_choice)
        _transx = finance_edit.select_transx(temp_inflows.cfs, 
            temp_outflows.cfs, _year_choice, _month_choice, 
            _inflow_len, _num_choice)
        
        finance_edit.handle_edit(_transx)
        
        print("\nDisplaying edited transactions:")
        finance_edit.view_transxs(_year_choice, _month_choice, 
                                  temp_inflows.cfs, temp_outflows.cfs)
        editing_transx = basic_view.binary_choice(
                                    "\nEdit more transactions? ", False, '')
    return temp_inflows, temp_outflows, _year_choice, _month_choice
        

# To anticipate documents containing no Revenues and/or no Expenses 
# define_year_and_month lists various alternatives. If the dictionary 
# representing imported Expenses is empty, a tuple containing the temporary
# Revenues' year and month transactions is returned. Vice versa if the Revenues
# dictionary is empty. If both dictionaries are empty, the function returns 
# None and displays a message indicating that finding a year and date 
# is impossible.  
def define_year_and_month(inflow_dict: dict, outflow_dict: dict) -> (int, int):
    '''Returns a two integer tuple whose values are based on whether 
    the parameters are empty dictionaries
    '''
    if outflow_dict == {}:
        _year_choice = list(inflow_dict.keys())[0]
        _month_choice = list(inflow_dict[_year_choice].keys())[0]
        return _year_choice, _month_choice
    elif inflow_dict != {}:
        _year_choice = list(outflow_dict.keys())[0]
        _month_choice = list(outflow_dict[_year_choice].keys())[0]
        return _year_choice, _month_choice
    elif outflow_dict == inflow_dict:
        print("No transactions found in document")


# file_to_import does what it implies - returns the string representing the 
# filename after checking that its extension ends with .txt - i.e. it is a 
# .txt file - and that the file exists. The function calls upon 
# _valid_file_type to make this choice.
def file_to_import() -> str:
    '''Prompts user to enter a .txt file name until a valid one is provided
    '''
    file_searching = True
    while file_searching:
        file_name = input("\nSelect file to import: ").strip()
        if file_name == basic_view.KILL_PHRASE:
            return basic_view.KILL_PHRASE
        print("Searching for file...".format(file_name))
        file_path = Path(file_name)
        
        if _valid_file_type(".txt", file_name) and file_path.exists():
            print("File found")
            return file_name
        if not _valid_file_type(".txt", file_name):
            print(
            "File '{}' does not end with '.txt'. Try again".format(file_name))
        if not file_path.exists():
            print("File '{}' does not exist. Try again".format(file_name))
                
        
def _valid_file_type(extension: str, file_name: str) -> bool:
    '''Returns true if the second string ends with the first string
    '''
    return file_name.lower().endswith(extension)


# _import_transxs does the hard work of importing the information from the .txt
# file, converting it into a CashFlow object, and returning a CashFlows object
# containing all of those edited transactions. The program will signpost to the 
# user its progress as the imports continue. 
# 
# Of special note is:
#     1. The encoding. ASCII encoding breaks the program whenever unanticipated
#        code is implemented; utf-8 is more comprehensive.
#     2. The series of if statements in the for loop. The first series of if 
#        statements tell the program that if the line imported is a subtotal 
#        line, or a line 
#        for the sake of design, it shouldn't be considered. 
#     3. The else statement hard-codes the cash flow sign index in the line and
#        adds the transactions into a temporary CashFlows object.

def _import_transxs(file_name: str) -> (int, str, cashflow.CashFlows, 
                                        cashflow.CashFlows):
    '''Imports file information and, line by line, adds them into a collection
    of transactions
    '''
    inflow_list, outflow_list = ([], [])
    temp_inflows, temp_outflows = (cashflow.CashFlows(), cashflow.CashFlows())

    basic_view.print_loading_newline("Importing transactions")
    
    try:
        basic_view.print_loading_newline("Opening and reading files")
        with io.open(file_name, "r", encoding="utf-8") as file_imported:
            imported_lines = file_imported.readlines()
            try:
                title = imported_lines[1].split()
                month_name, year = title[0], title[1]

                for line in imported_lines: 
                    if _contains_reject_condition(line):
                        continue
                    else:
                        new_cf = _to_CF_from(line, month_name, year)
                        if line[76] == "+":
                            temp_inflows = handle_new_cf(
                                            inflow_list, new_cf, temp_inflows)
                        elif line[76] == "-":
                            temp_outflows = handle_new_cf(
                                        outflow_list, new_cf, temp_outflows)                            
                return year, month_name, temp_inflows, temp_outflows
            except Exception as e:
                print(
                "An error has occurred while reading the file: {}".format(e))
            finally:
                file_imported.close()
    except Exception as e:
        print("An error occurred while opening the file: {}".format(e))
    finally:
        basic_view.print_loading_newline("File Closed")
    

# Return value used to determine how to process line
def _contains_reject_condition(line: str) -> bool:
    '''Returns True if the line contains a condition that marks it as not 
    a transaction. False otherwise.
    '''
    return "Transactions" in line \
            or "Net Income" in line \
            or "Net Expenses" in line \
            or "Net Revenues" in line \
            or "----------" in line \
            or "==========" in line \
            or "Savings" in line \
            or "Spendings" in line \
            or "Day" in line \
            or "Account" in line \
            or "Flow" in line \
            or "Description" in line \
            or "Price" in line \
            or "No entries" in line \
            or basic_view.LINE == line \
            or '\n' == line \
            or line.strip() == ""


# Only the first item in the Revenues and Expenses list contain a 
# currency sign, meaning that before being integrated into a CashFlows object,
# a CashFlow object needs to confirm its currency. Since handle_new_cf is 
# called every time the program realizes a new transaction is to be imported 
# into memory, the new transaction will be appended to a list. The program adds
# the currency of the first item of the list to the last item of this list, the
# new transaction - and then returns the list.  
def handle_new_cf(cf_list: [cashflow.CashFlows], cf: cashflow.CashFlow, 
                  cfs: cashflow.CashFlows) -> cashflow.CashFlows:
    '''Implements a CashFlow object into a CashFlows object
    '''
    cf_list.append(cf) # list to be used to edit currency values
    cf_list = _fix_currency(cf_list)
    cfs.insert_cfs(cf_list)
    return cfs


def _fix_currency(elements: [cashflow.CashFlow]) -> [cashflow.CashFlow]:
    '''Revises a list of CashFlow objects so that all elements of the 
    list contain a currency symbol attribute
    '''
    if elements[-1].currency == ' ': # or element.currency == '':
        print("Converting currency symbols")
        elements[-1].currency = elements[0].currency
    return elements
        

# _to_CF_from, given a month and year of a transaction, converts a line 
# of text representing a transaction into a CashFlow object. If an error 
# is raised in the process, the program will overlook the object entirely 
# - the user will have to update the object in edits.
def _to_CF_from(
    read_line: str, month_name: str, year: str) -> cashflow.CashFlow:
    '''Converts a string representing transactions into a CashFlow object.
    Returns such an object.
    '''
    new_CF = cashflow.CashFlow()
    try:
        _convert_str_to_date(new_CF, read_line, month_name, year)
        _convert_str_to_acct(new_CF, read_line)
        _convert_str_to_desc(new_CF, read_line)
        _convert_str_to_price(new_CF, read_line) 
        _convert_str_to_curr(new_CF, read_line)
        _convert_str_to_cf_dirx(new_CF, read_line) 
        return new_CF 
    except Exception as e:
        print("An error has occurred: {}".format(e), 
              "\nUnable to construct CashFlow object", 
              "\nMoving on to constructing new CashFlow object")
        pass


def _convert_str_to_date(cf: cashflow.CashFlow, read_line: str,
                         month_name: str, year: str) -> None:
    '''Converts strings representing date, month, and year of a 
    transaction to day, month, and year attributes of a CashFlow object
    '''
    try:
        cf.update_day(read_line[0:10].strip())
        cf.update_month(MONTH_NAMES_TO_NUMBS[month_name])
        cf.update_year(year)
    except Exception as e:
        print("An error occurred in determining date: {}".format(e)) 
        
    
# Text Conversion
def _convert_str_to_acct(cf: cashflow.CashFlow, read_line: str) -> None:
    '''Converts strings representing an account as an attribute
    of a CashFlow object
    '''
    try:
        cf.update_acct(read_line[10:40].rstrip())
    except Exception as e:
        print("An error occurred in determining account name: {}".format(e))


def _convert_str_to_desc(cf: cashflow.CashFlow, read_line: str) -> None:
    '''Converts strings representing a description as an attribute of
    a CashFlow object
    '''
    try:
        cf.update_desc(read_line[40:65].rstrip())
    except Exception as e:
        print("An error occurred in determining description: {}".format(e))


# Price Conversion
def _convert_str_to_curr(cf: cashflow.CashFlow, read_line: str) -> None:
    '''Converts strings representing a currency as an attribute of
    a CashFlow object
    '''
    curr = read_line[65].strip()
    if curr != '':
        try:
            cf.update_curr(curr)
        except Exception as e:
            print("An error occurred in determining currency: {}".format(e))


def _convert_str_to_price(cf: cashflow.CashFlow, read_line: str) -> None:
    '''Converts strings representing a price as an attribute of
    a CashFlow object
    '''
    try: 
        cf.update_price(read_line[66:76].strip())
    except Exception as e:
        print("An error has occurred in determining price: {}".format(e))


# Cash Flow Conversion
def _convert_str_to_cf_dirx(cf: cashflow.CashFlow, read_line: str) -> None:
    '''Converts strings representing a cash flow direction as an attribute of
    a CashFlow object
    '''
    STR_AS_CF = {'+': True, '-': False}
    try: 
        cf.update_cash_flow_direction(STR_AS_CF[read_line[76]])
    except Exception as e:
        print(
        "An error has occurred in determining cash flow direction: {}".format(
                                                                        e))
