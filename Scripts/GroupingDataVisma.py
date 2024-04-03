import os
import pandas as pd
from datetime import datetime
from configparser import ConfigParser
import openpyxl

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# Read config.ini file
config_object = ConfigParser()
config_object.read("Config/config.ini")

# Get the MonthYear
monthyear = config_object["MonthYear"]
year = monthyear["year"]
month = monthyear["month"]

# Get the current date and time
current_time = datetime.now()
# Format the timestamp as 'YYYYMMM-YYYYMMM'
timestamp = current_time.strftime('%Y%m%d%H%M%S')

# Define the directory where the Fuzzy Logic matched CSV files are located
directories = [
    f'ResultOutput/VismaFiles/{year}/{month}/Matched'
]
# Initialize an empty list to store DataFrames
dfs = []

# Iterate through the directories and read all CSV files
for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith("Matched.csv"):
            file_path = os.path.join(directory, filename)
            df = pd.read_csv(file_path)
            dfs.append(df)

# Concatenate the DataFrames in the list
combined_data = pd.concat(dfs, ignore_index=True)

# Group the data by 'CustomerNo' and sort each group by 'Date'
sorted_data = combined_data.groupby('CustomerNo').apply(lambda x: x.sort_values(by='Date')).reset_index(drop=True)

# Print the sorted data
#print(sorted_data)

# Save the sorted data to an Excel file
sorted_data.to_excel(f'ResultOutput/MatchedVismaPayments-{month}-{year}_{timestamp}.xlsx', index=False)
#print(sorted_data)
