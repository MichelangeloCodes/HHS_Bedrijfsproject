import csv
from csv_subscriber.os_save_file import copy_csv_with_new_name

temp_file_name = 'new_names.csv'

def write_csv(data):
    # Open the file in append mode to prevent overwriting
    with open(temp_file_name, 'a', newline='') as new_file:
        fieldnames = ['name', 'age']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter=',')
        
        # Write header only if the file is empty
        if new_file.tell() == 0:
            csv_writer.writeheader()
        
        for row in data:
            csv_writer.writerow(row)

    # Call the function to copy the file with a new name
    copy_csv_with_new_name(temp_file_name)


def read_csv_dict():
    with open ('new_names.csv', 'r' ) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for line in csv_reader:
            print(line)
        for line in csv_reader:
            print("NAME:", {line['name']})
        for line in csv_reader:
            print(line['age'])

def read_csv_selection(entry):
    with open ('new_names.csv', 'r' ) as csv_file:
        csv_reader = csv.DictReader(csv_file)
       
        if entry == 1:
            index = 'name'
        elif entry == 2:
            index = 'age'

        for line in csv_reader:
            print(line[index])

