#!/bin/bash


mysql -e "CREATE DATABASE IF NOT EXISTS Ticker;"
mysql -e "CREATE USER IF NOT EXISTS 'Ticker'@'%' identified by '92b9a3b730';"
mysql -e "CREATE USER IF NOT EXISTS 'rohit'@'192.168.%' identified by 'admin1234';"
mysql -e "GRANT ALL PRIVILEGES ON *.* TO rohit@'192.168.%';"
