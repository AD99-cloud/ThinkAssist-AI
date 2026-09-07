FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY SRC ./SRC
COPY DATA ./DATA
COPY UI ./UI

EXPOSE 8000

CMD ["uvicorn", "SRC.api:app", "--host", "0.0.0.0", "--port", "8000"]