# FINANCE PROGRAM
README.md<br />
Author: mankaine<br />
Published 8 April 2016<br />

## TABLE OF CONTENTS
1. DESCRIPTION
2. REPOSITORY CHANGELOG
3. EXAMPLE IMPLEMENTATION


### DESCRIPTION
This program is intended to log and finance your budget. <br />

Features:<br />
Enter transactions in a shell user interface<br />
Import, edit, and view transactions<br />
View transactions<br />
Set budgets<br />

Written in Python. Most ideal to run in a Python interpreter/Terminal<br />

### REPOSITORY CHANGELOG
#### 8/29/2016
Updated to ver. 1.0.1. <br />
Now contains revised data entry and edit modules. <br />
Now users can break out of entering transaction information and edit information is displayed more accurately. <br />
Comments on all modules have been made more consistent. <br />
Removed duplicate menu options from main_menu.py.<br />
Closed older branches.<br />

#### 08/28/2016
Version 1.0 uploaded. <br />
Now contains import, settings, and viewing budget breakdown. <br />
Other modules updated to be more accurate in preserving data.<br />

#### 07/23/2016
First part of v.03 of finance program uploaed. <br />
Now features separate modules for a main menu, entering transactions, and viewing , editing, and exporting transactions. <br />
Creates room available to code for budget. Previous version modules removed.<br />

#### 06/13/2016
v.02 uploaded in two modules, finance_view and finance_model.<br />
Extent of program is that it records a list of transactions by date, category, description, and price.<br />
Creates an list of these transactions exportable to a .txt document.<br />
 
#### 04/08/2016
v.01 of Finance_program uploaded.

###EXAMPLE IMPLEMENTATION
Every function that contains a loop, except those that have the option to exit out of a menu, has implemented a break word. The word's value can be edited in Settings.

At the end of each question a user can input what is in the brackets, a number, or another value. If the choice is invalid, the interpreter will ask again until a valid choice is provided.  

Every time the program starts up, it contains absolutely no information from the previous session. A user must, therefore, add all the information agains from before. While future versions may work on implementing the code necessary to integrate information when Finance Program is initialized, users of the current version are recommended to export all data. 

####INPUTTING TRANSACTIONS
<pre><code>
========== FINANCE PROGRAM ==========

MAIN MENU:
1. Enter Transactions
2. Edit Transactions
3. Import Transactions
4. Export Transactions
5. View Transactions
6. Budget Accounts
7. Access Settings
8. Access Settings
9. Exit

Your input: 1

========== ENTERING TRANSACTIONS ==========
Enter [i]ndividually or by [m]onth? a
a is an invalid choice. Choose either i or m
Enter [i]ndividually or by [m]onth? i

========== Entering by individual transaction ==========

========== Journalizing New Entry ==========
Cash flow: [p]ositive or [n]egative? p

Year: 2016
Month (number): 8
Day: 29

Account: Food
Description: Arby's

Price: 5.29

Updated transaction:
Attribute:   Date       Account              Description           Price      Flow
Information:  8/29/2016 Food                 Arby's               $      5.29 +

Edit transaction? yes
Enter attribute to edit (type in 'Delete' to remove transaction): flow

Enter new cash flow
Cash flow: [p]ositive or [n]egative? n

Updated transaction:
No.  Date       Account                       Description              Price     
--------------------------------------------------------------------------------
  0.  8/29/2016 Food                          Arby's                   $     5.29 -
if Delete was selected, confirmation is that the previous item in the list is displayed

Edit transaction again? no
Enter new transaction? yes

========== Journalizing New Entry ==========
Cash flow: [p]ositive or [n]egative? p

Year: 2016
Month (number): 8
Day: 20

Account: Salary
Description: Memes, Inc.

Price: 500.00

Updated transaction:
Attribute:   Date       Account              Description           Price      Flow
Information:  8/20/2016 Salary               Memes, Inc.          $    500.00 +

Edit transaction? no
Enter new transaction? no

MAIN MENU:
1. Enter Transactions
2. Edit Transactions
3. Import Transactions
4. Export Transactions
5. View Transactions
6. Budget Accounts
7. Access Settings
8. Access Settings
9. Exit

Your input: 1

========== ENTERING TRANSACTIONS ==========
Enter [i]ndividually or by [m]onth? m

========== Entering by month ==========
Year: 2016
Month (number): 7
========== Entering Transactions for the Year 2016, Month 7 ==========
========== Entering New Transaction ==========
Cash flow: [p]ositive or [n]egative? p

Day: 20

Account: Salary
Description: Memes, Inc.

Price: 500.00

Updated transaction:
Attribute:   Date       Account              Description           Price      Flow
Information:  7/20/2016 Salary               Memes, Inc.          $    500.00 +

Edit transaction? no
Enter new transaction for month 7, year 2016? yes
========== Entering New Transaction ==========
Cash flow: [p]ositive or [n]egative? n

Day: 23

Account: Memes
Description: Bad Luck Brian

Price: 300.00

Updated transaction:
Attribute:   Date       Account              Description           Price      Flow
Information:  7/23/2016 Memes                Bad Luck Brian       $    300.00 -

Edit transaction? no
Enter new transaction for month 7, year 2016? no

========== RETURNING TO MAIN MENU ==========
</code></pre>

#### IMPORTING TRANSACTIONS
Transactions that are imported must be formatted, stating the day, description, account, price, and flow:
<pre><code>
         August 2016 Transactions                            
--------------------------------------------------------------------------------
                                    Revenues                                    
--------------------------------------------------------------------------------
Day       Account                       Description              Price      Flow
--------------------------------------------------------------------------------
 7        Cash                          For The Hat              $    20.00 +
 4        Cash                          For Allowance                100.00 +
Net Revenues ................................................... $   120.00
                                                                  ----------

                                    Expenses                                    
--------------------------------------------------------------------------------
Day       Account                       Description              Price      Flow
--------------------------------------------------------------------------------
 4        Fast Food                     McDonald's               $     1.52 -
 5        Clothing                      JCPenny                        0.86 -
 5        Clothing                      JCPenny                       28.35 -
 6        Car Maintenance               Pep Boys                     223.65 -
 7        Fast Food                     The Hat                        7.94 -
Net Expenses ................................................... $   293.11
                                                                  ----------
Net Income ..................................................... $  -173.11
                                                                  ==========
</code></pre>
While the lines and subtotals are not considered, the bits the processor uses is the month; year;  the "Revenues" and "Expenses" strings; and the transaction information per line. All of this information is reproduced in the module to ensure that the interpreter imports the data correctly, and provides the user a chance to edit the function if anything goes wrong.

<pre><code>
MAIN MENU:
1. Enter Transactions
2. Edit Transactions
3. Import Transactions
4. Export Transactions
5. View Transactions
6. Budget Accounts
7. Access Settings
8. Exit

Your input: 
 not among options. Reenter an integer
Your input: 3

========== MOVING TO IMPORT MENU ==========

Select file to import: /Users/mankaine/Documents/finances/transactions/8_aug.txt
Searching for file...
File '/Users/mankaine/Documents/finances/transactions/8_aug.txt' does not exist. Try again

Select file to import: /Users/mankaine/Documents/finances/transactions/2016_8_aug.txt
Searching for file...
File found
Import file? yes

========== Importing transactions ==========

========== Opening and reading files ==========

========== File Closed ==========

========== Displaying Options ==========
Sort by [d]ate, [a]ccount, d[e]scription, [p]rice, or [f]low? d
Display in reverse? no

========== Displaying Transactions for Month 8, Year 2016 ==========

Day   Account              Description          Price      Flow
--------------------------------------------------------------------------------
  4   Cash                 For Allowance        $   100.00 +
  4   Fast Food            McDonald's                 1.52 -
  5   Clothing             JCPenny                    0.86 -
  5   Clothing             JCPenny                   28.35 -
  6   Car Maintenance      Pep Boys                 223.65 -
  7   Cash                 For The Hat               20.00 +
  7   Fast Food            The Hat                    7.94 -

Edit a transaction? no
Return to main menu? yes
========== RETURNING TO MAIN MENU ==========

MAIN MENU:
1. Enter Transactions
2. Edit Transactions
3. Import Transactions
4. Export Transactions
5. View Transactions
6. Budget Accounts
7. Access Settings
8. Exit

Your input: 3

========== MOVING TO IMPORT MENU ==========

Select file to import: /Users/mankaine/Documents/finances/transactions/2016_7_jul.txt
Searching for file...
File found
Import file? yes

========== Importing transactions ==========

========== Opening and reading files ==========

========== File Closed ==========

========== Displaying Options ==========
Sort by [d]ate, [a]ccount, d[e]scription, [p]rice, or [f]low? d
Display in reverse? no

========== Displaying Transactions for Month 7, Year 2016 ==========

Day   Account              Description          Price      Flow
--------------------------------------------------------------------------------
  1   Fast Food            Chick-fil-a          $     8.23 -
  7   Car Maintenance      PCC Parking Fees           2.00 -
  8   Car Maintenance      PCC Parking Fees           2.00 -
  9   Groceries            Super A Foods             11.06 -
 11   Car Maintenance      PCC Parking Fees           2.00 -
 13   Car Maintenance      PCC Parking Permit        20.00 -
 13   Entertainment        Spotify Premium            4.99 -
 13   Fast Food            Subway                     3.82 -
 13   Fast Food            Subway                     2.00 -
 14   Restaurant           85C Bakery - Mom's cake      32.00 -
 18   Restaurant           Dog Haus                   9.79 -
 18   Restaurant           Dog Haus                   2.00 -
 20   Supplies             Amazon                    67.19 -
 23   Restaurant           Red Robin                 13.19 -
 24   Groceries            Super A Foods              2.79 -
 24   Restaurant           Alberto's                 16.58 -
 24   Supplies             Office Depot              22.10 -
 25   Car Maintenance      Gas - Shell               30.07 -
 28   Car Maintenance      Pep Boys                  16.31 -
 30   Restaurant           Chick-fil-a                4.74 -
 30   Restaurant           Chick-fil-a               23.63 -

Edit a transaction? no
Return to main menu? no

Select file to import: hopes and memes
Searching for file...
File 'hopes and memes' does not end with '.txt'. Try again
File 'hopes and memes' does not exist. Try again

Select file to import: /Users/mankaine/Documents/finances/transactions/2016_6_jun.txt
Searching for file...
File found
Import file? yes

========== Importing transactions ==========

========== Opening and reading files ==========

========== File Closed ==========

========== Displaying Options ==========
Sort by [d]ate, [a]ccount, d[e]scription, [p]rice, or [f]low? d
Display in reverse? no

========== Displaying Transactions for Month 6, Year 2016 ==========

Day   Account              Description          Price      Flow
--------------------------------------------------------------------------------
  1   Cash                 Movie Gift Card      $    20.00 +
  1   Residence            Authorization Fee         40.00 -
  1   Restaurant           Wahoo's                   10.56 -
  3   Transportation       Lyft                       1.95 -
  3   Restaurant           Poke Dot                   9.45 -
  3   Fast Food            Chipotle                  12.47 -
  6   Salary               BLP                      400.00 +
  6   Fast Food            Wendy's                    8.08 -
  7   Restaurant           The Habit                 11.50 -
  9   Snacks               Zot n Go                   3.88 -
 10   Snacks               Starbucks                  2.45 -
 13   Entertainment        Spotify Premium            4.99 -
 14   Entertainment        Now you see me 2          19.75 -
 16   Restaurant           Aloha BBQ                 11.97 -
 16   Clothing             JCPenny                   34.89 -
 16   Clothing             JCPenny                   16.34 -
 16   Clothing             JCPenny                   21.79 -
 19   Restaurant           Gen Grill                 59.92 -
 20   Salary               BLP                      275.00 +
 20   Groceries            GoodNews Global Inc.       2.59 -
 23   Fast Food            In n Out                   8.07 -
 25   Cash                 birthday money            50.00 +
 26   Fast Food            McDonald's                 7.83 -
 27   Educational Supplies PCC ACCT1A Book           85.78 -

Edit a transaction? no
Return to main menu? yes
========== RETURNING TO MAIN MENU ==========
</code></pre>
