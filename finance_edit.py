# finance_edit.py
# by mankaine
# July 12, 2016

# Implements user interface aspect that edits transaction.

import cashflow
import finance_entry
import basic_view


ATTRIBUTES = ['Date', 'Account', 'Description', 'Price', 'Flow']


# OutsideListRangeError is raised when a user enters a value representing
# a month or year to edit that is not been yet entered as having a transaction.
class OutsideListRangeError (Exception):
    pass


# INDIVIDUAL EDITING ##########################################################
# When a user decides to edit a transaction immediately after creating it, 
# handle_edit is called from the finance_entry module. While it does not return
# anything, the function updates the CashFlow class. 
def handle_edit (
    transx: cashflow.CashFlow, inflows: cashflow.CashFlows,
    outflows: cashflow.CashFlows) -> None:
    '''Displays and edits one transaction
    '''
    editing = True
    while editing:
        _attrib = _select_attrib(ATTRIBUTES, transx, inflows, outflows)
        _transx = _edit_transx(transx, _attrib)
        _view_edit(_transx)
        cashflow.update_cfs(inflows, outflows)
        editing = basic_view.binary_choice(
                                "\nEdit transaction again? ", False, '')


# EDITING MULTIPLE TRANSACTIONS ################################################
# handle_edit_choice is called in the main_menu module and displays the 
# transactions that can be edited, the updated transaction, and the updated list
# of transactions in the initially selected month and year.
def handle_edit_choice (inflows: cashflow.CashFlows, 
                        outflows: cashflow.CashFlows) -> None:    
    '''Displays revenues, expenses, and enables user to edit the attributes of
    the transactions one at a time
    '''
    cf = (inflows, outflows)
    
    year, month = choose_timeframe(cf[0], cf[1])    
    if month == 0:
        basic_view.print_loading_newline("RETURNING TO MAIN MENU")
        return
    
    view_transxs(year, month, cf[0].cfs, cf[1].cfs)
    
    editing_transx = True
    while editing_transx:
        pcf_len, num_choice = select_transx_index(
                                cf[0].cfs, cf[1].cfs, year, month)
        if pcf_len == num_choice and pcf_len == -1:
            basic_view.print_loading_newline("RETURNING TO MAIN MENU")
            return
        transx = select_transx(
            cf[0].cfs, cf[1].cfs, year, month, pcf_len, num_choice)
        
        handle_edit(transx, cf[0], cf[1])
        
        print("\nDisplaying edited transactions:")
        view_transxs(year, month, cf[0].cfs, cf[1].cfs)
        editing_transx = basic_view.binary_choice(
                                "\nEdit more transactions? ", False, '')


# Called to return year and month to view transactions to edit. Returns tuple
# representing (year, month) by integers
def choose_timeframe (inflows: cashflow.CashFlows,
                      outflows: cashflow.CashFlows) -> (int, int):
    year = basic_view.view_years(
        inflows.cfs, outflows.cfs, "Years to edit:")
    month = basic_view.view_months(
        year, inflows.cfs, outflows.cfs, "Months to edit:")
    return year, month


# CHOOSING THE TRANSACTION TO EDIT ############################################
# basic_view.view_years and basic_view.view_months are called in order to 
# allow the user to choose a month and year to focus in on. 

# After a month and year have been selected, a user must see which transactions
# to edit. This need is met by view_transxs, and _view_tansxs_formatted. The 
# former calls the latter to display a list of transactions, which is either 
# positive or negative cash flow.
def view_transxs (year: int, month: int, inflows: dict, outflows: dict) -> str:
    '''Displays possible transaction to edit within a year and month
    '''
    cf = (inflows, outflows)
    
    print("{} {} Transactions".format(basic_view.MONTHS[month], year))
    print(basic_view.LINE)
    _view_tranxs_formatted('Savings', year, month, cf[0], 0)
    print()
    
    pcf_len = transxs_in_month(year, month, cf[0])    
    _view_tranxs_formatted('Expenses', year, month, cf[1], pcf_len)
    
    # Note that for the Negative Cash Flow implementation of 
    # _view_tranxs_formatted, the length of the PCF dict is a parameter. 
    # This prevents two different transactions of earnings and spendings 
    # from having the same value. 
    
    
# view_transxs_formatted will display the attributes, and then then the index
# number, date, description, account, and price of each transaction in a list.
# For the sake of design, only the first transaction in the list has a currency 
# symbol.
def _view_tranxs_formatted (message: str, year: int, month: int, 
                            cfs_dict: dict, list_boost: int) -> str:
    '''Displays possible revenues to edit within a year and month
    '''
    print("{:^84}".format(message))
    print(basic_view.LINE + ("-" * 7))
    print(("\n{:5} {:10} {:28} {:24} {:10} {:4}").format("No.",
        "Date", "Account", "Description", "Price", "Flow"))
    print(basic_view.LINE + ("-" * 7))

    if year in cfs_dict:
        if month in cfs_dict[year]:
            cfs_dict[year][month].sort(key = lambda transx: transx.date) 
            for transx in cfs_dict[year][month]:
                transx_str = "{:3}. {:2}/{:2}/{:4} {:30}{:25}".format(
                        cfs_dict[year][month].index(transx) + 1 + list_boost, 
                        transx.month, transx.day, transx.year, transx.acct_name, 
                        transx.desc)
                if cfs_dict[year][month][0] == transx:
                    transx_str += "{:3}{:7.2f} {}".format(transx.currency, 
                        transx.price,
                        basic_view.CF_AS_STR[transx.is_sav])
                else:
                    transx_str += "{:10.2f} {}".format(transx.price, 
                        basic_view.CF_AS_STR[transx.is_sav])
                print(transx_str)
        else:
            print("\n{:^80}\n".format("No entries"))
    else:
        print("\n{:^80}\n".format("No entries"))


# handle_edit_choice calls select_transx_index to find not only the numbering
# of the transaction the user wishes to edit, but also the amount of positive 
# cash flow transactions entered. So, the function returns a tuple containing 
# these values, but only after the transactions are displayed.
#
# The function first determines the length of the revenues transactions, 
# and then prompts the user to enter a value representing the number order 
# of the transaction. select_transx passes these two numbers to select_transx,
# which returns the actual transaction selected.
def transxs_in_month (year: int, month: int, cfs: dict) -> int:
    '''Returns the length of the value of a dictionary's third dimension
    '''
    cf_amount = 0
    if year in cfs:
        if month in cfs[year]:
            cf_amount = len(cfs[year][month])
        else:
            cf_amount = 0
    else:
        cf_amount = 0
    return cf_amount


def select_transx_index (inflows: dict, outflows: dict, year: int, month: int
                         ) -> (int, int):
    '''Displays possible transaction to edit within a year and month, prompts 
    user to choose a transaction until a valid one is provided, and returns
    the transaction
    '''
    pcf_len = transxs_in_month(year, month, inflows)
    ncf_len = transxs_in_month(year, month, outflows)
    
    selecting_transx = True
    while selecting_transx:
        try: 
            number_choice_str = input("\nEnter number: ").strip()
            
            # User breaks out
            if number_choice_str == basic_view.KILL_PHRASE:
                return -1, -1
            
            # Conversion
            chosen_num = int(number_choice_str)
            if 1 > chosen_num or (pcf_len + ncf_len) < chosen_num:
                raise OutsideListRangeError()
             
        except ValueError:
            print("{} not an integer. Try again.".format(number_choice_str))
        except OutsideListRangeError:
            print("{} outside of the range 1 to {}. Try again.".format(
                chosen_num, pcf_len + ncf_len))
        else:
            # Break out of loop, return the number of inflows and index of 
            # user's choice in listed transactions
            selecting_transx = False
            return pcf_len, chosen_num
        
        
def select_transx (pcfs: dict, ncfs: dict, year: int, 
                    month: int, pcf_len: int, num_choice: int
                    ) -> cashflow.CashFlow:
    '''Returns a transaction based on indexed number
    '''
    transx_ind = num_choice - 1 
    
    # User selects Inflow
    if pcf_len > 0 and transx_ind <= pcf_len - 1:
        return pcfs[year][month][transx_ind]
    
    # User selects Outflow and Inflows are recorded 
    elif 0 <= pcf_len - 1 < transx_ind:
        return ncfs[year][month][transx_ind - pcf_len]
    
    # User selects Outflow without Inflows recorded 
    elif pcf_len == 0:
        return ncfs[year][month][transx_ind]
     

# CHOOSING WHAT TO EDIT #######################################################
# Now that the transaction has been chosen, the program must figure out how to 
# edit it. It requests the user to answer this question, and passes the answer
# to _edit_transx, where individual functions edit, update, and revise the 
# values specified.
def _select_attrib (
    attribs: [str], transx: cashflow.CashFlow, inflows: cashflow.CashFlows,
    outflows: cashflow.CashFlows) -> str:
    '''Displays possible attributes to edit, and returns the string 
    representing the attribute
    '''
    selecting_attrib = True
    while selecting_attrib:
        attrib_str = input(
        "Enter attribute to edit (type in 'Delete' to remove transaction): "
        ).strip()
        if attrib_str == basic_view.KILL_PHRASE:
            basic_view.print_loading_newline("Returning to previous state")
            break
        elif attrib_str == "Delete":
            choice = basic_view.binary_choice(
            "Are you sure you want to delete this transaction? ", False, "")
            if choice:
                _delete_transx(transx, inflows, outflows)
                break
        elif attrib_str.title() not in attribs:
            print("{} not an option. Select one of the following: {}.".format(
                                                    attrib_str, ATTRIBUTES)) 
        else:
            return attrib_str.title()


def _delete_transx(
    transx: cashflow.CashFlow, inflows: cashflow.CashFlows, 
    outflows: cashflow.CashFlows) -> None:
    '''Deletes a transaction from a CashFlows object
    '''
    if transx.is_sav:
        inflows.cfs[transx.year][transx.month].remove(transx)
    else:
        outflows.cfs[transx.year][transx.month].remove(transx)


def _edit_transx (transx: cashflow.CashFlow or cashflow.CashFlow,
                 attrib: str) -> cashflow.CashFlow:
    '''Edits the attribute appropriate to the transaction
    '''
    print()
    
    if attrib == 'Date':
        _edit_date(transx)
    elif attrib == 'Account':
        _edit_acct(transx)
    elif attrib == 'Description':
        _edit_desc(transx)
    elif attrib == 'Price':
        _edit_price(transx)
    elif attrib == 'Flow':
        _edit_flow(transx)        
    return transx


# EDITING THE TRANSACTION #####################################################
def _edit_date (transx: cashflow.CashFlow) -> None:
    '''Prompts a user to enter a transaction's new date, and saves the result
    '''
    print("Enter new date")
    year = finance_entry.enter_year()
    transx.update_year(year)

    month = finance_entry.enter_month()
    transx.update_month(month)
    
    day = finance_entry.enter_day()
    transx.update_day(day)
    
    transx.update_date()
    print()
        
    
def _edit_acct (transx: cashflow.CashFlow) -> None:
    '''Prompts a user to enter a transaction's new account, and saves the 
    result
    '''
    account = input("Enter new Account: ").strip()    
    transx.update_acct(account)
    print()


def _edit_desc (transx: cashflow.CashFlow) -> None:
    '''Prompts a user to enter a transaction's new description, and saves the 
    result
    '''
    description = input("Enter new Description: ").strip()
    transx.update_desc(description)
    print()
  
  
def _edit_price (transx: cashflow.CashFlow) -> None:
    '''Prompts a user to enter a transaction's new description, and saves the 
    result
    '''
    price = input(
        ("Enter new Price ({}): ").format(basic_view.CURRENCY)).strip()
    transx.update_curr(basic_view.CURRENCY)
    transx.update_price(price)
    print()


def _edit_flow (transx: cashflow.CashFlow) -> None:
    '''Prompts a user to edit a transaction's cash flow direction, and saves 
    the 
    result
    '''
    print("Enter new cash flow")
    new_flow = finance_entry._enter_cf_dir()
    transx.update_cash_flow_direction(new_flow)
    print()


# CONFIRMING EDITS ############################################################
# Following the program showing initial transactions and the attribute to edit,
# _view_edited_transxs displays to the screen the updated transaction, so the 
# viewer may check if the revision was entered correctly, as well as to confirm 
# that the user is satisfied with the revision.
def _view_edit (transx: cashflow.CashFlow or cashflow.CashFlow) -> str:
    '''Displays to the screen an updated transaction
    '''
    print("Updated transaction:")
    print(('{:10} {:30}{:25}{:10}'.format(
        "Date", "Account", "Description", "Price", "Flow")))
    print(basic_view.LINE)
    print("{:2}/{:2}/{:4} {:30}{:25}{:3}{:7.2f} {}".format(
          transx.month, transx.day, transx.year, transx.acct_name, 
          transx.desc, transx.currency, transx.price, 
          basic_view.CF_AS_STR[transx.is_sav]))
    print("if Delete was selected, confirmation is that the previous item in",
          "the list is displayed")
    
