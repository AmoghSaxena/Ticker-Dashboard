FROM python:3.10-slim


# COPY /etc/timezone /etc/timezone

RUN apt-get update && apt install -y command-not-found
RUN apt-file update
RUN update-command-not-found

RUN apt-get update && apt-get install -yq --no-install-recommends \
    mariadb-client-core-10.5 openssh-server screen redis nginx

RUN apt  update

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements/production.txt 
COPY ./requirement.txt /requirementmain.txt
RUN pip install -r /requirementmain.txt 


COPY ./dockersetup/startworker /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./dockersetup/startbeat /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./dockersetup/createadmin /createadmin
RUN sed -i 's/\r$//g' /createadmin
RUN chmod +x /createadmin

COPY ./dockersetup/startservices /startservices
RUN sed -i 's/\r$//g' /startservices
RUN chmod +x /startservices

WORKDIR /app

