# basic_view module.py 
 # By mankaine
# July 11, 2016

# Implements the shell user interface elements that are used by more than one module.

MONTHS = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',        # Called in finance_edit._view_transxs,
          6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October',     # finance_export.handle_export_choice,
          11: 'November', 12: 'December'}                                       # finance_export._view_months,
                                                                                # finance_export.export_transxs, and
                                                                                # finance_view.view_transxs

LINE = ('-' * 80)                                                               # Prints a line - style points!

CURRENCY = '$'                                                                  # Default currency - editable in settings.py
                                                                                # Currency not accepted in unicode? Use three 
                                                                                # letter abbreivation instead.

CF_AS_STR = {True: "+", False: '-'}                                             # Boolean to string conversion - useful when printing
                                                                                # Flows

KILL_PHRASE = "HARAMBE111"                                                      # Breaks out of loops where specified.
                                                                                # Change in settings.py


def print_loading_newline (message: str):                                       # for display
    '''Displays message, creating a new line
    '''
    print("\n========== {} ==========".format(message))


def print_loading (message: str):                                               # for display
    '''Displays message
    '''
    print('========== {} =========='.format(message))
  
    
def binary_choice (message: str, reverse: bool,                                 # for yes/no questions
        error_message_add_on: str) -> bool:
    '''Prompts a user for a yes/no choice until a yes/no choice is made. 
    Returns choice
    '''
    while True:
        user_choice = input(message).strip().lower()
        if user_choice == 'yes' and reverse == False:                           # Return True for answer in Affirmative     
            return True
        elif user_choice == 'no' and reverse == False:                          # Return False for answer in Negative
            return False
        elif user_choice == 'yes' and reverse == True:                          # Return False for answer in Affirmative
            return False
        elif user_choice == 'no' and reverse == True:                           # Return True for answer in Negative
            return True
        else:
            print("{} not an acceptable choice. Enter either 'yes' or 'no'".format(
                user_choice) + error_message_add_on)                            # If input is neither yes nor no

def menu_input(menu: str, top: int) -> int:                                     # Called in any menu function. 
    '''Prompt user for a response until a valid one is given
    '''
    print(menu)
    choice = input("Your input: ")
    if choice == KILL_PHRASE:
        return choice
    
    still_looking = True
    while still_looking:
        try:
            choice = int(choice)
        
        except:
            print('{} not among options. Reenter an integer'.format(choice))
            choice = input("Your input: ")
    
        else:
            if choice not in range(1, top):
                print('{} not among options. Try again.'.format(choice))
                choice = input("Your input: ")
            else:
                still_looking = False
                return choice
            

# view_year and view_months allow the user to focus in to the month that he 
# or she wishes to find the transaction to edit. It will prompt the user for a 
# month/year pair until a valid one is provided. 
#
# view_years calls on _collect_keys to provide a list of years. The interpreter 
# uses this list to loop through and display all the possible choices, and 
# check against a user's choice. view_months calls on _collect_month_keys, 
# which itself calls on _collect_keys; the interpreter must first determine 
# if a year represents a key within the positive and negative cash flow 
# dictionaries first, to prevent raising a KeyError. 

# Of special note is the else option in the if-else statements; the extend 
# method adds a list's elements to another and does not return anything, so 
# the list that .extend is called on must be defined first.

def _collect_keys (dict_one: dict, dict_two: dict) -> [int]:
    '''Returns the first-level keys of two dicts 
    '''
    unique_keys = []
    if dict_one == {}:
        unique_keys = list(dict_two.keys())
    elif dict_two == {}:
        unique_keys = list(dict_one.keys())
    else:
        unique_keys = list(dict_one.keys())
        for key_to_check in list(dict_two.keys()):
            if key_to_check not in unique_keys:
                unique_keys.append(key_to_check)
    return unique_keys                                                          # Prevents repreating timeframes
 

def view_years (pos_cfs: dict, neg_cfs: dict, message: str) -> int:             # view_months and this function will return
    '''Displays possible choices of year to revise transaction.                 
    Returns the year chosen
    '''                                                                         # 0 if kill phrase is input            
    unique_years = sorted(_collect_keys(pos_cfs, neg_cfs))

    print(message)       
    for year in unique_years:
        print('   {}'.format(year))

    while True:
        try:
            year_input = input("Enter year: ").strip()
            if year_input == KILL_PHRASE:
                return 0                
            
            year_input = int(year_input)
            if year_input not in unique_years:
                raise ValueError()
        except:
            print(
            "{} not acceptable entry. Enter available years.".format(
            year_input))
        else:
            return year_input                
    
            
def _collect_month_keys (year: int, dict_one: dict, dict_two: dict) -> [int]:
    '''Returns a list representing the months of a certain year in two
    dictionaries
    '''
    result = []
    if year not in dict_one:
        result = _collect_keys({}, dict_two[year])
    elif year not in dict_two:
        result = _collect_keys(dict_one[year], {})
    else:
        result = _collect_keys(dict_one[year], dict_two[year]) 
    return result


def view_months (year: int, pos_cfs: dict, neg_cfs: dict, 
        message: str) -> int: 
    '''Displays possible choices of month to revise transaction. 
    Returns the month      
    '''
    if year == 0:
        return 0
    
    unique_months = sorted(_collect_month_keys (year, pos_cfs, neg_cfs))

    print("\n{}".format(message))
    for month in unique_months:
        print('   {}. {}'.format(month, MONTHS[month]))
    
    while True:
        try:
            month_input = input("Enter month (number): ").strip()
            if month_input == KILL_PHRASE:
                return 0
            month_input = int(month_input)
            if month_input not in unique_months:
                raise ValueError()
        except:
            print(
            "{} not acceptable entry. Enter available months.".format(
            month_input))
        else:
            return month_input
