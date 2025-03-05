import os
import pytest
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from utils.regex.regex_utils import extract_assessment_plan


def test_extract_assessment_plan():   
    pn_to_analyze_1 = os.path.join(os.path.dirname(__file__), '../../../progress_notes/pn_1')

    with open(pn_to_analyze_1, 'r') as file:
        text = file.read()

    result = extract_assessment_plan(text)
    expected = """1. Gastroesophageal reflux disease -
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
    assert result == expected, f"Expected: {expected}, but got: {result}"
