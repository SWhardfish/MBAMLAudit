import pandas as pd
from fuzzywuzzy import fuzz
import json
import os
from configparser import ConfigParser
import logging

pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 1000)

# Configure the logging system
logging.basicConfig(filename='processing.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Read config.ini file
config_object = ConfigParser()
config_object.read("Config/config.ini")

# Get the MonthYear
monthyear = config_object["MonthYear"]
year = monthyear["year"]
month = monthyear["month"]

# Get the FF9SE Customers from Config.ini
FF9SECustomersFile = config_object["FF9SECustomersFile"]
FF9SECustFile = FF9SECustomersFile["FF9SECustFile"]

# Output Directory
output_dir = f'ResultOutput/VismaFiles/{year}/{month}/Matched/'
# Ensure output directories exist
os.makedirs(output_dir, exist_ok=True)


# Iterate over each JSON file in '../PreProcessed/...'
directory_path = f'ResultOutput/VismaFiles/{year}/{month}/PreProcessed/'

for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        # Create an empty list to store data for the CSV for each file
        csv_data = []
        with open(os.path.join(directory_path, filename), 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)

        header = data.get('header', {})
        payments = data.get('payments', [])

        # Read 'Date' field from the JSON data -FIX THIS AS NOT AVAILABLE IN VISMA JSON
        date = header.get('Date', "")

        file2_df = pd.read_csv(f'{FF9SECustFile}', sep=';')

        # Join address fields into one
        file2_df["FFNameAddress"] = file2_df["Name"] + ',' + file2_df["Address"] + ' ' + file2_df["Post Code"] + ' ' + \
                                    file2_df["City"]
        file2_df["FFAddress"] = file2_df["Address"] + ' ' + file2_df["Post Code"] + ' ' + file2_df["City"]
        #Get additional data from FF Customer file
        file2_df["FFName"] = file2_df["Name"]
        file2_df["FFPersonNo"] = file2_df["Social Security No_"]
        file2_df["FFOrgNumber"] = file2_df["VAT Registration No_"]


        # Iterate over payments in the JSON data
        for payment in payments:
            Id = payment.get("id", )
            PaymentRecord = payment.get("PaymentRecord(20)", {})
            CustomerNo = PaymentRecord.get("CustomerNo", "NotFound")
            InvoiceNo = PaymentRecord.get("InvoiceNo", "NotFound")
            Amount = PaymentRecord.get("Amount", "")
            CompanyNumber = payment.get("CompanyNumber", "")
            Name = payment.get("Name", "")
            Address = payment.get("Address", "")
            City = payment.get("City", "")
            BGMaxNameAddress = f"{Name}, {Address} {City}"
            BGMaxAddress = f"{Address} {City}"

            if CompanyNumber:
                matching_row = file2_df[file2_df['VAT Registration No_'] == CompanyNumber]
                if not matching_row.empty:
                    FFNameAddress = matching_row.iloc[0]['FFNameAddress']
                    FFName = matching_row.iloc[0]['FFName']
                    FFAddress = matching_row.iloc[0]['FFAddress']
                    FFOrgNumber = matching_row.iloc[0]['VAT Registration No_']
                    FFPersonNo = matching_row.iloc[0]['FFPersonNo']

                    similarity = "100"  # Set the similarity to "100" when CompanyNumber matches
                    similarity_name = "100"  # Set the similarity to "100" when CompanyNumber matches
                    similarity_address = "100"  # Set the similarity to "100" when CompanyNumber matches
                    #CustomerNo = CompanyNumber  # Set CustomerNo to CompanyNumber when there's a match
                else:
                    # No match found for CompanyNumber, so check CustomerNO = 'No_'
                    matching_row = file2_df[file2_df['No_'] == CustomerNo]
                    if not matching_row.empty:
                        FFNameAddress = matching_row.iloc[0]['FFNameAddress']
                        FFName = matching_row.iloc[0]['FFName']
                        FFAddress = matching_row.iloc[0]['FFAddress']
                        FFPersonNo = matching_row.iloc[0]['FFPersonNo']
                        FFOrgNumber = matching_row.iloc[0]['VAT Registration No_']
                        similarity = fuzz.token_set_ratio(BGMaxNameAddress, FFNameAddress)
                        similarity_name = fuzz.token_set_ratio(Name, FFName)
                        similarity_address = fuzz.token_set_ratio(BGMaxAddress, FFAddress)
                    else:
                        FFNameAddress = f'No CustomerNumber {CustomerNo} match in FF9 Customer Table'
                        similarity = 0
                        similarity_name = 0
                        similarity_address = 0
                        # Log the information
                        logging.info(f"No CustomerNumber match for {CustomerNo} in {filename}")
            else:
                # CompanyNumber is empty, so check 'No_'
                matching_row = file2_df[file2_df['No_'] == CustomerNo]
                if not matching_row.empty:
                    FFNameAddress = matching_row.iloc[0]['FFNameAddress']
                    FFName = matching_row.iloc[0]['FFName']
                    FFAddress = matching_row.iloc[0]['FFAddress']
                    FFPersonNo = matching_row.iloc[0]['FFPersonNo']
                    FFOrgNumber = matching_row.iloc[0]['VAT Registration No_']
                    similarity = fuzz.token_set_ratio(BGMaxNameAddress, FFNameAddress)
                    similarity_name = fuzz.token_set_ratio(Name, FFName)
                    similarity_address = fuzz.token_set_ratio(BGMaxAddress, FFAddress)
                else:
                    FFNameAddress = f'No CustomerNumber {CustomerNo} match in FF9 Customer Table'
                    similarity = 0
                    similarity_name = 0
                    similarity_address = 0
                    # Log the information
                    logging.info(f"No CustomerNumber match for {CustomerNo} in {filename}")

            #Correct the Amount value- to remove the last two 00.
            #try:
            #    Amount = int(Amount) / 100
            #    print(Amount)
            #except ValueError:
            #    Amount = None  # You can set it to a default value or handle it in another way if needed

            # Append data to the CSV format
            csv_data.append([CustomerNo, InvoiceNo, date, Id, BGMaxNameAddress, Amount, FFNameAddress, FFPersonNo, FFOrgNumber, similarity, similarity_name, similarity_address])

        # Write the data to a CSV file
        #output_filename = f'../BGMaxFiles/{year}/{month}/Matched/{os.path.splitext(os.path.basename(filename))[0]}_output.csv'
        #output_filename = f'../VismaFiles/Matched/{os.path.splitext(os.path.basename(filename))[0]}_output.csv'
        output_filename = f'ResultOutput/VismaFiles/{year}/{month}/Matched/{os.path.splitext(os.path.basename(filename))[0]}_Matched.csv'
        df = pd.DataFrame(csv_data, columns=["CustomerNo", "InvoiceNo", "Date", "Id", "BGMaxNameAddress", "Amount", "FFNameAddress", "FFPersonNo", "FFOrgNumber", "similarity", "similarity_name", "similarity_address"])
        df.to_csv(output_filename, index=False)
        #print(output_filename)
