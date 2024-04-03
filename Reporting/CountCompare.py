import os
import json
import calendar
import matplotlib.pyplot as plt
import seaborn as sns

base_directory = '../BGMaxFiles/'

# List of directories to process  - NOT IN USE
directories = [
    '../BGMaxFiles/2022/Jan/',
    '../BGMaxFiles/2022/Feb/',
    '../BGMaxFiles/2022/Mar/',
    '../BGMaxFiles/2022/Apr/',
    '../BGMaxFiles/2022/May/',
    '../BGMaxFiles/2022/Jun/',
    '../BGMaxFiles/2022/Jul/',
    '../BGMaxFiles/2022/Aug/',
    '../BGMaxFiles/2022/Sep/',
    '../BGMaxFiles/2022/Oct/',
    '../BGMaxFiles/2022/Nov/',
    '../BGMaxFiles/2022/Dec/',
    '../BGMaxFiles/2023/Jan/',
    '../BGMaxFiles/2023/Feb/',
    '../BGMaxFiles/2023/Mar/',
    '../BGMaxFiles/2023/Apr/',
    '../BGMaxFiles/2023/May/',
    '../BGMaxFiles/2023/Jun/',
    '../BGMaxFiles/2023/Jul/',
    '../BGMaxFiles/2023/Aug/',
    '../BGMaxFiles/2023/Sep/',
    '../BGMaxFiles/2023/Oct/',
    '../BGMaxFiles/2023/Nov/',
    '../BGMaxFiles/2023/Dec/'
]

# Initialize counts for each pattern
pattern_counts = {"20": 0, "22": 0, "25": 0, "26": 0, "27": 0, "28": 0, "29": 0}

# Iterate over the directories for Code 1
for directory_path in directories:
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    for pattern in pattern_counts.keys():
                        if line.strip().startswith(pattern):
                            pattern_counts[pattern] += 1

# Calculate the total count for Code 1
total_count_code1 = sum(pattern_counts.values())

# Initialize a variable to store the total count of 'id' in JSON files for Code 2
total_count_code2 = 0

# Iterate over the years (2022 and 2023) for Code 2
for year in [2022, 2023]:
    for month in range(1, 13):
        month_name = f"{year}/{calendar.month_abbr[month]}"
        month_directory = os.path.join(base_directory, month_name, "PreProcessed/InvoiceProcessed")

        if os.path.exists(month_directory):
            files = os.listdir(month_directory)

            if len(files) > 0:
                for filename in files:
                    file_path = os.path.join(month_directory, filename)
                    if os.path.isfile(file_path) and filename.endswith('.json'):
                        with open(file_path, 'r', encoding="utf8") as file:
                            data = json.load(file)
                            if 'payments' in data and isinstance(data['payments'], list):
                                for payment in data['payments']:
                                    if 'id' in payment:
                                        total_count_code2 += 1

# Create subplots
plt.figure(figsize=(12, 5))

# Subplot for Code 1
plt.subplot(1, 2, 1)
patterns = pattern_counts.keys()
counts = pattern_counts.values()
sns.set(style="whitegrid")
ax1 = sns.barplot(x=list(patterns), y=list(counts), palette="Blues", width=0.3)  # Use a neutral blue palette
ax1.set(xlabel='BGMax Row Types', ylabel='Counts')
plt.title('Row counts in the raw BGMax Files Jan 2022 - Dec 2023')
for pattern, count in zip(patterns, counts):
    ax1.text(pattern, count, str(count), ha='center', va='bottom', size=10)

# Subplot for Code 2
plt.subplot(1, 2, 2)
plt.bar("Total", total_count_code2, color='lightgray', width=0.1)  # Use a light gray color
plt.text(0, total_count_code2 + 10, f"Total: {total_count_code2}", ha='center', fontsize=10)
#plt.xlabel("Total")
plt.ylabel("Count of payment records (id) in JSON files")
plt.title("Count of payment records (id) in JSON files for 2022 and 2023")

plt.tight_layout()
plt.show()
