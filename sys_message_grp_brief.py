project_brief = """
- Develop a business automation program that extract and summarise data from a finance dashboard. 
- The automation will perform the tasks from the following data files:
    a. Profit & Loss (.csv) : The program will firstly compute the
    difference in the net profit column. If the net profit is always
    increasing, find out the day and amount the highest
    increment occurs. If the net profit is always decreasing, find
    out the day and amount the highest decrement occurs. If net
    profit fluctuates, list down all the days and amount when deficit
    occurs, and find out the top 3 highest deficit amount and the days it
    happened.
    b. Cash-On-Hand (.csv): The program will firstly compute the
    difference in Cash-on-Hand. If the cash-on-hand is always
    increasing, find out the day and amount the highest
    increment occurs. If the cash-on-hand is always decreasing,
    find out the day and amount the highest decrement occurs. If
    cash-on-hand fluctuates, list down all the days and amount when
    deficit occurs, and find out the top 3 highest deficit amount and the
    days it happened.
    c. Overheads (.csv): The program will find the highest overhead
    category.
    d. Write the computed amount to a text file and name it as 'summary_report.txt'.
    e. Organize the code and data files into the following folder structure:
        Folder : project_group
        │ - team_members.txt
        | - main.py
        | - cash_on_hand.py
        │ - overheads.py
        │ - profit_loss.py
        │ - summary_report.txt
        └─── Folder: csv_reports
                - Cash_on_Hand.csv
                - Overheads.csv
                - Profits_and_Loss.csv

        Dedicate each python file to achieve specific tasks. For example, the
        cash_on_hand.py should only contain codes that compute the difference in Cash-
        on-Hand.csv, while overheads.py should only contain codes that find the highest
        overhead category. Organizing code this way makes the overall program more
        manageable, easier to maintain and debug errors.
"""

coh_decreasing = """
Day,Cash On Hand
40,2571502
41,2569504
42,2568706
43,2565808
44,2563010
45,2562012
46,2560114
47,2558216
48,2556458
49,2554420
"""

coh_increasing = """
Day,Cash On Hand
40,2571502
41,2573489
42,2575476
43,2577463
44,2579450
45,2581437
46,2583424
47,2585411
48,2587398
49,2589385
"""

coh_volatile ="""
Day,Cash On Hand
40,2571502
41,1115609
42,1055099
43,1003310
44,364763
45,244591
46,300807
47,316348
48,564179
49,179747
"""

pnl_decreasing = """
Day,Sales,Trading Profit,Operating Expense,Net Profit
40,14481055,6170905,3667884,2503021
41,14581932,6246685,3727854,2502020
42,14714710,6335491,3790422,2501012
43,14833531,6418158,3865832,2493018
44,14930686,6488829,3963814,2442010
45,15057632,6548661,4029052,2432016
46,15157737,6616222,4092941,2403009
47,16759515,6935340,4155458,2333001
48,16797892,6944441,4258004,2003013
49,16938318,6972213,4323322,2002055
"""



pnl_increasing = """
Day,Sales,Trading Profit,Operating Expense,Net Profit
40,14481055,6170905,3667884,2503021
41,14581932,6246685,3727854,2543025
42,14714710,6335491,3790422,2573023
43,14833531,6418158,3865832,2583024
44,14930686,6488829,3963814,2593010
45,15057632,6548661,4029052,2603026
46,15157737,6616222,4092941,2623000
47,16759515,6935340,4155458,2643028
48,16797892,6944441,4258004,2663129
49,16938318,6972213,4323322,2673050

"""


pnl_volatile = """
Day,Sales,Trading Profit,Operating Expense,Net Profit
40,14481055,6170905,3667884,2503021
41,14581932,6246685,3727854,2518831
42,14714710,6335491,3790422,2545069
43,14833531,6418158,3865832,2552326
44,14930686,6488829,3963814,2525015
45,15057632,6548661,4029052,2519609
46,15157737,6616222,4092941,2523281
47,16759515,6935340,4155458,2779882
48,16797892,6944441,4258004,2686437
49,16938318,6972213,4323322,2648891

"""


overheads = """
"Category","Overheads"
"Salary Expense",25.66
"Interest Expense ",2.14
"Rental Expense",25.97
"Overflow Expense - Retail",0.32
"Overflow Expense - Warehouse",0.12
"Penalty Expense",2.46
"Depreciation Expense",17.3
"Maintenance Expense",5.23
"Shipping Expense",11.25
"Human Resource Expense",15.55
"""

output_volatile = """
[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH DEFICIT] DAY: 41, AMOUNT: USD1455893.00
[CASH DEFICIT] DAY: 42, AMOUNT: USD60510.00
[CASH DEFICIT] DAY: 43, AMOUNT: USD51789.00
[CASH DEFICIT] DAY: 44, AMOUNT: USD638547.00
[CASH DEFICIT] DAY: 45, AMOUNT: USD120172.00
[CASH DEFICIT] DAY: 49, AMOUNT: USD384432.00
[HIGHEST CASH DEFICIT] DAY: 41, AMOUNT: USD1455893.00
[2ND HIGHEST CASH DEFICIT] DAY: 44, AMOUNT: USD638547.00
[3RD HIGHEST CASH DEFICIT] DAY: 49, AMOUNT: USD384432.00
[NET PROFIT DEFICIT] DAY: 44, AMOUNT: USD27311.00
[NET PROFIT DEFICIT] DAY: 45, AMOUNT: USD5406.00
[NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD93445.00
[NET PROFIT DEFICIT] DAY: 49, AMOUNT: USD37546.00
[HIGHEST NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD93445.00
[2ND HIGHEST NET PROFIT DEFICIT] DAY: 49, AMOUNT: USD37546.00
[3RD HIGHEST NET PROFIT DEFICIT] DAY: 44, AMOUNT: USD27311.00
"""


output_increasing = """
[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH SURPLUS] CASH ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY
[HIGHEST CASH SURPLUS] DAY: 49, AMOUNT: USD1987.00
[NET PROFIT SURPLUS] NET PROFIT ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY
[HIGHEST NET PROFIT SURPLUS] DAY: 41, AMOUNT: USD40004.00
"""



output_decreasing = """
[HIGHEST OVERHEAD] RENTAL EXPENSE: 25.97%
[CASH DEFICIT] CASH ON EACH DAY IS LOWER THAN THE PREVIOUS DAY
[HIGHEST CASH DEFICIT] DAY: 43, AMOUNT: USD2898.00
[NET PROFIT DEFICIT] NET PROFIT ON EACH DAY IS LOWER THAN THE PREVIOUS DAY
[HIGHEST NET PROFIT DEFICIT] DAY: 48, AMOUNT: USD329988.00
"""