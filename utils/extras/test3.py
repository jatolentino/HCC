import vertexai
from vertexai.preview.generative_models import GenerativeModel
import os
from dotenv import load_dotenv
load_dotenv()

PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION')
CREDENTIALS_PATH = os.getenv('CREDENTIALS_PATH')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

project_id = PROJECT_ID
location = LOCATION

vertexai.init(project=project_id, location=location)

model = GenerativeModel('gemini-pro')
response = model.generate_content('Say hi')

print(response.text)