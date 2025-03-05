from pipeline import langGraph_evaluation

plan="""1. Gastroesophageal reflux disease -
Stable
Continue the antacids
F/U in 3 months
K21.9: Gastro-esophageal reflux disease without esophagitis"""
print(langGraph_evaluation(plan))