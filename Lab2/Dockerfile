FROM ubuntu:22.04

RUN apt-get update -y && apt-get install -y iputils-ping

RUN apt-get install python3 -y

WORKDIR /app

COPY . .

ENTRYPOINT ["python3", "main.py"]