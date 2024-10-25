import csv
import datetime

# Function to read CSV and return rows as list of dictionaries
def read_csv(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

# Function to write combined data back to a new CSV
def write_combined_csv(file_name, combined_data, fieldnames):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)

# Read both CSV files
file1 = 'Fai Adesso - Form Responses 1.csv'
file2 = 'Fai Adesso! 6th Ottobre  (Responses) - Form Responses 1.csv'

data1 = read_csv(file1)
data2 = read_csv(file2)

# Combine data from both files
combined_data = data1 + data2

# Sort combined data by the date field (assuming 'Timestamp' is the column header for date)
# Adjust 'Timestamp' to match the actual date column in your CSVs
combined_data.sort(key=lambda row: datetime.datetime.strptime(row['Timestamp'], "%m/%d/%Y %H:%M:%S"))

# Get fieldnames from the first file (assuming both CSVs have the same structure)
fieldnames = combined_da

# Write sorted and combined data to a new CSV
write_combined_csv('Combined_Fai_Adesso.csv', combined_data, fieldnames)

print("CSV files have been combined and sorted into 'Combined_Fai_Adesso.csv'")
