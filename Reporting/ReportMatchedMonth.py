import os
import csv
import matplotlib.pyplot as plt
from configparser import ConfigParser

#Read config.ini file
config_object = ConfigParser()
config_object.read("../config.ini")

#Get the MonthYear
monthyear = config_object["MonthYear"]
year = monthyear["year"]
month = monthyear["month"]

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

def iterate_csv_files(directory_path):
    total_counts = {'100%': 0, '99-90%': 0, '89-80%': 0, '79-70%': 0, '69-60%': 0,
                     '59-50%': 0, '49-40%': 0, '39-30%': 0, '29-20%': 0, '19-10%': 0,
                     '9-1%': 0, '0%': 0}

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            file_counts = process_csv_file(file_path)

            # Aggregate the counts for each file
            for key in total_counts:
                total_counts[key] += file_counts[key]

            print(f'Processed file: {filename}')

    return total_counts

def plot_similarity_occurrences(counts):
    labels = ['100%', '99-90%', '89-80%', '79-70%', '69-60%', '59-50%', '49-40%',
              '39-30%', '29-20%', '19-10%', '9-1%', '0%']
    occurrences = [counts['100%'], counts['99-90%'], counts['89-80%'], counts['79-70%'],
                   counts['69-60%'], counts['59-50%'], counts['49-40%'], counts['39-30%'],
                   counts['29-20%'], counts['19-10%'], counts['9-1%'], counts['0%']]

    plt.bar(labels, occurrences)
    plt.xlabel('Similarity Categories')
    plt.ylabel('Number of Matches')
    plt.title(f'Occurrences of Similarity Categories {month} {year} ')
    #plt.title(f'Occurrences of Similarity Categories Jan 2022-Jan 2024 (Visma) ')

    # Add counts on top of the bars
    for i in range(len(labels)):
        plt.text(i, occurrences[i] + 0.5, str(occurrences[i]), ha='center')

    # Angle the text on the X-axis
    plt.xticks(rotation=45, ha='right')

    plt.show()

if __name__ == '__main__':
    directory_path = f'../BGMaxFiles/{year}/{month}/Matched'
    #directory_path = f'../VismaFiles/VismaMatched'
    total_counts = iterate_csv_files(directory_path)

    total_count = sum(total_counts.values())
    print(f'Total Count: {total_count} occurrences')

    for category, occurrences in total_counts.items():
        print(f'{category}: {occurrences} occurrences')

    plot_similarity_occurrences(total_counts)
