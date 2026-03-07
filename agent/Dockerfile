FROM python:3.14-slim

WORKDIR /agent-app 

COPY . .

RUN apt update -y && apt upgrade -y 

RUN  pip install -r  requirements.txt

EXPOSE 3000

