import json
import csv
import glob
import time

# Create a list to hold the combined profiles data
profiles = []
tm = time.strftime('%m%Y')
foldername = 'GitSevers_'+ tm
print(foldername)

# Load and combine the JSON data from all files in the directory that match the pattern
path = r'C:\Users\santo\Documents\JSON_PROG'
for file_path in glob.glob(path + '\*.json'):
    #print(file_path)
    with open(file_path) as f:
        data = json.load(f)
        profiles.extend(data['Profiles'])

# Create a list to hold the flattened data
flattened_data = []

# Loop through each profile in the profiles list
for profile in profiles:
    # Extract the Name and Tags columns
    name = profile['Name']
    tags = ' '.join(profile['Tags'])

    # Split the Command column into Username and Hostname columns
    split_command = profile['Command'].split()
    if len(split_command) > 1:
        at_index = split_command[1].find('@')
        if at_index > -1:
            username = split_command[1][:at_index]
            hostname = split_command[1][at_index+1:]
        else:
            username = ''
            hostname = ''
    else:
        username = ''
        hostname = ''

    # Create a dictionary to hold the flattened row data
    flattened_row = {
        'session_name': name,
        'description': tags,
        'username': username,
        'hostname': hostname,
        'emulation': 'XTerm',
        'protocol': 'SSH2',
        'folder': foldername  
            
    }

    # Append the flattened row to the flattened data list
    flattened_data.append(flattened_row)

# Write the flattened data to a CSV file
with open('output.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['session_name', 'description', 'username',
                            'hostname', 'emulation', 'protocol','folder'])  # Add the new column to the fieldnames
    writer.writeheader()
    writer.writerows(flattened_data)
