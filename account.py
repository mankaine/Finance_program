# account.py 
# by mankaine 
# August 7, 2016
# 
# Manages and calculates information regarding user input and budgets.

from collections import namedtuple
import cashflow

# The five attributes of Budget_Info contain unique information to each 
# month and year. acct_transxs is designed to contain a list of 
# CashFlow objects whose account name is that of the Account.name. 
# budget is the budget of the Account for the month and reached represents
# how much of that budget has been spent or saved. perc_remain and 
# perc_reached represent how much has been saved/spent and remain of the budget
# as expressed in decimal form. 
Budget_Info = namedtuple(
    "Budget_Info",  ["acct_transxs", "budget", "reached", "remain", 
                     "perc_remain", "perc_reached"])


# The Account class is called by finance_budget_edit to display, process, and 
# handle changes in and decisions to view the budget values. It contains the
# name of the account - which should be an account name in the list of 
# transactions created in finance_entry or finance_edit (or an account that 
# will be created) - and the information unique to year and month. This 
# information is also sorted by year and month in the dictionary self.budgets
#  - the keys of the dictionary of the first level contains year and the 
# second level dicts contain the month number - 1 starting with January, and so on. 
class Account:
    def __init__(self):
        '''Initializes the Account class
        '''
        self.budgets = {}
        self.name = None
        self.is_saving = None
        
    
    # update_name will be handled by finance_budget_edit to update the name of the 
    # Account.
    def update_name(self, name: str) -> None:
        '''Updates the self.name attribute
        '''
        self.name = name
        
    def update_savings_value (self, value: bool):
        '''Updates the value of self.is_saving to the value of the parameter
        '''
        self.is_saving = value 
        
        
    # create_budget_placeholders will be called to create a series of year and
    # month keys, as well as placeholder values of the Budget_Info tuple that
    # contain the values unique to year and month. If updated, these values 
    # must first go through update_budget_transxs. Because the class 
    # representing positive and negative cash flows will be passed through 
    # this function, create_budget_placeholders will be called at least twice;
    # this means that conditionals need to be created at every level to 
    # prevent the values from being overwritten.
    def fill_transxs (self, transxs: [cashflow.CashFlow]):
        '''Updates self.budget to contain the values of the year and month
        keys
        '''
        self.budgets = {}
        
        for transx in transxs:
            if transx.year not in self.budgets:
                self.budgets[transx.year] = {}
            if transx.month not in self.budgets[transx.year]:
                self.budgets[transx.year][transx.month] = Budget_Info(
                [transx], None, None, None, 0.00, 0.00)
            else:
                self.budgets[transx.year][transx.month].acct_transxs.append(
                transx)
    
    
    def update_budget (self, new_budget: float, month: int, year: int):
        '''Updates budget value
        '''
        self.budgets[year][month] = self.budgets[year][month]._replace(
            budget = new_budget)
    
    
    # called in finance_budget_view_one_month
    def recalc_acct_budget_attrib (self):
        '''Forces Account object to update the amount spent/earned and percent
        attributes for each budget
        '''
        for year in self.budgets:
            for month in self.budgets[year]:
                self._recalc_reached(year, month)
                self._recalc_remain(year, month)
                self._recalc_perc(year, month)
        
        
    def _recalc_reached(self, year: int, month: int):
        '''Recalculates the amount saved/spent in an account 
        '''
        amt_reached = 0
        
        for transx in self.budgets[year][month].acct_transxs:
            amt_reached += transx.price
        self.budgets[year][month] = self.budgets[year][month]._replace(
            reached = amt_reached)
    
    
    def _recalc_remain(self, year: int, month: int):
        '''Recalculates the amount remaining in a budget for a month/year pair
        '''
        amt_remain = self.budgets[year][month].budget - \
        self.budgets[year][month].reached
        if amt_remain < 0:
            amt_remain = 0
        self.budgets[year][month] = self.budgets[year][month]._replace(
            remain = amt_remain)
    
    
    def _recalc_perc(self, year: int, month: int):
        '''Recalculates the percentage remaining in an account after total savings/
        spendings
        '''
        new_perc_reached = round(
            self.budgets[year][month].reached/self.budgets[year][month].budget,
            2)
        
        new_perc_remain = 1 - new_perc_reached
        if new_perc_remain < 0:
            new_perc_remain = 0.00
            
        self.budgets[year][month] = self.budgets[year][month]._replace(
            perc_remain = new_perc_remain, perc_reached = new_perc_reached)
        
    
    def update_is_savings(self, new_val: bool):
        '''Updates the Account's is_savings value
        '''
        self.is_saving = new_val
                 
def remove_duplicates (accts: [Account]) -> None:
    '''Removes Accounts with the same name as another Account
    '''
    acct_names_reviewed = []
    for acct in accts:
        if acct.name not in acct_names_reviewed:
            acct_names_reviewed.append(acct.name)
        else:
            accts.remove(acct)
