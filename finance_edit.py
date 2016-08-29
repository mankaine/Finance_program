# finance_edit.py
# by mankaine
# July 12, 2016

# Implements user interface aspect that edits transaction.

ATTRIBUTES = ['Date', 'Account', 'Description', 'Price', 'Flow']


# OutsideListRangeError is raised when a user enters a value representing
# a month or year to edit that is not been yet entered as having a transaction.
class OutsideListRangeError (Exception):
    pass


# INDIVIDUAL EDITING ###########################################################################
# When a user decides to edit a transaction immediately after creating it, handle_edit is called
# from the finance_entry module. While it does not return anything, the function updates
# the CashFlow class. 
def handle_edit (
    transx: cashflow.CashFlow, inflows: cashflow.CashFlows,
    outflows: cashflow.CashFlows) -> None:
    '''Displays and edits one transaction
    '''
    editing = True
    while editing:
        _attrib = _select_attrib(ATTRIBUTES, transx, inflows, outflows)
        _transx = _edit_transx(transx, _attrib)
        _view_edited_transx(_transx, 0)
        editing = basic_view.binary_choice("\nEdit transaction again? ", False, '')


# EDITING MULTIPLE TRANSACTIONS ################################################
# handle_edit_choice is called in the main_menu module and displays the 
# transactions that can be edited, the updated transaction, and the updated list
# of transactions in the initially selected month and year.
def handle_edit_choice (inflows: cashflow.CashFlows, 
                        outflows: cashflow.CashFlows) -> None:    
    '''Displays revenues, expenses, and enables user to edit the attributes of
    the transactions one at a time
    '''
    _year_choice = basic_view.view_years(
                    inflows.cfs, outflows.cfs, "Years to edit:")
    _month_choice = basic_view.view_months(
                    _year_choice, inflows.cfs, outflows.cfs, "Months to edit:")
    if _month_choice == 0:
        basic_view.print_loading_newline("RETURNING TO MAIN MENU")
        return
    
    view_transxs(_year_choice, _month_choice, inflows.cfs, outflows.cfs)
    
    editing_transx = True
    while editing_transx:
        _pcf_len, _num_choice = select_transx_index(
            inflows.cfs, outflows.cfs, _year_choice, _month_choice)
        if _pcf_len == _num_choice and _pcf_len == -1:
            basic_view.print_loading_newline("RETURNING TO MAIN MENU")
            return
        _transx = select_transx(
            inflows.cfs, outflows.cfs, _year_choice, _month_choice, _pcf_len,
            _num_choice)
        
        handle_edit(_transx, inflows, outflows)
        _update_cfs(inflows, outflows)
        
        print("\nDisplaying edited transactions:")
        view_transxs(_year_choice, _month_choice, inflows.cfs, outflows.cfs)
        editing_transx = basic_view.binary_choice("\nEdit more transactions? ", False, '')


# CHOOSING THE TRANSACTION TO EDIT ############################################
# basic_view.view_years and basic_view.view_months are called in order to 
# allow the user to choose a month and year to focus in on. 

# After a month and year have been selected, a user must see which transactions to edit.
# This need is met by view_transxs, and _view_tansxs_formatted. The former calls the 
# latter to display a list of transactions, which is either positive or negative cash flow.
def view_transxs (year: int, month: int, inflows: dict, outflows: dict) -> str:
    '''Displays possible transaction to edit within a year and month
    '''
    print("{} {} Transactions".format(basic_view.MONTHS[month], year))
    print(basic_view.LINE)
    _view_tranxs_formatted('Savings', year, month, inflows, 0)
    print()
    
    pcf_len = transxs_in_month(year, month, inflows)    
    _view_tranxs_formatted('Expenses', year, month, outflows, pcf_len)
    
    # Note that for the Negative Cash Flow implementation of _view_tranxs_formatted,
    # the length of the PCF dict is a parameter. This prevents two different
    # transactions of earnings and spendings from having the same value. 
    
    
# view_transxs_formatted will display the attributes, and then then the index number,
# date, description, account, and price of each transaction in a list. For the sake of design,
# only the first transaction in the list has a currency symbol.
def _view_tranxs_formatted (message: str, year: int, month: int, 
                            master_dict: dict, list_boost: int) -> str:
    '''Displays possible revenues to edit within a year and month
    '''
    print("{:^84}".format(message))
    print(basic_view.LINE + ("-" * 7))
    print(("\n{:5} {:10} {:28} {:24} {:10} {:4}").format("No.",
        "Date", "Account", "Description", "Price", "Flow"))
    print(basic_view.LINE + ("-" * 7))

    if year in master_dict:
        if month in master_dict[year]:
            master_dict[year][month].sort(key = lambda transx: transx.date) 
            for transx in master_dict[year][month]:
                if master_dict[year][month][0] == transx:
                    print("{:3}. {:2}/{:2}/{:4} {:30}{:25}{:3}{:7.2f} {}".format(
                        master_dict[year][month].index(transx) + 1 + list_boost, 
                        transx.month, transx.day, transx.year, transx.acct_name, 
                        transx.desc, transx.currency, transx.price,
                        basic_view.CF_AS_STR[transx.pos_cash_flow]))
                else:
                    print("{:3}. {:2}/{:2}/{:4} {:30}{:25}{:10.2f} {}".format(
                        master_dict[year][month].index(transx) + 1 + list_boost, 
                        transx.month, transx.day, transx.year, transx.acct_name,
                        transx.desc, transx.price, 
                        basic_view.CF_AS_STR[transx.pos_cash_flow]))
        else:
            print("\n{:^80}\n".format("No entries"))
    else:
        print("\n{:^80}\n".format("No entries"))


# handle_edit_choice calls select_transx_index to find not only the numbering of the 
# transaction the user wishes to edit, but also the amount of positive cash flow
# transactions entered. So, the function returns a tuple containing these values, 
# but only after the transactions are displayed.
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


def select_transx_index (inflows: dict, outflows: dict, year: int, month: int) -> (int, int):
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
            if number_choice_str == basic_view.KILL_PHRASE:
                return -1, -1
            number_choice = int(number_choice_str)
            if 1 > number_choice or (pcf_len + ncf_len) < number_choice:
                raise OutsideListRangeError() 
        except ValueError:
            print("{} not an integer. Try again.".format(number_choice_str))
        except OutsideListRangeError:
            print("{} outside of the range 1 to {}. Try again.".format(
                number_choice, pcf_len + ncf_len))
        else:
            selecting_transx = False 
            return pcf_len, number_choice - 1
        
        
def select_transx (pcfs: dict, ncfs: dict, year: int, 
                    month: int, pcf_len: int, num_choice: int) -> cashflow.CashFlow:
    '''Returns a transaction based on selected information
    '''
    if pcf_len > 0 and num_choice <= pcf_len:
        return pcfs[year][month][num_choice - 1]
    elif pcf_len > 0 and pcf_len < num_choice:
        return ncfs[year][month][num_choice - (pcf_len) - 1]
    elif pcf_len == 0:
        return ncfs[year][month][num_choice - 1]
 

# Necessary to sort inflows and outflows - otherwise the shell UI will display
# transactions that are savings in expenses and vice versa
def _update_cfs (inflows: cashflow.CashFlows, outflows: cashflow.CashFlows) -> None:
    '''Places all positive cashflows in pcfs and negative cash flows in ncfs 
    '''
    add_to_ncfs = inflows.filter_transx_flows(True)
    add_to_pcfs = outflows.filter_transx_flows(False)
    
    inflows.merge_dicts(add_to_pcfs)
    outflows.merge_dicts(add_to_ncfs)
    
    add_to_pcfs = inflows.resort_dicts_by_date()
    add_to_ncfs = outflows.resort_dicts_by_date()
    
    inflows.merge_dicts(add_to_pcfs)
    outflows.merge_dicts(add_to_ncfs)
    

# CHOOSING WHAT TO EDIT ###################################################################
# Now that the transaction has been chosen, the program must figure out how to edit it.
# It requests the user to answer this question, and passes the answer
# to _edit_transx, where individual functions edit, update, and revise the values specified.
def _select_attrib (
    attribs: [str], transx: cashflow.CashFlow, inflows: cashflow.CashFlows,
    outflows: cashflow.CashFlows) -> str:
    '''Displays possible attributes to edit, and returns the string representing 
    the attribute
    '''
    selecting_attrib = True
    while selecting_attrib:
        attrib_str = input(
        "Enter attribute to edit (type in 'Delete' to remove transaction): ").strip()
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
            print("{} not an option. Select one of the following: {}.".format(attrib_str, ATTRIBUTES)) 
        else:
            return attrib_str.title()


def _delete_transx(
    transx: cashflow.CashFlow, inflows: cashflow.CashFlows, 
    outflows: cashflow.CashFlows) -> None:
    '''Deletes a transaction from a CashFlows object
    '''
    if transx.pos_cash_flow:
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


# EDITING THE TRANSACTION ##################################################################
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
    '''Prompts a user to enter a transaction's new account, and saves the result
    '''
    account = input("Enter new Account: ").strip()    
    transx.update_acct(account)
    print()


def _edit_desc (transx: cashflow.CashFlow) -> None:
    '''Prompts a user to enter a transaction's new description, and saves the result
    '''
    description = input("Enter new Description: ").strip()
    transx.update_desc(description)
    print()
  
  
def _edit_price (transx: cashflow.CashFlow) -> None:
    '''Prompts a user to enter a transaction's new description, and saves the result
    '''
    price = input(("Enter new Price ({}): ").format(basic_view.CURRENCY)).strip()
    transx.update_curr(basic_view.CURRENCY)
    transx.update_price(price)
    print()


def _edit_flow (transx: cashflow.CashFlow) -> None:
    '''Prompts a user to edit a transaction's cash flow direction, and saves the 
    result
    '''
    print("Enter new cash flow")
    new_flow = finance_entry._enter_cf_dir()
    transx.update_cash_flow_direction(new_flow)
    print()


# CONFIRMING EDITS #################################################################################
# Following the program showing initial transactions and the attribute to edit, _view_edited_transxs
# displays to the screen the updated transaction, so the viewer may check if the revision was 
# entered correctly, as well as to confirm that the user is satisfied with the revision.
def _view_edited_transx (transx: cashflow.CashFlow or cashflow.CashFlow,
                        rank: int) -> str:
    '''Displays to the screen an updated transaction
    '''
    print("Updated transaction:")
    print(('{:5}{:10} {:30}{:25}{:10}'.format("No.", "Date", "Account", "Description", "Price", "Flow")))
    print(basic_view.LINE)
    print("{:3}. {:2}/{:2}/{:4} {:30}{:25}{:3}{:7.2f} {}".format(
          rank, transx.month, transx.day, transx.year, transx.acct_name, 
          transx.desc, transx.currency, transx.price, basic_view.CF_AS_STR[transx.pos_cash_flow]))
    print("if Delete was selected, confirmation is that the previous item in the list is displayed")
    
