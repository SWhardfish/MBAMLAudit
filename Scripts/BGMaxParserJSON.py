import re
import json
import os
from configparser import ConfigParser

# Read config.ini file
config_object = ConfigParser()
config_object.read("Config/config.ini")

# Get the MonthYear from Config.ini
monthyear = config_object["MonthYear"]
month = monthyear["month"]
year = monthyear["year"]


# Function to create a unique ID
def generate_unique_id(data, record_type, filename_prefix):
    if record_type == 'payments':
        if 'id' not in data:
            data['id'] = 1
        else:
            data['id'] += 1
        return f'{filename_prefix}-{data["id"]}'

# Define the regex pattern for rows starting with '20'
regex_pattern_20 = r'^20.*([5|3|8|9]\d{7})([9|8|7|1]\d{6})([7][0-9])(\d{18})(.*[2159][4|5][0-9][0-9].*)'
# Define the regex pattern for rows starting with '22'
regex_pattern_22 = r'^22.*([5|3|8|9]\d{7})([9|8|7|1]\d{6})([7][0-9])(.*[0][0])(.*[2159][4|5][0-9][0-9].*)'
# Define the regex pattern for rows starting with '25'
regex_pattern_25 = r'^25([5]\d{7})?([8]\d{6})?([7][0-9])?(.*d*[,][0-9][0-9])'

# Specify the input directory and output directory
input_dir = f'InputData/PaymentData/BGMaxPayments'  # BGMax files directory
output_dir = f'ResultOutput/BGMaxFiles/{year}/{month}/PreProcessed'  # PreProcessed JSON output files

# Ensure output directories exist
os.makedirs(output_dir, exist_ok=True)

# List files in the input directory
for filename in os.listdir(input_dir):
    if os.path.isfile(os.path.join(input_dir, filename)):
        # Extract the last eight digits from the filename to use as a prefix
        filename_prefix = re.search(r'(\d{8})$', filename).group(1)

        # Initialize variables for each file
        data = {}
        current_payment = {}
        payments = []
        insert_row_after_initial_01 = False
        found_row_22 = False  # Add a flag to track the presence of row 22

        # Read the text file with 'utf-8' encoding
        with open(os.path.join(input_dir, filename), 'r') as file:
            for line in file:
                line = line.strip()
                first_two_digits = line[:2]

                if first_two_digits == '01':
                    data['header'] = {}
                    date_match = re.search(r'((19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))', line)
                    if date_match:
                        data['header']['Date'] = date_match.group(0)
                    else:
                        insert_row_after_initial_01 = True
                elif insert_row_after_initial_01:
                    # Insert the row after the initial '01' without a date
                    data['header']['Date'] = line
                    insert_row_after_initial_01 = False
                elif first_two_digits == '05':
                    data['header']['Opening'] = line[2:]
                elif first_two_digits == '15':
                    data['header']['Deposit'] = line[2:]
                elif first_two_digits == '70':
                    data['header']['End'] = line[2:]
                elif first_two_digits == '20':
                    unique_id = generate_unique_id(data, 'payments', filename_prefix)
                    match = re.match(regex_pattern_20, line)
                    if match:
                        current_payment = {
                            'id': unique_id,
                            'PaymentRecord(20)': {
                                'CustomerNo': match.group(1),
                                'InvoiceNo': match.group(2),
                                'Amount': match.group(4).lstrip('0'),
                                'OrgRow': line  # Add the OrgRow field
                            },
                            'XRefRecord(22)': []  # Initialize the list for 'XRefRecord(22)'
                        }
                    else:
                        current_payment = {
                            'id': unique_id,
                            'PaymentRecord(20)': {
                                'CustomerNo': 'NotFound',
                                'InvoiceNo': 'NotFound',
                                'Amount': 'NotFound',
                                'OrgRow': line  # Add the OrgRow field
                            }
                        }
                    payments.append(current_payment)
                elif first_two_digits == '21':
                    current_payment['DeductionRecord(21)'] = current_payment.get('DeductionRecord(21)', [])
                    current_payment['DeductionRecord(21)'].append(line[2:])
                elif first_two_digits == '22':
                    found_row_22 = True  # Set the flag to indicate the presence of row 22
                    match = re.match(regex_pattern_22, line)
                    if match:
                        if 'XRefRecord(22)' not in current_payment:
                            current_payment['XRefRecord(22)'] = []
                        current_payment['XRefRecord(22)'].append({
                            'XRefCustomerNo': match.group(1),
                            'XRefInvoiceNo': match.group(2),
                            'XRefAmount': match.group(4).lstrip('0')
                        })
                elif first_two_digits == '23':
                    current_payment['XRefNEGRecord(23)'] = current_payment.get('XRefNEGRecord(23)', [])
                    current_payment['XRefNEGRecord(23)'].append(line[2:])
                elif first_two_digits == '25':
                    match = re.match(regex_pattern_25, line)
                    if match:
                        if 'PaymentInfoRecord(25)' not in current_payment:
                            current_payment['PaymentInfoRecord(25)'] = []
                        current_payment['PaymentInfoRecord(25)'].append({
                            'CustomerNo': match.group(1),
                            'InvoiceNo': match.group(2),
                            'Amount': match.group(4).lstrip('0')
                        })
                elif first_two_digits == '26':
                    current_payment['Name'] = line[2:]
                elif first_two_digits == '27':
                    # Remove spaces from the last 5 digits for lines starting with '27'
                    line = line[:len(line) - 5] + line[len(line) - 5:].replace(" ", "")
                    current_payment['Address'] = line[2:]
                elif first_two_digits == '28':
                    current_payment['City'] = line[2:]
                elif first_two_digits == '29':
                    current_payment['CompanyNumber'] = line[2:].lstrip('0')

        # Format the JSON structure
        formatted_data = {
            'header': data.get('header', {}),
            'payments': payments
        }

        # Create the output file path
        output_filename = os.path.splitext(filename)[0] + '.json'
        output_path = os.path.join(output_dir, output_filename)

        # Write the JSON data to the output file with 'utf-8' encoding
        with open(output_path, 'w', encoding='utf-8') as json_file:
            json.dump(formatted_data, json_file, ensure_ascii=False, indent=4)

        #print(f'Updated JSON file saved as {output_path}')
