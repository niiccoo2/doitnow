import csv
import datetime

# Function to read CSV and return rows as list of dictionaries
def read_csv(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader), reader.fieldnames

# Function to write combined data back to a new CSV
def write_combined_csv(file_name, combined_data, fieldnames):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in combined_data:
            # Ensure all fields are present in the row, add missing fields as empty strings
            writer.writerow({field: row.get(field, '') for field in fieldnames})

# Read both CSV files
file1 = 'Fai_Adesso_Form_Responses_1.csv'
file2 = 'Fai_Adesso_Form_Responses_6th.csv'

data1, fieldnames1 = read_csv(file1)
data2, fieldnames2 = read_csv(file2)

# Combine data from both files
combined_data = data1 + data2

# Combine and deduplicate fieldnames from both files
combined_fieldnames = list(set(fieldnames1 + fieldnames2))

# Sort combined data by the date field (assuming 'Timestamp' is the column header for date)
# Adjust 'Timestamp' to match the actual date column in your CSVs
combined_data.sort(key=lambda row: datetime.datetime.strptime(row['Timestamp'], "%m/%d/%Y %H:%M:%S"))

# Write sorted and combined data to a new CSV with unified fieldnames
write_combined_csv('Combined_Fai_Adesso.csv', combined_data, combined_fieldnames)

print("CSV files have been combined and sorted into 'Combined_Fai_Adesso.csv'")
