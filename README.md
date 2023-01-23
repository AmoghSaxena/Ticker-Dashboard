# Ticker Dashboard
[![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Fira+Code&pause=1000&width=435&lines=Ticker%2FOn+Screen+Promotion)](https://git.io/typing-svg)

This is the Ticker/On Screen Promotion Server files which can be hosted as **Standalone** or **Dockerized Container**

>##### MAKE SURE TO CHANGE THE  `/etc/env/ticker.env`  FOR TICKER SETTINGS OR COPY `sample.env to /etc/env/ticker.env` SO THAT IT CAN BUILD ACCORDING TO THE REQUIREMENTS


#### _Requirements for this project to run:_ 
> For Standalone

| Requirements | Version |
| ------ | ------ |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=yellow) | ![Python](https://img.shields.io/badge/V3.9+-3776AB?style=for-the-badge) |
| ![Pip](https://img.shields.io/badge/PIP-3776AB?style=for-the-badge&logo=python&logoColor=yellow) | ![Python](https://img.shields.io/badge/V22.0+-3776AB?style=for-the-badge) |

 
> For Dockerized Setup


| Requirements | Version |
| ------ | ------ |
| ![Python](https://img.shields.io/badge/Docker-3776AB?style=for-the-badge&logo=docker&logoColor=yellow) | ![Python](https://img.shields.io/badge/v20.10+-3776AB?style=for-the-badge) |
| ![Python](https://img.shields.io/badge/Docker-Compose-3776AB?style=for-the-badge&logo=docker&logoColor=yellow) | ![Python](https://img.shields.io/badge/v2.4+-3776AB?style=for-the-badge) |



## To Run the server follow the Steps below!
- Step 1 [Clone this Repository]
`git clone https://dvgit.digivalet.com/scm/pyt/ticker-dashboard.git TickerDashboard`
- Step 2 [Change the Working directory to the cloned directory]
`cd TickerDashboard`

#### _To Start with it with Docker you can run few Simple Commands_
- Step 3 [Create Docker Network]
`docker network create tickernetwork`
- Step 4 [Edit `sample-env` for environment and `dbconfig/my.cnf` for database configuration and `docker-compose.yml` and then move sample-env file]
`cp sample-env /etc/env/ticker.env`
- Step 5 [Make Initial Build]
`docker-compose build`
- Step 6 [Run the Cloud Server]
`docker-compose up -d`

#### _To Start with it as a Standalone_
- Step 3 [Install the Requirements - Make sure you Have Python3.8 +]
`pip install -r requirements.txt`

- Step 4 [To perform Migrations]
`python manage.py makemigrations`

- Step 5 [To migrate the database]
`python manage.py migrate`

- Step 6 [This will run your server on Port 5085]
`gunicorn --config gunicorn-cfg.py ticker_dashboard.wsgi`
 


## Changelogs 
```
Changes between 1.3 and 1.4:
--------------------------------

Core:
 * Fixed Celery Worker Crash Issue


Changes between 1.2 and 1.3:
--------------------------------

Core:
 * Added Closing API Support
 * Fixed Priority for Multiple Ticker Launch

APIs:
 * Modified Ticker API for priority
     - Dashboard will first close Ticker and then launch new Ticker.


Changes between 1.1 and 1.2:
--------------------------------

Platform support changes:
 * 1.2-beta requires:
     - Docker 19.x.x or later (Only if Using Dockerized Method)
     - Python 3.9 or later (Only if Using Standalone Method)
     - Pip3 20.x or later (Only if Using Standalone Method)
 * Added Docker-Compose Support to the project

Core:
 * Shrink Docker Size from 580MB to 140MB
     - Fixed The flow and using Minimal OS for shrinking the size
 * Optimized the code redusing the memory usage and threadcounts
 * Reframed the Docker file to support Docker-Compose


Changes for 1.1:
--------------------------------

APIs:
 * Added New API/s TV & iPad Status
     - DVC will now give TV & iPad Status for the ticker.

Database:
 * Added New Table for DND & Ticker Status as well for future enhancement


Changes for 1.0:
--------------------------------

Platform support changes:
 * Linux on ARM is now supported
 * Windows is now supported as well.

Core:
 * New API Installed:
     - Fixed The flow of API Manupliation
 * New Dashboard Added for Ticker
```
