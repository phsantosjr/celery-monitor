FROM python:3.9.13-slim

MAINTAINER Loja Conectada <contato@lojaconectada.com.br>

RUN apt-get update -y
RUN pip3 install --upgrade pip

RUN mkdir /opt/app
RUN mkdir /opt/app/celery-monitor
RUN mkdir /opt/app/celery-monitor/logs

ADD ./requirements-prod.txt /opt/app/celery-monitor/requirements-prod.txt
ADD ./requirements.txt /opt/app/celery-monitor/requirements.txt

RUN pip install -r /opt/app/celery-monitor/requirements-prod.txt -U

ADD . /opt/app/celery-monitor
ENV PYTHONPATH $PYTHONPATH:/opt/app/celery-monitor
WORKDIR /opt/app/celery-monitor

EXPOSE 8905