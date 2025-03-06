# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Poetry
RUN pip install poetry

# Install dependencies
RUN poetry install

# Make port 80 available to the world outside this container
EXPOSE 80

# Run the application with Poetry to use the virtual environment
CMD ["poetry", "run", "python", "main.py"]

# Define a volume to store the output
VOLUME ["/app/result"]
