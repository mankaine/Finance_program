# valid.py 
# Library to determine validity of arguments  

from calendar import isleap 

def year(y):
    """Succeeds silently if input is of 10,000 years, zero based indexing 
    """
    assert -1 <= y <= 9999, "valid.year: {} not in range 0 to 9999 inclusive".format(y)


def month(m):
    """Succeeds silently if input is a valid month, zero based indexing 
    """
    assert -1 <= m <= 11, "valid.month: {} not in range 0 to 9999 inclusive".format(m)


def day(y, m, d): 
    """Succeeds silently if input represents a valid day of the year,
    zero based indexing  
    """
    if m in [0,2,4,6,7,9,11]: 
        assert -1 <= d <= 30, "valid.day: {} not in range 0 to 30 inclusive".format(d)
    elif m in [3,5,8,10]: 
        assert 0 <= d <= 29, "valid.day: {} not in range 0 to 29 inclusive".format(d)
    else: 
        if isleap(y+1):
            assert -1 <= d <= 28, "valid.day: {} not in range 0 to 28 inclusive".format(d)
        else: 
            assert -1 <= d <= 27, "valid.day: {} not in range 0 to 27 inclusive".format(d)

def kind(k):
    """Succeeds silently if input is in the range of Transaction type 
    codes
    
    0: Recurring Expenses
    1: Variable Expenses 
    2: Investments 
    3: Savings 
    """
    assert k in range(0,4), "valid.kind: {} not in range 0 to 4".format(k)


def name(a):
    """Succeeds silently if input is of type string
    """
    assert type(a) == str, "kind.name: " + type(a) + " is not str"
    
    
def cr_account(a):
    """Succeeds silently if input is of type string
    """
    assert type(a) == str, "kind.account: " + type(a) + " is not str"
    

def dr_account(a):
    """Succeeds silently if input is of type string
    """
    assert type(a) == str, "kind.account: " + type(a) + " is not str"

    
def description(d):
    """Succeeds silently if input is of type string
    """
    assert type(d) == str, "kind.description: " + type(d) + " is not str"
    

def currency(c):
    """Succeeds silently if input is of type string and is no more than three 
    characters 
    """ 
    assert type(c) == str, "kind.currency: "+ str(type(c)) + " is not str" 
    assert len(c) <= 3, "kind.currency: {} is not of length 3 or less".format(len(c))
    

def amount(a):
    """Succeeds silently if input is of type int. This value represents amounts of 
    money to avoid float rounding errors 
    """
    assert type(a) == int, "kind.amount: {} is not of type int".format(type(a))


def flow(f):
    """Succeeds silently if input is positive or negative one
    """
    assert f in (1, -1), "kind.flow: {} is not in (-1,1)".format(f) 


# Testing
if __name__ == "__main__": 
    year(0)
    year(9999)
    year(1000)
    try: 
        year(-4)
    except: 
        pass
    
    month(0)
    month(6)
    month(11)
    try: 
        month(-4)
    except: 
        pass
    
    day(2016, 1, 2)
    day(2016, 0, 2)
    day(2015, 0, 8)
    day(2014, 0, 5)
    try: 
        day(2016, 21, 30)
    except: 
        pass 
    
    kind(0)
    kind(1)
    kind(2)
    try :
        kind(8)
    except: 
        pass
    
    description("")
    description("5")
    description("ABC") 
    try: 
        description(5)
    except: 
        pass 
    
    dr_account("")
    cr_account("ABC")  
    try: 
        dr_account(5)
    except: 
        pass 
    
    name("")
    name("ABC")
    try: 
        name(5)
    except: 
        pass
    
    amount(100)
    amount(-100)
    amount(0)
    try: 
        amount("a")
    except: 
        pass 
    
    currency("")
    currency("$")
    currency("HKD")
    try:
        currency(1)
    except: 
        pass 
        
    flow(-1)
    flow(1)
    try: 
        flow(0)
    except: 
        pass 
