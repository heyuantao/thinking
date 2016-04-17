#FROM ubuntu:latest
FROM ubuntu:14.04
RUN rm /etc/apt/sources.list
ADD sources.list /etc/apt/
#RUN mkdir /opt
WORKDIR /opt
ADD requirment.txt /opt
RUN apt-get update
RUN apt-get install -y  python-dev python-pip 
RUN pip install -i http://pypi.douban.com/simple/  -r requirment.txt 

