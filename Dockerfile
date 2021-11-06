# syntax=docker/dockerfile:1
FROM python:3.7-slim
WORKDIR /home/app

RUN apt-get update
RUN apt-get install less

COPY . .

RUN ./lib.sh install

# CMD [ "python3", "-u", "server.py", "--i=0" ]