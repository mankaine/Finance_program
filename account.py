# account.py 
# Contains Account class 

from transaction import Transaction
from collections import namedtuple, defaultdict
import valid

Budget = namedtuple("Budget", "goal reached ts_amt")
# goal:        amount of money planned to be saved/spent 
# reached:     amount of money saved/spent 
# ts_amt:      Number of Transactions that have the same Account name, year, and month 


class Account:
    @staticmethod 
    def _cond(y,m,t): return t.get_year() == y and t.get_month() == m
    
     
    def __init__(self, name: str, kind, ts: [Transaction], budgets):
        self._name      = name 
        self._kind      = kind 
        self._ts        = ts 
        self._budgets   = budgets 
        
        self._fill_budgets(self._sum_transxs())
        

    def __eq__(self, right):
        """Equality method. Returns True if the type of right is an Account and has 
        identical attribute values. 
        """
        assert type(right) == Account, \
            "Account.__eq__: type of other operand {} is {}, not Account".format(
                right, type(right))
        return repr(self) == repr(right) 
    
    
    def __lt__(self, right):
        """Returns True if the name and savings variables are the same, and all transactions of 
        the self are a subset of the other
        """ 
        assert type(right) == Account, \
            "Account.__eq__: type of other operand {} is {}, not Account".format(
                right, type(right))
        name    = self._name == right.get_name()
        kind    = self._kind == right.get_kind()
        return name and kind and all(i in right.get_ts() for i in self._ts)

    
    def __repr__(self):
        return "Account({},{},{},{})".format(
            repr(self._name),self._kind,self._ts, self._budgets)
    
    
    def __contains__(self, item):
        """Contains method: Returns True if item is a Transaction object and in the 
        collection of Transactions. Also returns True if an item is a tuple and 
        matches up with a budget
        """
        assert type(item) in (Transaction, tuple), \
            "Account.__contains__: type of item {} is {}, not Transaction or tuple".format(
            item, type(item))
        if type(item) == Transaction: 
            return any(item == j for j in self._ts)
        else:
            return any(item == self._budgets[y][m] for y in self._budgets for m in self._budgets[y]) 

    
    def _sum_transxs(self):
        """Returns the sum of sorted transactions 
        """
        d = defaultdict(dict)
        for t in self._ts: 
            y, m = t.get_year(), t.get_month()
            if m not in d[y]: 
                d[y][m] = (t.get_amount()*t.flow(self._name))
            else: 
                d[y][m] += (t.get_amount()*t.flow(self._name))
        return d 
        
        
    def _fill_budgets(self, d):
        """Fills in Budgets that are not provided
        """
        for y in d: 
            for m in d[y]:  
                if y not in self._budgets:
                    self._budgets[y] = dict()
                if m not in self._budgets[y]: 
                    self._budgets[y][m] = Budget(
                        d[y][m], d[y][m], 
                        len([i for i in self._ts if Account._cond(y,m,i)]))
                
    
    def _revise_budget(self, y, m):
        """Changes the budget of a year and month
        """
        ts = [i.get_amount()*i.flow(self._name) for i in self._ts if Account._cond(y,m,i)]
        self._budgets[y][m] = Budget(
            sum(ts), self._budgets[y][m].reached, len(ts))


    def add(self, t):
        assert type(t) == Transaction, \
            "account.Account.add_t: {} is not type Transaction".format(type(t))
        self._ts.append(t)
        self._revise_budget(t.get_year(), t.get_month())
    
    
    def update_all_reached(self):
        """Updates all reached attributes
        """
        for y in self._budgets:
            for m in self._budgets[y]:
                self.set_reached(
                    y, m, sum(t.get_amount() for t in self._ts if Account._cond(y,m,t) ))
    
    
    def remove_empty_budgets(self):
        """Removes all Account Budget values that do not correspond 
        to any Transactions  
        """
        _budgets_without_empties = defaultdict(dict) 
        for y in self._budgets: 
            for m in self._budgets[y]:
                _ts_amt = [t for t in self._ts if Account._cond(y,m,t)]
                if _ts_amt != 0:
                    _budgets_without_empties[y][m] = Budget(
                        self.get_goal(y,m), self.get_reached(y,m), _ts_amt)
        self.set_budgets(_budgets_without_empties) 
                     
    
    
    # Setters 
    def set_name(self, new_name: str):
        valid.name(new_name)
        self._name = new_name 
        
    def set_kind(self, new_kind: int):
        valid.kind(new_kind)
        self._kind = new_kind
        
    def set_budgets(self, new_budgets: dict):
        valid.budgets(new_budgets)
        self._budgets = new_budgets
    
    def set_reached(self, y: int, m: int, v: float):
        valid.amount(v)
        self._budgets[y][m] = Budget(self.get_goal(y,m), v, self.get_ts_amt(y,m))
    
    def set_goal(self, y: int, m: int, v: float):
        valid.amount(v)
        self._budgets[y][m] = Budget(v, self.get_reached(y,m), self.get_ts_amt(y,m))
        
    
    # Analysis of Account
    def sum_remain(self, y: int, m: int) -> float:                              
        '''Returns remaining amount of funds for Account given month and year
        '''
        l, s = self.get_goal(y,m), self.get_reached(y,m)
        if (l < 0 and s < 0) or (l > 0 and s > 0): 
            return l - s 
        return l + s
         
         
    def perc_reached(self, y: int, m: int) -> float:
        '''Returns how much was spent in a given month as a percentage of budget
        '''
        return self.get_reached(y,m) / self.get_goal(y,m)
    
    
    def perc_remain(self, y: int, m: int) -> float: 
        '''Returns how much remains in Account given month and year, as percentage
        of budget
        '''
        return (self.get_goal(y,m) - self.get_reached(y,m) / self.get_goal(y,m))

    
    # Getters     
    def get_name(self): return self._name 
    
    def get_kind(self): return self._kind
    
    def get_budgets(self, year=None, month=None):
        if year == month == None: 
            return self._budgets 
        if type(year) == int: 
            assert year in self._budgets, \
                "account.get_budgets: Year {} not in Accounts".format(year)
            if month == None: 
                return self._budgets[year]
        if type(month) == int: 
            assert month in self._budgets, \
            "account.get_budgets: Month {} not in Accounts, Year {}".format(
                month, year)
            return self._budgets[year][year]
    
    def get_goal(self, y, m): 
        assert y in self._budgets and m in self._budgets[y], \
            "account.get_goal: {} and/or {} not in appropriate range".format(
                y,m)
        return self._budgets[y][m].goal
    
    def get_reached(self, y, m):
        assert y in self._budgets and m in self._budgets[y], \
            "account.get_reached: {} and/or {} not in appropriate range".format(
                y,m)
        return self._budgets[y][m].reached
    
    def get_remain(self, y, m):
        assert y in self._budgets and m in self._budgets[y], \
            "account.get_remain: {} and/or {} not in appropriate range".format(
                y,m)
        return self.get_goal(y,m) - self.get_reached(y,m)
    
    def get_ts_amt(self, y, m):
        assert y in self._budgets and m in self._budgets[y], \
            "account.get_ts_amt: {} and/or {} not in appropriate range".format(
                y,m)
        return self._budgets[y][m].ts_amt
    
    
    def get_ts(self):
        return self._ts
    
    
    def merge(self, right): 
        """Merges two or more Account objects. Returns a new Account object that contains the name, transactions,
        and type of both Accounts
        """
        err_name = "account.Account.merge: "
        for i in right: 
            assert type(i) == Account, \
            err_name+"second argument {} is of type {}, not Account".format(i, type(i))
            assert self._name == i.get_name(), \
            err_name+ "right.get_name should be {} but is {}".format(
                self._name, right.get_name())
            assert self._kind == i.get_kind(), \
            err_name+"kind of right should be {} but is {}".format(
                self._kind, right.get_name())
        unique_ts = self._ts
        iterated = self._ts
        for acct in right:  
            for t in acct.get_ts():
                if t not in iterated: 
                    unique_ts.append(t)
        return Account(self._name, self._kind, unique_ts, {})            


    def remove(self, t: Transaction):
        """Removes transaction from Transaction object collection in 
        Account. Updates from removal
        """
        assert t in self._ts, \
        "account.Account.remove: {} not in self._ts".format(t)
        y,m = t.get_year(), t.get_month()
        self._ts.remove(t)
        self._budgets[y][m] = Budget(
            self.get_goal(y,m), 
            self.get_reached(y,m) - (t.get_amount()), self.get_ts_amt(y,m) - 1)


# Testing 
if __name__ == "__main__": 
    # Initializing     
    t1 = Transaction(2015, 11, 24, "Fast Food", "Cash", 'McDonald\'s', 300)
    t2 = Transaction(2015, 11, 24, "Fast Food", "Debit", "McDonald's", 200)
    t3 = Transaction(2015, 10, 24, "Fast Food", "Cash", "Wendy's", 500)
    t4 = Transaction(2015, 10, 23, "Fast Food", "Gifts", "Wendy's", 400)
    t5 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)
    
    # Testing Initialization 
    a1 = Account("Fast Food", 0, [t1, t2, t3], {})
    a2 = Account(
        "Fast Food", 0, [t1, t2, t3], 
        {2015: {10: Budget(goal=-100, reached=-100, ts_amt=1), 
                11: Budget(goal=-800, reached=-800, ts_amt=2)}})
    a3 = Account("Fast Food", 0, [t1, t2, t3], {})
    a4 = Account("Cash", 0, [t1, t4], {})
    
    print(a1.get_budgets())
    print(a2.get_budgets())
    print(a3.get_budgets())
    print(a4.get_budgets())
 
    # Testing Relational Operators 
    print() 
    print(a1 == a3)
    print(a1 == a2) 
    print(a1 > a2)
    print(a2 < a1)
     
    # Testing Adding Transactions 
    print() 
    a1.add(t4)
    print(t4 in a1)
     
    # Testing Removing Transactions 
    print() 
    print(a1.get_budgets())
    a1.remove(t4)
    print(t4 in a1)
    print(a1.get_budgets())
    try: 
        a1.remove(t5)
    except: 
        print("t5 not in a1")
    print(t5 in a1) 
     
    # Testing All Getters
    print() 
    print(a1.get_name()) 
    print(a1.get_ts())
    print(a1.get_budgets()) 
    print(a1.get_kind())

    print()     
    print(a1.get_goal(2015,11))
    print(a1.get_reached(2015,11))
    print(a1.get_remain(2015,11))
    print(a1.get_ts_amt(2015,11))
     
    # Testing Setters
    print()
    print(a1.get_goal(2015,11))
    a1.set_goal(2015,11,-100)
    print(a1.get_remain(2015,11))
    a1.set_reached(2015,11,-100) 
    print(a1.get_remain(2015,11))
     
    # Testing Analysis
    print()
    print(a1.sum_remain(2015,11)) 
    print(a1.perc_reached(2015,11))
    print(a1.perc_remain(2015,11))
