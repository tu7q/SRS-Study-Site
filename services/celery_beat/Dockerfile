FROM python:3.10-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# create and set /opt/djangoapp as the working directory
RUN mkdir -p /opt/app/web
WORKDIR /opt/app

# copy entrypoint and make it executable
COPY ./services/celery_beat/entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# install the required python utilities
COPY requirements.txt requirements.txt 
COPY requirements_prod.txt requirements_prod.txt 

RUN python3 -m pip install -r requirements.txt 
RUN python3 -m pip install -r requirements_prod.txt 

RUN useradd celerybeat
# Change to non-root privilege
USER celerybeat
