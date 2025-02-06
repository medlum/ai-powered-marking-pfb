mark_rubrics = """
1.⁠ ⁠Program Correctness (Max 30 marks)
- 24 marks and more: Output produced by the code is fully correct, meets all requirements, no errors.
- 21 to less than 24 marks: Output is mostly correct with minor mistakes or missing punctuations.
- 18 to less than 21 marks: Partially correct, logical errors.
- 15 to less than 18 marks: Limited correctness, major failures, incorrect.
- Less than 15 marks: Incorrect or non-functional, significant logic errors.

2.⁠ ⁠Code Readability (Max 20 marks)
- 16 marks and more: Excellent readability, meaningful names, consistent formatting (PEP8), proper indentation, clear inline comments.
- 14 to less than 16 marks: Mostly readable, minor inconsistencies in formatting or naming, limited comments for complex logic.
- 12 to less than 14 marks: Some readability issues, inconsistent spacing, missing comments, unclear variable names.
- 10 to less than 12 marks: Hard to read, lack of indentation, poor naming, minimal commenting, messy structure.
- Less than 10 marks: Very poor readability, no comments, unreadable formatting, confusing structure.

3.⁠ ⁠Code Efficiency (Max 20 marks)
- 16 marks and more: Highly optimized, efficient algorithms, no redundant computations, uses built-in functions properly.
- 14 to less than 16 marks: Mostly efficient, minor unnecessary loops or operations, some scope for optimization.
- 12 to less than 14 marks: Correct logic but inefficient, unnecessary loops, redundant calculations, poor data structures.
- 10 to less than 12 marks: Inefficient code, high time complexity, excessive memory use, performance issues.
- Less than 10 marks: Highly inefficient, repetitive computations, excessive memory use, brute force solutions.

4.⁠ ⁠Documentation (Max 25 marks)
- 20 marks and more: Well-structured documentation, clear docstrings, meaningful comments, algorithm explanations.
- 17.5 to less than 20 marks: Mostly well-documented, but some function docstrings or explanations may be missing.
- 15 to less than 17.5 marks: Some documentation present but lacks details in function descriptions or inline comments.
- 12.5 to less than 15 marks: Minimal documentation, few comments, missing docstrings for key functions.
- Less than 12.5 marks: No meaningful documentation, missing docstrings, no explanation of the code.

5.⁠ ⁠Assignment Specifications (Max 5 marks)
- 4 marks and more: Fully meets all assignment requirements, such as file name 'spaceSummary.txt' when writing output to filem, 
output contains "Efficient Transit Payment Summary" heads, 
correct terms like "Staff", "Boxes_Picked", "Profit, "Commission", "Salary" are used. 
Use of Path.cwd() to read and write files.
- 3.5 to less than 4 marks: Mostly meets specifications, but minor missing details or formatting issues.
- 3 to less than 3.5 marks: Partially meets specifications, missing some key requirements but still functional.
- 2.5 to less than 3 marks: Significant missing requirements, incorrect submission format.
- Less than 1.5 marks: Does not follow assignment requirements, incorrect format, missing important elements.

"""

code_solutions = """

from pathlib import Path
import csv

# Create a file path to the CSV file
fp = Path.cwd() / "SpaceUsage.csv"

# Read the CSV file
with fp.open(mode="r", encoding="UTF-8", newline="") as file:
    reader = csv.reader(file)
    next(reader)  # Skip header row

    # Create an empty list to store usage records
    UsageRecords = []

    # Append records into the UsageRecords list
    for row in reader:
        # Extract relevant fields: Order No., SKU, Staff, Boxes_Picked, Unit_Cost_Price, Unit_Selling_Price
        UsageRecords.append([row[0], row[1], row[2], row[3], row[4], row[5]])

print(UsageRecords)


def handle_money(sales):
    "Remove currency symbols and commas from a sales string and convert it to a float."
    sales = sales.replace('S$', '').replace(',', '').strip()
    return float(sales)


def getEarningPerOrder(profit):
    "Calculate the earning per order based on the given profit."
    "Commission structure: - 2% for profit up to 1500"
    "- 4% for profit between 1501 and 3000"
    "- 5% for profit between 3001 and 4500"
    "- 6% for profit above 4500"
    
    "Returns:    float: Rounded earning value"
    earning = 0
    if profit <= 0:
        return 0
    if 0 < profit <= 1500:
        earning += profit * 0.02
    elif profit <= 3000:
        earning += 1500 * 0.02 + (profit - 1500) * 0.04
    elif profit <= 4500:
        earning += 1500 * 0.02 + 1500 * 0.04 + (profit - 3000) * 0.05
    else:
        earning += 1500 * 0.02 + 1500 * 0.04 + 1500 * 0.05 + (profit - 4500) * 0.06
    
    return round(earning, 2)

# Dictionary to store staff sales summary
salesSummary = {}
# Dictionary to store total boxes picked per SKU
sku_sales = {}

# Process each record to calculate boxes picked, profit, and commission
for record in UsageRecords:
    sku_id = record[1]
    staff = record[2]
    boxes_picked = int(record[3])
    cost = handle_money(record[4])
    price = handle_money(record[5])

    # Initialize staff summary if not present
    if staff not in salesSummary:
        salesSummary[staff] = {
            'boxes_picked': 0,
            'profit': 0,
            'commission': 0,
            'salary': 1000  # Basic salary
        }

    # Update staff's total boxes picked
    salesSummary[staff]['boxes_picked'] += boxes_picked

    # Calculate profit per order
    profit = boxes_picked * (price - cost)
    salesSummary[staff]['profit'] += profit

    # Calculate and update commission
    commission = getEarningPerOrder(profit)
    salesSummary[staff]['commission'] += commission

    # Add commission to salary
    salesSummary[staff]['salary'] += commission

    # Update total SKU sales count
    if sku_id not in sku_sales:
        sku_sales[sku_id] = 0
    sku_sales[sku_id] += boxes_picked

# Create a sorted list of SKUs based on sales volume
topSKU = sorted([(value, key) for key, value in sku_sales.items()], reverse=True)

# Write the calculated information to a text file
fp_txt = Path.cwd() / "spaceSummary.txt"
with fp_txt.open(mode="w", encoding="UTF-8") as file:
    file.write("Efficient Transit Payment Summary\n")
    file.write("==================================\n")
    file.write("Staff,Boxes Picked,Profits,Commission,Salary\n")
    
    for staff in sorted(salesSummary):
        info = salesSummary[staff]
        file.write(f"{staff},{info['boxes_picked']},{info['profit']:.2f},{info['commission']:.2f},{info['salary']:.2f}\n")
    
    number_of_sku = len(topSKU)
    top_of_sku = min(5, number_of_sku)  # Get top 5 or fewer SKUs
    file.write(f'\n\nTop {top_of_sku} of {number_of_sku} SKUs\n')
    file.write('===================\n')
    for sku in topSKU[:top_of_sku]:
        file.write(f"{sku[0]},{sku[1]}\n")

"""

instructions = """
Follow this set of instructions to mark the student's code:


- Mark the student's code using the given marking rubrics available to you. 
- Assign a mark for each of the criterion in the marking rubrics.
- Use the given data "SpaceUsage.csv" to evaluate the code for program correctness. Check if the code is able to produce the correct output and write to "spaceSummary.txt".
- Do not assign more than the maximum mark found in each criterion.
- Write a short comment on each area after assigning the marks.
- Tally the marks in each area.
- To check for program correctness, evaluate if the code is able to produce the expected output.
- Return the output with the areas, mark, comment in a table.
- Return the total mark and an overall comment in strings.    
-
"""

correct_output = """
Efficient Transit  Payment Summary
==================================
Staff,Boxes Picked,Profits,Commission,Salary
Staff_01,2466,90088.40,2510.88,3510.88
Staff_02,2634,100132.60,3039.83,4039.83
Staff_03,2333,86641.50,2511.63,3511.63
Staff_04,2240,78891.13,2265.97,3265.97
Staff_05,2485,85370.66,2289.80,3289.80
Staff_06,2343,76838.92,2109.25,3109.25
Staff_07,2424,90428.26,2606.91,3606.91
Staff_08,2478,91948.89,2667.47,3667.47
Staff_09,2372,74549.38,2149.08,3149.08
Staff_10,2536,78181.62,2108.20,3108.20


Top 5 of 20 SKUs
===================
1782,SKU_012
1774,SKU_003
1601,SKU_001
1589,SKU_017
1503,SKU_016

"""

data = """
Order No.,SKU,Staff,Boxes_Picked,Unit_Cost_Price,Unit_Selling_Price
1000,SKU_007,Staff_03,76,S$12.43,S$66.6
1001,SKU_020,Staff_06,9,S$16.61,S$71.82
1002,SKU_015,Staff_06,74,S$30.5,S$77.09
1003,SKU_011,Staff_03,58,S$12.28,S$49.39
1004,SKU_008,Staff_07,17,S$35.54,S$55.97
1005,SKU_007,Staff_03,7,S$24.85,S$46.1
1006,SKU_019,Staff_08,46,S$24.42,S$79.7
1007,SKU_011,Staff_10,13,S$27.77,S$77.08
1008,SKU_011,Staff_04,40,S$34.74,S$61.6
1009,SKU_004,Staff_01,42,S$20.43,S$73.68
1010,SKU_008,Staff_04,9,S$30.34,S$60.84
1011,SKU_003,Staff_07,50,S$26.97,S$64.94
1012,SKU_002,Staff_04,27,S$18.01,S$43.56
1013,SKU_012,Staff_06,66,S$36.36,S$70.21
1014,SKU_006,Staff_09,5,S$33.92,S$45.11
1015,SKU_002,Staff_01,29,S$29.75,S$73.04
1016,SKU_001,Staff_05,37,S$35.52,S$71.28
1017,SKU_012,Staff_07,38,S$36.02,S$68.35
1018,SKU_012,Staff_01,83,S$31.25,S$41.45
1019,SKU_017,Staff_04,8,S$35.11,S$52.13
1020,SKU_010,Staff_06,65,S$30.92,S$50.52
1021,SKU_016,Staff_02,86,S$30.4,S$54.41
1022,SKU_015,Staff_10,17,S$28.56,S$43.51
1023,SKU_015,Staff_05,71,S$32.58,S$77.48
1024,SKU_019,Staff_10,89,S$14.76,S$62.15
1025,SKU_012,Staff_01,45,S$36.43,S$52.22
1026,SKU_020,Staff_06,4,S$36.16,S$55.88
1027,SKU_003,Staff_06,36,S$10.88,S$57.89
1028,SKU_005,Staff_04,70,S$34.77,S$64.02
1029,SKU_019,Staff_08,31,S$13.87,S$60.63
1030,SKU_007,Staff_04,19,S$20.05,S$76.78
1031,SKU_009,Staff_08,61,S$32.31,S$59.88
1032,SKU_007,Staff_08,54,S$14.82,S$79.69
1033,SKU_018,Staff_05,39,S$34.54,S$74.06
1034,SKU_004,Staff_04,91,S$34.96,S$48.34
1035,SKU_014,Staff_02,74,S$25.22,S$77.22
1036,SKU_018,Staff_03,90,S$10.19,S$44.65
1037,SKU_009,Staff_03,19,S$18.61,S$72.7
1038,SKU_002,Staff_04,39,S$28.51,S$55.22
1039,SKU_020,Staff_04,67,S$39.44,S$75.12
1040,SKU_015,Staff_10,45,S$28.95,S$74.72
1041,SKU_007,Staff_05,13,S$17.79,S$72.24
1042,SKU_012,Staff_04,92,S$29.02,S$71.6
1043,SKU_008,Staff_10,58,S$26.2,S$52.19
1044,SKU_015,Staff_08,20,S$33.4,S$43.24
1045,SKU_003,Staff_06,92,S$13.21,S$56.12
1046,SKU_014,Staff_06,72,S$32.83,S$46.94
1047,SKU_017,Staff_08,61,S$26.24,S$67.8
1048,SKU_004,Staff_07,39,S$38.89,S$53.84
1049,SKU_018,Staff_10,1,S$20.26,S$79.02
1050,SKU_008,Staff_10,3,S$28.98,S$65.64
1051,SKU_004,Staff_08,77,S$37.96,S$72.9
1052,SKU_002,Staff_02,92,S$13.08,S$45.3
1053,SKU_006,Staff_09,62,S$38.12,S$74.48
1054,SKU_010,Staff_01,63,S$30.64,S$76.91
1055,SKU_004,Staff_08,25,S$12.04,S$59.48
1056,SKU_018,Staff_04,56,S$19.03,S$64.25
1057,SKU_012,Staff_04,33,S$31.25,S$70.59
1058,SKU_002,Staff_05,38,S$12.02,S$46.99
1059,SKU_010,Staff_08,6,S$27.47,S$60.1
1060,SKU_004,Staff_05,58,S$20.38,S$55.95
1061,SKU_014,Staff_08,44,S$28.63,S$45.85
1062,SKU_016,Staff_10,45,S$11.37,S$54.7
1063,SKU_015,Staff_01,32,S$36.15,S$42.73
1064,SKU_008,Staff_10,45,S$39.2,S$41.03
1065,SKU_014,Staff_09,61,S$39.07,S$45.41
1066,SKU_008,Staff_06,47,S$32.49,S$78.52
1067,SKU_016,Staff_03,21,S$13.9,S$61.98
1068,SKU_013,Staff_08,80,S$32.75,S$78.63
1069,SKU_018,Staff_09,85,S$10.74,S$57.3
1070,SKU_015,Staff_06,75,S$10.66,S$52.47
1071,SKU_013,Staff_07,36,S$19.71,S$60.25
1072,SKU_009,Staff_01,99,S$24.66,S$57.58
1073,SKU_015,Staff_05,19,S$33.11,S$44.23
1074,SKU_013,Staff_05,20,S$30.5,S$65.63
1075,SKU_001,Staff_10,57,S$23.38,S$48.64
1076,SKU_007,Staff_04,18,S$18.21,S$64.78
1077,SKU_009,Staff_06,47,S$39.91,S$66.01
1078,SKU_001,Staff_07,49,S$22.79,S$46.08
1079,SKU_012,Staff_09,14,S$23.54,S$42.45
1080,SKU_008,Staff_01,15,S$14.91,S$71.23
1081,SKU_011,Staff_06,31,S$33.84,S$58.39
1082,SKU_019,Staff_07,1,S$30.81,S$42.33
1083,SKU_017,Staff_03,54,S$16.62,S$79.79
1084,SKU_008,Staff_08,3,S$12.47,S$42.31
1085,SKU_003,Staff_05,16,S$30.41,S$67.8
1086,SKU_003,Staff_09,87,S$29.64,S$79.35
1087,SKU_001,Staff_05,57,S$18.2,S$49.57
1088,SKU_005,Staff_09,75,S$38.53,S$45.69
1089,SKU_010,Staff_10,12,S$14.53,S$44.86
1090,SKU_007,Staff_04,74,S$22.97,S$52.13
1091,SKU_009,Staff_09,96,S$38.31,S$44.04
1092,SKU_007,Staff_05,16,S$22.59,S$67.69
1093,SKU_009,Staff_10,72,S$29.16,S$42.49
1094,SKU_008,Staff_09,76,S$21.93,S$60.38
1095,SKU_012,Staff_03,24,S$18.23,S$79.87
1096,SKU_002,Staff_04,28,S$39.52,S$72.56
1097,SKU_001,Staff_09,8,S$22.28,S$64.61
1098,SKU_016,Staff_10,92,S$36.82,S$52.25
1099,SKU_005,Staff_06,36,S$16.9,S$64.96
1100,SKU_003,Staff_02,90,S$16.39,S$61.08
1101,SKU_012,Staff_07,8,S$10.93,S$57.04
1102,SKU_008,Staff_02,58,S$29.55,S$45.23
1103,SKU_003,Staff_02,60,S$21.06,S$75.46
1104,SKU_001,Staff_01,50,S$35.93,S$57.99
1105,SKU_003,Staff_03,28,S$24.2,S$47.78
1106,SKU_005,Staff_06,92,S$39.05,S$54.71
1107,SKU_015,Staff_08,41,S$15.57,S$56.57
1108,SKU_014,Staff_09,64,S$36.06,S$73.1
1109,SKU_003,Staff_07,27,S$33.3,S$69.34
1110,SKU_001,Staff_04,63,S$33.13,S$70.77
1111,SKU_005,Staff_06,17,S$35.34,S$40.44
1112,SKU_014,Staff_05,73,S$32.83,S$56.65
1113,SKU_007,Staff_08,33,S$28.79,S$59.25
1114,SKU_009,Staff_01,84,S$13.94,S$40.77
1115,SKU_015,Staff_01,77,S$10.98,S$50.39
1116,SKU_015,Staff_06,92,S$37.63,S$70.41
1117,SKU_010,Staff_10,29,S$28.5,S$45.48
1118,SKU_013,Staff_02,13,S$33.9,S$61.41
1119,SKU_019,Staff_05,46,S$24.45,S$48.61
1120,SKU_007,Staff_01,35,S$13.52,S$40.48
1121,SKU_017,Staff_07,6,S$13.76,S$49.65
1122,SKU_020,Staff_01,82,S$30.57,S$79.03
1123,SKU_004,Staff_04,69,S$22.91,S$72.06
1124,SKU_005,Staff_09,47,S$16.02,S$78.38
1125,SKU_007,Staff_01,25,S$24.75,S$59.51
1126,SKU_013,Staff_04,66,S$11.93,S$44.39
1127,SKU_015,Staff_06,10,S$27.46,S$61.92
1128,SKU_011,Staff_06,56,S$18.07,S$58.18
1129,SKU_004,Staff_08,30,S$33.93,S$73.77
1130,SKU_013,Staff_01,5,S$19.31,S$43.92
1131,SKU_007,Staff_07,33,S$23.66,S$59.53
1132,SKU_019,Staff_01,65,S$10.35,S$46
1133,SKU_002,Staff_07,18,S$12.17,S$52.99
1134,SKU_010,Staff_03,96,S$21.77,S$69.49
1135,SKU_013,Staff_08,49,S$24.4,S$59.04
1136,SKU_006,Staff_03,11,S$28,S$55.04
1137,SKU_012,Staff_01,85,S$18.75,S$55.78
1138,SKU_012,Staff_08,26,S$30.85,S$58.38
1139,SKU_020,Staff_03,63,S$35.8,S$71.4
1140,SKU_011,Staff_02,89,S$33.4,S$75.68
1141,SKU_007,Staff_01,86,S$11.19,S$78.21
1142,SKU_001,Staff_03,59,S$24.42,S$71.48
1143,SKU_001,Staff_02,27,S$13.15,S$52.62
1144,SKU_020,Staff_02,49,S$17.26,S$67.53
1145,SKU_013,Staff_06,77,S$39.6,S$57.5
1146,SKU_009,Staff_01,33,S$14.27,S$50.19
1147,SKU_003,Staff_02,98,S$24.97,S$73.63
1148,SKU_007,Staff_06,99,S$28.54,S$41.54
1149,SKU_006,Staff_03,1,S$31.07,S$76.07
1150,SKU_008,Staff_04,21,S$26.79,S$58.46
1151,SKU_009,Staff_01,55,S$10.29,S$65.49
1152,SKU_005,Staff_08,6,S$19.79,S$66.37
1153,SKU_001,Staff_07,92,S$25.53,S$75.8
1154,SKU_019,Staff_07,81,S$12.64,S$65.47
1155,SKU_010,Staff_03,69,S$20.52,S$64.56
1156,SKU_012,Staff_10,95,S$11,S$42.67
1157,SKU_015,Staff_10,5,S$12.36,S$60.74
1158,SKU_009,Staff_03,3,S$21.91,S$46.01
1159,SKU_020,Staff_02,53,S$13.98,S$69.5
1160,SKU_017,Staff_01,23,S$27.03,S$60.49
1161,SKU_017,Staff_07,53,S$30.68,S$67.21
1162,SKU_020,Staff_07,37,S$34.02,S$41.67
1163,SKU_012,Staff_02,74,S$16,S$43.39
1164,SKU_007,Staff_07,74,S$15.02,S$68.65
1165,SKU_002,Staff_08,83,S$13.14,S$42.88
1166,SKU_003,Staff_01,17,S$29.09,S$42.85
1167,SKU_017,Staff_09,85,S$31.19,S$40.48
1168,SKU_005,Staff_07,78,S$10.95,S$78.26
1169,SKU_017,Staff_03,73,S$38.09,S$69.5
1170,SKU_017,Staff_08,1,S$11.56,S$54.13
1171,SKU_017,Staff_07,51,S$26.24,S$51.86
1172,SKU_002,Staff_08,45,S$31.27,S$53.99
1173,SKU_002,Staff_06,77,S$36.13,S$70.99
1174,SKU_005,Staff_09,4,S$31.42,S$66.45
1175,SKU_001,Staff_05,62,S$34.05,S$47.41
1176,SKU_001,Staff_03,65,S$20.18,S$46.96
1177,SKU_019,Staff_03,32,S$34.44,S$43.94
1178,SKU_002,Staff_01,34,S$12.4,S$66.41
1179,SKU_012,Staff_08,92,S$36.84,S$70.57
1180,SKU_006,Staff_02,95,S$26.43,S$50.6
1181,SKU_004,Staff_03,72,S$34.52,S$40.84
1182,SKU_011,Staff_08,39,S$23.57,S$43.29
1183,SKU_017,Staff_08,26,S$29.31,S$78.71
1184,SKU_006,Staff_04,34,S$25.79,S$51.82
1185,SKU_005,Staff_04,54,S$31.95,S$70.77
1186,SKU_020,Staff_05,3,S$12.45,S$64.99
1187,SKU_002,Staff_06,50,S$11.81,S$55.28
1188,SKU_006,Staff_05,12,S$17.41,S$48.23
1189,SKU_011,Staff_07,65,S$14.79,S$44.86
1190,SKU_016,Staff_02,54,S$36.15,S$64.6
1191,SKU_016,Staff_07,5,S$16.58,S$70.99
1192,SKU_001,Staff_10,94,S$39.28,S$65.76
1193,SKU_009,Staff_07,94,S$20.11,S$61.21
1194,SKU_006,Staff_01,57,S$15.46,S$41.68
1195,SKU_016,Staff_07,17,S$33.69,S$78.74
1196,SKU_003,Staff_05,47,S$29.76,S$71.95
1197,SKU_020,Staff_03,23,S$24.95,S$51.71
1198,SKU_004,Staff_03,79,S$26.66,S$79.2
1199,SKU_019,Staff_04,85,S$31.58,S$64.08
1200,SKU_003,Staff_02,14,S$16.85,S$63.3
1201,SKU_019,Staff_02,66,S$39.89,S$69.92
1202,SKU_020,Staff_01,75,S$39.24,S$72.47
1203,SKU_007,Staff_05,51,S$29.51,S$66.26
1204,SKU_020,Staff_04,38,S$15.99,S$45.12
1205,SKU_009,Staff_10,64,S$30.41,S$53.53
1206,SKU_001,Staff_02,98,S$12.17,S$77.12
1207,SKU_008,Staff_03,38,S$10.92,S$48.98
1208,SKU_007,Staff_07,50,S$17.73,S$54.89
1209,SKU_018,Staff_07,98,S$23.88,S$57.28
1210,SKU_008,Staff_04,82,S$36.05,S$57.58
1211,SKU_001,Staff_05,30,S$31.82,S$64.52
1212,SKU_011,Staff_05,79,S$32.28,S$77.72
1213,SKU_018,Staff_06,91,S$22.76,S$49.63
1214,SKU_010,Staff_09,51,S$20.38,S$44.86
1215,SKU_003,Staff_02,63,S$21.13,S$47.9
1216,SKU_007,Staff_05,98,S$39.63,S$75.48
1217,SKU_016,Staff_03,52,S$11.2,S$65.83
1218,SKU_016,Staff_04,38,S$36.01,S$51.44
1219,SKU_020,Staff_10,97,S$27.36,S$72.64
1220,SKU_017,Staff_06,88,S$23.16,S$74.45
1221,SKU_002,Staff_08,79,S$31.76,S$73.86
1222,SKU_001,Staff_01,30,S$24.6,S$76.76
1223,SKU_016,Staff_10,51,S$36.2,S$50.09
1224,SKU_012,Staff_08,81,S$37.02,S$70.2
1225,SKU_005,Staff_07,5,S$22.65,S$58.42
1226,SKU_005,Staff_01,29,S$18.3,S$73.68
1227,SKU_009,Staff_02,4,S$27.77,S$69.14
1228,SKU_009,Staff_03,10,S$37.37,S$71.06
1229,SKU_003,Staff_01,56,S$16.32,S$66.25
1230,SKU_019,Staff_09,17,S$28.69,S$47.1
1231,SKU_016,Staff_08,74,S$28.95,S$61.8
1232,SKU_016,Staff_02,17,S$31.99,S$79.39
1233,SKU_003,Staff_09,84,S$13.95,S$77.5
1234,SKU_020,Staff_07,88,S$31.47,S$41.73
1235,SKU_001,Staff_09,69,S$37.27,S$46.59
1236,SKU_020,Staff_06,34,S$15.39,S$45.27
1237,SKU_011,Staff_06,6,S$17.13,S$69.04
1238,SKU_017,Staff_04,53,S$39.14,S$72.71
1239,SKU_008,Staff_10,66,S$15.43,S$48.54
1240,SKU_004,Staff_10,77,S$35.63,S$60.23
1241,SKU_006,Staff_02,43,S$24.77,S$73.63
1242,SKU_008,Staff_07,75,S$17.42,S$69.31
1243,SKU_020,Staff_05,23,S$36.12,S$61.69
1244,SKU_003,Staff_06,55,S$23.36,S$63.61
1245,SKU_016,Staff_02,80,S$25.44,S$60.33
1246,SKU_003,Staff_05,95,S$20.78,S$51.9
1247,SKU_018,Staff_10,75,S$27.79,S$62.6
1248,SKU_014,Staff_04,16,S$14.91,S$67.56
1249,SKU_018,Staff_09,8,S$21.73,S$74.93
1250,SKU_002,Staff_06,4,S$39.08,S$65.45
1251,SKU_003,Staff_02,4,S$17.74,S$70.44
1252,SKU_016,Staff_01,56,S$29.7,S$46.4
1253,SKU_009,Staff_05,25,S$19.76,S$58.46
1254,SKU_004,Staff_09,67,S$33.2,S$40.37
1255,SKU_001,Staff_06,96,S$13.93,S$49.87
1256,SKU_004,Staff_10,67,S$39.09,S$69.06
1257,SKU_001,Staff_07,27,S$23.61,S$79.67
1258,SKU_014,Staff_05,93,S$17.08,S$43.97
1259,SKU_016,Staff_10,32,S$12.2,S$56.06
1260,SKU_020,Staff_06,50,S$15.09,S$72
1261,SKU_008,Staff_05,61,S$25.59,S$48.16
1262,SKU_007,Staff_09,51,S$20.11,S$62.2
1263,SKU_003,Staff_06,19,S$34.87,S$69.32
1264,SKU_017,Staff_08,21,S$22.93,S$64.64
1265,SKU_001,Staff_02,5,S$17.46,S$47.52
1266,SKU_016,Staff_09,82,S$28.51,S$54.22
1267,SKU_012,Staff_05,92,S$31.2,S$71.35
1268,SKU_019,Staff_07,42,S$15.01,S$62.17
1269,SKU_014,Staff_10,61,S$15.03,S$40.21
1270,SKU_006,Staff_01,22,S$11.1,S$70.44
1271,SKU_006,Staff_10,21,S$32.09,S$41.41
1272,SKU_013,Staff_05,70,S$29.91,S$69.83
1273,SKU_019,Staff_10,1,S$24.24,S$48.1
1274,SKU_008,Staff_02,5,S$35.33,S$78.32
1275,SKU_002,Staff_06,12,S$34.17,S$54.72
1276,SKU_001,Staff_01,90,S$27.56,S$53.08
1277,SKU_015,Staff_03,46,S$36.05,S$45.96
1278,SKU_001,Staff_05,34,S$16.18,S$52.22
1279,SKU_005,Staff_04,49,S$13.36,S$75.07
1280,SKU_016,Staff_03,78,S$18.09,S$79.85
1281,SKU_019,Staff_10,90,S$11.71,S$54.73
1282,SKU_004,Staff_05,45,S$25.94,S$57.94
1283,SKU_003,Staff_08,27,S$38.1,S$68.88
1284,SKU_017,Staff_04,73,S$11.18,S$75.45
1285,SKU_017,Staff_01,26,S$13.66,S$63.72
1286,SKU_012,Staff_07,47,S$23.57,S$55.66
1287,SKU_014,Staff_08,86,S$38.02,S$56.5
1288,SKU_006,Staff_03,56,S$19.48,S$67.82
1289,SKU_003,Staff_06,94,S$25.22,S$40.13
1290,SKU_009,Staff_02,63,S$11.25,S$64.78
1291,SKU_005,Staff_07,48,S$14.45,S$54.22
1292,SKU_017,Staff_08,61,S$39.6,S$71.77
1293,SKU_014,Staff_06,81,S$38.95,S$43.72
1294,SKU_003,Staff_06,26,S$10.15,S$63.53
1295,SKU_001,Staff_05,36,S$38.55,S$59.24
1296,SKU_020,Staff_08,1,S$29.17,S$65.69
1297,SKU_001,Staff_01,8,S$36.04,S$42.59
1298,SKU_003,Staff_10,99,S$23.64,S$63.2
1299,SKU_018,Staff_04,52,S$25.47,S$62.46
1300,SKU_010,Staff_04,79,S$24.67,S$62.43
1301,SKU_003,Staff_03,47,S$30.01,S$64.14
1302,SKU_008,Staff_03,56,S$14.19,S$67.06
1303,SKU_014,Staff_04,86,S$10.9,S$72.2
1304,SKU_018,Staff_01,14,S$19.24,S$50.79
1305,SKU_015,Staff_02,90,S$31.14,S$73
1306,SKU_002,Staff_09,28,S$16.06,S$59.93
1307,SKU_010,Staff_10,87,S$30.2,S$43.08
1308,SKU_002,Staff_02,78,S$39.1,S$42.34
1309,SKU_017,Staff_05,88,S$12.82,S$53.37
1310,SKU_008,Staff_09,2,S$30.18,S$71.4
1311,SKU_001,Staff_09,26,S$23.31,S$68.31
1312,SKU_009,Staff_08,14,S$36.04,S$71.54
1313,SKU_011,Staff_01,59,S$15.31,S$60.69
1314,SKU_016,Staff_01,56,S$30.78,S$57.61
1315,SKU_007,Staff_09,7,S$35.14,S$45.9
1316,SKU_010,Staff_08,3,S$38.34,S$53.13
1317,SKU_003,Staff_10,23,S$30.5,S$57.36
1318,SKU_018,Staff_09,18,S$24.92,S$43.54
1319,SKU_013,Staff_07,38,S$28.54,S$48.82
1320,SKU_007,Staff_03,99,S$36.07,S$63.93
1321,SKU_004,Staff_03,15,S$27.12,S$69.43
1322,SKU_013,Staff_02,64,S$10.91,S$79.93
1323,SKU_020,Staff_05,89,S$37.93,S$77.32
1324,SKU_001,Staff_03,28,S$30.69,S$65.7
1325,SKU_008,Staff_06,74,S$30.3,S$56.85
1326,SKU_014,Staff_02,39,S$16.47,S$65.45
1327,SKU_016,Staff_03,57,S$29.77,S$71.43
1328,SKU_014,Staff_05,17,S$21.82,S$44.73
1329,SKU_012,Staff_01,86,S$29.54,S$56.4
1330,SKU_019,Staff_01,90,S$13.2,S$73.59
1331,SKU_015,Staff_10,44,S$29.74,S$55.35
1332,SKU_002,Staff_09,25,S$39.98,S$62.87
1333,SKU_002,Staff_07,17,S$11.45,S$63.51
1334,SKU_019,Staff_01,13,S$39.32,S$47.38
1335,SKU_017,Staff_08,84,S$22.21,S$54.49
1336,SKU_020,Staff_03,25,S$36.12,S$53.38
1337,SKU_010,Staff_08,68,S$33.47,S$41.05
1338,SKU_006,Staff_05,10,S$27.01,S$40.97
1339,SKU_015,Staff_01,67,S$32.15,S$73.27
1340,SKU_011,Staff_07,18,S$36.36,S$50.92
1341,SKU_005,Staff_05,86,S$22.12,S$60.72
1342,SKU_001,Staff_06,34,S$19.81,S$51.95
1343,SKU_008,Staff_06,8,S$30.03,S$77.63
1344,SKU_012,Staff_08,40,S$34.24,S$50.37
1345,SKU_012,Staff_09,83,S$32.87,S$57.19
1346,SKU_005,Staff_02,42,S$33.93,S$74.91
1347,SKU_007,Staff_09,41,S$23.07,S$73.68
1348,SKU_004,Staff_10,6,S$34.54,S$47.44
1349,SKU_006,Staff_09,52,S$13.61,S$72.11
1350,SKU_013,Staff_10,26,S$26.33,S$58.33
1351,SKU_020,Staff_10,64,S$10.17,S$59.32
1352,SKU_015,Staff_07,98,S$19.74,S$45.34
1353,SKU_003,Staff_01,59,S$20.99,S$43.22
1354,SKU_008,Staff_07,56,S$21.89,S$69.12
1355,SKU_020,Staff_10,59,S$30.86,S$59.86
1356,SKU_016,Staff_05,70,S$21.66,S$57.47
1357,SKU_013,Staff_06,33,S$23.46,S$69.18
1358,SKU_018,Staff_10,53,S$17.13,S$70.62
1359,SKU_010,Staff_07,22,S$21.2,S$46.36
1360,SKU_019,Staff_05,21,S$16.82,S$64.41
1361,SKU_017,Staff_07,70,S$12.2,S$45.41
1362,SKU_019,Staff_09,70,S$28.1,S$70.06
1363,SKU_005,Staff_03,4,S$30.05,S$66.28
1364,SKU_009,Staff_08,94,S$28.58,S$78.26
1365,SKU_012,Staff_02,75,S$23.9,S$42.76
1366,SKU_001,Staff_07,62,S$21.39,S$42.28
1367,SKU_001,Staff_02,62,S$35.9,S$51.29
1368,SKU_015,Staff_04,94,S$25.57,S$50.47
1369,SKU_002,Staff_07,95,S$24.38,S$49.88
1370,SKU_016,Staff_03,24,S$10.77,S$76.25
1371,SKU_008,Staff_02,55,S$20.24,S$49.98
1372,SKU_013,Staff_10,9,S$21.41,S$50.88
1373,SKU_001,Staff_07,3,S$21.96,S$70.38
1374,SKU_016,Staff_01,31,S$27.41,S$57.99
1375,SKU_007,Staff_08,40,S$26.01,S$71.07
1376,SKU_005,Staff_03,36,S$28.24,S$42.61
1377,SKU_003,Staff_02,24,S$32.95,S$59.5
1378,SKU_012,Staff_03,95,S$34.39,S$41.34
1379,SKU_016,Staff_05,6,S$31.54,S$42.51
1380,SKU_019,Staff_08,66,S$38.67,S$76.26
1381,SKU_005,Staff_10,84,S$10.55,S$45.57
1382,SKU_014,Staff_07,92,S$15.87,S$61.3
1383,SKU_005,Staff_07,75,S$10.23,S$56.44
1384,SKU_015,Staff_07,4,S$29.42,S$53.89
1385,SKU_017,Staff_08,79,S$36.94,S$75.99
1386,SKU_014,Staff_01,6,S$17.3,S$40.87
1387,SKU_020,Staff_04,94,S$37.81,S$66.55
1388,SKU_005,Staff_06,51,S$11.81,S$78.54
1389,SKU_012,Staff_09,62,S$38.03,S$62.41
1390,SKU_016,Staff_02,57,S$20.55,S$77.47
1391,SKU_016,Staff_01,66,S$13.04,S$42.09
1392,SKU_007,Staff_10,79,S$24.58,S$56.75
1393,SKU_004,Staff_02,75,S$17.7,S$50.41
1394,SKU_001,Staff_07,8,S$18.55,S$69.23
1395,SKU_005,Staff_03,26,S$19.22,S$79.25
1396,SKU_010,Staff_10,51,S$34.09,S$50.26
1397,SKU_005,Staff_02,45,S$26.17,S$66.17
1398,SKU_004,Staff_07,44,S$19.34,S$47.92
1399,SKU_002,Staff_02,5,S$28.31,S$62.61
1400,SKU_020,Staff_03,70,S$31.48,S$58.56
1401,SKU_010,Staff_07,26,S$18.18,S$78.88
1402,SKU_019,Staff_04,68,S$22.41,S$64.34
1403,SKU_001,Staff_01,19,S$13.66,S$53.98
1404,SKU_005,Staff_05,84,S$15.43,S$44.56
1405,SKU_013,Staff_09,97,S$30.43,S$46.05
1406,SKU_004,Staff_08,20,S$15.44,S$49.01
1407,SKU_016,Staff_09,12,S$25.75,S$50.04
1408,SKU_016,Staff_10,47,S$31.27,S$74.02
1409,SKU_002,Staff_09,1,S$13.21,S$62.45
1410,SKU_017,Staff_07,90,S$27.02,S$60.94
1411,SKU_020,Staff_04,14,S$17.7,S$44.59
1412,SKU_012,Staff_05,64,S$38.89,S$74.41
1413,SKU_018,Staff_01,38,S$24.51,S$68.91
1414,SKU_003,Staff_01,37,S$34.18,S$42.71
1415,SKU_001,Staff_03,11,S$26.51,S$68.31
1416,SKU_001,Staff_08,77,S$11.3,S$61.74
1417,SKU_019,Staff_02,3,S$28.99,S$43.27
1418,SKU_011,Staff_04,33,S$38.54,S$58.33
1419,SKU_005,Staff_02,6,S$28.05,S$59.39
1420,SKU_012,Staff_05,50,S$34.58,S$46.63
1421,SKU_003,Staff_09,10,S$36.53,S$77.83
1422,SKU_001,Staff_01,5,S$16.84,S$74
1423,SKU_001,Staff_05,23,S$16.36,S$66.76
1424,SKU_008,Staff_09,10,S$28.33,S$58.49
1425,SKU_010,Staff_01,44,S$22.33,S$56.47
1426,SKU_011,Staff_09,2,S$35.2,S$66.04
1427,SKU_012,Staff_08,13,S$37,S$61.82
1428,SKU_013,Staff_04,40,S$20.6,S$42.49
1429,SKU_012,Staff_10,2,S$17.11,S$60.5
1430,SKU_014,Staff_05,84,S$33.42,S$72.26
1431,SKU_002,Staff_05,65,S$18.24,S$58.37
1432,SKU_019,Staff_06,63,S$34.68,S$42.08
1433,SKU_018,Staff_07,73,S$22.71,S$71.45
1434,SKU_003,Staff_08,17,S$30.03,S$48.05
1435,SKU_017,Staff_08,9,S$12.87,S$50.34
1436,SKU_008,Staff_02,75,S$28.72,S$46.59
1437,SKU_010,Staff_09,15,S$23.55,S$53.21
1438,SKU_002,Staff_07,24,S$27.6,S$70.27
1439,SKU_019,Staff_04,38,S$15.04,S$60.78
1440,SKU_009,Staff_04,35,S$32.11,S$48.2
1441,SKU_007,Staff_08,94,S$35.88,S$75.11
1442,SKU_004,Staff_04,95,S$16.5,S$75.18
1443,SKU_018,Staff_06,49,S$12.87,S$74.82
1444,SKU_013,Staff_05,69,S$10.71,S$49.55
1445,SKU_011,Staff_03,62,S$29.26,S$58.05
1446,SKU_004,Staff_10,60,S$28.21,S$79.4
1447,SKU_004,Staff_02,50,S$26.4,S$70.88
1448,SKU_010,Staff_09,78,S$16.96,S$41.09
1449,SKU_005,Staff_10,75,S$21.73,S$42.61
1450,SKU_009,Staff_09,9,S$27.83,S$58.56
1451,SKU_003,Staff_01,34,S$24.9,S$76.37
1452,SKU_017,Staff_10,76,S$39.63,S$61.55
1453,SKU_003,Staff_03,99,S$14.09,S$59.91
1454,SKU_016,Staff_08,35,S$30.85,S$44.22
1455,SKU_004,Staff_06,1,S$22.13,S$66.27
1456,SKU_018,Staff_05,40,S$22.85,S$72.88
1457,SKU_017,Staff_05,64,S$31.53,S$55.22
1458,SKU_007,Staff_06,22,S$30.77,S$71.02
1459,SKU_005,Staff_07,60,S$39.74,S$78.58
1460,SKU_012,Staff_01,64,S$13.85,S$48.15
1461,SKU_017,Staff_09,93,S$13.12,S$60.93
1462,SKU_013,Staff_03,72,S$31.73,S$51.49
1463,SKU_003,Staff_04,11,S$27.35,S$71.71
1464,SKU_009,Staff_10,14,S$18.22,S$63.1
1465,SKU_017,Staff_01,60,S$12.38,S$65.38
1466,SKU_017,Staff_10,30,S$12.57,S$71.92
1467,SKU_020,Staff_03,35,S$36.83,S$55.84
1468,SKU_016,Staff_02,85,S$15.76,S$76.6
1469,SKU_013,Staff_02,37,S$19.7,S$61.32
1470,SKU_019,Staff_01,5,S$16.8,S$46.32
1471,SKU_017,Staff_08,83,S$20.65,S$67.84
1472,SKU_004,Staff_03,78,S$12.08,S$71.73
1473,SKU_012,Staff_03,26,S$25.57,S$52.67
1474,SKU_009,Staff_06,62,S$12.03,S$74.29
1475,SKU_019,Staff_08,4,S$34.01,S$76.25
1476,SKU_012,Staff_09,89,S$17.01,S$51.08
1477,SKU_009,Staff_09,42,S$26.2,S$79.34
1478,SKU_007,Staff_04,89,S$36.4,S$45.63
1479,SKU_014,Staff_05,18,S$29.53,S$48.08
1480,SKU_020,Staff_02,40,S$25.99,S$47.37
1481,SKU_019,Staff_09,72,S$19.73,S$75.76
1482,SKU_015,Staff_08,39,S$19.99,S$66.17
1483,SKU_016,Staff_03,14,S$30.08,S$46.08
1484,SKU_005,Staff_09,32,S$39.82,S$57.61
1485,SKU_003,Staff_03,51,S$29.86,S$64.61
1486,SKU_012,Staff_09,38,S$26.73,S$43.34
1487,SKU_020,Staff_02,97,S$31.92,S$75.3
1488,SKU_004,Staff_10,23,S$23.96,S$72.14
1489,SKU_016,Staff_09,63,S$11.8,S$60.21
1490,SKU_007,Staff_08,15,S$26.87,S$78.69
1491,SKU_013,Staff_09,97,S$38.73,S$56.71
1492,SKU_010,Staff_05,25,S$15.26,S$79.36
1493,SKU_007,Staff_02,17,S$30.7,S$66.72
1494,SKU_014,Staff_08,97,S$16.03,S$65.39
1495,SKU_005,Staff_06,66,S$26.07,S$46.64
1496,SKU_003,Staff_08,78,S$12.9,S$75.28
1497,SKU_011,Staff_05,53,S$23.51,S$57.1
1498,SKU_011,Staff_10,51,S$32.68,S$46.49
1499,SKU_018,Staff_02,39,S$20.43,S$40.5

"""