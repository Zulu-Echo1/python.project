import os
import csv

CHUNK_SIZE_MB = 5
BYTES_IN_MB = 1024 * 1024

def split_large_csv(file_path, chunk_size=CHUNK_SIZE_MB):
    file_size = os.path.getsize(file_path)
    print(f"Processing file: {file_path}, Size: {file_size / BYTES_IN_MB:.2f} MB")
    if file_size <= chunk_size * BYTES_IN_MB:
        print(f"File {file_path} is smaller than {chunk_size} MB, skipping.")
        return

    # Rename original large file
    base_name, extension = os.path.splitext(file_path)
    large_file_path = f"{base_name}_large{extension}"
    os.rename(file_path, large_file_path)
    print(f"Renamed original file to: {large_file_path}")

    with open(large_file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        header = next(reader)
        chunk_index = 1
        rows_in_chunk = []
        current_chunk_size = 0

        for row in reader:
            row_size = sum(len(str(cell)) for cell in row) + len(row)  # Rough estimate of row size in bytes
            if current_chunk_size + row_size > chunk_size * BYTES_IN_MB:
                # Write current chunk to a new file
                chunk_filename = f"{chunk_index}_{os.path.basename(base_name)}{extension}"
                with open(os.path.join(os.path.dirname(file_path), chunk_filename), 'w', newline='') as chunk_file:
                    writer = csv.writer(chunk_file)
                    writer.writerow(header)
                    writer.writerows(rows_in_chunk)
                print(f"Created chunk file: {chunk_filename}")

                # Reset for next chunk
                chunk_index += 1
                rows_in_chunk = []
                current_chunk_size = 0

            rows_in_chunk.append(row)
            current_chunk_size += row_size

        # Write any remaining rows to a new file
        if rows_in_chunk:
            chunk_filename = f"{chunk_index}_{os.path.basename(base_name)}{extension}"
            with open(os.path.join(os.path.dirname(file_path), chunk_filename), 'w', newline='') as chunk_file:
                writer = csv.writer(chunk_file)
                writer.writerow(header)
                writer.writerows(rows_in_chunk)
            print(f"Created chunk file: {chunk_filename}")

def main():
    # Use the directory of the script
    current_directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Script directory: {current_directory}")

    # Iterate over all files in the directory
    for filename in os.listdir(current_directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(current_directory, filename)
            print(f"Checking file: {filename}")
            split_large_csv(file_path)

if __name__ == "__main__":
    main()