FROM ubuntu:latest
ADD . /opt
WORKDIR /opt
RUN apt-get update
RUN apt-get install python-pip
RUN apt-get install python-dev 
RUN pip install -r requirment.txt

