FROM selenium/standalone-chrome:latest

USER root

COPY main.py /app/main.py
WORKDIR /app

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install selenium

CMD ["python3", "main.py"]
