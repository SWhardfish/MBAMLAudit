import os
import csv
import matplotlib.pyplot as plt

def process_csv_file(file_path):
    similarity_occurrences = [0] * 101  # Initialize occurrences for percentages 0 to 100

    try:
        with open(file_path, 'r', encoding="utf8") as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header

            for row in csv_reader:
                # Assuming the similarity is in the last column of each row
                similarity = int(row[-1])
                if 0 <= similarity <= 100:
                    similarity_occurrences[similarity] += 1

        return similarity_occurrences

    except Exception as e:
        print(f'Error processing file: {file_path}')
        print(f'Error message: {str(e)}')
        return [0] * 101

def iterate_csv_files(directory_path):
    total_occurrences = [0] * 101  # Initialize total occurrences for percentages 0 to 100

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)
            file_occurrences = process_csv_file(file_path)

            # Aggregate the occurrences for each file
            total_occurrences = [total + current for total, current in zip(total_occurrences, file_occurrences)]

            print(f'Processed file: {filename}')

    return total_occurrences

def plot_similarity_occurrences(occurrences):
    # Modify this to include occurrences for similarities less than 100
    percentages = list(range(101))
    plt.bar(percentages, occurrences)
    plt.xlabel('Similarity Percentage')
    plt.ylabel('Occurrences')
    plt.title('Occurrences of Similarity Percentages')
    plt.xlim(-1, 101)  # Set the x-axis limit to show 0-100
    plt.show()

if __name__ == '__main__':
    # Replace with the actual directory path where your CSV files are located
    directory_path = '../ResultOutput/BGMaxFiles/2024/Mar/Matched'
    total_occurrences = iterate_csv_files(directory_path)

    # Print total occurrences for each similarity percentage
    for percentage, occurrences in enumerate(total_occurrences):
        print(f'Similarity {percentage}%: {occurrences} occurrences')

    # Plot a graph of occurrences for each similarity percentage
    plot_similarity_occurrences(total_occurrences)
