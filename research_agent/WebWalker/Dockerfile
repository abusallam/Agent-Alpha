FROM python:3.9-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV PYTHONPATH="/usr/src/app"
ENV OPENAI_API_KEY=""
ENV OPENAI_MODEL_SERVER=""
ENV DASHSCOPE_API_KEY=""

CMD ["uvicorn", "src.api_wrapper:app", "--host", "0.0.0.0", "--port", "8000"]
