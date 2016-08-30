# finance_budget_view_one_month.py
# by mankaine
# August 11, 2016
#
# Execute code that creates a shell user interface, which will 
# enable user to view budget analysis

import cashflow
import basic_view
import account

BUDGETED_SAVINGS = []
BUDGETED_EXPENSES = []
ACCOUNT_LINE = '-' * 58

# called by finance_budget_menu
def view_acct_by_months(
    inflows: cashflow.CashFlows, outflows: cashflow.CashFlows, 
    accts: [account.Account]) -> str:
    '''Displays to user a breakdown of accounts in a month 
    '''
    _year = basic_view.view_years(
            inflows.cfs, outflows.cfs, "Years containing accounts")
    _month = basic_view.view_months(
            _year, inflows.cfs, outflows.cfs, 
            "Months containing accounts")
    if _month == 0:
        basic_view.print_loading_newline("Returning to budget menu")
        return
    
    viewing = True
    while viewing:
        force_attrib_recalc(accts)
        _display_accts(_year, _month, accts)
        
        if basic_view.binary_choice("\nView account sheets? ", False, ''):
            try:
                acct_num_str = input("Enter account number: ")
                acct_num_int = _filter_acct_num(int(acct_num_str))
            except:
                print(
                "{} is not an acceptable input. Enter an integer between 1 and {}".format(
                acct_num_str, len(BUDGETED_EXPENSES) + len(BUDGETED_SAVINGS)))
            else:
                print()
                view_specific_account(acct_num_int, _year, _month)
                viewing = basic_view.binary_choice(
                        "\nView another account sheet for {} {}? ".format(
                        basic_view.MONTHS[_month], _year), False, "")
        
        else:
            viewing = False
    
    basic_view.print_loading_newline("Returning to budget menu")
        
def _filter_acct_num(acct_num: int) -> int:
    '''Continues to loop through a question asking for an integer that represents
    an Account in a list. Returns the appropriate integer if a valid number is chosen 
    and prints an error message otherwise, without raising an error
    '''
    while True:
        if 0 < acct_num <= len(BUDGETED_EXPENSES) + len(BUDGETED_SAVINGS):
            return acct_num 
        else:
            raise Exception

def view_specific_account(acct_num: int, year: int, month: int) -> str:
    print(acct_num)
    if acct_num <= len(BUDGETED_SAVINGS):
        _display_savings_acct(BUDGETED_SAVINGS[acct_num - 1], year, month)
    elif acct_num > len(BUDGETED_SAVINGS):
        print(BUDGETED_EXPENSES)
        _display_expenses_acct(
                BUDGETED_EXPENSES[acct_num - (1 + len(BUDGETED_SAVINGS))], 
                year, month)
        
        
def _display_savings_acct(
    acct: account.Account, year: int, month: int) -> str:
    '''Displays specified saving Account 
    '''
    _print_acct_header(acct, year, month)
    _print_acct_transxs(acct, year, month)
    print("{:48}${:9.2f}".format("Total amount remaining to save:", 
        acct.budgets[year][month].remain))
    
    print("{:48}{:10}".format(" " * 48, "=========="))
    print("{:43}{:7.2f}% {:>6}".format(" " * 43, 
        (100 * acct.budgets[year][month].perc_reached), "SAVED"))
    print("{:43}{:7.2f}% {:6}".format(" " * 43, 
        (100 * acct.budgets[year][month].perc_remain), "REMAIN"))


def _display_expenses_acct(
    acct: account.Account, year: int, month: int) -> str:
    '''Displays specified expense Account
    '''
    _print_acct_header(acct, year, month)
    try:
        _print_acct_transxs(acct, year, month)
        if acct.budgets[year][month].remain >= 0:
            _display_under_budget_expense(acct, year, month)
        else:
            _display_over_budget_expense (acct, year, month)
    except Exception as e:
        print("Insufficient information to display rest of {}: {}".format(
            acct.name, e))


def _display_under_budget_expense(
    acct: account.Account, year: int, month: int) -> str:
    '''Displays an expense Account summary under budget
    '''
    print("{:48}${:9.2f}".format("Total amount remaining:", 
                acct.budgets[year][month].remain))
    
    print("{:48}{:10}".format((" " * 48), '=========='))
    
    print("{:43}{:7.2f}% {:>6}".format('-' * 43, 
            (100 * acct.budgets[year][month].perc_reached), "SPENT"))
    print("{:43}{:7.2f}% {:6}".format('-' * 43,
            (100 * acct.budgets[year][month].perc_remain), "REMAIN"))


def _display_over_budget_expense(
    acct: account.Account, year: int, month: int) -> str:
    '''Displays an expense Account summary over budget
    '''
    print("{:48}${:.2f}".format("Amount over budget:", abs(
        acct.budgets[year][month].budget - acct.budgets[year][month].reached)))
            
    print("{:48}{:10}".format((" " * 48), '=========='))
    
    print("{:43}{:7.2f}% {:>6}".format('-' * 43, 
            (100 * acct.budgets[year][month].perc_reached), "SPENT"))
    print("{:43}{:7.2f}% {:6}".format('-' * 43,
            (100 * acct.budgets[year][month].perc_remain), "REMAIN"))


def _print_acct_header(
    acct: account.Account, year: int, month: int) -> str:
    '''Prints header for Account sheet
    '''
    print(ACCOUNT_LINE)
    print("{:^58}".format(acct.name + " Account"))
    print(ACCOUNT_LINE)
    print("{:^58}".format((
        basic_view.MONTHS[month] + " " + str(year) + " Budget")))
    print(ACCOUNT_LINE)
    print("{:6}{:41}${:9.2f}".format(
        "BUDGET", '.' * 42, acct.budgets[year][month].budget))


def _print_acct_transxs (
    acct: account.Account, year: int, month: int) -> str:
    '''Prints transactions related to an Account
    '''
    print("      {:5}{:25}{:6}".format("Date", "Description", "Amount"))
    print('      {}'.format("-" * 40))
    
    for transx in acct.budgets[year][month].acct_transxs:
        formatted_amt = '(' + '{:.2f}'.format(transx.price) + ')'
        print("      {:^5}{:25}{:10}".format(transx.day,
            transx.desc, formatted_amt))
     

def _display_accts (
    year: int, month: int, accts: [account.Account]) -> str:
    '''Prints budgets of accounts in a month/year
    '''    
    _print_month_acct_header(year, month)
    _print_savings_accts(accts, year, month)
    _print_expenses_accts(
            accts, year, month, len(BUDGETED_SAVINGS))
    _print_nonsorted_accts(accts, year, month)


def force_attrib_recalc (accts: [account.Account]) -> None:
    '''Forces Account object to update the amount spent/earned and percent 
    attributes for each budget
    '''
    for acct in accts:
        try:
            acct.recalc_acct_budget_attrib()
        except:
            continue


def _print_month_acct_header(year: int, month: int) -> str:
    '''Prints formatted header for month and year of budget
    accounts
    '''
    print(basic_view.LINE)
    print("{:^80}".format("Account Budgets"))
    print(basic_view.LINE)
    print("{:^80}".format((basic_view.MONTHS[month] + ' ' + str(year))))
    print(basic_view.LINE)
    print("{:4}{:32}{:14}{:10}{}".format(
            "No.", "Account Name", "Budget", "Spent", "Remaining"))
    print(basic_view.LINE)


def _print_savings_accts(
    accts: [account.Account], year: int, month: int) -> str:
    '''Prints a series of strings containing information about an
    Account for a specified month and year under the assumption 
    that those Accounts are savings
    '''
    print("{:^80}".format("Savings"))
    print(basic_view.LINE)
    
    for acct in accts:
        if acct.is_saving and acct not in BUDGETED_SAVINGS \
        and acct.budgets[year][month].budget != None:
            BUDGETED_SAVINGS.append(acct)
    
    num_on_list = 0
    for acct in BUDGETED_SAVINGS:
        num_on_list += 1
        _print_acct_info(acct, year, month, num_on_list)


def _print_expenses_accts(
    accts: [account.Account], year: int, month: int, int_boost: int) -> str:
    '''Prints a series of strings containing information about an
    Account for a specified month and year, assuming those Accounts
    are not savings 
    '''
    print("{:^80}".format("Expenses"))
    print(basic_view.LINE)
    
    for acct in accts:
        if not acct.is_saving and acct not in BUDGETED_EXPENSES \
        and acct.budgets[year][month].budget != None:
            BUDGETED_EXPENSES.append(acct)
    
    num_on_list = int_boost
    for acct in BUDGETED_EXPENSES: 
        num_on_list += 1
        _print_acct_info(acct, year, month, num_on_list)
            

def _print_nonsorted_accts(
    accts: [account.Account], year: int, month: int) -> str:
    '''Prints message that Account has not been labeled as a saving or expense
    '''
    print("{:^80}".format("Unsorted Accounts"))
    print(basic_view.LINE)
    
    for acct in accts:
        if (acct not in BUDGETED_EXPENSES) and (acct not in BUDGETED_SAVINGS):
            print("     {:27}{:14}{:14.2f}".format(
                acct.name, (" " * 14), acct.budgets[year][month].reached))
            

def _print_acct_info(
    acct: account.Account, year: int, month: int, num_on_list: int) -> str:
    '''Prints a single line of budget information: title, budget, reached, 
    remaining, and percentage remaining
    '''
    try:
        print("{:3}. {:27}{:14.2f}{:14.2f}{:9.2f} ({:7.2f}%)".format(
            num_on_list, acct.name,
            acct.budgets[year][month].budget,
            acct.budgets[year][month].reached,
            acct.budgets[year][month].remain,
            acct.budgets[year][month].perc_remain * 100))
    except:
        print("{:^80}".format("Insufficient information to display {}".format(
            acct.name)))
