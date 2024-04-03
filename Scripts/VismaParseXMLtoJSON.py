import xml.etree.ElementTree as ET
import json
import os
from configparser import ConfigParser

def xml_to_json(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Initialize an empty list to store JSON records
    json_records = []

    # Iterate over each record in the XML
    for payment in root.findall('.//Details'):
        # Initialize a dictionary to store record attributes
        record = {}

        # Extract attributes from each record
        record_attributes = payment.attrib

        # Replace the . with ,
        amount = record_attributes.get("Amount")
        if '.' in amount:
            amount = amount.replace('.', ',')

        # Create the PaymentRecord(20) dictionary
        payment_record = {
            "CustomerNo": record_attributes.get("CustomerNo"),
            "InvoiceNo": record_attributes.get("InvoiceNo"),
            "Amount": amount,
            "OrgRow": f"{record_attributes.get('DebtorOrgNo')} {record_attributes.get('DebtorName')} {record_attributes.get('DebtorCity')} {record_attributes.get('DebtorAddress')} {record_attributes.get('DebtorPostCode')}"
        }

        # Remove '-' from CompanyNumber
        company_number = record_attributes.get("PayerOrgNumber").replace('-', '')

        # Create the JSON record
        record = {
            "id": record_attributes.get("Date"),
            "PaymentRecord(20)": payment_record,
            "XRefRecord(22)": [],
            "Name": record_attributes.get("PayerName"),
            "Address": f"{record_attributes.get('PayerAddress')} {record_attributes.get('PayerPostCode')}",
            "City": record_attributes.get("PayerCity"),
            "CompanyNumber": company_number,
            "Match": record_attributes.get("Match")
        }

        # Append the JSON record to the list
        json_records.append(record)

    # Create the final JSON object
    json_data = {"payments": json_records}

    # Convert the JSON object to a JSON string
    json_string = json.dumps(json_data, ensure_ascii=False, indent=4)

    return json_string

# Read config.ini file
config_object = ConfigParser()
config_object.read("Config/config.ini")

# Get the MonthYear from Config.ini
monthyear = config_object["MonthYear"]
month = monthyear["month"]
year = monthyear["year"]

# Get the FF9SE Customers from Config.ini
VismaPaymentsFile = config_object["VismaPaymentsFile"]
VismaPaymFile = VismaPaymentsFile["VismaPaymFile"]

# File path to XML input
xml_file = f"{VismaPaymFile}"

# Convert XML to JSON
json_output = xml_to_json(xml_file)

# File path to save JSON output
output_file_path = f'ResultOutput/VismaFiles/{year}/{month}/PreProcessed'  # PreProcessed JSON output files


# Ensure output directories exist
os.makedirs(output_file_path, exist_ok=True)

"""
# Write JSON output to file
with open(output_file_path, 'w', encoding='utf8') as output_file:
    output_file.write(json_output)

print("JSON output has been saved to:", output_file_path)
"""

# Specify the JSON filename
output_filename = f"VismaPreProcess-{year}-{month}.json"
output_file_full_path = os.path.join(output_file_path, output_filename)

# Write JSON output to file
with open(output_file_full_path, 'w', encoding='utf8') as output_file:
    output_file.write(json_output)

print("JSON output has been saved to:", output_file_full_path)