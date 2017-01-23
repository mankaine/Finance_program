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
        
    
    def update_name(self, name: str) -> None:# account.py 
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
    def _cond(y,m,t): return t["year"] == y and t["month"] == m
    
     
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
        assert type(right) == Account, "Account.__eq__: type of other operand {} is {}, not Account".format(right, type(right))
        return repr(self) == repr(right) 
    
    
    def __lt__(self, right):
        """Returns True if the name and savings variables are the same, and all transactions of 
        the self are a subset of the other
        """ 
        assert type(right) == Account, "Account.__eq__: type of other operand {} is {}, not Account".format(right, type(right))
        name    = self._name == right["name"]
        kind    = self._kind == right["kind"]
        return name and kind and all(i in right["ts"] for i in self._ts)

    
    def __repr__(self):
        return "Account({},{},{},{})".format(repr(self._name),self._kind,self._ts, self._budgets)


    def __setitem__(self, name, value):
        if "__init__" in self.__dict__: 
            assert (name) in self.__dict__, \
            "transaction.Transaction.__setattr__: attribute {} does not exist".format(name)
        assert "_"+name in ("_kind", "_name", "_budget", "_ts"), name
        exec("valid." + name + "({})".format(repr(value)))
        self.__dict__["_"+name] = value

    
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
            y, m = t["year"], t["month"]
            if m not in d[y]: 
                d[y][m] = (t["amount"]*t.flow(self._name))
            else: 
                d[y][m] += (t["amount"]*t.flow(self._name))
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
        ts = [i["amount"]*i.flow(self._name) for i in self._ts if Account._cond(y,m,i)]
        self._budgets[y][m] = Budget(
            sum(ts), self._budgets[y][m].reached, len(ts))


    def add(self, t):
        assert type(t) == Transaction, "account.Account.add_t: {} is not type Transaction".format(type(t))
        self._ts.append(t)
        self._revise_budget(t["year"], t["month"])
    
    
    def update_all_reached(self):
        """Updates all reached attributes
        """
        def _cond(t,y,m): return t["year"] == y and t["month"] == m
        for y in self._budgets:
            for m in self._budgets[y]:
                self.set_reached(
                    y, m, sum(t["amount"] for t in self._ts if _cond(t,y,m) ))
    
    
    def set_reached(self, y: int, m: int, v: float):
        valid.amount(v)
        self._budgets[y][m] = Budget(self[("goal", y, m)], v, self[("ts_amt", y, m)])
    
    
    def set_goal(self, y: int, m: int, v: float):
        valid.amount(v)
        self._budgets[y][m] = Budget(v, self[("reached", y, m)], self[("ts_amt", y, m)])
        
        
    # Analysis of Account
    def sum_remain(self, y: int, m: int) -> float:                              
        '''Returns remaining amount of funds for Account given month and year
        '''
        l, s = self[("goal", y, m)], self[("reached", y, m)]
        if (l < 0 and s < 0) or (l > 0 and s > 0): 
            return l - s 
        return l + s
         
         
    def perc_reached(self, y: int, m: int) -> float:
        '''Returns how much was spent in a given month as a percentage of budget
        '''
        return self[("reached", y, m)] / self[("goal", y, m)]
    
    
    def perc_remain(self, y: int, m: int) -> float: 
        '''Returns how much remains in Account given month and year, as percentage
        of budget
        '''
        return (self[("goal", y, m)] - self[("reached", y, m)]) / self[("goal", y, m)]

    
    # Getters 
    def __getitem__(self, name): 
        err_name = "account.Account.__getitem__: "
        if type(name) == str: 
            assert "_"+name in self.__dict__, err_name+"_"+name+" not in Account namespace"
            return self.__dict__["_"+name]
        elif type(name) == tuple: 
            assert len(name) == 3, err_name+"Length of tuple should be 3 but is {}".format(len(name))
            name, y, m = name
            assert y in self._budgets, err_name+str(y)+" not in self._budgets"
            assert m in self._budgets[y], err_name+str(m)+" not in self._budgets["+str(y)+"]"
            if name == "goal":      return self._budgets[y][m].goal
            elif name == "reached": return self._budgets[y][m].reached
            elif name == "ts_amt":  return self._budgets[y][m].ts_amt
            elif name == "remain": 
                l, s = self[("goal", y, m)], self[("reached", y, m)]
                if (l < 0 and s < 0) or (l > 0 and s > 0): 
                    return l - s 
                return l +  s 
            else: raise IndexError(err_name+"Item {} not in the namespace of an Account object".format(name))
        else: 
            raise TypeError(err_name+"{} is of type {}, not str or tuple".format(name, type(name)))
                
    
    def merge(self, right): 
        """Merges two or more Account objects. Returns a new Account object that contains the name, transactions,
        and type of both Accounts
        """
        err_name = "account.Account.merge: "
        for i in right: 
            assert type(i) == Account, \
            err_name+"second argument {} is of type {}, not Account".format(i, type(i))
            assert self._name == i._name, \
            err_name+ "right.get_name should be {} but is {}".format(self["name"], i["name"])
            assert self._kind == i["kind"], \
            err_name+"kind of right should be {} but is {}".format(self["kind"], right["right"])
        unique_ts = self._ts
        iterated = self._ts
        for acct in right:  
            for t in acct["ts"]:
                if t not in iterated: 
                    unique_ts.append(t)
        return Account(self._name, self._kind, unique_ts, {})            


    def remove(self, t: Transaction):
        """Removes transaction from Transaction object collection in Account. Updates from 
        removal
        """
        assert t in self._ts, "account.Account.remove: {} not in self._ts".format(t)
        y,m = t["year"], t["month"]
        self._ts.remove(t)
        self._budgets[y][m] = Budget(
            self[("goal",y,m)], self[("reached", y, m)] - (t["amount"]), self[("ts_amt",y,m)])


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
    
    print(a1["budgets"])
    print(a2["budgets"])
    print(a3["budgets"])
    print(a4["budgets"])
 
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
    print(a1["budgets"])
    a1.remove(t4)
    print(t4 in a1)
    print(a1["budgets"])
    try: 
        a1.remove(t5)
    except: 
        print("t5 not in a1")
    print(t5 in a1) 
     
    # Testing All Getters
    print() 
    print(a1["name"]) 
    print(a1["ts"])
    print(a1["budgets"]) 
    print(a1["kind"])

    print()     
    print(a1[("goal", 2015, 11)])
    print(a1[("reached", 2015, 11)])
    print(a1[("remain", 2015, 11)])  
    print(a1[("ts_amt", 2015, 11)])
     
    # Testing Setters
    print()
    print(a1[("goal", 2015,11)]) 
    a1.set_goal(2015,11,-100)
    print(a1[("goal", 2015,11)])
    print(a1[("reached", 2015, 11)])
    a1.set_reached(2015,11,-100) 
    print(a1[("reached", 2015, 11)])
     
    # Testing Analysis
    print()
    print(a1.sum_remain(2015,11)) 
    print(a1.perc_reached(2015,11))
    print(a1.perc_remain(2015,11))
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
