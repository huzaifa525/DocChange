FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["gunicorn", "wsgi:app", "-b", "0.0.0.0:8080", "--workers=4"]