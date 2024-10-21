import os

def __init__():
    pass

def main():
    # Use the current working directory
    current_directory = os.getcwd()

    # Iterate over all files in the directory
    for filename in os.listdir(current_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(current_directory, filename)

            # Remove trailing commas from each line in the CSV file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            cleaned_lines = [line.rstrip(',\n') + '\n' for line in lines]

            # Save the cleaned CSV with the same name
            with open(file_path, 'w') as file:
                file.writelines(cleaned_lines)

            print(f"Cleaned trailing commas in CSV: {filename}")

if __name__ == "__main__":
    main()