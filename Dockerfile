# docker build -t openrunlog/mongodb-server

FROM ubuntu:12.04

RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y python-dev build-essential
RUN apt-get install -y python-setuptools
RUN apt-get install -y git

RUN curl -O https://raw.github.com/pypa/pip/master/contrib/get-pip.py
RUN python get-pip.py

# openrunlog
RUN mkdir /openrunlog

# do pip stuff here to prevent annoying re-install
ADD requirements.txt /openrunlog/requirements.txt
RUN pip install -r /openrunlog/requirements.txt

ADD . /openrunlog
WORKDIR /openrunlog

ENV ORL_DB_NAME openrunlog
# ENV ORL_DB_URI 
ENV ORL_DEBUG True
ENV ORL_COOKIE_SECRET insertyourrandomstringhere

EXPOSE 11000
ENTRYPOINT ["supervisord", "-c", "/openrunlog/supervisord.conf", "-n"]
