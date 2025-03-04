import json

# Function to read the text file and convert it to a dictionary
def convert_txt_to_json(txt_file_path, json_file_path):
    try:
        # Initialize an empty dictionary to store the data
        data = {}

        # Open the text file for reading
        with open(txt_file_path, 'r') as file:
            # Read the file line by line
            for line in file:
                # Strip any extra whitespace and newline characters
                line = line.strip()

                # Split the line by commas
                parts = line.split(',')

                # Only process lines that have at least two columns
                if len(parts) >= 2:
                    code = parts[0].strip()  # First column (code)
                    description = parts[1].strip()  # Second column (description)
                    data[code] = description.replace('\"','')

        # Write the dictionary to a JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Data successfully written to {json_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# File paths
txt_file_path = 'HCC_relevant_codes.csv'  # Replace with your actual txt file path
json_file_path = 'HCC_relevant_codes.json'     # This is where the json will be saved

# Call the function to convert txt to json
convert_txt_to_json(txt_file_path, json_file_path)