FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=US/Chicago
RUN apt update && apt-get install -y tzdata


RUN apt-get update && apt-get -y install python3 python3-pip npm

# Build the python backend
ADD requirements.txt /
RUN pip3 install -r /requirements.txt

