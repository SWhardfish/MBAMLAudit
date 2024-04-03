import csv
import os
import matplotlib.pyplot as plt

def count_rows_in_csv(directory):
    total_rows = 0

    # Loop through all files in the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', newline='', encoding='utf-8') as file:
                        csv_reader = csv.reader(file)
                        rows_in_file = sum(1 for row in csv_reader)
                        total_rows += rows_in_file
                except Exception as e:
                    print(f"Error reading file {filename}: {str(e)}")

    return total_rows

# Replace 'your_base_directory_path' with the base directory path containing the CSV files
base_directory_path = '../ResultOutput/BGMaxFiles/'

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
total_rows = 0
rows_per_month = {'2024': []}

for year in ["2024"]:
    for month in months:
        directory_path = os.path.join(base_directory_path, year, month, "PreProcessed")
        rows_in_month = count_rows_in_csv(directory_path)
        print(f"Total rows in {month} {year}: {rows_in_month}")
        rows_per_month[year].append(rows_in_month)
        total_rows += rows_in_month

print(f"Total rows in all CSV files for 2024: {total_rows}")

# Plotting the data
years = list(rows_per_month.keys())
for i, year in enumerate(years):
    plt.bar([j + i * 0.2 for j in range(len(months))], rows_per_month[year], width=0.2, align='center', label=year)

plt.xlabel('Month')
plt.ylabel('Total Rows')
plt.title('Total Rows in BGMax Files for Each Month for 2024')
plt.xticks([i + 0.2 for i in range(len(months))], months)
plt.legend()
plt.tight_layout()
plt.show()
