import re
# pn_to_analyze = "progress_notes/pn_1"
# with open(pn_to_analyze, 'r') as file:
#     text = file.read()

text = """
SPO2-98%
J44.9: Chronic
X79XXXA
"""

def extract_code(text):
    lines = text.split('\n')
    # Regex pattern to extract medical codes
    #pattern = r'([A-Z]\d+\.?(\d+)?)'
    
    #pattern = r'([A-Za-z]{1})\d+(\.\d+)?'
    #pattern = r'([A-Z]\d+(\.\d+)?)' # testing

    pattern = r'[A-Z]\d+\.?(\d+)?'
    
    
    
    # match = re.search(pattern, text)
    # if match:
    #     return match.group(0)
    # return None
    codes = []
    # print(lines)
    for line in lines:
        
        match = re.search(pattern, line)
        if match:
            print("line: ", line)
            print(match)
            match = match.group(0).replace(':','')
            match = match.replace('.', '')
            codes.append(match.strip())
    #return codes
    if codes:
        return codes
    else:
        return f"Error: No Codes Found"
    
print(extract_code(text))