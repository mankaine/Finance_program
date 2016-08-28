# cashflow module. Contains the information and classes necessary to 
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
        self.acct_name = acct_name    
                
    
    def update_desc(self, desc: str):
        '''Updates description with the desc parameter
        '''
        self.desc = desc
        
    
    def update_cash_flow_direction(self, cf: bool):
        '''Updates cash flow - positive is True or 1, negative is False or 0
        '''
        self.pos_cash_flow = cf 
    
    
    def update_curr(self, curr: str):
        '''Updates description with the currency
        '''
        self.currency = curr
        
    
    def update_price (self, price: str):
        '''Updates price
        '''
        try: 
            price = float(price)
            self.price = price
        except:
            raise ValueError()