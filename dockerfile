FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
COPY config.py .
COPY dictionaries.py .
COPY keyboards.py .
COPY utils.py .
COPY web.py .

CMD ["python", "web.py"]