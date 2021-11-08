# syntax=docker/dockerfile:1
FROM python:3
WORKDIR /home/app

RUN apt-get update
RUN apt-get install less

## This copies meta-data folders. Copy only what is necessary.
COPY . .

RUN ./lib.sh install

# CMD [ "python3", "-u", "server.py", "--i=0" ]