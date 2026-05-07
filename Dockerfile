FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY src/ ./src/

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["python", "server.py", "-m", "prod"]
