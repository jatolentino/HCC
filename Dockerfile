# Use a lightweight Python 3.11 image
FROM python:3.11-slim

# Define build arguments
ARG GOOGLE_API_KEY=""
ARG GOOGLE_PROJECT_ID=""
ARG USE_FALLBACK_EXTRACTION="false"

# Set environment variables from build arguments
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY} \
    GOOGLE_APPLICATION_CREDENTIALS="/app/credentials/service-account.json" \
    GOOGLE_PROJECT_ID=${GOOGLE_PROJECT_ID} \
    USE_FALLBACK_EXTRACTION=${USE_FALLBACK_EXTRACTION}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Set environment variables for Poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Set the working directory
WORKDIR /app

# Copy Poetry files first to leverage Docker cache
COPY pyproject.toml poetry.lock* /app/

# Install dependencies without the project (dependency-only mode first)
RUN poetry install --no-root

# Copy the entire application code
COPY . /app

# Re-install the project to include the app itself
RUN poetry install

# Create a directory for credentials
RUN mkdir -p /app/credentials

# Create a directory for results
RUN mkdir -p /app/results

# Add the current directory to PYTHONPATH
ENV PYTHONPATH="${PYTHONPATH}:/app"

# Mount point for the service account credentials
VOLUME ["/app/credentials"]

# Mount point for the output results
VOLUME ["/app/results"]

# Run the HCC extractor app
CMD ["poetry", "run", "python", "apps/hcc_extractor_app/app.py"]