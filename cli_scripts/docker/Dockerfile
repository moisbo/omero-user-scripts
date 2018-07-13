FROM centos:7

WORKDIR /tmp

RUN yum update -y && \
    yum install -y unzip zip vim telnet wget

RUN wget http://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm && \
    rpm -ivh epel-release-latest-7.noarch.rpm

RUN wget -P /etc/yum.repos.d https://zeroc.com/download/Ice/3.6/el7/zeroc-ice3.6.repo && \
    yum install -y ice-all-runtime ice-all-devel bzip2-devel openssl-devel zlib-devel libjpeg-devel gcc gcc-c++

RUN yum update -y && \
    yum install -y python-pip python-devel numpy scipy python-matplotlib python-tables python-redis

COPY requirements.txt \
     ./

ARG OMEROPY=OMERO.py-5.4.1-ice36-b75

ADD docker/${OMEROPY}.zip /

RUN pip install --no-cache-dir -r requirements.txt

ENV OMERO=OMERO.py-5.4.1-ice36-b75

ENV PATH=$PATH:/${OMERO}/lib/python:/${OMERO}/bi

ENV PYTHONPATH=$PYTHONPATH:/${OMERO}/lib/python:/${OMERO}/bin

RUN export OMERO=OMERO.py-5.4.1-ice36-b75 && \
    unzip /${OMERO}.zip -d / && \
    mkdir downloads

COPY download_files.py \
     test_connect.py \
     Parse_OMERO_Properties.py \
     ./