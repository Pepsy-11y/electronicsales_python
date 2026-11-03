#Electronics Sales Data Analysis Using Python
## 1. Project Overview
This project involves analysing an electronics sales dataset using Python. 
The goal was to explore sales transactions, understand revenue performance and identify 
patterns across products, stores and payment methods.

Rather than relying on raw figures, I worked on preparing the data, performing calculations 
and extracting information that could help explain business performance and support better decision-making.
## 2. Project Objectives
The analysis focused on:
- Understanding the structure and quality of the sales data.
- Cleaning and preparing raw records for analysis.
- Calculating total sales revenue and key descriptive statistics.
- Comparing revenue across different products, stores and payment methods.
- Identifying the top three products by revenue.
- Examining high-value transactions exceeding KES 50,000.
- Validating selected calculations using Pandas.
  
## 3. Tools and Technologies
- Python: Main programming language used to process and analyse the dataset.
- CSV module: Read and handled records from the CSV file.
- Regular Expressions (re): Assisted with cleaning and standardising values.
- Decimal: Supported accurate financial calculations.
- Pandas: Used to cross-check selected results and validate the analysis.
  
## 4. Analysis Workflow
The project followed a structured data analysis process:
1. Data ingestion: Loaded the sales dataset using Python's CSV module and inspected the available records and columns.
2. Data cleaning: Identified and handled inconsistencies in the data, including values requiring conversion and
   standardisation.
4. Data transformation: Converted relevant fields into appropriate numeric formats to support accurate calculations.
5. Data analysis: Used Python functions to calculate revenue, summarise sales performance and compare results across
   different categories.
7. Validation: Used Pandas to independently verify selected calculations and improve confidence in the results.
   
## 5. Key Analysis Areas
The project explored several business questions:
- How much revenue was generated from the recorded transactions?
- Which products contributed the most revenue?
- How did revenue vary across stores?
- Which payment methods accounted for sales revenue?
- Which transactions had a value exceeding KES 50,000?
- What were the average, median, minimum and maximum sales values?

## 6. Project Structure

day2-sales-analytics/
│
├── data/
│   └── electronics_sales.csv
│
├── notebooks/
│   └── sales_analysis.py
│
├── output/
│   └── sales_report.txt
│
├── requirements.txt
└── README.md

## 7. Key Learning Outcomes
Working on this project strengthened my practical understanding of Python programming and its application in data analysis.
I gained experience in:
- Writing reusable functions to organise analytical tasks.
- Reading and processing CSV files.
- Working with dictionaries, lists and loops.
- Handling missing, inconsistent and incorrectly formatted values.
- Using regular expressions and Decimal for data cleaning and financial calculations.
- Performing aggregations and descriptive statistical analysis.
- Validating results using Pandas.
  
## 8. Conclusion
This project provided practical experience in taking raw sales data through a structured analysis process. 
It helped me develop a better understanding of how Python can be used to clean data, perform calculations and 
generate information that is useful for business analysis.
The project also strengthened my ability to approach data-related problems logically, write organised code and 
verify analytical results.
