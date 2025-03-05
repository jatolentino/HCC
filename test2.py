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

def match_icd10_codes(text):
    """
    Extracts icd-10 codes matching the pattern from the indivual assessment plans (text).

    Assumption:
        Each indivual assessment plan has maximun one code
    Args:
        text (str): Each individual assessment plan.

    Returns:
        list: A list of matching icd-10 codes, or an empty list if no matches are found.

    Raises:
        TypeError: If the input is not a text string
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")

    pattern = r"[A-TV-Z][0-9][0-9AB]\.?[0-9A-TV-Z]{0,4}"
    #icd10 = []
    icd10 = None

    matches = re.findall(pattern, text)
    if matches:
        icd10 = matches[0]
        return icd10
    return None

text = """2. Hyperglycemia due to type 2 diabetes mellitus -
   Worsening
   Continue Metformin1000 mg BID and Glimepiride 8 mg
   Recommend a low sugar and low carbohydrate diet. Fruits and vegetables are acceptable.
   Discussed 1/2 plate with non-starchy vegetables, 1/4 of plate with carbohydrates such as whole grain, 1/4 of plate with lean protein.
   Include healthy fats in your meal like: Olive oil, canola oil, avocado, and nuts
   E11.65: Type 2 diabetes mellitus with hyperglycemia"""
   
print(match_icd10_codes(text))