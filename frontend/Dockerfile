FROM ubuntu:latest

RUN apt-get update && apt-get -y upgrade && apt-get -y install npm 

RUN mkdir /data/
RUN mkdir /data/src

COPY . /data/

RUN npm install -g npm@latest
RUN cd /data && npm install 

EXPOSE 8080
