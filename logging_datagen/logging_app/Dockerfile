FROM python:3.10

RUN apt-get update && apt-get install procps -y

WORKDIR /opt/app

COPY . .

CMD ["./loggingdatagen"]
