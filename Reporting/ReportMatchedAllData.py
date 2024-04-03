import os
import csv
import matplotlib.pyplot as plt
from configparser import ConfigParser

# Read config.ini file
config_object = ConfigParser()
config_object.read("../config.ini")

# Get the MonthYear
years = [2022, 2023]  # Specify the years
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]  # Specify the months

def process_csv_file(file_path):
    similarity_counts = {'100%': 0, '99-90%': 0, '89-80%': 0, '79-70%': 0, '69-60%': 0,
                         '59-50%': 0, '49-40%': 0, '39-30%': 0, '29-20%': 0, '19-10%': 0,
                         '9-1%': 0, '0%': 0}

    try:
        with open(file_path, 'r', encoding="utf8") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header

            for row in csv_reader:
                # Assuming the similarity is in the last column of each row
                similarity = int(row[-1])
                if similarity == 100:
                    similarity_counts['100%'] += 1
                elif 90 <= similarity <= 99:
                    similarity_counts['99-90%'] += 1
                elif 80 <= similarity <= 89:
                    similarity_counts['89-80%'] += 1
                elif 70 <= similarity <= 79:
                    similarity_counts['79-70%'] += 1
                elif 60 <= similarity <= 69:
                    similarity_counts['69-60%'] += 1
                elif 50 <= similarity <= 59:
                    similarity_counts['59-50%'] += 1
                elif 40 <= similarity <= 49:
                    similarity_counts['49-40%'] += 1
                elif 30 <= similarity <= 39:
                    similarity_counts['39-30%'] += 1
                elif 20 <= similarity <= 29:
                    similarity_counts['29-20%'] += 1
                elif 10 <= similarity <= 19:
                    similarity_counts['19-10%'] += 1
                elif 1 <= similarity <= 9:
                    similarity_counts['9-1%'] += 1
                else:
                    similarity_counts['0%'] += 1

        return similarity_counts

    except Exception as e:
        print(f'Error processing file: {file_path}')
        print(f'Error message: {str(e)}')
        return {'100%': 0, '99-90%': 0, '89-80%': 0, '79-70%': 0, '69-60%': 0,
                '59-50%': 0, '49-40%': 0, '39-30%': 0, '29-20%': 0, '19-10%': 0,
                '9-1%': 0, '0%': 0}
    pass

def iterate_csv_files(years, months):
    monthly_counts = {}  # Create a dictionary to store counts per month

    for year in years:
        for month in months:
            directory_path = f'../BGMaxFiles/{year}/{month}/Matched'

            if os.path.exists(directory_path):  # Check if the directory exists
                monthly_counts[(year, month)] = {'100%': 0, '99-90%': 0, '89-80%': 0, '79-70%': 0, '69-60%': 0,
                                                  '59-50%': 0, '49-40%': 0, '39-30%': 0, '29-20%': 0, '19-10%': 0,
                                                  '9-1%': 0, '0%': 0}

                for filename in os.listdir(directory_path):
                    if filename.endswith('.csv'):
                        file_path = os.path.join(directory_path, filename)
                        file_counts = process_csv_file(file_path)

                        # Aggregate the counts for each file and month
                        for key in monthly_counts[(year, month)]:
                            monthly_counts[(year, month)][key] += file_counts[key]

                        print(f'Processed file: {filename} ({month} {year})')
            else:
                print(f'Directory not found for {month} {year}. Skipping.')

    return monthly_counts  # Return monthly counts

def plot_similarity_occurrences(monthly_counts):
    labels = ['100%', '99-90%', '89-80%', '79-70%', '69-60%', '59-50%', '49-40%',
              '39-30%', '29-20%', '19-10%', '9-1%', '0%']
    month_categories = {}  # Create a dictionary to store category counts per month

    for (year, month), counts in monthly_counts.items():
        month_label = f'{month} {year}'
        occurrences = [counts['100%'], counts['99-90%'], counts['89-80%'], counts['79-70%'],
                       counts['69-60%'], counts['59-50%'], counts['49-40%'], counts['39-30%'],
                       counts['29-20%'], counts['19-10%'], counts['9-1%'], counts['0%']]
        month_categories[month_label] = occurrences

    num_months = len(month_categories)
    width = 0.05
    x = range(len(labels))

    fig, ax = plt.subplots(figsize=(16, 7))

    for i, (month_label, occurrences) in enumerate(month_categories.items()):
        x_pos = [pos + i * width for pos in x]
        ax.bar(x_pos, occurrences, width=width, label=month_label)

    ax.set_xlabel('Similarity Categories')
    ax.set_ylabel('Number of Matches')
    ax.set_title(f'Occurrences of Similarity Categories by Month')
    ax.set_xticks([pos + width * (num_months - 1) / 2 for pos in x])
    ax.set_xticklabels(labels)
    ax.legend(loc='upper center', title='Months')

    # Angle the text on the X-axis
    plt.xticks(rotation=45, ha='right')

    plt.show()

if __name__ == '__main__':
    monthly_counts = iterate_csv_files(years, months)

    # Sum counts for all months
    total_counts = {key: sum(val[key] for val in monthly_counts.values()) for key in monthly_counts[(years[0], months[0])].keys()}

    for (year, month), counts in monthly_counts.items():
        print(f'{month} {year}:')
        for category, occurrences in counts.items():
            print(f'{category}: {occurrences} occurrences')

    plot_similarity_occurrences(monthly_counts)
