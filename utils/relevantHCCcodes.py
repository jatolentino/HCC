import re
import json

text1 = """Assessment / Plan

1.        Fibromyalgia -
Improving
Continue Lyrica 75 mg twice daily for pain management
Recommend gentle stretching and low-impact exercises
Monitor symptoms at follow-up
M79.7: Fibromyalgia
        2.        Hypertension -
Stable
Continue Amlodipine 10 mg daily
Encourage blood pressure monitoring and adherence to a low-sodium diet
BP today was 138/82 mmHg
I10: Essential (primary) hypertension
Essential E10: (primary) hypertension"""
   

def extract_codes(text):
    try:
        # Regex pattern to match the code (letters followed by numbers and an optional period with more digits)
        #pattern = r'^\s*[A-Za-z]+\d+(\.\d+)?'
        pattern = r'^\s*[A-Za-z]+\d+(\.\d+)?:' # works
        #pattern = r'\s*-\s*([A-Za-z]+\d+(\.\d+)?)\s*$'
        #pattern = r'([A-Z]\d+\.?(\d+)?)'
        
        lines = text.split('\n')
        
        # Find all matches using the pattern
        codes = []
        # print(lines)
        for line in lines:
            match = re.match(pattern, line)
            if match:
                match = match.group(0).replace(':','')
                match = match.replace('.', '')
                codes.append(match.strip())
        #return codes
        if codes:
            return codes
        else:
            return f"Error: No Codes Found"
    
    except Exception as e:
        # Return the error message if something goes wrong
        return f"Error: {str(e)}"


def find_numbered_lines(text):
    # Regex pattern to match lines starting with a number followed by ". "
    pattern = r'^\d+\.\s.*'
    
    # Split the input text into lines and check each line against the pattern
    lines = text.split('\n')
    #result = [line for line in lines if re.match(pattern, line)]
    #result = [(index + 1, line) for index, line in enumerate(lines) if re.match(pattern, line)]
    result = [index  for index, line in enumerate(lines) if re.match(pattern, line)]
    
    l = []
    # print(lines)
    # print()
    for i in result:
        print(lines[i])
        l.append(extract_code(lines[i]))
    
    return l

def check_key_in_json(json_file_path, key):
    try:
        # Open the JSON file and load its contents into a dictionary
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Check if the key exists in the dictionary
        if key in data:
            #print(f"The key '{key}' is present in the JSON file.")
            return True
        else:
            return False
            #print(f"The key '{key}' is NOT present in the JSON file.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        

# Find if a code is present in my dictionary:
# JSON file path
json_file_path = 'HCC_relevant_codes.json'  # Replace with your actual JSON file path
code_to_check = "A021"  # The key you want to check

# Check if the key exists in the JSON file
#check_key_in_json(json_file_path, code_to_check)


# Extracting codes
pn_to_analyze = "progress_notes/pn_1"
with open(pn_to_analyze, 'r') as file:
    text = file.read()
    the_codes = extract_codes(text)
    print("All codes: ", the_codes)
    # print HCC relevanat codes
    relevant_codes = [e for e in the_codes if check_key_in_json(json_file_path, e)]
    print("Relevant HCC codes: ", relevant_codes)
