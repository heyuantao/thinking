FROM python
ADD . /opt
ADD /etc/shadowsocks/shadowsocks.json /etc/shadowsocks
WORKDIR /opt
RUN apt-get update
RUN apt-get install python-dev 
RUN pip install -r requirment.txt


