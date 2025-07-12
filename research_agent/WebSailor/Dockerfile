# Base on Python 3.11-slim as mentioned in WebSailor's README for conda env
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies that might be needed by sglang or other packages
# Omitting tmux and nvitop for now as they seem specific to the eval script's debug/manual use
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
# sglang installation can be heavy; ensure network stability or pre-built wheels if issues arise
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire WebSailor application code
# This assumes the Dockerfile is in research_agent/WebSailor/
COPY . .

# Set PYTHONPATH to include the src directory and the root, helpful for imports
ENV PYTHONPATH="/usr/src/app:/usr/src/app/src"

# Environment variables to be passed by docker-compose for the API and agent configuration
# These are examples; actual ones will depend on how ReactAgent is configured in api_wrapper.py
ENV MODEL_PATH_WEBSAILOR=""
ENV SUMMARY_MODEL_PATH_WEBSAILOR=""
ENV GOOGLE_API_KEY="" # For tool_search.py potentially
ENV JINA_API_KEY="" # For tool_visit.py potentially (if JinaReader is used)
ENV DASHSCOPE_API_KEY="" # If ReactAgent uses DashScope Qwen models
# Add other necessary ENV VARS for LLM connection, tool keys etc.

# Expose the port the API server (Uvicorn + FastAPI) will run on
# This will be defined in the CMD of the api_wrapper.py
# Let's assume port 8002 for this service for now
EXPOSE 8002

# The CMD will be to run the api_wrapper.py using Uvicorn.
# This will be created in a subsequent step.
# Example: CMD ["uvicorn", "src.api_wrapper:app", "--host", "0.0.0.0", "--port", "8002"]
# For now, leave a placeholder or a more generic entrypoint if the wrapper isn't ready.
# As a sensible default for now, allowing the container to be run and then exec into:
CMD ["bash"]
