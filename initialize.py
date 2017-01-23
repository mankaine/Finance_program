# open.py 
# Opens file to import Accounts and Transactions

from account import Account, Budget
from transaction import Transaction

def main(filename: str) -> ({str:None}, [Account], [Transaction]):
    """Returns a 3-tuple (Accounts, Transactions) after processing an opened file
    """
    acts = list(); ts = list(); var = dict()
    print("    Opening file")
    f = open(filename)
    print("    Retrieving Data")
    for i in f:
        try:
            e = eval(i) 
            if type(e) == Account: 
                acts.append(e)
            elif type(e) == Transaction: 
                ts.append(e)
            elif type(e) == dict: 
                var = e
            else: continue 
        except Exception as e: 
            print("    An error has occurred: {}".format(e))
    f.close()  
    print("    File closed")
            
    # Add Transactions in Accounts, but only if the Transaction is not in 
    # the list of Transaction objects already 
    ts = ts + [t for a in acts for t in a["ts"] if t not in ts]
    return var, acts, ts


if __name__ == "__main__":
    from pprint import pprint 
    def cprint(a: Account):
        """Clean prints an Account
        """
        print("Account({},{},".format(a["name"], a["kind"]))
        pprint(a["ts"])
        print(",")
        pprint(a["budgets"])

    var, ats, ts = main("test.txt")
    
    print()
    print("Imported Accounts") 
    for a in ats: 
        cprint(a)
    
    print()
    print("Imported Transactions")
    for t in ts: 
        print(t)
    
    print()
    print("Imported variables")
    print(var)