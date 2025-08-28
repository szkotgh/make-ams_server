FROM python:3.11-slim

LABEL maintainer="me@gunhee.kr"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
