# save.py 
# Saves current session to a text file 

from transaction import Transaction
from account     import Account, Budget

# file = "data.txt"

def main(ts: [Transaction], ats: [Account], var, filename: str) -> None:
    """Writes to a specified document current session
    """
    opened_file = open(filename, "w")
    print("    Export File Opened")
    print("    Beginning Export") 
    for i in (ts if ats == [] else ats):
        try:
            opened_file.write(repr(i)+"\n")
        except Exception as e:
            print("    An error has occurred: {}".format(e))
    opened_file.write(repr(var) + "\n")
    opened_file.close() 
    print("    Export File Closed") 
    
    
if __name__ == "__main__":
    t0 = Transaction(2015, 11, 24, "Cash", "Accounts Recievable", "Job", 400)
    t1 = Transaction(2015, 11, 24, "Fast Food", "Cash", 'McDonald\'s', 300)
    t2 = Transaction(2015, 11, 24, "Fast Food", "Debit", "McDonald's", 200)
    t3 = Transaction(2015, 10, 24, "Fast Food", "Cash", "Wendy's", 500)
    t4 = Transaction(2015, 10, 23, "Fast Food", "Gifts", "Wendy's", 400)
    t5 = Transaction(2015, 10, 22, "Drinks", "Savings", "Coffee", 200)
    ts  = [t0,t1,t2,t3,t4,t5]
    
    a0 = Account(
        'Cash',2,
        [Transaction(2015, 11, 24, "Cash", "Accounts Recievable", "Job", 400, '$'), 
         Transaction(2015, 11, 24, "Fast Food", "Cash", "McDonald's", 300, '$'), 
         Transaction(2015, 10, 24, "Fast Food", "Cash", "Wendy's", 500, '$')],
                 {2015: {10: Budget(goal=-500, reached=-500, ts_amt=1), 
                         11: Budget(goal=100, reached=100, ts_amt=2)}})
    ats = [a0]
    
    main(ts, ats, {"user":1}, "test.txt")