# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available for the Uvicorn server
EXPOSE 8000

# Define environment variable (can be overridden in docker-compose)
ENV PYTHONPATH="/usr/src/app"
ENV OPENAI_API_KEY=""
ENV OPENAI_MODEL_SERVER=""
ENV DASHSCOPE_API_KEY=""
# Add other ENV VARS that api_wrapper.py or WebWalker might need for LLM config at runtime

# Run the FastAPI wrapper with Uvicorn when the container launches
# Ensure api_wrapper.py is in the src directory for this CMD to work as written.
CMD ["uvicorn", "src.api_wrapper:app", "--host", "0.0.0.0", "--port", "8000"]
