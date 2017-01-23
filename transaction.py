# transaction.py 
# Contains Transaction Class 

std_curr = "$"
import valid

class Transaction:
    def __init__(self, year, month, day, dr_acct, cr_acct, description, amount, currency=std_curr):
        """Initializes Transaction.  
        """
        self._year          = year
        self._month         = month
        self._day           = day 
        self._dr_account    = dr_acct 
        self._cr_account    = cr_acct
        self._description   = description
        self._currency      = currency
        self._amount        = amount    


    def __repr__(self):
        return 'Transaction({}, {}, {}, "{}", "{}", "{}", {}, {})'.format(
            self._year, self._month, self._day, self._dr_account, self._cr_account, self._description, 
            self._amount, repr(self._currency))
        
    
    def __eq__(self, right):
        assert type(right) == Transaction, \
        "transaction.Transaction.__eq__: Right operand is of type {} not Transaction".format(type(right))
        return repr(self) == repr(right)
    
    
    # Setters    
    def set_year(self, new_year: int) -> None:
        valid.year(new_year)
        self._year = new_year 
        
    def set_month(self, new_month: int):
        valid.month(new_month)
        self._month = new_month 

    def set_day(self, new_day: int):
        valid.day(self._year, self._month, new_day)
        self._day = new_day 

    def set_dr_account(self, account_name: str):
        valid.dr_account(account_name)
        self._dr_account = account_name
        
    def set_cr_account(self, account_name: str):
        valid.cr_account(account_name)
        self._cr_account = account_name

    def set_description(self, new_desc: str):
        valid.description(new_desc)
        self._description = new_desc 

    def set_currency(self, new_currency: str): 
        valid.currency(new_currency)
        self._currency = new_currency
        
    def set_amount(self, new_amount): 
        valid.amount(new_amount)
        self._amount = new_amount
    
    
    # Getters 
    def get_year(self):         return self._year
    def get_month(self):        return self._month 
    def get_day(self):          return self._day 
    def get_dr_account(self):   return self._dr_account 
    def get_cr_account(self):   return self._cr_account 
    def get_description(self):  return self._description 
    def get_currency(self):     return self._currency 
    def get_amount(self):       return self._amount 


    def flow(self, a):
        """Returns an indication of positive flow if the account name is 
        in line with a positive account
        """
        return 1 if self._dr_account == a else -1
        

# Testing 
if __name__ == "__main__": 
    # Checking repr
    t1 = Transaction(2015, 11, 24, "Cash", "Fast Food", 'McDonald\'s', 400)
    print(t1)
    
    t2 = Transaction(2015, 11, 24, "Cash", "Fast Food", "McDonald's", 400)
    print(t2)
    
    # Checking getters
    print(t2.get_year())
    print(t1.get_cr_account())
    print(t2.get_amount())
    
    print()
    # Checking setters 
    print(t1.get_amount())
    t1.set_amount(300)
    print(t1.get_amount())
    
    print()
    # Checking equality
    print(t1 == t2)
    