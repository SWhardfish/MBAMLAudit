import os
import subprocess
import time
from configparser import ConfigParser

# Read config.ini file
config_object = ConfigParser()
config_object.read("Config/config.ini")

# Get the MonthYear from Config.ini
monthyear = config_object["MonthYear"]
month = monthyear["month"]
year = monthyear["year"]

# Start the overall timer
start_time_total = time.time()

# Run VismaParseXMLtoJSON.py with timer
start_time_sub = time.time()
subprocess.run(["C:/Users/exi162/PycharmProjects/AMLAudit/venv/Scripts/python.exe", "Scripts/VismaParseXMLtoJSON.py"])
end_time_sub = time.time()
print(f" BGMaxParserJSON.py for {month}-{year}: {end_time_sub - start_time_sub} seconds")

# Run FuzzyMatching.py with timer
start_time_sub = time.time()
subprocess.run(["C:/Users/exi162/PycharmProjects/AMLAudit/venv/Scripts/python.exe", "Scripts/FuzzyMatchingVisma.py"])
end_time_sub = time.time()
print(f"   FuzzyMatching.py for {month}-{year}: {end_time_sub - start_time_sub} seconds")

# Run GroupingData.py after running the above scripts
start_time_sub = time.time()
subprocess.run(["C:/Users/exi162/PycharmProjects/AMLAudit/venv/Scripts/python.exe", "Scripts/GroupingDataVisma.py"])
end_time_sub = time.time()
print(f"    GroupingData.py for {month}-{year}: {end_time_sub - start_time_sub} seconds")

# Print total script execution time
end_time_total = time.time()
print( )
print(f"Total script execution time for {month}-{year}: {end_time_total - start_time_total} seconds")
