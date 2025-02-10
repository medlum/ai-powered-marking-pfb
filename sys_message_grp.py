
system_message = """
- You are an AI assistant to a programming lecturer who teach Python. 
- You are tasked by him to mark the students'coding assignments.
- Follow the instructions to mark:
    -- Read the student's brief to understand the assignment requirement. 
    -- Refer to the marking rubrics available for assigning marks. 
    -- Do not assign more than the maximum mark in each marking criterion.
    -- Provide a detail feedback on each of the submitted Python files and comment on the strong and weak aspects of student's code. Give specific instances where the codes are lacking or good.
    -- Assign a mark for each of the criterion.
    -- Be stringent when marking.
    -- Return the marks and feedback in a dictionary : 
        {
            'Team members': [ ],
            'Program Correctness': [ ],
            'Code Readability': [ ],
            'Code Efficiency': [ ],
            'Documentation': [ ],
            'Assignment Specifications': [ ]
            'Feedback' : [ ]
        
        }  
    -- 'Program Correctness', 'Code Readability', 'Code Efficiency','Documentation', 'Assignment Specifications' keys only accept marks as values.
    -- Use single quotation '' for strings in the dictionary.
    -- Your answer should only contain the returned dictionary and nothing else. 
    -- You need to check if the student's code is able to produce the correct output in a txt file.

- Use the following resources to help you when marking:
    -- Various csv data given by the programming lecturer to evaluate the 'program correctness' criteria.
    -- Various 'summary_report.txt' files provided by the programming lecturer that you can refer to for the correct output.
    -- Code solutions provided by the programming lecturer as a point of reference for a model solution.

"""


mark_rubrics = """
1.⁠ ⁠Program Correctness (Max 7 marks)
- 5.6 marks and more: Output produced by the code is fully correct for 'cash on hand', 'profit and loss', 'highest overhead' and it meets all requirements with no errors.
- 4.9 to less than 5.6 marks: Output is mostly correct with minor mistakes or missing punctuations.
- 4.2 to less than 4.9 marks: Partially correct, logical errors.
- 3.5 to less than 4.2 marks: Limited correctness, major failures, incorrect.
- Less than 3.5 marks: Incorrect or non-functional, significant logic errors.

2.⁠ ⁠Code Readability (Max 2 marks)
- 1.6 marks and more: Excellent readability, meaningful names, consistent formatting, proper indentation, clear inline comments.
- 1.4 to less than 1.6 marks: Mostly readable, minor inconsistencies in formatting or naming, limited comments for complex logic.
- 1.2 to less than 1.4 marks: Some readability issues, inconsistent spacing, missing comments, unclear variable names.
- 1 to less than 1.2 marks: Hard to read, lack of indentation, poor naming, minimal commenting, messy structure.
- Less than 1 marks: Very poor readability, no comments, unreadable formatting, confusing structure.

3.⁠ ⁠Code Efficiency (Max 5 marks)
- 4 marks and more: Highly optimized, efficient algorithms, no redundant computations, uses built-in functions properly, write meaningful functions to reduce repeating codes.
- 3.5 to less than 4 marks: Mostly efficient, minor unnecessary loops or operations, some scope for optimization.
- 3 to less than 3.5 marks: Correct logic but inefficient, unnecessary loops, redundant calculations, poor data structures.
- 2.5 to less than 3 marks: Inefficient code, high time complexity, excessive memory use, performance issues.
- Less than 2.5 marks: Highly inefficient, repetitive computations, excessive memory use, brute force solutions.

4.⁠ ⁠Documentation (Max 3 marks)
- 2.4 marks and more: Well-structured documentation, clear docstrings, meaningful comments, algorithm explanations.
- 2.1 to less than 2.4 marks: Mostly well-documented, but some function docstrings or explanations may be missing.
- 1.8 to less than 2.1 marks: Some documentation present but lacks details in function descriptions or inline comments.
- 1.5 to less than 1.8 marks: Minimal documentation, few comments, missing docstrings for key functions.
- Less than 1.5 marks: No meaningful documentation, missing docstrings, no explanation of the code.

5.⁠ ⁠Assignment Specifications (Max 3 marks)
- 2.4 marks and more: Fully meets all assignment requirements, for example:
    -- Filename convention: 'summary_report.txt' are used when writing output to file.
    -- The contents of all the output match the programming lecturer's given output.
    -- Did not import additional python modules except for 'csv' and 'pathlib' modules.
    -- Strict use 'pathlib' module to handle reading and writing files.
- 2.1 to less than 2.4 marks: Mostly meets specifications, but minor missing details or formatting issues.
- 1.8 to less than 2.1 marks: Partially meets specifications, missing some key requirements but still functional.
- 1.5 to less than 1.8 marks: Significant missing requirements, incorrect submission format.
- Less than 1.5 marks: Does not follow assignment requirements, incorrect format, missing important elements.
"""

code_coh = """
from pathlib import Path

def cashOnHands(transactions: list, trend: str, filename: str):
    '''
    - Write cash on hands (from transactions) messages to file (filename) based on the trend supplied: "up", "down", "no", "volatile"
    - Required parameters: transactions as list, trend as str and filename as str.
    '''
    file_path = Path(filename)

    if trend == 'up':
        transactions.sort(reverse=True)
        with file_path.open('a') as file:
            file.write("[CASH SURPLUS] CASH ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
            file.write(f"[HIGHEST CASH SURPLUS] DAY: {transactions[0][1]}, AMOUNT: USD{transactions[0][0]:.2f}\n")
    elif trend == 'down':
        transactions.sort()
        with file_path.open('a') as file:
            file.write("[CASH DEFICIT] CASH ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
            file.write(f"[HIGHEST CASH DEFICIT] DAY: {transactions[0][1]}, AMOUNT: USD{abs(transactions[0][0]):.2f}\n")
    elif trend == 'no':
        with file_path.open('a') as file:
            file.write("[NO CASH SURPLUS] CASH ON EACH DAY IS THE SAME AS PREVIOUS DAY\n")
            file.write(f"[CASH ON HAND] AMOUNT: USD{transactions[0][2]:.2f}\n")
    else:
        with file_path.open('a') as file:
            deficitDaysCount = 0
            for line in transactions:
                if line[0] < 0:
                    file.write(f"[CASH DEFICIT] DAY: {line[1]}, AMOUNT: USD{abs(line[0]):.2f}\n")
                    deficitDaysCount += 1
            transactions.sort(reverse=True)
            highestDeficit = transactions.pop()
            file.write(f"[HIGHEST CASH DEFICIT] DAY: {highestDeficit[1]}, AMOUNT: USD{abs(highestDeficit[0]):.2f}\n")
            if deficitDaysCount > 1:
                highestDeficit = transactions.pop()
                file.write(f"[2ND HIGHEST CASH DEFICIT] DAY: {highestDeficit[1]}, AMOUNT: USD{abs(highestDeficit[0]):.2f}\n")
            if deficitDaysCount > 2:
                highestDeficit = transactions.pop()
                file.write(f"[3RD HIGHEST CASH DEFICIT] DAY: {highestDeficit[1]}, AMOUNT: USD{abs(highestDeficit[0]):.2f}\n")
"""

code_pnl = """
from pathlib import Path

def profit_loss(transactions: list, trend: str, filename: str):
    file_path = Path(filename)

    if trend == 'up':
        transactions.sort(reverse=True)
        with file_path.open('a', newline='') as file:
            file.write("[NET PROFIT SURPLUS] NET PROFIT ON EACH DAY IS HIGHER THAN THE PREVIOUS DAY\n")
            file.write(f"[HIGHEST NET PROFIT SURPLUS] DAY: {transactions[0][1]}, AMOUNT: USD{transactions[0][0]:.2f}\n")
    elif trend == 'down':
        transactions.sort()
        with file_path.open('a', newline='') as file:
            file.write("[NET PROFIT DEFICIT] NET PROFIT ON EACH DAY IS LOWER THAN THE PREVIOUS DAY\n")
            file.write(f"[HIGHEST NET PROFIT DEFICIT] DAY: {transactions[0][1]}, AMOUNT: USD{abs(transactions[0][0]):.2f}\n")
    elif trend == 'no':
        with file_path.open('a', newline='') as file:
            file.write("[NO NET PROFIT SURPLUS] NET PROFIT ON EACH DAY IS THE SAME AS PREVIOUS DAY\n")
            file.write(f"[HIGHEST NET PROFIT] AMOUNT: USD{transactions[0][2]:.2f}\n")
    else:
        deficitDaysCount = 0
        with file_path.open('a', newline='') as file:
            for line in transactions:
                if line[0] < 0:
                    file.write(f"[NET PROFIT DEFICIT] DAY: {line[1]}, AMOUNT: USD{abs(line[0]):.2f}\n")
                    deficitDaysCount += 1
            transactions.sort(reverse=True)
            highestDeficit = transactions.pop()
            file.write(f"[HIGHEST NET PROFIT DEFICIT] DAY: {highestDeficit[1]}, AMOUNT: USD{abs(highestDeficit[0]):.2f}\n")
            if deficitDaysCount > 1:
                highestDeficit = transactions.pop()
                file.write(f"[2ND HIGHEST NET PROFIT DEFICIT] DAY: {highestDeficit[1]}, AMOUNT: USD{abs(highestDeficit[0]):.2f}\n")
            if deficitDaysCount > 2:
                highestDeficit = transactions.pop()
                file.write(f"[3RD HIGHEST NET PROFIT DEFICIT] DAY: {highestDeficit[1]}, AMOUNT: USD{abs(highestDeficit[0]):.2f}\n")

"""

code_overheads = """
from pathlib import Path

def highestOverheads(transactions: list, summaryReport: str):
    '''
    - Sort the list in descending order so that the highest is at the top of the list. Compose a string message for the highest overheads.
    - Required parameters: transactions as list and summaryReport as str.
    '''
    transactions.sort(reverse=True)

    message = f"[HIGHEST OVERHEAD] {transactions[0][1].upper()}: {transactions[0][0]:.2f}%\n"
    file_path = Path(summaryReport)
    with file_path.open('w', newline='') as file:
        file.write(message)
"""

code_main = """
import myTools
import overheads
import coh
import pnl

### FILE PATH SETTINGS
summaryReportFile = "summaryReport.txt"
overheadsFile = "csv_reports/Overheads.csv"
cashOnHandsFile = "csv_reports/COHdecreasing.csv"
profit_lossFile = "csv_reports/PNLdecreasing.csv"

#### OVERHEADS
overheadsTransactions = myTools.openOverheadsFile(overheadsFile)
overheads.highestOverheads(overheadsTransactions, summaryReportFile)


#### CASH ON HANDS
COHtransactions = myTools.openCOHfile(cashOnHandsFile)
myTools.addColumn(COHtransactions) # insert cash on hands difference between current and previous days to a new column
COHtrend = myTools.checkTrend(COHtransactions)
coh.cashOnHands(COHtransactions, COHtrend, summaryReportFile)

### PROFIT AND LOSS
PNLtransactions = myTools.openPNLfile(profit_lossFile)
myTools.addColumn(PNLtransactions) # insert profit difference between current and previous days to a new column
PNLtrend = myTools.checkTrend(PNLtransactions)
pnl.profit_loss(PNLtransactions,PNLtrend,summaryReportFile)

"""

code_tool = """
import csv
from pathlib import Path

def checkTrend(transactions: list):
    '''
    - Checks for trend in the last column of transactions list provided. Returns the trend as "down", "up", "no" or "volatile" 
    - Required parameter: transactions as a  list
    '''
    total_lines = len(transactions)
    decrease = 0
    increase = 0
    previous = transactions[0][-1]
    for item in transactions:
        if item[-1] > previous:
            increase += 1
        elif item[-1] < previous:
            decrease += 1
        previous = item[-1]
    if (increase == 0) and (decrease > 0):
        return 'down'
    elif (increase > 0) and (decrease == 0):
        return 'up'
    elif (increase == 0) and (decrease == 0):
        return 'no'
    else:
        return 'volatile'

def addColumn(transactions: list):
    '''
    - Find the difference between current and previous day from the last column of each list and insert the difference into the front of each list in transactions.
    - Required parameter: transactions as a list
    '''
    previous = transactions[0][-1]
    for item in transactions:
        net_value = item[-1] - previous
        previous = item[-1]
        item.insert(0, net_value)

def openPNLfile(filename: str):
    ''''
    - Open CSV file in read mode, convert all digit strings to numeric. Returns a list.
    - Required parameter: filename as string
    '''
    file_path = Path(filename)
    with file_path.open('r', newline='') as file:
        reader = csv.reader(file)
        transactions = []
        next(reader)  # Skip header
        for line in reader:
            line = [int(x) for x in line]
            transactions.append(line)
    return transactions

def openCOHfile(filename: str):
    ''''
    - Open CSV file in read mode, convert all digit strings to numeric. Returns a list.
    - Required parameter: filename as string
    '''
    file_path = Path(filename)
    with file_path.open('r', newline='') as file:
        reader = csv.reader(file)
        transactions = []
        next(reader)  # Skip header
        for line in reader:
            line = [int(x) for x in line]
            transactions.append(line)
    return transactions

def openOverheadsFile(filename: str):
    '''
    - Open CSV file in read mode, convert all digit strings to numeric, swop the order of the two columns and returns a list.
    - Required parameter: filename as string    
    '''
    file_path = Path(filename)
    with file_path.open('r', newline='') as file:
        reader = csv.reader(file)
        transactions = []
        next(reader)  # Skip header
        for line in reader:
            # Swap the order of the two columns and convert to appropriate types
            line = [float(line[1]), line[0]]
            transactions.append(line)
    return transactions

"""