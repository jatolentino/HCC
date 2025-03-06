import os
import pytest
import sys
import constants
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from utils.regex.regex_utils import extract_assessment_plan, extract_each_plan, \
    match_icd10_codes, is_icd10_an_hcc

def test_extract_assessment_plan():
    pn_to_analyze_1 = os.path.join(os.path.dirname(__file__), '../../../progress_notes/pn_1')
    with open(pn_to_analyze_1, 'r') as file:
        text = file.read()

    result = extract_assessment_plan(text)
    expected = constants.plan_section
    assert result == expected, f"Expected: {expected}, but got: {result}"

def test_extract_each_plan():
    result = extract_each_plan(constants.plan_section)
    expected = constants.list_of_sections
    assert result == expected, f"Expected: {expected}, but got: {result}"
    
def test_match_icd10_codes():
    result = match_icd10_codes(constants.individual_assessment_plan)
    expected = "J44.9"
    assert result == expected, f"Expected: {expected}, but got: {result}"

def test_is_icd10_an_hcc():
    result = is_icd10_an_hcc("J44.9", constants.individual_assessment_plan)
    expected = {
            "condition_code": "J449",
            "condition_name": "Chronic obstructive pulmonary disease",
            "is_hcc": True
        }
    assert result == expected, f"Expected: {expected}, but got: {result}"