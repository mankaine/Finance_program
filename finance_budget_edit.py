# finance_budget_edit.py 
# by mankaine. 
# August 7, 2016
 
# Module that is specific to displaying user's budget information and 
# prompting user to edit them. 

import account
import basic_view
import cashflow    


def edit_acct_budgets(                                                          # only public function; called in finance_budget_menu
    inflows: cashflow.CashFlows, outflows: cashflow.CashFlows,
    accts_coll: [account.Account]
    ) -> [account]:
    '''Displays to the user a table of accounts and their budgets in a year/
    month pair. Prompts the user to edit these values and records the changes
    in these values. Loops until the user decides to exit
    '''
    acct_names_str = _create_acct_str(accts_coll)                               # Display budgets to edit
    _display_full_budgets(acct_names_str, accts_coll)
 
    if basic_view.binary_choice("\nEdit a budget? ", False, ''):                # Edit budgets
        accts_coll = _edit_budget_loop(accts_coll)
    
    basic_view.print_loading_newline("Returning to budget menu")                # Prepare for budget menu
    return accts_coll
        
        
def _edit_budget_loop (
    accts: [account.Account]) -> [account.Account]:                     
    '''Prompts user the choice to edit budgets. If the user decides to do so,
    Replaces budget of a certain account and time period with the ones 
    specified by user
    '''
    editing_budgets = True
    while editing_budgets:
        _budget_name, _budget_year, _budget_month = _select_budget(accts)       # Selection of Account name, year, and month
        if _budget_name == basic_view.KILL_PHRASE:
            break
        
        _update_specified_budget(                                               # Prompts user for edit
                accts, _budget_name, _budget_year, _budget_month)           
        
        _display_confirmed_edit(                                                # Checks for confirmation
                accts, _budget_name, _budget_year, _budget_month)               
        
        editing_budgets = basic_view.binary_choice(                             # Checks if whether to break revision loop
                "\nEdit another budget? ", False, '')                           
    return accts                                                                # Passed to edit_acct_budgets
             
                
def _select_budget (
    flow_accts: [account.Account]) -> (str, int, int):
    '''Returns the budget year, month, and name after prompting the user for
    such values 
    '''
    selecting_budget = True
    while selecting_budget:
        
        _specified_acct, budget_name = _scan_budget_name(flow_accts)            # Selection of Account 
        if budget_name == basic_view.KILL_PHRASE:
            return budget_name, 0, 0
        
        _year_choice = basic_view.view_years(                                   # Selection of time frame
            _specified_acct.budgets, _specified_acct.budgets, 
            "\nBudget years:")
        _month_choice = basic_view.view_months(
            _year_choice, _specified_acct.budgets, _specified_acct.budgets,
            "Budget months:")
        return budget_name, _year_choice, _month_choice
                

def _scan_budget_name (flow_accts: [account.Account]                            # called by _select_budget
    ) -> account.Account or None:
    '''Returns Account whose name is the specified string, None otherwise
    '''
    finding_acct_name = True
    while finding_acct_name:
        budget_name = input("Budget name (no dashes): ").strip()
        if budget_name == basic_view.KILL_PHRASE:
            return flow_accts[0], budget_name
        
        for acct in flow_accts:
            if budget_name == acct.name:
                finding_acct_name = False
                return acct, budget_name                                    
        
        if finding_acct_name:
            print("{} not among budgets. Try again".format(budget_name))
             

def _update_specified_budget (
    accts: [account.Account], budget_name: str, budget_year: int, 
    budget_month: int) -> None:
    '''Prompts user for a new budget value for a specific time period 
    and Account. Replaces budget of that time period with a new budget value.
    '''
    for acct in accts:
        if acct.name == budget_name:
            while True:
                basic_view.print_loading_newline("Editing budget information")  # Prompts user for new budget name
                new_budget_str = input(
                    "Enter new budget ({}): ".format(basic_view.CURRENCY)
                    ).strip()
                savings_or_expense = basic_view.binary_choice(
                    "\nIs account savings? ", False, '')
                try: # Processing input
                    # Handles input off to account - updates 
                    # Account type and budget
                    new_budget_flt = float(new_budget_str)
                    acct.update_budget(
                        new_budget_flt, budget_month, budget_year)
                    acct.update_savings_value(savings_or_expense)
                    return
                except:
                    print("{} not an acceptable input. Enter a number".format(
                                                            new_budget_str))
                                    

def _display_confirmed_edit (                                                   # Ensures a certain budget, and only that budget,
    accts: [account.Account], budget_name: str, budget_year: int,               # was edited
    budget_month: int) -> str:
    '''Displays budgets for a specific period for all Accounts
    '''
    basic_view.print_loading_newline("Displaying edited information")
    _display_full_budgets(_create_acct_str(accts), accts)


def _create_acct_str(collection: [account.Account]) -> [str]:
    '''Returns a list, each element itself being a list of strings representing
    the account name, any stylistic edits, and whether the Account is savings
    '''
    acct_names = []
    is_svg_str = {True: "SAVING", False: "EXPENSE", None: "  NONE  "}
    for acct in collection:
        acct_name_broken = [is_svg_str[acct.is_saving]]

        if " " in acct.name:                                                    # " " (space) in Account name
            acct_name_broken.extend(_break_name_with_space(acct))
        else:                                                                   # " " not in Account name
            acct_name_broken.extend(_break_name_without_space(acct))                    

        acct_names.append(acct_name_broken)
    return acct_names                                                           # Internal list contains sparsed Account names


def _break_name_with_space (acct: account.Account) -> [str]:
    '''Returns a list of strings that represent an Account's name with spaces,
    separated at every 7th character
    '''
    acct_name_broken = []
    init_list = acct.name.split(" ")
    
    for elem in init_list:
        if len(elem) <= 7:
            acct_name_broken.append(elem)
        else:
            for iter_num in range(len(elem) // 7 + 1):
                if 7 * iter_num < len(elem):
                    str_to_append = elem[7 * (iter_num) : 7 * (1 + iter_num)]
                    if str_to_append != elem[-len(str_to_append):]:
                        str_to_append += "-"
                    acct_name_broken.append(str_to_append)
    return acct_name_broken                                                     # Passed to _create_acct_str


# For style, _break_name_without_space will break slightly differently from 
# _break_name_with_space. The Account name without spaces will be processed 
# by _break_name_without_space only at every 7th character to be easier on the eyes. 
def _break_name_without_space (acct: account.Account) -> [str]:
    '''Returns a list of strings that represent an Account's name without spaces,
    separated at every 7th character 
    '''
    acct_name_broken = []
    
    for acct_ind in range((len(acct.name) // 7) + 2):                        
        if 7 * acct_ind < len(acct.name):
            str_to_append = acct.name[7 * (acct_ind) : 7 * (acct_ind + 1)]
            if str_to_append != acct.name[-len(str_to_append)::]:
                str_to_append += "-"
                acct_name_broken.append(str_to_append)
            else:
                acct_name_broken.append(
                        acct.name[7 * (acct_ind) : len(acct.name)])
    return acct_name_broken


# _display_full_budgets display the full information for each Account in regards
# to budget. It's called by _display_confirmed_edit and prints for most lines 
# the Account names. The value returned from is passed to broken_acct_names.  
def _display_full_budgets (
    broken_acct_names: [str], accts: [account.Account]) -> str:
    '''Displays titles, and Accounts' budgets by year and month
    '''    
    print("Budget Amounts:")
    
    # Find length of longest Account name: it is necessary for a special way of
    # indexing. To access the inner most element of a 2-D list one would use 
    # two for loops, but such iterates through each element of the inner list
    # completely. This would display the Account name across horizontally instead
    # of vertically. Instead, _print_binded_acct_one_line handles the loops 
    # properly, but depends on the longest Account name to loop through a specific 
    # number of times - largest_list_len determines this value.  
    largest_list_len = 0
    for broken_acct_name in broken_acct_names:
        if len(broken_acct_name) > largest_list_len:
            largest_list_len = len(broken_acct_name)
            
    # Print Account name: the range of 0 to (largest_list_len - 1) is passed through 
    # _print_binded_acct_one_line as line_ind in order to properly loop through - 
    # it will concatenate to each individual line the nth element of each list inside 
    # of broken_acct_names.
    for line_ind in range(largest_list_len):
        _print_binded_acct_one_line(broken_acct_names, line_ind)
    
    # Print Account date, year, and budget
    print('-' * (len("Account Name:") + (len(broken_acct_names) * 10) + 10))
    print("Year  Month")
    print("-" * 19)
    _display_accts_budgets(accts)
    _display_net_flows(accts)


def _display_net_flows(accts: [account.Account]) -> str:                        # called by _display_full_budgets
    '''Displays on the screen total inflows and outflows
    '''
    net_inf, net_out = _calc_total_flows(accts)
    
    print("\nNET INFLOWS: {}{:.2f}".format(basic_view.CURRENCY, net_inf))
    print("NET OUTLOWS: {}{:.2f}".format(basic_view.CURRENCY, net_out))
    
    print("-" * (
    len("NET INFLOWS  ") + len(basic_view.CURRENCY) + max(
    len(str(net_inf)), len(str(net_out)))))
    
    print("NET FLOWS:   {}{:.2f}".format(
    basic_view.CURRENCY, net_inf - net_out))
    
    print("=" * (
    len("NET INFLOWS  ") + len(basic_view.CURRENCY) + len(
    basic_view.CURRENCY) + len(str(net_inf - net_out))))
    

def _calc_total_flows (accts: [account.Account]) -> (float, float):             # Called by _display_net_outflows 

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


def _print_binded_acct_one_line (acct_names: [str], line_ind: int) -> str:
    '''Prints a string, which are composed of previously separated strings
    '''
    if line_ind == 0:                                                           # value is between 0 and length of longest inner list
        binded_name_line = "Account Type:      "                                # in the list returned by _create_acct_str
    elif line_ind == 1:
        binded_name_line = "Account Name:      "
    else:
        binded_name_line = " " * len("Account Name:      ")
        
    for acct_ind in range(len(acct_names)):
        try:
            binded_name_line += "{:10}".format(acct_names[acct_ind][line_ind])
        except:
            binded_name_line += "{:10}".format(" " * 8)                         # Placeholder if exception raised
    print(binded_name_line)                                                     # Properly formatted to give illusion of columns


def _display_accts_budgets(accts: [account.Account]) -> str: 
    '''Displays Accounts' budgets by year and month
    '''
    empty_budget_dicts = _create_budget_str_to_print(accts)

    for year in empty_budget_dicts:     
        first_month_not_added = True
        str_to_print = '{:<6}'.format(year)                                     # print year
        for month_num in empty_budget_dicts[year]:                              # print month
            if first_month_not_added:
                str_to_print += '{:<13}'.format(basic_view.MONTHS[month_num])
                first_month_not_added = False
            else:
                str_to_print += "\n      {:<13}".format(                        # For style: each unique year displayed only once
                                basic_view.MONTHS[month_num])
            for budgets_str in empty_budget_dicts[year][month_num]:             # print budget
                str_to_print += budgets_str
        print(str_to_print)        
    

def _create_budget_str_to_print(accts: [account.Account]) -> dict:
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

def _return_unique_months (accts: [account.Account]) -> set:                    # Ensures budgets are in line with months
    '''Returns a set composed of the unique months of all transactions 
    recorded
    '''
    unique_months = set()
    
    for acct in accts:
        for year in acct.budgets:
            for month in acct.budgets[year]:
                unique_months.add(month)
    return unique_months                                                        # Passed to_create_budget_str_to_print
    

def _create_dict_budget_str (accts: [account.Account]) -> dict:                 # Passes a series of empty dicts and ints to prevent
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
                    
    
