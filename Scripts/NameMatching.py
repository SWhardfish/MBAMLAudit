import os
import json
import pandas as pd
from fuzzywuzzy import fuzz
from configparser import ConfigParser
import logging

def setup_logging(logfile_path):
    logging.basicConfig(filename=logfile_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    return data

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

def load_csv(file_path):
    return pd.read_csv(file_path, delimiter=';')

def fuzzy_match(json_data, csv_data, logfile):
    json_df = pd.DataFrame(json_data.get('payments', []))
    json_df['CustomerNo'] = json_df['PaymentRecord(20)'].apply(lambda x: x.get('CustomerNo', ''))
    json_df = json_df[json_df['CustomerNo'] == 'NotFound']

    for index, json_row in json_df.iterrows():
        json_name = json_row['Name']
        json_address = json_row['Address']
        json_city = json_row['City']

        csv_data['similarity'] = csv_data.apply(lambda x: fuzz.token_set_ratio(f"{x['Name']} {x['Address']} {x['City']} {x['Post Code']}",
                                                                               f"{json_name} {json_address} {json_city}"), axis=1)

        match = csv_data[csv_data['similarity'] > 80].head(1)

        if not match.empty:
            csv_entry = match.iloc[0]
            payment_id = json_row['id']
            payment_index = json_row.name
            csv_index = match.index[0]

            json_data['payments'][payment_index]['PaymentRecord(20)']['CustomerNo'] = csv_entry['No_']
            logging.info(f"Fuzzy Name match found: JSON file '{logfile}', "
                         f"Payment ID '{payment_id}', "
                         f"Payment Index '{payment_index}', "
                         f"CSV Index '{csv_index}', "
                         f"CustomerNo updated to '{csv_entry['No_']}'")

    return json_data

def update_json_file(json_file_path, csv_file_path, output_file_path, logfile):
    json_data = load_json(json_file_path)
    csv_data = load_csv(csv_file_path)
    updated_json_data = fuzzy_match(json_data, csv_data, logfile)
    save_json(output_file_path, updated_json_data)

if __name__ == "__main__":
    # Read config.ini file
    config_object = ConfigParser()
    config_object.read("Config/config.ini")

    # Get the MonthYear from Config.ini
    monthyear = config_object["MonthYear"]
    year = monthyear["year"]
    month = monthyear["month"]

    # Get the FF9SE Customers from Config.ini
    FF9SECustomersFile = config_object["FF9SECustomersFile"]
    FF9SECustFile = FF9SECustomersFile["FF9SECustFile"]

    # Specify the input and output directories
    input_directory = f"ResultOutput/BGMaxFiles/{year}/{month}/PreProcessed/InvoiceProcessed"
    output_directory = f"ResultOutput/BGMaxFiles/{year}/{month}/PreProcessed/InvoiceProcessed/NameProcessed"
    #log_directory = "../NameMatching"

    # Ensure the output directory exists, create if not
    os.makedirs(output_directory, exist_ok=True)

    # Setup logging
    logfile_path = os.path.join(output_directory, 'Name_matching_log.txt')
    setup_logging(logfile_path)

    # Loop through all JSON files in the input directory
    for json_filename in os.listdir(input_directory):
        if json_filename.endswith('.json'):
            json_file_path = os.path.join(input_directory, json_filename)
            csv_file_path = f"{FF9SECustFile}"
            output_file_path = os.path.join(output_directory, json_filename.replace('.json', '_NameMatch.json'))

            update_json_file(json_file_path, csv_file_path, output_file_path, json_filename)
