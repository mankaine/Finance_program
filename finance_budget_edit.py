# finance_budget_edit.py 
# by mankaine 
# August 7, 2016
 
# Module that is specific to displaying user's budget information and 
# prompting user to edit them. 

from account import Account
from basic_view import *
from cashflow import CashFlows    


def edit_acct_budgets(                                                          # only public function; 
    inflows: CashFlows, outflows: CashFlows, accts_coll: [Account]              #     called in finance_budget_menu
    ) -> [Account]:
    '''Displays to the user a table of accounts and their budgets in a year/
    month pair. Prompts the user to edit these values and records the changes
    in these values. Loops until the user decides to exit
    '''
    _display_full_budgets(accts_coll)                                           # User must see budgets to edit
 
    if binary_choice("\nEdit a budget? ", False, ''):                           # Edit budgets
        accts_coll = _edit_budget_loop(accts_coll)
    
    print_loading_newline("Returning to budget menu")                           # Prepare for budget menu
    return accts_coll
        
        
def _edit_budget_loop (
    accts: [Account]) -> [Account]:                     
    '''Prompts user the choice to edit budgets. If the user decides to do so,
    Replaces budget of a certain account and time period with the ones 
    specified by user
    '''
    editing_budgets = True
    while editing_budgets:
        _budget_name, _budget_year, _budget_month = _select_budget(accts)       # Selection of Account name, year, and month
        if _budget_name == KILL_PHRASE:
            break
        
        _update_specified_budget(                                               # Prompts user for edit
                accts, _budget_name, _budget_year, _budget_month)           
        
        _display_confirmed_edit(                                                # Checks for confirmation
                accts, _budget_name, _budget_year, _budget_month)               
        
        editing_budgets = binary_choice(                                        # Checks if whether to break revision loop
                "\nEdit another budget? ", False, '')                           
    return accts                                                                # Passed to edit_acct_budgets
             
                
def _select_budget (
    flow_accts: [Account]) -> (str, int, int):
    '''Returns the budget year, month, and name after prompting the user for
    such values 
    '''
    selecting_budget = True
    while selecting_budget:
        
        _specified_acct, budget_name = _scan_budget_name(flow_accts)            # Select Account 
        if budget_name == KILL_PHRASE:                               
            return budget_name, 0, 0
        
        _year_choice = view_years(                                              # Select time frame
            _specified_acct.budgets, _specified_acct.budgets, 
            "\nBudget years:")
        _month_choice = view_months(
            _year_choice, _specified_acct.budgets, _specified_acct.budgets,
            "Budget months:")
        return budget_name, _year_choice, _month_choice
                

def _scan_budget_name (flow_accts: [Account]                                    # called by _select_budget
    ) -> Account or None:
    '''Returns Account whose name is the specified string, None otherwise
    '''
    finding_acct_name = True
    while finding_acct_name:
        budget_name = input("Budget name (no dashes): ").strip()
        if budget_name == KILL_PHRASE:
            return flow_accts[0], budget_name
        
        for acct in flow_accts:
            if budget_name == acct.name:
                finding_acct_name = False
                return acct, budget_name                                    
        
        if finding_acct_name:
            print("{} not among budgets. Try again".format(budget_name))
             

def _update_specified_budget (
    accts: [Account], budget_name: str, budget_year: int, 
    budget_month: int) -> None:
    '''Prompts user for a new budget value for a specific time period 
    and  Replaces budget of that time period with a new budget value.
    '''
    for acct in accts:
        if acct.name == budget_name:
            while True:
                print_loading_newline("Editing budget information")             # Prompts user for new budget name
                new_budget_str = input(
                    "Enter new budget ({}): ".format(CURRENCY)
                    ).strip()
                if new_budget_str == KILL_PHRASE:
                    break
                savings_or_expense = binary_choice(
                    "\nIs account savings? ", False, '')
                try:
                    new_budget_flt = float(new_budget_str)
                    acct.update_budget(
                        new_budget_flt, budget_month, budget_year)
                    acct.update_savings_value(savings_or_expense)
                    return
                except:
                    print("{} not an acceptable input. Enter a number".format(
                                                            new_budget_str))
                                    

def _display_confirmed_edit (                                                   # Ensures a certain budget, and only that budget,
    accts: [Account], budget_name: str, budget_year: int,                       # was edited
    budget_month: int) -> str:
    '''Displays budgets for a specific period for all Accounts
    '''
    print_loading_newline("Displaying edited information")
    _display_full_budgets(accts)


def _months_range(accts: [Account]) -> [int]:
    '''Returns a list of integers representing all the months that contain
    at least one budget (1 being January, 12 being December)
    '''
    month_nums = []
    
    for acct in accts:
        for year in acct.budgets: 
            for month in acct.budgets[year]:
                if month not in month_nums:
                    month_nums.append(month)
    return sorted(month_nums)                                                   # Passed to _create_acct_str


def _create_acct_str(accts: [Account]) -> [str]:
    '''Returns a list of strings, each containing the Account name, type,
    and amount for each timeframe
    '''
    acct_data = []
    is_svg_str = {True: "Saving", False: "Spending", None: "TBD"}               # Better to use these strings than bools
    accts = sorted(accts, key = lambda acct: acct.name)                         # List not sorted by name during init
    
    for acct in accts:
        acct_str = "{:30}{:8}".format(acct.name, is_svg_str[acct.is_saving])
        for year in acct.budgets:
            for month in _months_range(accts):
                if month in acct.budgets[year]:
                    bdgt_info = acct.budgets[year][month]
                    if bdgt_info.budget != None:
                        acct_str += "{:>8.2f}".format(bdgt_info.budget) + ' '
                    else:
                        acct_str += "{:<8}".format("None") + " " 
                else:
                    acct_str += "{:<8}".format("----") + " " 
        acct_data.append(acct_str)
    return acct_data                                                            # Passed to _display_full_budgets 


def _display_full_budgets (accts: [Account]) -> str:                            
    '''Displays titles, and Accounts' budgets by year and month
    '''                                                                         # Called by _display_confirmed_edit 
    print("Budget Amounts:")                                                    # Row 1
        
    year_data = _return_unique_years(accts)                                     # Start of row 2
    year_str = " " * 38
    for year in year_data: 
        year_str += str(year) + ('\t' * year_data[year])
    print(year_str)                                                             # End of row 2
    
    month_and_col_name_line = "{:30}{:8}".format("Name", "Type")                # Start of row 3
    for month in _return_unique_months(accts):
        month_and_col_name_line += "{:9}".format(MONTHS[month][0:3])
    
    print(month_and_col_name_line)                                              # End of row 3
    
    for acct_line in _create_acct_str(accts):
        print(acct_line)                                                        # Row 4 to row n-5
        
    _display_net_flows(accts)                                                   # Row n-5 to n


def _return_unique_years (accts: [Account]) -> {int: int}: 
    '''Returns unique years among all Accounts, and the number of 
    months each year has
    '''                                                                         # Need to find strings of years
    acct_years = {}                                                             # Value determines distance between years
    for acct in accts:                                                          
        for year in acct.budgets: 
            if year in acct_years \
            and len(acct.budgets[year]) > acct_years[year]:                     # Longest length accounts for all months
                acct_years[year] = len(acct.budgets[year])
            if year not in acct_years:    
                acct_years[year] = len(acct.budgets[year])                      # Years will be repeated; this line filters repeats     
    return acct_years                                                           # Passed to _display_full_budgets                                                   


def _return_unique_months (accts: [Account]) -> [int]:      
    '''Returns unique months among all Accounts
    '''                                                                         # Need to find strings of months
    acct_mo = []
    for acct in accts:
        for year in acct.budgets:
            for month in acct.budgets[year]:
                if month not in acct_mo:                                        # Prevents duplicate months
                    acct_mo.append(month)
    return sorted(acct_mo)                                                      # Passed to _display_full_budgets
                                                                                # Without sorted(), months displayed out of order

def _display_net_flows(accts: [Account]) -> str:                                # called by _display_full_budgets
    '''Displays on the screen total inflows and outflows
    '''
    net_inf, net_out = _calc_total_flows(accts)
    
    print("\nNET INFLOWS: {}{:.2f}".format(CURRENCY, net_inf))
    print("NET OUTLOWS: {}{:.2f}".format(CURRENCY, net_out))
    
    print("-" * (
    len("NET INFLOWS  ") + len(CURRENCY) + max(
    len(str(net_inf)), len(str(net_out)))))
    
    print("NET FLOWS:   {}{:.2f}".format(
    CURRENCY, net_inf - net_out))
    
    print("=" * (
    len("NET INFLOWS  ") + len(CURRENCY) + len(
    CURRENCY) + len(str(net_inf - net_out))))
    

def _calc_total_flows (accts: [Account]) -> (float, float):                     # Called by _display_net_outflows 
    '''Returns a tuple of two floats representing the total
    inflows and outflows of all transactions
    '''
    inflows_total = 0.00
    outflows_total = 0.00
    
    for acct in accts:
        for year in acct.budgets:
            for month in acct.budgets[year]:
                for transx in acct.budgets[year][month].acct_transxs:
                    if transx.is_sav:
                        inflows_total += transx.price
                    else:
                        outflows_total += transx.price
                        
    return inflows_total, outflows_total


def _display_accts_budgets(accts: [Account]) -> str: 
    '''Displays Accounts' budgets by year and month
    '''
    empty_budget_dicts = _create_budget_str_to_print(accts)

    for year in empty_budget_dicts:     
        first_month_not_added = True
        str_to_print = '{:<6}'.format(year)                                     # print year
        for month_num in empty_budget_dicts[year]:                              # print month
            if first_month_not_added:
                str_to_print += '{:<13}'.format(MONTHS[month_num])
                first_month_not_added = False
            else:
                str_to_print += "\n      {:<13}".format(                        # For style: each unique year displayed only once
                                MONTHS[month_num])
            for budgets_str in empty_budget_dicts[year][month_num]:             # print budget
                str_to_print += budgets_str
        print(str_to_print)        
    

def _create_budget_str_to_print(accts: [Account]) -> dict:
    '''Creates strings and dictionary necessary to display budgets by year 
    and month. Returns both in a dictionary
    '''
    dicts_to_fill = _create_dict_budget_str(accts)                              # Returns keys and values 
    unique_months = _return_unique_months(accts)
    
    for acct in accts:
        for year in acct.budgets:
            for month in unique_months:
                if month in acct.budgets[year]:
                    if acct.budgets[year][month].budget != None:
                        dicts_to_fill[year][month] += '{:>10.2f}'.format(
                        acct.budgets[year][month].budget)
                    else:
                        dicts_to_fill[year][month] += '{:>10}'.format("None")
                else:
                    dicts_to_fill[year][month] += '{:>10}'.format("N/A")
    return dicts_to_fill                                                        # Passed to _display_accts_budgets; needed to
                                                                                # display each Account's month, year, and budget
    

def _create_dict_budget_str (accts: [Account]) -> dict:                         # Passes a series of empty dicts and ints to prevent
    '''Creates dictionary whose keys are the years and months of transactions    
    referring to an account and whose values are empty dicts 
    '''                                                                         # Exceptions being raised in 
    empty_budget_dicts = {}                                                     # _create_budget_str_to_print
    
    for acct in accts:
        for year in acct.budgets:
            if year not in empty_budget_dicts:
                empty_budget_dicts[year] = {}
            for month in acct.budgets[year]:
                if month not in empty_budget_dicts[year]:
                    empty_budget_dicts[year][month] = ''
    return empty_budget_dicts
                    
    
