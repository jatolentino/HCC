import vertexai
from vertexai.preview.generative_models import GenerativeModel
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\vertexai\hcc-project-452815-6fcd339bc332.json"

project_id = 'hcc-project-452815'
location = 'us-central1'

vertexai.init(project=project_id, location=location)

model = GenerativeModel('gemini-pro')
response = model.generate_content('Say hi')

print(response.text)