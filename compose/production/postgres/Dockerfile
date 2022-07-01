FROM postgres:10.8

RUN mkdir -p /usr/local/bin/maintenance/
COPY ./compose/production/postgres/maintenance/* /usr/local/bin/maintenance/
RUN chmod -R 777 /usr/local/bin/maintenance
RUN mv /usr/local/bin/maintenance/* /usr/local/bin