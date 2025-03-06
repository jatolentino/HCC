import os
from utils.regex.regex_utils import extract_assessment_plan, \
    extract_each_plan, match_icd10_codes, is_icd10_an_hcc
from pipeline import langGraph_evaluation

def layers(progress_note):
    try:
        if not isinstance(progress_note, str):
            raise ValueError("Input progress_note must be a string")
        
        assessment_section = extract_assessment_plan(progress_note)
        assessment_plans = extract_each_plan(assessment_section)
        output = []
        for plan in assessment_plans:
            icd10_code = match_icd10_codes(plan)
            output_plan = {}
            if icd10_code:
                partial_output = is_icd10_an_hcc(icd10_code, plan)
                condition_data = langGraph_evaluation(plan)
                output_plan.update(partial_output)
                if partial_output["is_hcc"]:
                    output_plan["condition_data"] = condition_data
            output.append(output_plan)

        # print(output)
        return output
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    # Define the root folder path
    root_folder = 'pn'
    result_folder = 'result'

    # Check if the folder exists
    if os.path.exists(root_folder) and os.path.isdir(root_folder):
        # Get the list of files (without extensions) inside the 'pn' folder
        pn_paths = [os.path.join(root_folder, f).replace('\\', '/') for f in os.listdir(root_folder) if os.path.isfile(os.path.join(root_folder, f))]
    else:
        print(f"Error: The folder '{root_folder}' does not exist.")
    
    if(len(pn_paths)) != 0:
        for pn_path in pn_paths:
            with open(pn_path, 'r') as file:
                progress_note = file.read()
            
            output = layers(progress_note)
            
            # Write the output to a file inside the 'result' folder
            output_file_path = os.path.join(result_folder, 'output.txt')
            with open(output_file_path, 'a') as output_file:  # Use 'a' to append the output
                output_file.write(f"{pn_path}:\n")
                output_file.write(str(output) + '\n\n')
                
            print(f"Processed {pn_path}, output written to {output_file_path}")