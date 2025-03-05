import re

def extract_assessment_plan(text):
    """
    Extracts the assesment plan section from the progress note text.

    Args:
        text (str): The progress note text.

    Returns:
        text (str): The assessment plan section in plain text

    Raises:
        TypeError: If the input is not a string, or if there were no assessment section found
    """
    try:
        # Check if the input text is a string
        if not isinstance(text, str):
            raise ValueError("Input text must be a string")

        # Define the pattern to extract the "Assessment / Plan" section
        pattern = r"Assessment / Plan\n\n(.*?)(?=\n\nReturn to Office|\Z)"

        # Extract the Assessment / Plan section using regex
        match = re.search(pattern, text, re.DOTALL)

        if match:
            assessment_plan = match.group(1)
            return assessment_plan
        else:
            # If regex doesn't match, split the text into lines and look for "Assessment / Plan"
            lines = text.split('\n')
            idxAss_Plam = None

            # Find the index of the line containing "Assessment / Plan"
            for idx, line in enumerate(lines):
                if "Assessment / Plan" in line:
                    idxAss_Plam = idx
                    break  # Stop searching once we find the first occurrence

            # If "Assessment / Plan" is not found, raise an error
            if idxAss_Plam is None:
                raise ValueError('"Assessment / Plan" section not found in the text')

            # Set the start and end indices to extract the assessment plan text
            start_index = idxAss_Plam + 1
            end_index = len(lines)  # Assuming the end is the end of the document

            # Ensure the start index is within bounds
            if start_index >= end_index:
                raise IndexError("Start index for assessment plan extraction is out of bounds")

            # Extract the assessment plan text and return it
            assessment_plan = '\n'.join(lines[start_index:end_index])
            return assessment_plan

    except Exception as e:
        # Catch all exceptions and print an error message
        return f"Error occurred: {str(e)}"

def extract_each_plan(input_text):
    # Regular expression to extract the sections
    # Removing white spaces in the beginning of each line
    input_text = '\n'.join(line.lstrip() for line in input_text.splitlines())
    
    # Removing empty lines fromt the text:
    input_text =  '\n'.join([line for line in input_text.splitlines() if line.strip()])

    # Get indexes (start_of_section_idx_line) if section start wih 1. or 1)
    # i.e [0,5,15,20,25]
    lines = input_text.splitlines()
    len_text = len(lines)
    start_of_section_idx_line = []
    pattern = r"(^(\s?\d+)\.\s)|(^(\s\d+)\)\s)"
    for index, line in enumerate(lines):
        if re.match(pattern, line):
             start_of_section_idx_line.append(index)
    
    # Get section from index to index + 1 => i.e: [0:5] : Section 1
    section = []
    for i,e in enumerate(start_of_section_idx_line):
        if e != (start_of_section_idx_line[-1]):
            unit_section = '\n'.join(lines[e:start_of_section_idx_line[i+1]])
            section.append(unit_section)
        else:
            unit_section = '\n'.join(lines[e:])
            section.append(unit_section)
    
    # Return the list of sections
    return section

def match_icd10_codes(text):
    """
    Extracts icd-10 codes matching the pattern from the given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of matching icd-10 codes, or an empty list if no matches are found.

    Raises:
        TypeError: If there were no icd-10 codes found within the text
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    pattern = r"[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}"
    if matches:
        matches = re.findall(pattern, text)
    else:
        raise TypeError("There were no icd10 codes found in the provided text")
    
    return matches


def is_icd10_an_hcc(code):
    """
    Verify if the icd-10 code provided as input is an HCC code according to the hash table located in HCC_relevant_codes.json

    Args:
        code (str): the icd-10 code.

    Returns:
        boolean: Returns True if the icd-10 code is found in the HCC hash table (therefore is HCC relevant) or False if it is not present in the hash table 
        (list: A list of matching HCC codes, or an empty list if no matches are found.)

    Raises:
        TypeError: If the hcc_json_file_path.json is not a valid path, or if the json file is not formatted properly, or if the code provided as input is not a string
    """
    try:
        # Open the JSON file and load its contents into a dictionary
        hcc_json_file_path = 'HCC_relevant_codes.json'
        with open(hcc_json_file_path, 'r') as json_file:
            data = json.load(json_file)
            
        if not isinstance(code, str):
            raise ValueError("Input code must be a string")

        # Check if the code exists in the dictionary
        if code in data:
            #print(f"The code '{code}' is present in the JSON file.")
            return True
        else:
            return False
            #print(f"The code '{code}' is NOT present in the JSON file.")
    
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{hcc_json_file_path}' was not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error: The file '{hcc_json_file_path}' is not a valid JSON file.")