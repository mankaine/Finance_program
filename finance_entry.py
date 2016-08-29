# enter_transaction module. Enables user to input transactions in the 
# shell as part of the user interface.
# By mankaine
# July 12, 2016

import cashflow
import basic_view
import finance_edit


# ENTERING TRANSACTION ########################################################
# handle_choice_one is the first function that enter_transaction implements. It 
# contains all the monthly and individual transaction entry functions, and prompts
# the user to choose between the two until the user indicates that he or she no longer
# wishes to enter such information. After the function finishes looping through the 
# individual or monthly transactions, the function prompts the user whether to continue,
# and determines if that choice is valid. It will continue prompting for that choice
# until a valid one is made. 
def handle_entry_choice (inflows: cashflow.CashFlows, outflows: cashflow.CashFlows) -> None:
    '''Prompts user to choose whether to enter transactions by month 
    or individually, and filters choices
    '''
    entering_pace = True
    while entering_pace:
        pace = input("Enter [i]ndividually or by [m]onth? ").strip()
        if pace == 'i':
            _enter_indiv_entry_loop(inflows, outflows)
            entering_pace = False
        elif pace == 'm':
            _entries_in_month_loop(inflows, outflows)
            entering_pace = False
        elif pace == basic_view.KILL_PHRASE:
            basic_view.print_loading_newline("RETURNING TO MAIN MENU")
            break
        else:
            print('{} is an invalid choice. Choose either i or m'.format(pace))


# enter_year, enter_month, and enter_day all construct a Transaction class
# to check if the input is within range without having to construct a Revenue
# or Expense class.
def enter_year () -> int:
    '''Prompts user for a valid year
    '''
    entering = True
    while entering:
        trans = cashflow.CashFlow()
        try:
            year = (input("Year: ").strip())
            if year == basic_view.KILL_PHRASE:
                return -1
            trans.update_year(year)
        except:
            print("""{} outside of the acceptable range for year entries. 
            Enter integer between 1 and 9999.\n""".format(year))
        else:
            return int(year)
    
    
def enter_month() -> int:
    '''Prompts user for a valid month
    '''
    entering = True
    while entering:
        trans = cashflow.CashFlow()
        try:
            month = (input("Month (number): ").strip())
            if month == basic_view.KILL_PHRASE:
                return -1
            trans.update_month(month)
        except:
            print("""{} outside of the acceptable range for month entries. 
            Enter integer between 1 and 12.\n""".format(month))
        else:
            return int(month)         
        
        
def enter_day() -> int:
    '''Prompts user for a valid day
    '''
    entering = True
    while entering:
        trans = cashflow.CashFlow()
        try:
            day = (input("Day: ").strip())
            if day == basic_view.KILL_PHRASE:
                return -1
            trans.update_day(day)
        except: 
            print("{} outside of the acceptable range. Try again.\n".format(
                                                                    day))
        else:
            return int(day)


def enter_price() -> int:
    '''Prompts user for a valid price
    '''
    entering = True
    while entering:
        trans = cashflow.CashFlow()
        try: 
            price = input("Price: ").strip()
            if price == basic_view.KILL_PHRASE:
                return -1
            trans.update_price(price)
        except:
            print("{} not an option. Try again.\n".format(price))
        else:
            return float(price)
        
        
## ENTERING INDIVIDUAL TRANSACTIONS ###########################################
# After printing a confirmation message, _enter_indiv_entry_loop will prompt user
# for information to enter an individual revenue or expense. This is included
# in the function _enter_indiv_entry. Afterward, it will prompt user to continue, 
# and for both questions will continuously prompt the question until a valid 
# answer is provided. 
def _enter_indiv_entry_loop (inflows: cashflow.CashFlow, outflows: cashflow.CashFlow) -> None:
    '''Prompts a loop for user to enter transactions individually, without specific 
    regard to month. Appends them to a dictionary
    '''
    basic_view.print_loading_newline("Entering by individual transaction")
    
    entering = True
    while entering:
        transx = _enter_indiv_entry()
        if transx == None:
            break
        elif transx.pos_cash_flow:
            inflows.insert_cf(transx)
        else:
            outflows.insert_cf(transx)         
        _view_transx(transx, inflows, outflows)
        
        entering = basic_view.binary_choice(
            "Enter new transaction? ", False, '')

# Each individual aspect of the transaction prompts the user to enter the relevant information,
# updates the value of the Transaction object created in each Revenue or Expense, and then the
# Revenue or Expense object itself. This redundancy updates the memory reference. When the 
# transaction is completely entered, it is appended to the appropriate list of Revenue or Expense
# objects and allowed to be viwed by the user using _view_trans. The function 
# _enter_indiv_entry will return None if the user decides to execute the 
# kill phrase. 

def _enter_indiv_entry () -> cashflow.CashFlow or None:
    '''Prompts user to enter an individual journal entry to create a new
    Transaction object. Returns that object.
    '''
    basic_view.print_loading_newline("Journalizing New Entry")
    
    cash_flow = cashflow.CashFlow()

    cf_dir = _enter_cf_dir()
    if cf_dir == None:
        return
    cash_flow.update_cash_flow_direction(cf_dir)
    print()     
    
    year = enter_year()
    if year == -1:
        return
    cash_flow.update_year(year)
    
    month = enter_month()
    if month == -1: 
        return
    cash_flow.update_month(month)
    
    day = enter_day()
    if day == -1:
        return
    cash_flow.update_day(day)
    cash_flow.update_date()
    print() 
    
    acct = input("Account: ").strip()
    if acct == "":
        return 
    cash_flow.update_acct(acct)
      
    desc = input("Description: ").strip()
    if desc == "":
        return
    cash_flow.update_desc(desc) 
    print() 
    
    fncl_amt = enter_price()
    if fncl_amt == -1:
        return 
    cash_flow.update_price(fncl_amt)
    
    return cash_flow
                
        
## ENTERING TRANSACTIONS BY MONTH #############################################
# _enter_month_entry is formatted similar to _enter_indiv_entry_loop, save that 
# the former implements year and month entry before calling functions
# enter_month_revenue and enter_month_expense. 
def _entries_in_month_loop (inflows: cashflow.CashFlow, outflows: cashflow.CashFlow) -> None:
    '''Prompts user to enter transactions all occuring in the specified 
    month and year
    '''
    basic_view.print_loading_newline("Entering by month")
    
    year = enter_year()
    month = enter_month()

    entering_transx = True
    basic_view.print_loading("Entering Transactions for the Year {}, Month {}".format(year, month))
    
    while entering_transx:
        basic_view.print_loading("Entering New Transaction")
        cf_direction_pos = _enter_cf_dir()
        if cf_direction_pos:
            transx = _enter_month_transx(year, month, cf_direction_pos)
            inflows.insert_cf(transx)
        else:
            transx = _enter_month_transx(year, month, cf_direction_pos)
            outflows.insert_cf(transx)
        _view_transx(transx, inflows, outflows)
       
        entering_transx = basic_view.binary_choice(
            ("Enter new transaction for month {}, year {}? ".format(month, year)), False, '\n')
        if entering_transx == False:
            basic_view.print_loading_newline("RETURNING TO MAIN MENU")


def _enter_cf_dir () -> bool:
    '''Returns a boolean representing a cash flow direction
    '''
    while True:
        cf_question = input("Cash flow: [p]ositive or [n]egative? ").strip()
        if cf_question == 'p':
            return True
        elif cf_question == 'n':
            return False
        elif cf_question == basic_view.KILL_PHRASE:
            return None
        else:
            print("{} not an option. Select either 'p' or 'n'\n".format(cf_question))
    

def _enter_month_transx(year: int, month: int, cf_dir: bool) -> cashflow.CashFlow:
    '''Enters transaction based on month, year, and cash flow
    '''
    cash_flow = cashflow.CashFlow()
    cash_flow.update_cash_flow_direction(cf_dir)
    print()  
    day = enter_day()
    cash_flow.update_year(year) 
    cash_flow.update_month(month)
    cash_flow.update_day(day)
    cash_flow.update_date()
    print() 
    acct = input("Account: ").strip()
    cash_flow.update_acct(acct)      
    desc = input("Description: ").strip()
    cash_flow.update_desc(desc)
    print() 
    fncl_amt = enter_price()
    cash_flow.update_price(fncl_amt)
        
    return cash_flow        

    
# ## VIEWING TRANSACTIONS #######################################################
# # After each transaction has been made, it must be reviewed for edits. 
# # _view_trans allows the user to check over the transaction and ensure 
# # that it has been properly entered. If not, it enables the user to edit it, 
# # passing editing responsibilities off to a function in another module.
def _view_transx (
    cf: cashflow.CashFlow, inflows: cashflow.CashFlows, 
    outflows:cashflow.CashFlows) -> str:
    '''Displays formatted transaction
    '''
    cf_symbol = basic_view.CF_AS_STR[cf.pos_cash_flow]
    
    print("\nUpdated transaction:")
    print("{:12} {:10} {:20} {:20}  {:10} {}".format(
          "Attribute:", "Date", "Account", "Description", "Price", "Flow"))
    print("{:12} {:2}/{:2}/{:4} {:20} {:20} {}{:10.2f} {}".format(
          "Information:", cf.month, cf.day, cf.year, cf.acct_name,
          cf.desc, cf.currency, cf.price, cf_symbol ))

    edit_needed = basic_view.binary_choice("\nEdit transaction? ", False, '') 
    if edit_needed:
        finance_edit.handle_edit(cf, inflows, outflows)