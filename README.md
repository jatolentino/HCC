# Clinical HCC Extractor

## Overview
The Clinical HCC Extractor is a Python-based AI solution that automates the extraction of HCC-relevant conditions from clinical progress notes. It leverages Google's Vertex AI Gemini 1.5 Flash and the LangGraph framework to process clinical notes, identify medical conditions, and determine their HCC relevance.

## Features
- Extracts medical conditions with ICD-10 codes from clinical progress notes
- Validates conditions against HCC-relevant codes
- Structures extracted data in a standardized JSON format
- Processes multiple progress notes in batch
- Stores results in a mounted volume for easy access

## Architecture
The solution follows a layered architecture:
1. **Document Loading Layer**: Reads and prepares progress notes for processing
2. **Condition Extraction Layer**: Uses LLMs to extract conditions and their details
3. **HCC Validation Layer**: Verifies if extracted conditions are HCC-relevant
4. **Output Layer**: Formats and outputs the structured data

## Setup Instructions

### Prerequisites
- Python 3.11 or higher
- Docker (for containerized deployment)
- Google Cloud Service Account with access to Vertex AI

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/clinical-hcc-extractor.git
   cd clinical-hcc-extractor
   ```

2. **Set up the environment variables**
   ```bash
   cp .env.example .env
   # Edit the .env file and add your Google Cloud credentials
   ```

3. **Install dependencies using Poetry**
   ```bash
   poetry install
   ```

4. **Prepare your Google Cloud credentials**
   - Create a service account in Google Cloud Console
   - Grant it access to Vertex AI (requires the "Vertex AI User" role at minimum)
   - Download the JSON key file and save it as **`credentials/service-account.json`**
   - Make sure the credentials directory exists: `mkdir -p credentials`
   - Ensure the path in your .env file matches where you saved the credentials

## Running the Solution

### Using Poetry (Local Development)
```bash
# Process all progress notes and output results
poetry run python apps/hcc_extractor_app/app.py

# Start the LangGraph development web app
poetry run langgraph dev
```

### Using Docker
```bash
# Build the Docker image
docker build -t clinical-hcc-extractor \
  --build-arg GOOGLE_API_KEY=your_api_key \
  --build-arg GOOGLE_PROJECT_ID=your_project_id .

# Run the container with mounted volumes for credentials and results
# On Windows Git Bash, use this format
docker run \
  -v //$(pwd)/credentials/service-account.json:/app/credentials/service-account.json \
  -v //$(pwd)/results:/app/results \
  clinical-hcc-extractor

# On Linux/Mac
docker run \
  -v /path/to/service-account.json:/app/credentials/service-account.json \
  -v $(pwd)/results:/app/results \
  clinical-hcc-extractor

# On Windows PowerShell, use this format for mounting volumes
docker run `
  -v "${PWD}/credentials/service-account.json:/app/credentials/service-account.json" `
  -v "${PWD}/results:/app/results" `
  clinical-hcc-extractor

# On Windows Command Prompt, use this format
docker run ^
  -v "%cd%\credentials\service-account.json:/app/credentials/service-account.json" ^
  -v "%cd%\results:/app/results" ^
  clinical-hcc-extractor
```

> **Important**: Make sure your service-account.json file has the necessary permissions to access Vertex AI. The file should be stored securely and never committed to version control.

## Accessing the Results
The extracted conditions are saved as JSON files in the `results` directory (when running locally) or in the mounted volume (when running with Docker). Each progress note generates a separate JSON file with the following structure:

```json
[
  {
    "condition_code": "K21.9",
    "condition_name": "Gastroesophageal reflux disease",
    "is_hcc": false,
    "condition_data": "Stable\nContinue the antacids\nF/U in 3 months"
  },
  {
    "condition_code": "E11.65",
    "condition_name": "Hyperglycemia due to type 2 diabetes mellitus",
    "is_hcc": true,
    "condition_data": "Worsening\nContinue Metformin1000 mg BID and Glimepiride 8 mg\nRecommend a low sugar and low carbohydrate diet.\nDiscussed 1/2 plate with non-starchy vegetables\nInclude healthy fats in your meal like: Olive oil"
  }
]
```

## LangGraph Development Web App
The LangGraph development web app allows you to visualize and debug the processing workflow:

1. Start the app:
   ```bash
   poetry run langgraph dev
   ```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8000)

3. Use the web interface to trace and debug the execution graph

## Testing
Run the tests to ensure the system is working correctly:

```bash
poetry run pytest
```

## Limitations and Known Issues
- The system expects progress notes to follow a specific format with an "Assessment / Plan" section
- Large batches of progress notes might require significant memory

## Future Improvements
- Add support for more diverse progress note formats
- Implement parallel processing for better scalability
- Enhance the extraction accuracy with domain-specific training