FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=US/Chicago
RUN apt update && apt-get install -y tzdata

RUN apt-get update && apt-get -y upgrade && apt-get -y install npm nodejs

RUN mkdir /data/
RUN mkdir /data/src

COPY . /data/

# RUN npm install -g npm@latest
RUN cd /data && npm install 

EXPOSE 8080
