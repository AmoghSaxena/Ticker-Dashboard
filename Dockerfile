
# FROM python:3.9
FROM mariadb:jammy

ENV TZ Asia/Kolkata
ENV DVS_FQDN_ENTRY "172.25.0.91 dvs-uatblue.digivalet.com"
ENV TICKER_FQDN 'ticker.dns.army'
ENV MYSQL_ROOT_PASSWORD root
ENV MARIADB_DATABASE Ticker
ENV DJANGO_SUPERUSER_USERNAME testuser
ENV DJANGO_SUPERUSER_PASSWORD testpass
ENV DJANGO_SUPERUSER_EMAIL admin@admin.com

ENV PYTHONUNBUFFERED 1

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -yq tzdata && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get install -yq --no-install-recommends \
    python3-pip net-tools iproute2 command-not-found python-is-python3 openssh-server screen redis

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

COPY ./dockersetup/startservices /startservices
RUN sed -i 's/\r$//g' /startservices
RUN chmod +x /startservices

COPY ./dockersetup/startserver /startserver
RUN sed -i 's/\r$//g' /startserver
RUN chmod +x /startserver

COPY . /app

# RUN pip install -r /app/requirement.txt 
RUN echo ${DVS_FQDN_ENTRY} >> /etc/hosts
RUN echo ${MARIADB_DATABASE} > /app/DATABASE_NAME.txt
RUN echo ${MYSQL_ROOT_PASSWORD} > /app/MYSQL_ROOT_PASSWORD_FILE.txt
RUN echo ${TICKER_FQDN} > /app/TICKER_FQDN.txt
RUN cp /app/AdminFiles/* /usr/local/lib/python3.10/dist-packages/admin_volt/templates/admin/

WORKDIR /app

