from utils.regex.regex_utils import extract_assessment_plan, \
    extract_each_plan, match_icd10_codes, is_icd10_an_hcc
from pipeline import langGraph_evaluation

if __name__ == "__main__":
    pn_to_analyze = "progress_notes/pn_1"
    with open(pn_to_analyze, 'r') as file:
        progress_note = file.read()
    
    assessment_section = extract_assessment_plan(progress_note)
    assessment_plans = extract_each_plan(assessment_section)
    output = {}
    for plan in assessment_plans:
        icd10_code = match_icd10_codes(plan)
        if icd10_code:
            #print("icd10_code =>", type(icd10_code))
            #print(plan)
            partial_output = is_icd10_an_hcc(icd10_code, plan)
            condition_data = langGraph_evaluation(plan)
            output.update(partial_output)
            output["condition_data"] = condition_data
            print(output)
     
     
"""  
Test on  progress_notes/pn_1
{'condition_code': 'K219', 'is_hcc': False, 'condition_data': {'assessment_plan': '1. Gastroesophageal reflux disease -\nStable\nContinue the antacids\nF/U in 3 months\nK21.9: Gastro-esophageal reflux disease without esophagitis', 'extracted_text': '- Continue the antacids\n- F/U in 3 months', 'condition_data': '[\n  "- Continue the antacids",\n  "- F/U 
in 3 months"\n]'}}

{'condition_code': 'E1165', 'is_hcc': True, 'condition_data': {'assessment_plan': '2. Hyperglycemia due to type 2 diabetes mellitus -\nWorsening\nContinue Metformin1000 mg BID and Glimepiride 8 mg\nRecommend a low sugar and low carbohydrate diet. Fruits and vegetables are acceptable.\nDiscussed 1/2 plate with non-starchy vegetables, 1/4 of plate with carbohydrates such as whole grain, 1/4 of plate with lean protein.\nInclude healthy fats in your meal like: Olive oil, canola oil, avocado, and nuts\nE11.65: Type 2 diabetes mellitus with hyperglycemia', 'extracted_text': '## Extracted Management Information:\n\n* Continue Metformin 1000 mg BID and Glimepiride 8 mg\n* Recommend a low sugar and low carbohydrate diet. Fruits and vegetables are acceptable.\n* Discussed 1/2 plate with non-starchy vegetables, 1/4 of plate with carbohydrates such as whole grain, 1/4 of plate with lean protein.\n* Include healthy fats in your meal like: Olive oil, canola oil, avocado, and nuts', 'condition_data': '[\n  "## Extracted Management Information:",\n  "* Continue Metformin 1000 mg BID and Glimepiride 8 mg",\n  "* Recommend a low sugar and low carbohydrate diet. Fruits and vegetables are acceptable.",\n  "* Discussed 1/2 plate with non-starchy vegetables, 1/4 of plate with carbohydrates such as whole grain, 1/4 of plate with lean protein.",\n  "* Include healthy fats in your meal like: Olive oil, canola oil, avocado, and nuts"\n]'}, 'condition_name': 'Type 2 diabetes mellitus with hyperglycemia'}

{'condition_code': 'J449', 'is_hcc': True, 'condition_data': {'assessment_plan': '3. Chronic obstructive lung disease -\nUnchanged\nSPO2-98% today\nMaintain current inhaler regimen: Tiotropium and Fluticasone/Salmeterol.\nCounseled for smoking cessation today\nJ44.9: Chronic obstructive pulmonary disease, unspecified', 'extracted_text': '- Maintain current inhaler regimen: Tiotropium and Fluticasone/Salmeterol.\n- Counseled for smoking cessation today', 'condition_data': '[\n  "- Maintain current inhaler regimen: Tiotropium and 
Fluticasone/Salmeterol.",\n  "- Counseled for smoking cessation today"\n]'}, 'condition_name': 'Chronic obstructive pulmonary disease'}

{'condition_code': 'I10', 'is_hcc': False, 'condition_data': {'assessment_plan': '4. Essential hypertension -\nStable\non Metoprolol and Losartan-HCTZ\nBP checks at home: high in morning before meds\nBP: 140/80 today\nI10: Essential (primary) hypertension', 'extracted_text': '## Extracted Management Information:\n\n* Medications or treatment regimens:\n 
   * Metoprolol\n    * Losartan-HCTZ\n* Patient counseling or education:\n    * BP checks at home: high in morning before meds\n* Direct management instructions:\n    * BP checks at home\n* Diagnostic or testing plans:\n    * BP checks at home\n* Referral information:\n    * None \n', 'condition_data': '[\n  "## Extracted Management Information:",\n  "* 
Medications or treatment regimens:",\n  "    * Metoprolol",\n  "    * Losartan-HCTZ",\n  "* Patient counseling or education:",\n  "    * BP checks at home: high in morning before meds",\n  "* Direct management instructions:",\n  "    * BP checks at home",\n  "* Diagnostic or testing plans:",\n  "    * BP checks at home",\n  "* Referral information:",\n  
"    * None"\n]'}, 'condition_name': 'Chronic obstructive pulmonary disease'}

{'condition_code': 'I5022', 'is_hcc': True, 'condition_data': {'assessment_plan': '5. Chronic systolic heart failure -\nImproving\nContinue current medications: Lisinopril 10 mg 
daily, Metoprolol 50 mg twice daily, Furosemide 40 mg daily.\nWeight today was 259 lbs; Monitor weight daily to detect fluid retention. Schedule follow-up appointments every 3 months to assess symptom control and adjust treatment as necessary\nEchocardiography ordered today to assess the CHF\nI50.22: Chronic systolic (congestive) heart failure', 'extracted_text': '## Extracted Management Details:\n\n* Continue current medications: Lisinopril 10 mg daily, Metoprolol 50 mg twice daily, Furosemide 40 mg daily.\n* Monitor weight daily to detect fluid retention.\n* Schedule follow-up appointments every 3 months to assess symptom control and adjust treatment as necessary.\n* Echocardiography ordered today to 
assess the CHF. \n', 'condition_data': '[\n  "## Extracted Management Details:",\n  "* Continue current medications: Lisinopril 10 mg daily, Metoprolol 50 mg twice daily, Furosemide 40 mg daily.",\n  "* Monitor weight daily to detect fluid retention.",\n  "* Schedule follow-up appointments every 3 months to assess symptom control and adjust treatment as 
necessary.",\n  "* Echocardiography ordered today to assess the CHF."\n]'}, 'condition_name': 'Chronic systolic (congestive) heart failure'}

{'condition_code': 'N184', 'is_hcc': True, 'condition_data': {'assessment_plan': '6. Chronic kidney disease stage 4\nImproving: As per lab results-egfr today 28 from 21 (in March 2024)\nContinue ACE inhibitor. Start atorvastatin 10 mg\nN18.4: Chronic kidney disease, stage 4 (severe)', 'extracted_text': '## Extracted Management Information:\n\n* Continue 
ACE inhibitor.\n* Start atorvastatin 10 mg. \n', 'condition_data': '[\n  "## Extracted Management Information:",\n  "* Continue ACE inhibitor.",\n  "* Start atorvastatin 10 mg."\n]'}, 'condition_name': 'Chronic kidney disease'}
Retrying langchain_google_vertexai.chat_models._completion_with_retry.<locals>._completion_with_retry_inner in 4.0 seconds as it raised ResourceExhausted: 429 Quota exceeded for 
aiplatform.googleapis.com/generate_content_requests_per_minute_per_project_per_base_model with base model: gemini-pro. Please submit a quota increase request. https://cloud.google.com/vertex-ai/docs/generative-ai/quotas-genai..

{'condition_code': 'E6601', 'is_hcc': True, 'condition_data': {'assessment_plan': '7. Morbid obesity -\nImproving\nEncouraged for at least 150 minutes of moderate-intensity aerobic activity per week.\nDiscussed importance of weight loss and healthy lifestyle changes\nContinue to track dietary intake and physical activity\nE66.01: Morbid (severe) obesity 
due to excess calories', 'extracted_text': '## Extracted Management Details:\n\n* Encouraged for at least 150 minutes of moderate-intensity aerobic activity per week.\n* Discussed importance of weight loss and healthy lifestyle changes\n* Continue to track dietary intake and physical activity \n', 'condition_data': '[\n  "## Extracted Management Details:",\n  "* Encouraged for at least 150 minutes of moderate-intensity aerobic activity per week.",\n  "* Discussed importance of weight loss and healthy lifestyle changes",\n  "* Continue to track dietary intake and physical activity"\n]'}, 'condition_name': 'Morbid (severe) obesity due to excess calories'}"""