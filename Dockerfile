FROM ubuntu:latest

RUN apt update && apt -y install aria2 \
		python3 \
		python3-pip


