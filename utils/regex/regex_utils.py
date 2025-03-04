import re

def extract_assessment_plan(text):
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
