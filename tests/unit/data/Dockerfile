FROM ubuntu
MAINTAINER Kimbro Staken

LABEL description="This text illustrates \
that label-values can span multiple lines. \
And be a real pain!" test="test_one" "two"="three" "empty"=""

RUN apt-get update
RUN apt-get install -y software-properties-common python curl
RUN curl -sL https://deb.nodesource.com/setup | bash -
RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ precise universe" >> /etc/apt/sources.list
RUN apt-get update
RUN apt-get install -y nodejs npm git
RUN npm install -g docpad@6.44

EXPOSE 80
EXPOSE 5432 443

ADD Dockerfile /
ADD ["Dockerfile", "/"]

COPY Dockerfile /
COPY ["Dockerfile", "/"]

VOLUME /testvol /test2vol
VOLUME ["/test1vol", "/test2vol", "/test3vol"]

USER root

ARG test
ARG test1=1

STOPSIGNAL 9

CMD ["/bin/bash"]
