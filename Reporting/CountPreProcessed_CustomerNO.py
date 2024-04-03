import os
import json
import matplotlib.pyplot as plt
from calendar import month_abbr

# Define the path to the directory
base_path = '../BGMaxFiles/'

# Define the months and years
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
years = [2022, 2023]

# Initialize dictionaries to store counts for the first subplot
total_customer_no = {}
total_not_found = {}

# Initialize dictionaries to store counts for the second subplot
total_customer_no_2 = {}
total_not_found_2 = {}

# Iterate over years and months
for year in years:
    for month in months:
        folder_path = os.path.join(base_path, str(year), month, 'PreProcessed')
        folder_path_2 = os.path.join(base_path, str(year), month, 'PreProcessed/InvoiceProcessed')

        # Check if the folder exists
        if os.path.exists(folder_path):
            key = f"{month_abbr[months.index(month) + 1]}-{year}"  # Format month-year

            total_customer_no[key] = 0
            total_not_found[key] = 0

            total_customer_no_2[key] = 0
            total_not_found_2[key] = 0

            # Iterate over files in the first folder
            for filename in os.listdir(folder_path):
                if filename.endswith('.json'):
                    file_path = os.path.join(folder_path, filename)

                    # Parse the JSON data from the file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Count "CustomerNo" and "CustomerNo": "NotFound"
                    for payment_record in data["payments"]:
                        customer_no = payment_record["PaymentRecord(20)"]["CustomerNo"]
                        if customer_no == "NotFound":
                            total_not_found[key] += 1
                        total_customer_no[key] += 1

            # Iterate over files in the second folder
            for filename in os.listdir(folder_path_2):
                if filename.endswith('.json'):
                    file_path = os.path.join(folder_path_2, filename)

                    # Parse the JSON data from the file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                    # Count "CustomerNo" and "CustomerNo": "NotFound" for the second subplot
                    for payment_record in data["payments"]:
                        customer_no = payment_record["PaymentRecord(20)"]["CustomerNo"]
                        if customer_no == "NotFound":
                            total_not_found_2[key] += 1
                        total_customer_no_2[key] += 1

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Create a bar chart for the first subplot
ax1.bar(total_customer_no.keys(), total_customer_no.values(), label="Total CustomerNo")
ax1.bar(total_not_found.keys(), total_not_found.values(), label="Total CustomerNo: NotFound")
ax1.set_ylabel("Count")
ax1.set_title("Total Counts for CustomerNo: NotFound (Pre-Processed)")
ax1.set_xticklabels(total_customer_no.keys(), rotation=45)  # Show x-axis labels for the first subplot
ax1.legend()

# Create a bar chart for the second subplot
ax2.bar(total_customer_no_2.keys(), total_customer_no_2.values(), label="Total CustomerNo")
ax2.bar(total_not_found_2.keys(), total_not_found_2.values(), label="Total CustomerNo: NotFound")
ax2.set_xlabel("Month-Year")
ax2.set_ylabel("Count")
ax2.set_title("Total Counts for CustomerNo: NotFound (InvoiceNo Processed)")
ax2.set_xticklabels(total_customer_no_2.keys(), rotation=45)  # Show x-axis labels for the second subplot
ax2.legend()

# Adjust the layout to prevent overlapping
plt.tight_layout()

# Show the chart
plt.show()
