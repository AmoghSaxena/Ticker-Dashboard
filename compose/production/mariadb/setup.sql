CREATE DATABASE Ticker;
CREATE USER Ticker@% identified by 92b9a3b730;
CREATE USER rohit@'192.168.%' identified by admin1234;
GRANT ALL PRIVILEGES ON Ticker.* TO rohit@'192.168.%';