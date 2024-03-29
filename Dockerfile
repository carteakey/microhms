# pull official base image
FROM python:3.10.7-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 

# copy project
COPY . /usr/src/app/
