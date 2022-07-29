CREATE DATABASE IF NOT EXISTS 'Ticker';
CREATE USER IF NOT EXISTS 'Ticker'@'%' identified by '92b9a3b730';
CREATE USER IF NOT EXISTS 'rohit'@'192.168.%' identified by 'admin1234';
GRANT ALL PRIVILEGES ON Ticker.* TO rohit@'192.168.%';