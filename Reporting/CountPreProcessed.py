import os
import json
import calendar
import matplotlib.pyplot as plt

# Base directory for the data
base_directory = "../BGMaxFiles"

# Initialize a variable to store the total count of 'id' in JSON files
total_count = 0

# Iterate over the years (2022 and 2023)
for year in [2022, 2023]:
    for month in range(1, 13):
        month_name = f"{year}/{calendar.month_abbr[month]}"
        month_directory = os.path.join(base_directory, month_name, "PreProcessed/InvoiceProcessed")

        # Check if the directory for the month exists
        if os.path.exists(month_directory):
            # List all files in the directory
            files = os.listdir(month_directory)

            # Check if the directory is not empty
            if len(files) > 0:
                for filename in files:
                    file_path = os.path.join(month_directory, filename)
                    if os.path.isfile(file_path) and filename.endswith('.json'):
                        with open(file_path, 'r', encoding="utf8") as file:
                            data = json.load(file)
                            if 'payments' in data and isinstance(data['payments'], list):
                                for payment in data['payments']:
                                    if 'id' in payment:
                                        total_count += 1

# Plot the total count in a single bar
plt.figure(figsize=(6, 6))
plt.bar("Total", total_count)
plt.text(0, total_count + 10, f"Total: {total_count}", ha='center', fontsize=12)  # Display the total count
plt.xlabel("Total")
plt.ylabel("Count of 'id' in JSON files")
plt.title("Count of 'id' in JSON files for 2022 and 2023")
plt.tight_layout()
plt.show()
