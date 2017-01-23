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
    
    
    def __setitem__(self, name, value):
        if "__init__" in self.__dict__: 
            assert (name) in self.__dict__, \
            "transaction.Transaction.__setattr__: attribute {} does not exist".format(name)
        assert "_"+name in (
            "_year", "_month", "_day", "_cr_account", "_dr_account", 
            "_description", "_currency", "_amount"), \
            "transaction.Transaction.__setitem__: {} not in self.__dict__".format("_" + name)
        if name == "day": 
            valid.day(self._year, self._month, value)
        else: 
            exec("valid." + name + "({})".format(repr(value)))
        self.__dict__["_"+name] = value
    
    
    def __getitem__(self, name): 
        assert "_"+name in self.__dict__, "_"+name
        return self.__dict__["_"+name]


    def flow(self, a):
        """Returns an indication of positive flow if the account name is 
        in line with a positive account
        """
        return 1 if self["dr_account"] == a else -1
        

# Testing 
if __name__ == "__main__": 
    # Checking repr
    t1 = Transaction(2015, 11, 24, "Cash", "Fast Food", 'McDonald\'s', 400)
    print(t1)
    
    t2 = Transaction(2015, 11, 24, "Cash", "Fast Food", "McDonald's", 400)
    print(t2)
    
    # Checking getters
    print(t2['year'])
    print(t1['cr_account'])
    print(t2['amount'])
    
    print()
    # Checking setters 
    print(t1['amount'])
    t1['amount'] = 300
    print(t1['amount'])
    
    print()
    # Checking equality
    print(t1 == t2)
    