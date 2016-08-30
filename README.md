# FINANCE PROGRAM
README.md<br />
Author: mankaine<br />
Published 8 April 2016<br />

## DESCRIPTION
This program is intended to log and finance your budget. <br />

Features:<br />
Enter transactions in a shell user interface<br />
Import, edit, and view transactions<br />
View transactions<br />
Set budgets<br />

Written in Python. Most ideal to run in a Python interpreter/Terminal<br />

## REPOSITORY CHANGELOG
### 8/29/2016
Updated to ver. 1.0.1. <br />
Now contains revised data entry and edit modules. <br />
Now users can break out of entering transaction information and edit information is displayed more accurately. <br />
Comments on all modules have been made more consistent. <br />
Removed duplicate menu options from main_menu.py.<br />
Closed older branches.<br />

### 08/28/2016
Version 1.0 uploaded. <br />
Now contains import, settings, and viewing budget breakdown. <br />
Other modules updated to be more accurate in preserving data.<br />

### 07/23/2016
First part of v.03 of finance program uploaed. <br />
Now features separate modules for a main menu, entering transactions, and viewing , editing, and exporting transactions. <br />
Creates room available to code for budget. Previous version modules removed.<br />

### 06/13/2016
v.02 uploaded in two modules, finance_view and finance_model.<br />
Extent of program is that it records a list of transactions by date, category, description, and price.<br />
Creates an list of these transactions exportable to a .txt document.<br />
 
### 04/08/2016
v.01 of Finance_program uploaded.

##EXAMPLE IMPLEMENTATION
###INPUTTING TRANSACTIONS
Every function that contains a loop, except those that have the option to exit out of a menu, has implemented a break word. The word's value can be edited in Settings.
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
