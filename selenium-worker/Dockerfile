FROM python:3.10-slim

WORKDIR /app
COPY main.py .

RUN pip install selenium redis beautifulsoup4

CMD ["python", "-u", "main.py"]
