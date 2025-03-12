# """
# Prompt templates for the HCC extraction agent.
# """

# from langchain.prompts import PromptTemplate

# # Template for processing a progress note
# note_processing_prompt = PromptTemplate.from_template(
#     """
# You are a clinical documentation expert specializing in analyzing medical progress notes.
# Your task is to analyze the provided clinical progress note and identify the Assessment/Plan section.

# Guidelines:
# - Look for a section titled "Assessment / Plan", "Assessment and Plan", "A/P", or similar
# - The Assessment/Plan section typically contains numbered conditions or problems with treatment plans
# - Each condition is usually numbered (e.g., "1.", "2.", etc.)
# - Extract both the assessment/plan section and identify the individual condition blocks within it

# Progress Note:
# ```
# {note_content}
# ```

# {format_instructions}
# """
# )

# # Template for extracting conditions from progress notes
# condition_extraction_prompt = PromptTemplate.from_template(
#     """
# You are a clinical documentation expert specializing in extracting structured information from medical progress notes.
# Your task is to extract medical conditions and their associated ICD-10 codes from each condition block.

# For each condition block:
# 1. Identify the medical condition name
# 2. Extract the associated ICD-10 code (format like "E11.65")
# 3. Capture the condition management details (status, medications, recommendations, etc.)

# Guidelines:
# - Extract only the information explicitly stated in the text
# - Be precise with ICD-10 codes - they follow the format of a letter followed by numbers and possibly a decimal point
# - Condition data should include all relevant clinical details (status, medications, follow-up plans)
# - Each condition should have all three pieces of information: code, name, and data

# Condition Blocks:
# ```
# {condition_blocks}
# ```

# {format_instructions}
# """
# )

# # Template for validating HCC relevance
# hcc_validation_prompt = PromptTemplate.from_template(
#     """
# You are a clinical documentation expert specializing in HCC (Hierarchical Condition Category) coding.
# Your task is to validate whether each extracted condition is HCC-relevant based on the provided list of HCC-relevant ICD-10 codes.

# A condition is HCC-relevant if its ICD-10 code exactly matches one in the provided list. 
# Partial matches are not sufficient - the code must match exactly.

# Guidelines:
# - For each condition, check if its code appears in the HCC codes list
# - Mark a condition as HCC-relevant (is_hcc = true) only if there is an exact match
# - Do not alter the condition code, name, or data
# - Be precise in your validation - this affects proper reimbursement

# Extracted Conditions:
# ```
# {conditions}
# ```

# HCC-Relevant Codes:
# ```
# {hcc_codes}
# ```

# {format_instructions}
# """
# )


# v1

"""
Prompt templates for the HCC extraction agent.
"""

from langchain.prompts import PromptTemplate

# Template for processing a progress note
note_processing_prompt = PromptTemplate.from_template(
    """
You are a clinical documentation expert specializing in analyzing medical progress notes.
Your task is to analyze the provided clinical progress note and identify the Assessment/Plan section.

Guidelines:
- Look for a section titled "Assessment / Plan", "Assessment and Plan", "A/P", or similar
- The Assessment/Plan section typically contains numbered conditions or problems with treatment plans
- Each condition is usually numbered (e.g., "1.", "2.", etc.)
- Extract both the assessment/plan section and identify the individual condition blocks within it

Progress Note:
```
{note_content}
```

{format_instructions}
"""
)

# Template for extracting conditions from progress notes
condition_extraction_prompt = PromptTemplate.from_template(
    """
You are a clinical documentation expert specializing in extracting structured information from medical progress notes.
Your task is to extract medical conditions and their associated ICD-10 codes from clinical documentation.

For each medical condition in the Assessment/Plan section:
1. Identify the medical condition name (e.g., "Substance use disorder", "Hyperlipidemia", "GERD")
2. Extract the associated ICD-10 code (format like "F19.20", "E78.5", "K21.9")
3. Capture the condition management details (status, medications, recommendations, etc.)

Guidelines:
- Extract only the information explicitly stated in the text
- Be precise with ICD-10 codes - they follow the format of a letter followed by numbers and possibly a decimal point
- Condition data should include all relevant clinical details (status, medications, follow-up plans)
- Each condition should have all three pieces of information: code, name, and data
- Make sure to extract ALL conditions mentioned in the Assessment/Plan section
- Look for condition codes in formats like "F19.20", "I25.10", etc.
- Pay special attention to numbered lists (1., 2., 3. or 1), 2), 3))

Here's the full note context for reference:
```
{full_note}
```

Assessment/Plan section:
```
{assessment_plan}
```

Condition Blocks to analyze:
```
{condition_blocks}
```

Return ALL medical conditions with their codes and management details.

{format_instructions}
"""
)

# Template for validating HCC relevance
hcc_validation_prompt = PromptTemplate.from_template(
    """
You are a clinical documentation expert specializing in HCC (Hierarchical Condition Category) coding.
Your task is to validate whether each extracted condition is HCC-relevant based on the provided list of HCC-relevant ICD-10 codes.

A condition is HCC-relevant if its ICD-10 code exactly matches one in the provided list. 
Partial matches are not sufficient - the code must match exactly.

Guidelines:
- For each condition, check if its code appears in the HCC codes list
- Mark a condition as HCC-relevant (is_hcc = true) only if there is an exact match
- Do not alter the condition code, name, or data
- Be precise in your validation - this affects proper reimbursement

Extracted Conditions:
```
{conditions}
```

HCC-Relevant Codes:
```
{hcc_codes}
```

{format_instructions}
"""
)