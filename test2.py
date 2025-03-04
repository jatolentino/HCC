import re

# Input text (including edge case)
pn_to_analyze = "progress_notes/pn_9"
with open(pn_to_analyze, 'r') as file:
    text = file.read()

def extract_assessment_plan(text):
    pattern = r"Assessment / Plan\n\n(.*?)(?=\n\nReturn to Office|\Z)"

    # Extract the Assessment / Plan section
    match = re.search(pattern, text, re.DOTALL)

    if match:
        assessment_plan = match.group(1)
        # print(assessment_plan)
        return assessment_plan
    else:
        lines = text.split('\n')
        idxAss_Plam = None
        for idx, line in enumerate(lines):
            if "Assessment / Plan" in line:
                idxAss_Plam = idx
        start_index = idxAss_Plam + 1
        end_index = len(lines)  # Assuming the end is the end of the document

        # Extract the assessment plan text
        assessment_plan ='\n'.join(lines[start_index : end_index])
        #print(assessment_plan)
        return assessment_plan
    
# print(extract_assessment_plan(text))