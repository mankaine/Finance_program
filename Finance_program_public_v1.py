# Finance Program v1
# Published 8 April 2016
# Author: mankaine

def header () -> str:
    '''Prints string
    '''
    fancy = 80*'-'
    print(fancy)
    print('Finance Program v1 | 8 April 2016 | Author: mankaine')
    print('A program to record your bling and cha-ching.')
    print(fancy)
    return

# Imports
from collections import namedtuple
import datetime
import math
from pathlib import Path

trans = '|{:10}|{:14}|{:29}|{}'


# Assignments
empty_list = []
Transaction = namedtuple('Transaction', 'date category description price')

main_menu ='-'*36+'MAIN MENU'+'-'*35+'''
ET: Enter list of Transactions
DT: Edit Transactions
VT: View Transactions
ST: Sort Transactions
XT: Export Transactions to a text file
ID: Import document of a Transaction list into Python
AD: Append a document of a Transaction to Transaction lists
EP: Exit Program
'''+'-'*80+'''

Your input: '''

def m_menu (TL: list) -> list:
    '''Displays main menu and interprets choice
    '''
    global main_menu
    while True:
        response = input(main_menu)
        if response == 'ET':
            TL = enter_Transaction_list(TL)
        elif response == 'DT':
            T = choose_transactions(TL)
            edit_transaction(T)
        elif response == 'VT':
            show_transactions(TL)
        elif response == 'ST':
            sort_transaction_menu(TL)
        elif response == 'XT':
            export_full(TL)
        elif response == 'ID':
            import_full(TL)
        elif response == 'AD':
            append_doc(TL)
        elif response == 'EP':
            print('EXIT: Successful.')
            return TL
        else:
            print('ERROR: Input not a choice in the menu.') 
        
# ENTER LIST OF TRANSACTIONS
### DATE
def enter_date() -> 'date':
    '''Returns date of transaction
    '''
    return input('Enter date (MM.DD.YYYY): ')

def split_date() -> 'date':
    '''Returns date formatted as date object
    '''
    d = enter_date().split('.')
    try:
        d_month = int(d[0])
        d_day = int(d[1])
        d_year = int(d[2])
        return datetime.date(d_year, d_month, d_day)
    except:
        print('ERROR: Input not in specfied format.')
    

def date_format() -> datetime.date:
    '''Returns formatted datetime.date
    '''
    try:
        d = split_date()
        return d.strftime('%m.%d.%Y')
    except AttributeError:
        print('ERROR: Unable to format because of incorrectly entered date.')
        return (datetime.date(1, 1, 1)).strftime('%m.%d.%Y')

### CATEGORY
def enter_category() -> str:
    '''Returns category of transaction
    '''
    return input('Enter category: ')

### DESCRIPTION
def enter_description() -> str:
    '''Returns description of transaction
    '''
    return input('Enter description: ')

### PRICE
def enter_price() -> str:
    '''Returns price of transaction
    '''
    try:
        return float(input('Enter price: '))
    except:
        print('ERROR: Price not entered in specified format.')
        return float(0)
    
### INPUT TRANSACTION
def enter_transaction() -> Transaction:
    '''Returns transaction
    '''
    attributes = {'Date': date_format(), 'Category': enter_category(),
                  'Description': enter_description(), 'Price': enter_price()}
    return_if_four = 0
    for i in attributes:
        if type(attributes[i]) == str or type(attributes[i]) == float:
            return_if_four += 1
        else:
            attribute_keys = list(attributes.keys())
            attribute_index = attribute_keys.index(i)
            print("ERROR:", attribute_keys[attribute_index], "is not entered correctly.",
                  "You can change it by editing Transactions under DT in the Main Menu.")
    if return_if_four == 4:
        return Transaction(attributes['Date'], attributes['Category'],
                           attributes['Description'], attributes['Price'])

def enter_Transaction_list(TL: list) -> list:
    '''Adds transactions to a list
    '''
    TL.append(enter_transaction())
    still_adding = True
    while still_adding:
        response = input('Add transaction (y or n)? ')
        if response == 'y':
            TL.append(enter_transaction())
        elif response == 'n':
            still_adding = False
            return TL
        else:
            print("ERROR: Response not 'y' or 'n'.")

# VIEW TRANSACTIONS
def show_transactions(TL: list):
    '''Prints formatted transactions
    '''
    if len(TL) > 0:
        global trans
        print(trans.format('DATE','CATEGORY','DESCRIPTION','PRICE'))
        print(trans.format('','','',''))
        for T in TL:
            print(trans.format(T.date, T.category, T.description, '$'+str(T.price)))
    else:
        print("No entries.")


# EDIT TRANSACTIONS
def show_transactions_numbered(TL: list) -> str:
    '''Shows transactions numbered
    '''
    if len(TL) > 0:
        num_trans = '|{:3d}. |{:10}|{:14}|{:29}${}'
        titles = '|{:3}|{:11}|{:14}|{:29}|{}'
        print(titles.format('NO.','DATE','CATEGORY','DESCRIPTION','PRICE'))
        print(titles.format('','','','',''))
        for i in range(len(TL)):
            print(num_trans.format(i+1, TL[i].date, TL[i].category,
                               TL[i].description, TL[i].price))
    else:
        print("No entries.")

def choose_transactions(TL: list) -> Transaction:
    '''Chooses transaction
    '''
    show_transactions_numbered(TL)
    response = int(input("Enter the number of the Transaction you would like to edit: "))
    try:
        return TL[response-1]
    except:
        print("ERROR: This transaction number does not exist.")

edit_transaction_menu = '-'*30+'''EDIT TRANSACTION MENU'''+'-'*29+'''
ED: Edit date
EC: Edit category
EE: Edit description
EP: Edit price
RM: Return to Main Menu
''' + 80*'-' + '''

Your input: '''

def edit_transaction(T: Transaction) -> Transaction:
    '''Provide a menu of possible edits to transactions,
    then interprets input
    '''
    global edit_transaction_menu
    while True:
        response = input(edit_transaction_menu)
        if response == 'ED':
            T = edit_date(T)
        elif response == 'EC':
            T = edit_category(T)
        elif response == 'EE':
            T = edit_description(T)
        elif response == 'EP':
            T = edit_price(T)
        elif response == 'RM':
            print("EXIT: Successful. Returning to Main Menu.")
            print()
            return T
        else:
            print("ERROR: Input not a listed choice.")
    

def edit_date(T: Transaction) -> Transaction:
    '''Returns an edited Transaction with new date
    '''
    T = T._replace(date = date_format())
    print("-"*32+"CHANGE CONFIRMED"+"-"*32)
    show_transactions([T])
    return T
    
def edit_category(T: Transaction) -> Transaction:
    '''Returns an edited Transaction with new category
    '''
    T = T._replace(category = enter_category())
    print("-"*32+"CHANGE CONFIRMED"+"-"*32)
    show_transactions([T])
    return T
    
def edit_description(T: Transaction) -> Transaction:
    '''Returns an edited Transaction with new description
    '''
    T = T._replace(description = enter_description())
    print("-"*32+"CHANGE CONFIRMED"+"-"*32)
    show_transactions([T])

    return T
    
def edit_price(T: Transaction) -> Transaction:
    '''Returns an edited Transaction with a new price
    '''
    T = T._replace(price = enter_price())
    print("-"*32+"CHANGE CONFIRMED"+"-"*32)
    show_transactions([T])
    return T

# ANALYSIS
s_t_menu = '-'*33+'''ANALYSIS MENU'''+'-'*32+'''
SD: Sort by date
SC: Sort by category
SE: Sort by description
SP: Sort by price
RM: Return to Main Menu
''' + 80*'-' + '''

Your input: '''
def sort_transaction_menu(TL: [Transaction]) -> None:
    '''Displays Analysis menu and records a choice
    '''
    global s_t_menu
    while True:
        response = input(s_t_menu)
        if response == 'SD':
            TL = sort_by_date(TL)
        elif response == 'SC':
            TL = sort_by_category(TL)
        elif response == 'SE':
            TL = sort_by_description(TL)
        elif response == 'SP':
            TL = sort_by_price(TL)
        else:
            print("ERROR:", response, "is an invalid choice. Try again.")

def sort_by_date (TL: [Transaction]) -> [Transaction]:
    '''Sorts list by date
    '''
    return TL.sort(key = lambda T: T.date)


def sort_by_category (TL: [Transaction]) -> [Transaction]:
    '''Sorts list by category
    '''
    return TL.sort(key = lambda T: T.category)

def sort_by_description (TL: [Transaction]) -> [Transaction]:
    '''Sorts list by description
    '''
    return TL.sort(key = lambda T: T.description)


def sort_by_price (TL: [Transaction]) -> [Transaction]:
    '''Sorts list by price
    '''
    return TL.sort(key = lambda T: T.price)

# MANAGING OTHER FILES
def filename() -> str:
    '''Asks user the name of the file to export to
    '''
    while True:
        file_name = Path(input('File name: '))
        try:
            if file_name.exists():
                return str(file_name)
            else:
                print("ERROR: File name does not exist.")
        except:
            print("ERROR: File name does not exist.")

# EXPORTING
def write_format() -> str:
    '''Writes in formatted information
    '''
    global trans
    g = input('Transaction list name: ')
    name = ('-'*(40-math.trunc(len(g)/2))+g+'-'*(40-math.trunc(len(g)/2))+'\n')
    names = (trans.format('DATE','CATEGORY','DESCRIPTION','PRICE')+'\n')
    blank = (trans.format('','','',''))
    return name+names+blank

def format_trans (T: Transaction) -> str:
    '''Write fromatted transaction
    '''
    global trans
    return trans.format(T.date, T.category, T.description, '$'+str(T.price))

def export_full (TL: list) -> None:
    '''Exports Transaction list out to the specified file
    '''
    file = open(filename(), 'a')
    try:
        file.write(write_format())
        for i in TL:
            file.write(format_trans(i))
    finally:
        file.close()

# IMPORT
def import_full (TL: [Transaction]) -> list:
    '''Imports a list of transactions into Python 
    '''
    file = filename()
    import_file = open(file, 'r')
    try:
        imported = import_file.readlines()
        for transaction in imported[3:]:
            TL.append(convert_text_to_Transaction(transaction))
        print("Import Successful.")
        show_transactions(TL)
        return TL
    finally:
        import_file.close()

def convert_text_to_Transaction(s: str) -> Transaction:
    '''Converts text to Transaction
    '''
    T_as_list = clean_up_exported(s)
    
    raw_date = T_as_list[0]
    date = convert_appended_date(raw_date)
    
    category = T_as_list[1]
    
    description = T_as_list[2]

    price = float(T_as_list[-1][1:])

    return Transaction(date, category, description, price)

def clean_up_exported (T: str) -> list:
    '''Returns a list and cleaned up version of a string
    '''
    exported_T = T.split('|')
    for element in range(len(exported_T)):
        exported_T[element] = exported_T[element].rstrip()
    return exported_T

def convert_appended_date (T: str) -> datetime.date:
    '''Returns a datetime.date object from a string
    '''
    date_elements = T.split('.')
    month = int(date_elements[0])
    day = int(date_elements[1])
    year = int(date_elements[2])
    return datetime.date(year, month, day).strftime('%m.%d.%Y')

def clean_up_text(D: list) -> 'description':
    '''Cleans up description so that it is a string
    '''
    description = ''
    for element in D:
        if type(D) == list:
            if len(D) == 1:
                description = element
            else:                
                description += (element)
                if element != D[-1]:
                    description += ' '
    return description

# APPEND
def append_doc (TL: list) -> None:
    '''Appends a list of transactions with a document full of Transactions 
    '''
    import_file = open(filename(), 'a')
    try:
        imported_TL = import_file.readlines()
        for imported_T in imported_TL:
            for T in TL:
                if format_trans(T) == imported_T:
                    TL_new = TL[TL.index(T+1):]
        for T in TL_new:
            file.write(format_trans(T))
    finally:
        file.close()
    
# EXECUTION
if __name__=='__main__':
    header()
    m_menu(empty_list)
