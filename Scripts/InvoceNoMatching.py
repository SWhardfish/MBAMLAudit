import re
import csv
import json
import os
from configparser import ConfigParser

# Read config.ini file
config_object = ConfigParser()
config_object.read("Config/config.ini")

# Get the MonthYear from Config.ini
monthyear = config_object["MonthYear"]
year = monthyear["year"]
month = monthyear["month"]

# Get the CustomerLedgerFile from Config.ini
FF9SECustomerLedgerFile = config_object["FF9SECustomerLedgerFile"]
FF9SECustLedgFile = FF9SECustomerLedgerFile["FF9SECustLedgFile"]


# Define the regular expression pattern to match 'OrgRow'
pattern = re.compile(r'([7|8]\d{6}).*(?:[7|8]\d{6})?')

# Read the CSV file and store it in a dictionary for quick lookups
csv_data = {}
csv_file_path = f'{FF9SECustLedgFile}'
with open(csv_file_path, 'r') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=';')
    for row in reader:
        invoice_no = row['Document No_']
        customer_no = row['Customer No_']
        csv_data[invoice_no] = customer_no

# Specify the input directory containing JSON files
input_directory = f'ResultOutput/BGMaxFiles/{year}/{month}/PreProcessed'
# Specify the output directory for updated JSON files
output_directory = f'ResultOutput/BGMaxFiles/{year}/{month}/PreProcessed/InvoiceProcessed'

# Ensure output directories exist
os.makedirs(output_directory, exist_ok=True)

# Loop through JSON files in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith(".json"):
        json_file_path = os.path.join(input_directory, filename)

        # Read the JSON file
        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        # Function to extract InvoiceNo using the precompiled regular expression pattern
        def extract_invoice_no(org_row):
            match = pattern.search(org_row)
            if match:
                return match.group(1)
            return None

        # Process the records in the JSON file
        for record in data["payments"]:
            payment_record = record.get("PaymentRecord(20)", {})
            customer_no = payment_record.get("CustomerNo")
            org_row = payment_record.get("OrgRow")

            # If 'CustomerNo' is "NotFound," extract 'InvoiceNo' and update 'CustomerNo'
            if customer_no == "NotFound":
                invoice_no = extract_invoice_no(org_row)
                #print(invoice_no)
                if invoice_no:
                    customer_no = csv_data.get(invoice_no, customer_no)
                    #print(customer_no)
                    payment_record["CustomerNo"] = customer_no

        # Save the updated JSON file in the output directory with the same filename
        updated_json_file_path = os.path.join(output_directory, filename)
        with open(updated_json_file_path, 'w', encoding='utf-8') as updated_json_file:
            json.dump(data, updated_json_file, indent=4, ensure_ascii=False)

        #print(f'Updated JSON file saved as {updated_json_file_path}')
