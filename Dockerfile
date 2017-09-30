FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir -p app
RUN pwd

ADD ./app /app
WORKDIR /app

RUN apt-get update 
RUN apt-get install -y  python3 python3-pip  

ADD requirements.txt /app
RUN pip3 install -r requirements.txt
WORKDIR /app/app
RUN cd /app/app