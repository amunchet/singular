FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=US/Chicago
RUN apt update && apt-get install -y tzdata


RUN apt update && apt -y install aria2 \
		python3 \
		python3-pip \
		ffmpeg


ADD requirements.txt /
RUN pip3 install -r requirements.txt

