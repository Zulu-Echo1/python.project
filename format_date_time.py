import os
import csv
import re
from datetime import datetime

def is_date_format(value):
    # Check if the value matches the default date format MM/DD/YYYY
    try:
        datetime.strptime(value, "%m/%d/%Y")
        return "%m/%d/%Y"
    except ValueError:
        return None

def is_time_format(value):
    # Check if the value matches the default time format HH:MM
    if re.match(r'\d{2}:\d{2}', value):
        return "%H:%M"
    return None

def convert_to_sql_format(value, value_type):
    if value_type == 'date':
        # Convert to SQL compatible date format (YYYY-MM-DD)
        try:
            return datetime.strptime(value, "%m/%d/%Y").strftime('%Y-%m-%d')
        except ValueError:
            return value
    elif value_type == 'time':
        # Convert to SQL compatible time format (HH:MM:SS)
        try:
            return datetime.strptime(value, "%H:%M").strftime('%H:%M:%S')
        except ValueError:
            return value
    return value

def clean_csv_dates_and_times(file_path):
    # Open the CSV file for reading
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)  # Read the header row
        rows = list(reader)  # Read all remaining rows

    updated_rows = []
    for row in rows:
        updated_row = []
        for i, value in enumerate(row):
            # Exclude the tail number column (assumed to be the fourth column, index 3)
            # Exclude the flight number column (assumed to be the third column, index 2)
            if i == 2 or i == 3:
                updated_row.append(value)
                continue

            # Check if the value is a date or time, and convert accordingly
            date_format = is_date_format(value)
            time_format = is_time_format(value)
            if date_format:
                updated_row.append(convert_to_sql_format(value, 'date'))
            elif time_format:
                updated_row.append(convert_to_sql_format(value, 'time'))
            else:
                updated_row.append(value)
        updated_rows.append(updated_row)

    # Write the cleaned data back to the CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)  # Write the header row
        writer.writerows(updated_rows)  # Write all updated rows
    print(f"Cleaned dates and times in file: {file_path}")

def main():
    # Use the directory of the script as the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {current_directory}")

    # Iterate over all files in the current directory
    for filename in os.listdir(current_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(current_directory, filename)
            print(f"Processing file: {filename}")
            clean_csv_dates_and_times(file_path)

if __name__ == "__main__":
    main()