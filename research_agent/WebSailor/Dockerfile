FROM python:3.11-slim

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="/usr/src/app:/usr/src/app/src"

ENV MODEL_PATH_WEBSAILOR=""
ENV SUMMARY_MODEL_PATH_WEBSAILOR=""
ENV GOOGLE_API_KEY=""
ENV JINA_API_KEY=""
ENV DASHSCOPE_API_KEY=""

EXPOSE 8002

CMD ["bash"]
