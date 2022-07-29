FROM mariadb:10.7

# RUN mkdir -p /usr/local/bin/maintenance/
# COPY ./compose/production/postgres/maintenance/* /usr/local/bin/maintenance/
# RUN chmod -R 777 /usr/local/bin/maintenance
# RUN mv /usr/local/bin/maintenance/* /usr/local/bin

RUN mysql -e "CREATE DATABASE Ticker;"
RUN mysql -e "CREATE USER Ticker@% identified by 92b9a3b730;"
RUN mysql -e "CREATE USER rohit@'192.168.%' identified by admin1234;"
RUN mysql -e "GRANT ALL PRIVILEGES ON Ticker.* TO rohit@'192.168.%';"