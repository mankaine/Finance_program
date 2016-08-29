# settings.py
# by mankaine
# August 26, 2016

# User interface that enables edit to settings
import basic_view

setting_menu = """
1. Change Currency
2. Change Cancel Phrase
3. View Credits
4. Return to Main Menu
"""

def _setting_menu_options(choice: int):
    '''Handles control flow to a function depending on user input
    '''
    if choice == 1:
        basic_view.print_loading_newline("Updating currency")
        basic_view.CURRENCY = _update_base_currency()
    elif choice == 2:
        basic_view.print_loading_newline("Updating New Break Phrase")
        basic_view.KILL_PHRASE = _handle_new_kill_phrase()
    elif choice == 3:
        print(user_cred)
    elif choice == 4:
        basic_view.print_loading_newline("RETURNING TO MAIN MENU")
    pass


# Option 1
new_curr_explained = """
The new value to be entered must be no longer than three characters long. It 
will represent the currency name/symbol that is used when recording future 
transactions (by default, the Currency value is the U.S. Dollar ($))
"""

def _update_base_currency() -> str:
    '''Updates the base currency used when creating new transactions
    '''
    print(new_curr_explained)
    while True:
        print("Current value: {}".format(basic_view.CURRENCY))
        new_c = input("Enter new currency: ").strip()
        if new_c == basic_view.KILL_PHRASE:
            return basic_view.CURRENCY 
        elif len(new_c) > 3:
            print("Entered currency is greater than length 3. Reenter currency")
        else:
            print("Updated value: {}".format(new_c))
            return new_c


# Option 2
kill_phrase_explained = """
The break phrase is used to exit out of any menu and the majority of options in
the Finance Program. Enter a phrase that contains at least three numbers and
at least five other characters
"""

def _handle_new_kill_phrase() -> str:
    '''Prompts user for a new kill phrase.
    '''
    print(kill_phrase_explained)
    while True:
        print("Current value: {}".format(basic_view.KILL_PHRASE))
        new_kp = input("Enter new kill phrase: ").strip()
        if new_kp == basic_view.KILL_PHRASE:
            print("Initial Kill Phrase selected")
            return new_kp
        
        elif len(new_kp) >= 8:
            num_amt = 0
            for char in new_kp:
                if char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
                    num_amt += 1
           
            if num_amt < 3:
                print(
                "Insufficient amount of numbers in suggested break phrase.", 
                "Please enter at least 3")
            else:
                print("Updated value: {}".format(new_kp))
                return new_kp


# Option 3
user_cred = """
Program made by William Khaine
Summer 2016
Independent Project
Version 1.0.1
"""


def run_setting_interface():
    '''Runs setting Interface
    '''
    acessing_settings = True
    while acessing_settings:
        choice = basic_view.menu_input(setting_menu, 5)
        _setting_menu_options(choice)
        if choice in [4, basic_view.KILL_PHRASE]:
            acessing_settings = False
 
