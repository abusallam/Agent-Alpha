FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="/usr/src/app"

EXPOSE 7860

CMD ["python", "-m", "demos.assistant_qwq_chat"]
