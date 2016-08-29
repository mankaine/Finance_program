# cashflow.py
# By mankaine

# July 2016

# Contains the information and classes necessary to 
# produce positive and negative cash flow.

class OutsideYearRange(Exception):
    pass

class OutsideMonthRange(Exception):
    pass

class OutsideDayRange(Exception):
    pass

class OutsideAccountRange(Exception):
    pass

ACCOUNT_INDEX = {}

from datetime import date
import basic_view

class CashFlows:
    def __init__(self):
        '''Initializes the CashFlows class.
        '''
        self.cfs = {}
        self.budget = {}
        self.total = 0
    
    
    def insert_cf (self, cf: "CashFlow"):
        '''Inserts a Cash Flow object as the appropriate value in a dictionary
        '''
        if cf.year not in self.cfs:
            self.cfs[cf.year] = {}
        if cf.month not in self.cfs[cf.year]:
            self.cfs[cf.year][cf.month] = []
        if cf not in self.cfs[cf.year][cf.month]:
            self.cfs[cf.year][cf.month].append(cf)
            
            
    def insert_cfs(self, cfs: 'CashFlow'):
        '''Inserts a list of CashFlow objects as appropriate values in a dictionary
        '''
        for cf in cfs:
            self.insert_cf(cf)


    def update_cfs_total (self):
        '''Updates the total sum of cash flows
        '''
        self.total = 0
        for year in self.cfs:
            for month in self.cfs[year]:
                for cf in self.cfs[year][month]:
                    self.total += cf.price
                    

    def calc_acct_total (self, acct: str):
        '''Calculates the total of an account
        '''
        acct_total = 0
        for year in self.cfs:
            for month in self.cfs[year]:
                for cf in self.cfs[year][month]:
                    if acct == 'ALL':
                        acct_total += cf.price
                    elif cf.acct_name == acct:
                        acct_total += cf.price
        return acct_total
                        
                        
    def return_year_month_total (self, year: int, month: int):
        '''Returns the sum of transactions occuring in year/month pair
        '''
        total_in_timeframe = 0 
        for cf in self.cfs[year][month]:
            total_in_timeframe += cf.price
        return total_in_timeframe
    
    
    def filter_transx_flows (self, flow_to_keep: bool) -> ["CashFlow"]:
        '''Removes CashFlow objects that are opposite of what
        the CashFlows object should be. Saves those removed to a list,
        which is returned
        '''
        flows_filtered_out = {}
        for year in self.cfs:
            for month in self.cfs[year]:
                for cf in self.cfs[year][month]:
                    if cf.pos_cash_flow != flow_to_keep:
                        self.cfs[year][month].remove(cf)
                        flows_filtered_out = _add_transx_to_dict(
                                        flows_filtered_out, cf)
        return flows_filtered_out
    
    
    def resort_dicts_by_date (self):
        transxs_to_resort = {}
        year_to_clean = 0
        month_to_clean = 0
        
        for year in self.cfs:
            for month in self.cfs[year]:
                for cf in self.cfs[year][month]:
                    
                    # transaction is not in the right dictionary according to year
                    if cf.year != year: 
                        year_to_clean = year
                        transxs_to_resort = _add_transx_to_dict(
                            transxs_to_resort, cf)
                        self.cfs[year][month].remove(cf)
                    
                    # trans. is not in the right list according to month
                    elif cf.month != month: 
                        year_to_clean, month_to_clean = year, month
                        transxs_to_resort = _add_transx_to_dict(
                            transxs_to_resort, cf)
                        self.cfs[year][month].remove(cf)
        
        self._clean_dicts(year_to_clean, month_to_clean)
        return transxs_to_resort
    
    
    def merge_dicts (self, dict_to_merge: dict) -> None:
        '''Merges the dictionary in the argument with the CashFlows dict
        '''
        for year in dict_to_merge:
            if year not in self.cfs:
                self.cfs[year] = {}
            for month in dict_to_merge[year]:
                if month not in self.cfs[year]:
                    self.cfs[year][month] = []
                self.cfs[year][month].extend(dict_to_merge[year][month])
                
                
    # Called in resort_dicts_by_date to remove any empty data structures. 
    # Done to prevent faulty display when calling basic_view.view_years 
    # and .view_months
    def _clean_dicts(self, year: int, month: int):
        '''Removes all empty dicts and lists from the CashFlows dictionary 
        '''
        if month != 0:
            if year in self.cfs:
                if self.cfs[year][month] == []:
                    self.cfs[year].pop(month)
        if year != 0:
            if self.cfs[year] == {}:
                self.cfs.pop(year)
        
                
# Called by filter_transx_flows to return a dictionary needed to contain
# past and new transactions that do not have the appropriate cash flow
def _add_transx_to_dict (init_dict: dict, transx: "CashFlow") -> dict:
    '''Returns a dictionary that contains the new transaction
    '''
    if transx.year not in init_dict:
        init_dict[transx.year] = {}
    if transx.month not in init_dict[transx.year]:
        init_dict[transx.year][transx.month] = []
    init_dict[transx.year][transx.month].append(transx)
    return init_dict


class CashFlow:
    def __init__(self):
        '''Initializes the PositiveCashFlow class. 
        '''
        self.year = 1
        self.month = 1
        self.day = 1
        self.date = date(self.year, self.month, self.day)

        self.acct_name = None
        
        self.desc = None

        self.pos_cash_flow = None
        self.currency = basic_view.CURRENCY
        self.price = 0


    # The following three methods change the year, month, and day. If the input is outside
    # of the acceptable range, the relevant error is raised.  
    def update_year (self, year: str):
        '''Changes the year parameter of the date. If the year is above or below the 
        acceptable date, an OutsideYearRange Error is raised.
        '''
        try: 
            if year == basic_view.KILL_PHRASE:
                self.year = -1
            year = int(year)
        except:
            raise OutsideYearRange()
        else:
            if year < 0 or year > 9999:
                raise OutsideYearRange()
            else:
                self.year = year


    def update_month (self, month: str):
        '''Changes the month parameter of the date. If the month is above or below the 
        acceptable date, an OutsideMonthRange Error is raised.
        '''
        try:
            if month == basic_view.KILL_PHRASE:
                self.month = -1
            month = int(month)
        except:
            raise OutsideMonthRange()
        else:
            if month < 0 or month > 12:
                raise OutsideMonthRange()
            else:
                self.month = month


    # change_day follows leap year rules: if the year is evenly divisible by 4 or 400, but 
    # not by 100, 29 days are in February. Otherwise, the month has 28 days.
    def update_day (self, day: str):
        '''Changes the day parameter of the date. If the day is above or below the acceptable
        date, an OutsideDayRange Error is raised.
        '''
        try:
            if day == basic_view.KILL_PHRASE:
                self.day = -1
            day = int(day)
        except:
            raise OutsideDayRange("{} is not an integer".format(day))   
        else:
            if self.month in [4, 6, 9, 11] and (day < 1 or day > 30): 
                # April, June, September, November
                raise OutsideDayRange(
                ("""date {} for the month of April, June, September, 
                or November is under 1 or over 31""".format(day)))
            elif self.month in [1, 3, 5, 7, 8, 10] and (day < 1 or day > 31): 
                # January, March, May, July, August, October
                raise OutsideDayRange(
                ("""date {} for the month of January, March, May, July, August,
                 or October is under 1 or over 31""".format(day)))
            elif self.month == 2: 
                # February
                if (self.year % 400 == 0 or self.year % 4 == 0) and self.year % 100 != 0 \
                and (day < 1 or day > 29):
                    raise OutsideDayRange(
                    ("""date {} for the month of February, 
                    leap year {} is under 1 or over 29""".format(day, self.year)))
                elif (self.year % 4 != 0) and (day < 1 or day > 28):
                    raise OutsideDayRange(
                    ("""date {} for the month of February, 
                    year {} is under 1 or over 28""".format(day, self.year)))

            self.day = day
                
    
    # return_date processes the date and returns it as a datetime object.
    def update_date (self):
        '''Updates and Returns date using the saved year, month, and date values
        '''
        self.date = date(self.year, self.month, self.day)
    
    
    # The following methods are called whenever the interface prompts the user for the 
    # appropriate change. The corresponding function in finance_entry calls the user to 
    # enter a number from an index of accounts. 
    def update_acct (self, acct_name: str):
        '''Updates account with the account parameter
        '''
        if acct_name == basic_view.KILL_PHRASE:
            self.acct_name = ""
        else:
            self.acct_name = acct_name    
                
    
    def update_desc(self, desc: str):
        '''Updates description with the desc parameter
        '''
        if desc == basic_view.KILL_PHRASE:
            self.desc = ""
        else:
            self.desc = desc
        
    
    def update_cash_flow_direction(self, flow: bool):
        '''Updates cash flow - positive is True or 1, negative is False or 0
        '''
        if flow == basic_view.KILL_PHRASE:
            self.pos_cash_flow = None
        else:
            self.pos_cash_flow = flow 
    
    
    def update_curr(self, curr: str):
        '''Updates description with the currency
        '''
        self.currency = curr
        
    
    def update_price (self, price: str):
        '''Updates price
        '''
        try: 
            if price == basic_view.KILL_PHRASE:
                price = -1
            else:
                price = float(price)
                self.price = price
        except:
            raise ValueError()
