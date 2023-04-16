FROM python:3.8
ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app

RUN apt-get update \
    && apt-get install -y netcat-openbsd \
    && apt-get clean

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY wait.sh /wait.sh
RUN chmod +x /wait.sh   

