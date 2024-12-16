import os
import csv
from csv_subscriber.add_date_and_time import get_date, get_time

def generate_new_filename():
    # Get the current date and time
    date_str = get_date()  # Example: 2024-12-11
    
    # Format the date and time for the filename
    filename = f"{date_str}_turtlebot_meassurents.csv"
    return filename

def copy_csv_with_new_name(original_file):
    # Check if the original file exists
    if not os.path.exists(original_file):
        print(f"File {original_file} does not exist.")
        return
    
    # Generate the new filename
    new_filename = generate_new_filename()
    
    # Path to the new file
    new_file_path = os.path.join('/home/workspace/meassurements/data_csv', new_filename)
    
    # Ensure the destination directory exists
    os.makedirs(os.path.dirname(new_file_path), exist_ok=True)
    
    # Read data from the original CSV file
    with open(original_file, 'r', newline='') as original_csv:
        csv_reader = csv.reader(original_csv)
        
        # Read the content of the original file into a list
        rows = list(csv_reader)
        
        # Print the rows read from the original file (for debugging)
        if rows:
            print(f"Read {len(rows)} rows from {original_file}")
        else:
            print("No data found in the original file.")
    
    # Write the data to the new CSV file
    if rows:
        with open(new_file_path, 'w', newline='') as new_csv:
            csv_writer = csv.writer(new_csv)
            
            # Write the rows to the new file
            csv_writer.writerows(rows)

        print(f"Data written to {new_file_path}")
    else:
        print(f"Error: No rows to write to {new_file_path}")

