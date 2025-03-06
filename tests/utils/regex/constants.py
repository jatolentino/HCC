plan_section = """1. Gastroesophageal reflux disease -
   Stable
   Continue the antacids
   F/U in 3 months
   K21.9: Gastro-esophageal reflux disease without esophagitis

2. Hyperglycemia due to type 2 diabetes mellitus -
   Worsening
   Continue Metformin1000 mg BID and Glimepiride 8 mg
   Recommend a low sugar and low carbohydrate diet. Fruits and vegetables are acceptable.
   Discussed 1/2 plate with non-starchy vegetables, 1/4 of plate with carbohydrates such as whole grain, 1/4 of plate with lean protein.
   Include healthy fats in your meal like: Olive oil, canola oil, avocado, and nuts
   E11.65: Type 2 diabetes mellitus with hyperglycemia

3. Chronic obstructive lung disease -
   Unchanged
   SPO2-98% today
   Maintain current inhaler regimen: Tiotropium and Fluticasone/Salmeterol.
   Counseled for smoking cessation today
   J44.9: Chronic obstructive pulmonary disease, unspecified

4. Essential hypertension -
   Stable
   on Metoprolol and Losartan-HCTZ
   BP checks at home: high in morning before meds
   BP: 140/80 today
   I10: Essential (primary) hypertension

5. Chronic systolic heart failure -
   Improving
   Continue current medications: Lisinopril 10 mg daily, Metoprolol 50 mg twice daily, Furosemide 40 mg daily.
   Weight today was 259 lbs; Monitor weight daily to detect fluid retention. Schedule follow-up appointments every 3 months to assess symptom control and adjust treatment as necessary
   Echocardiography ordered today to assess the CHF
   I50.22: Chronic systolic (congestive) heart failure

6. Chronic kidney disease stage 4
   Improving: As per lab results-egfr today 28 from 21 (in March 2024)
   Continue ACE inhibitor. Start atorvastatin 10 mg
   N18.4: Chronic kidney disease, stage 4 (severe)

7. Morbid obesity -
   Improving
   Encouraged for at least 150 minutes of moderate-intensity aerobic activity per week.
   Discussed importance of weight loss and healthy lifestyle changes
   Continue to track dietary intake and physical activity
   E66.01: Morbid (severe) obesity due to excess calories"""
   
list_of_sections = ['1. Gastroesophageal reflux disease -\nStable\nContinue the antacids\nF/U in 3 months\nK21.9: Gastro-esophageal reflux disease without esophagitis', '2. Hyperglycemia due to type 2 diabetes mellitus -\nWorsening\nContinue Metformin1000 mg BID and Glimepiride 8 mg\nRecommend a low sugar and low carbohydrate diet. Fruits and vegetables are acceptable.\nDiscussed 1/2 plate with non-starchy vegetables, 1/4 of plate with carbohydrates such as whole grain, 1/4 of plate with lean protein.\nInclude healthy fats in your meal like: Olive oil, canola oil, avocado, and nuts\nE11.65: Type 2 diabetes mellitus with hyperglycemia', '3. Chronic obstructive lung disease -\nUnchanged\nSPO2-98% today\nMaintain current inhaler regimen: Tiotropium and Fluticasone/Salmeterol.\nCounseled for smoking cessation today\nJ44.9: Chronic obstructive pulmonary disease, unspecified', '4. Essential hypertension -\nStable\non Metoprolol and Losartan-HCTZ\nBP checks at home: high in morning before meds\nBP: 140/80 today\nI10: Essential (primary) hypertension', '5. Chronic systolic heart failure -\nImproving\nContinue current medications: Lisinopril 10 mg daily, Metoprolol 50 mg twice daily, Furosemide 40 mg daily.\nWeight today was 259 lbs; Monitor weight daily to detect fluid retention. Schedule follow-up appointments every 3 months to assess symptom control and adjust treatment as necessary\nEchocardiography ordered today to assess the CHF\nI50.22: Chronic systolic (congestive) heart failure', '6. Chronic kidney disease stage 4\nImproving: As per lab results-egfr today 28 from 21 (in March 2024)\nContinue ACE inhibitor. Start atorvastatin 10 mg\nN18.4: Chronic kidney disease, stage 4 (severe)', '7. Morbid obesity -\nImproving\nEncouraged for at least 150 minutes of moderate-intensity aerobic activity per week.\nDiscussed importance of weight loss and healthy lifestyle changes\nContinue to track dietary intake and physical activity\nE66.01: Morbid (severe) obesity due to excess calories']

individual_assessment_plan = """3. Chronic obstructive lung disease -
   Unchanged
   SPO2-98% today
   Maintain current inhaler regimen: Tiotropium and Fluticasone/Salmeterol.
   Counseled for smoking cessation today
   J44.9: Chronic obstructive pulmonary disease, unspecified"""