FROM brunneis/python:3.8.3-ubuntu-20.04

USER root
WORKDIR /tmp

# for source
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# for compile
RUN  apt-get update \
  && apt-get install -y wget \
  && apt-get install -y build-essential \
  && rm -rf /var/lib/apt/lists/*

# for TA-Lib
RUN pip install numpy && \
  wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

# for python postgresql driver
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# install common tools

RUN apt-get -y install build-essential && apt-get -y install autoconf automake gdb git libffi-dev zlib1g-dev libssl-dev file git curl vim jq unzip software-properties-common sudo apt-transport-https

RUN DEBIAN_FRONTEND=noninteractive apt install -y docker.io && apt-mark hold docker.io && systemctl enable docker

# install awscli v2

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install

# copy the dependencies file to the working directory
COPY core/requirements.txt .
# install dependencies
RUN pip3 install -r requirements.txt