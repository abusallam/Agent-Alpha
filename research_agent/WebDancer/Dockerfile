# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set PYTHONPATH to ensure modules in subdirectories like 'demos' are found
ENV PYTHONPATH="/usr/src/app"

# Expose port 7860 for the Gradio UI (when CMD is not overridden)
EXPOSE 7860
# Port for the API (e.g., 8001) will be handled by Uvicorn command and docker-compose

# Default CMD is to run the Gradio UI app.
# For the API service, this CMD will be overridden in docker-compose.yml.
# API keys (GOOGLE_SEARCH_KEY, JINA_API_KEY, DASHSCOPE_API_KEY, etc.)
# should be passed as environment variables in docker-compose.yml for both UI and API services.
CMD ["python", "-m", "demos.assistant_qwq_chat"]
