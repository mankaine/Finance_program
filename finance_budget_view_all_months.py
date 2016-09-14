# finance_budget_view_all_months.py 
# By mankaine
# August 27, 2016
#
# Shell user interface module that allows user to one budget, of all months. Also allows user to view breakdown of one 
# month's budget.

import cashflow
import account
import basic_view
import finance_budget_view_one_month

def view_acct_all_months(                                                       # called by finance_budget_menu, option 3
    inflows: cashflow.CashFlows, outflows: cashflow.CashFlows, 
    accts: [account.Account]) -> None:
    '''Displays an account and its budget information
    '''
    acct_choice_num = _select_account(accts)
    if acct_choice_num == -1:
        basic_view.print_loading_newline("Returning to Budget Menu")
        return
    
    _display_budget(accts[acct_choice_num - 1])
    viewing_breakdown = basic_view.binary_choice(
    "View specific account? ", False, "")
    year, month = select_timefraome(inflows.cfs, outflows.cfs)
    
    while viewing_breakdown:
        if _handle_acct_choice_num(accts[acct_choice_num - 1], year, month) == -1:
            break
        else:
            view_budget_by_month (accts, acct_choice_num, year, month)

        viewing_breakdown = basic_view.binary_choice("View another account? ",
                                                      False, "")
    basic_view.print_loading_newline("Returning to Budget Menu")


                                                                                # SELECTING ACCOUNT
                                                                                # _select_account is called at the
def _select_account(accts: [account.Account]) -> int:                           # beginning of view_acct_all_months
    '''Prompts user to enter an Account to view, and continues to do
    so until a valid one is provided. Returns the selected Account
    '''
    while True:
        _display_accounts_avail(accts)
        choice_str = input("Select account (number): ").strip()
        if choice_str == basic_view.KILL_PHRASE:
            return -1
        try:
            choice_int = int(choice_str)
            return choice_int
        except:
            print(
            "{} is not an option. Select an integer between 1 and {}".format(
            choice_str, len(accts)))
            
            
def _display_accounts_avail(accts: [account.Account]) -> str:                   # Called by _select_account to display all Accounts
    '''Displays a numbered list of Accounts
    '''
    print("Available Accounts:")
    for acct_ind in range(len(accts)):
        print("   {:>3}. {}".format(acct_ind + 1, accts[acct_ind].name))
    print()


                                                                                # DISPLAYING BUDGETS
def _display_header(acct: account.Account) -> str:                              # called after the account is chosen.
    '''Prints header information 
    '''
    print("{:^80}".format(acct.name + " Budgets"))
    print(basic_view.LINE)
    if acct.is_saving:
        print("{:<35}{:<12}{:<13}{}".format(
                            "Period", "Budget", "Saved", "Remaining"))
    elif not acct.is_saving:
        print("{:<35}{:<12}{:<13}{}".format(
                            "Period", "Budget", "Spent", "Remaining"))
    print(basic_view.LINE)


def _display_budget (acct: account.Account) -> str:
    '''Displays to the screen Account information as set in Account.budgets
    '''
    _display_header(acct)
    finance_budget_view_one_month.force_attrib_recalc([acct])
    for year in acct.budgets:
        year_not_printed = True
        for month in acct.budgets[year]:
            _display_first_of_year(acct, year, month)
            if year_not_printed:
                year_not_printed = False
            else:
                _display_reg_of_year(acct, year, month)
                   

def _display_first_of_year (                                                    # Called by _display_budget
        acct: account.Account, year: int, month: int) -> str: 
    '''Prints a string representing the first budget of a year listed 
    '''
    budget_str, reached_str, remain_str, perc_remain_str = \
        _create_data_str(acct, year, month)
    print("{:<7}{:<28}{:>11}{:>13}{:>11}{:>10}".format(
        year, basic_view.MONTHS[month], budget_str, reached_str, 
        remain_str, perc_remain_str))

    
def _display_reg_of_year (                                                      # Called by _display_budget
        acct: account.Account, year: int, month: int) -> str:
    '''Prints a string representing the budget of a year listed, assuming
    that such a budget is not the first of a year
    '''
    budget_str, reached_str, remain_str, perc_remain_str = \
            _create_data_str(acct, year, month)

    print("       {:<28}{:>11}{:>13}{:>11}{:>10}".format(
        basic_view.MONTHS[month], budget_str, reached_str, 
        remain_str, perc_remain_str))


def _create_data_str (acct: account.Account, year: int, month: int
    ) -> (str, str, str, str):
    '''Returns a 4-tuple representing the string versions of attributes
    specific to the year and month of a budget belonging to an Account
    '''
    budget_info = acct.budgets[year][month]
    
    perc_remain_str = "(" + "{:.2f}".format(budget_info.perc_remain * 100)+ "%)"
    
    return (_create_indiv_str(budget_info.budget),                              # Passed to _display_first_of_year,
            _create_indiv_str(budget_info.reached),                             # _display_reg_of_year 
            _create_indiv_str(budget_info.remain),          
            perc_remain_str)


def _create_indiv_str (field: 'account.Account.budgets attribute') -> str:      # Called by _create_data_str
    '''Returns a string corresponding with an attribute's value
    '''
    if field == None:                                                           # Formatting strings doesn't work with NoneTypes,
        return "None"                                                           # and Account is initialized with NoneTypes
    else:
        return "{:10.2f}".format(field)
    

                                                                                # VIEWING SPECIFIC ACCOUNT BY ONE MONTH
def select_timefraome(inflows: cashflow.CashFlows,                              # Called by view_acct_all_months
                      outflows: cashflow.CashFlows,
                      ) -> (int, int):
    '''Returns a 2-tuple representing year and month of selected Account 
    timeframe
    '''
    year = basic_view.view_years(
                inflows.cfs, outflows.cfs, "\Years with Account")
    month = basic_view.view_months(year, inflows.cfs, outflows.cfs, 
                                       "Month with Account")
    return (year, month)                                                        # Passed to _handle_acct_choice_num,
                                                                                # view_budget_by_month to find specific budget info    

    
def view_budget_by_month (accts: [account.Account], acct_ind: int, 
               year: int, month: int) -> None:
    '''Executes code relevant to viewing budget by one month
    '''
    acct_ind = _acct_ind_in_list(accts[acct_ind - 1])
    finance_budget_view_one_month.view_specific_account(
                    acct_ind, year, month)

# Necessary to properly enter information in finance_budget_view_one_month. 
# The module calls based on one less of the returned number regardless of 
# whether the Account is a savings or expense. Thus, the value is adjusted 
# when control is given to view_specific_account.
def _acct_ind_in_list(acct: account.Account) -> int:
    '''Returns the index at which the Account is in the respective list
    '''
    if acct in finance_budget_view_one_month.BUDGETED_SAVINGS:
        return finance_budget_view_one_month.BUDGETED_SAVINGS.index(acct) + 1
    elif acct in finance_budget_view_one_month.BUDGETED_EXPENSES:
        return finance_budget_view_one_month.BUDGETED_EXPENSES.index(acct) + 1


# Required to display information completely. If any attribute in the item 
# contains a None type object, an Exception is raised. If such an item - 
# is_saving - equals None, then the interpreter returns -1 and forces the 
# user to enter valid information by accessing Option #1 and revising the
# budget and is_savings value.
def _handle_acct_choice_num(acct: account.Account, year: int, 
                            month: int) -> None or int:
    '''Appends user's choice to the appropriate list
    '''
    if acct.is_saving == None:
        print("Account not able to be accessed - must complete data (No 'None's)")
        print("Access Option 1 and revise the budget value of {}".format(acct.name))
        return -1
    if not acct.is_saving \
    and acct not in finance_budget_view_one_month.BUDGETED_EXPENSES \
    and acct.budgets[year][month].budget != None:
        finance_budget_view_one_month.BUDGETED_EXPENSES.append(acct)
    if acct.is_saving \
    and acct not in finance_budget_view_one_month.BUDGETED_SAVINGS\
    and acct.budgets[year][month].budget != None:
        finance_budget_view_one_month.BUDGETED_SAVINGS.append(acct)
