# finance_view.py
# by mankaine
# July 2016

# Deals specifically with viewing transactions as 
# selected in the main menu.
#
# This module shouldn't be confused with basic_view; that module
# refers to functions and variables used across multiple user
# interface modules.

import cashflow
import basic_view

# When called in the main_menu module, handle_view_choice will display another
# menu to provide users with a choice to view transactions within a month, the
# budget analysis, or return to the main menu. 
def handle_view_choice (inflows: cashflow.CashFlows, outflows: cashflow.CashFlows):
    '''Displays all transactions
    '''
    view_menu = """DISPLAY MENU
1. Display transactions within a month
2. Return to main menu
"""
    while True:
        menu_choice = basic_view.menu_input(view_menu, 5)
        if menu_choice == 1:
            _display_transx_month(inflows, outflows)
            basic_view.print_loading_newline("Returning to Display Menu")
        elif menu_choice == 2:
            break
        else:
            print('{} not an option. Please try again'.format(menu_choice))
    basic_view.print_loading_newline("RETURNING TO MAIN MENU")
        

# DISPLAYING TRANSACTIONS IN A MONTH/YEAR PAIR ################################
# The program will run through these series of functions to choose the month, 
# year, and display the resulting transactions.
def _display_transx_month (
    inflows: cashflow.CashFlows, outflows: cashflow.CashFlows):
    '''Displays the transactions with in a selected year and month
    '''
    _year_choice = basic_view.view_years(inflows.cfs, 
        outflows.cfs, "Years to view:")
    _month_choice = basic_view.view_months(_year_choice, 
        inflows.cfs, outflows.cfs, "Months to view:")
    view_transxs(_year_choice, _month_choice, inflows.cfs, outflows.cfs)
    

# The first two lines of code are implemented to display to the user that the 
# program is currently displaying selected transactions and the attributes of 
# those transactions. The if-else statements are necessary because the _display_cf
# function doesn't account for dictionaries that lack certain keys. So if one 
# dictionary representing cash flows in one direction is non-existent, 
# view_transxs should be able to display only one dictionary. But if both dicts
# contain the month and year pair, then _display_cfs_two_dicts is called.
# 
def view_transxs(year: int, month: int, 
                 inflows_dict: dict, outflows_dict: dict) -> str:
    '''Displays transactions within a selected month and year 
    '''
    basic_view.print_loading_newline("Displaying Options")        
    if year in inflows_dict or year in outflows_dict:
        if year not in inflows_dict:
            _display_cfs(outflows_dict, year, month)
        elif year not in outflows_dict:
            _display_cfs(inflows_dict, year, month)
    if year in inflows_dict and year in outflows_dict:
        if month in inflows_dict[year] and month in outflows_dict[year]:
            _display_cfs_two_dicts(inflows_dict, outflows_dict, year, month)
        elif month not in inflows_dict[year] and month in outflows_dict[year]:
            _display_cfs(outflows_dict, year, month)
        elif month in inflows_dict[year] and month not in outflows_dict[year]:
            _display_cfs(inflows_dict, year, month)

        
def _display_cfs(cfs_dict: cashflow.CashFlows, year: int, month: int) -> str:
    '''Displays Cash Flows within one dictionary
    '''
    all_transxs = []
    for cf in cfs_dict[year][month]: 
        all_transxs.append(cf)
    sorted_transxs = _sort_transxs(all_transxs)

    basic_view.print_loading_newline(
        "Displaying Transactions for Month {}, Year {}".format(month, year))
    print(("\n{:5} {:20} {:20} {:10} {:4}").format(
        "Day", "Account", "Description", "Price", "Flow"))
    print(basic_view.LINE)

    for cf in sorted_transxs:
        if cf == sorted_transxs[0]:
            _display_first_transx(cf)
        else:
            _display_other_transx(cf)
    

def _display_first_transx(cf: cashflow.CashFlow) -> str:
    '''Displays the first transaction in a list of cash flows, 
    formatted especially to indicate currency of a transaction
    '''
    print(("{:^5} {:20} {:20} {:3}{:7.2f} {}".format(
            cf.day, cf.acct_name, cf.desc, cf.currency, cf.price, 
            basic_view.CF_AS_STR[cf.pos_cash_flow])))
    
    
def _display_other_transx(cf: cashflow.CashFlow) -> str:
    '''Displays a transaction in a list of cash flows, assuming that the cash 
    flow object in the parameter is not the first in a list or 
    dictionary of cash flows
    '''
    print(("{:^5} {:20} {:20}    {:7.2f} {}".format(
            cf.day, cf.acct_name, cf.desc, cf.price, 
            basic_view.CF_AS_STR[cf.pos_cash_flow])))

# _display_cfs_two_dicts calls _sort_transxs to determine how to sort the order
# of the transactions to be displayed. The user is able to determine such a
# choice by choosing one of the five attributes, and then deciding if the order 
# should be reversed (e.g. backwards in alphabetical order, most recent to 
# earliest date, etc). 
def _display_cfs_two_dicts(
    inflows_dict: cashflow.CashFlows, outflows_dict: cashflow.CashFlows, 
    year: int, month: int) -> str or None:
    '''Displays both Positive and Negative Cashflows within a selected 
    year and month, assuming that both are recorded within the month. 
    Returns nothing if the user decides to exit early
    '''
    all_transxs = []
    for pos_cf in inflows_dict[year][month]: 
        all_transxs.append(pos_cf)
    for neg_cf in outflows_dict[year][month]:
        all_transxs.append(neg_cf)
    sorted_transxs = _sort_transxs(all_transxs)
    if sorted_transxs == None:
        return
    
    basic_view.print_loading_newline(
        "Displaying Transactions for Month {}, Year {}".format(month, year))
    print(("\n{:5} {:20} {:20} {:10} {:4}").format(
        "Day", "Account", "Description", "Price", "Flow"))
    print(basic_view.LINE)
   
    for transx in sorted_transxs:
        if transx == sorted_transxs[0]:
            _display_first_transx(transx)
        else:
            _display_other_transx(transx)
    

def _sort_transxs (transxs: list) -> list or None:
    '''Prompts user for a way to sort a list. Returns a list sorted according to 
    that choice or None if user decides to exit early.
    '''
    while True:
        attrib_choice = input(
        "Sort by [d]ate, [a]ccount, d[e]scription, [p]rice, or [f]low? ")\
        .strip()
        if attrib_choice == basic_view.KILL_PHRASE:
            break
        elif attrib_choice.lower() not in ['d', 'a', 'e', 'p', 'f']:
            print(
            "{} not an available choice. Select either 'd', 'a', 'e', 'p', or 'f'"\
            .format(attrib_choice))         
        else:
            rev_choice = basic_view.binary_choice(
        "Display in reverse? ", False, '')
        if attrib_choice.lower() == 'd':
            return _sort_by_date(transxs, rev_choice)
        elif attrib_choice.lower() == 'a':
            return _sort_by_acct(transxs, rev_choice)
        elif attrib_choice.lower() == 'e':
            return _sort_by_desc (transxs, rev_choice)
        elif attrib_choice.lower() == 'p':
            return _sort_by_price (transxs, rev_choice)
        elif attrib_choice.lower() == 'f':
            return _sort_by_flow (transxs, rev_choice)
        

def _sort_by_date (transxs: list, rev: bool) -> list:
    '''Sorts transactions in a list by date - starting from the most recent
    if reverse is True, the least so if False  
    '''
    for transx in transxs:
        transx.update_date()
    return sorted(transxs, key = lambda transx: transx.date, reverse = rev)


def _sort_by_acct (transxs: list, rev: bool) -> list:
    '''Sorts transactions in a list by account - from alphabetically starting
    from 'a' if reverse is False, and from 'z' if True
    '''
    return sorted(transxs, 
        key = lambda transx: transx.acct_name.lower(), reverse = rev)
    

def _sort_by_desc (transxs: list, rev: bool) -> list:
    '''Sorts transactions in a list by account - from alphabetically starting
    from 'a' if reverse is False, and from 'z' if True
    '''
    return sorted(transxs, key = lambda transx: transx.desc.lower(), 
                  reverse = rev)


def _sort_by_price (transxs: list, rev: bool) -> list:
    '''Sorts transactions in a list by price - from least expensive 
    if reverse if False from 'a' if reverse is False, and from the most if True
    '''
    return sorted(transxs, key = lambda transx: transx.price, reverse = rev)


def _sort_by_flow (transxs: list, rev: bool) -> list:
    '''Sorts transaction in a list by booleans - first True, then False. 
    Displayed False before True when rev's value is True
    '''
    return sorted(
        transxs, key = lambda transx: transx.pos_cash_flow, reverse = not rev)
