# finance_budget_menu.py
# by mankaine 
# August 7, 2016

# Manages and calculates information regarding user input and budgets.

from collections import namedtuple
import cashflow

Budget_Info = namedtuple(
    "Budget_Info",  ["acct_transxs",                                            # Contains transactions
                     "budget",                                                  # Budget for timeframe
                     "reached",                                                 # How close to budget
                     "remain",                                                  # budget - reached
                     "perc_remain",                                             # (budget - reached / budget) * 100%
                     "perc_reached"])                                           # (reached / budget) * 100%


class Account:
    def __init__(self):
        '''Initializes the Account class
        '''
        self.budgets = {}                                                       # contains Budget_Info for each timeframe 
        self.name = None                                                        # Name of Account
        self.is_saving = None                                                   # Whether Account is saving (True) or Expense (False)
        
    
    def update_name(self, name: str) -> None:
        '''Updates the self.name attribute
        '''
        self.name = name    
        
    def update_savings_value (self, value: bool):
        '''Updates the value of self.is_saving to the value of the parameter
        '''
        self.is_saving = value 
        
        
    def fill_transxs (self, transxs: [cashflow.CashFlow]):
        '''Updates self.budget to contain the values of the year and month
        keys
        '''
        self.budgets = {}
        
        for transx in transxs:
            if transx.year not in self.budgets:                                 # Prevents KeyError
                self.budgets[transx.year] = {}
            if transx.month not in self.budgets[transx.year]:                   # Prevents KeyError
                self.budgets[transx.year][transx.month] = Budget_Info(
                [transx], None, None, None, 0.00, 0.00)
            else:                                                               # year and month keys in self.budgets
                self.budgets[transx.year][transx.month].acct_transxs.append(
                transx)
    
    
    def update_budget (self, new_budget: float, month: int, year: int):
        '''Updates budget value
        '''
        self.budgets[year][month] = self.budgets[year][month]._replace(
            budget = new_budget)
    
    
    def recalc_acct_budget_attrib (self):                                       # Called in finance_budget_view_one_month
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
