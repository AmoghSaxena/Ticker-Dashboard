# Ticker/On Screen Promotion Dashboard Server.


># MAKE SURE TO CHANGE THE `ENV` FROM THE DOCKERFILE SO THAT IT CAN BUILD ACCORDING TO THE REQUIREMENTS


#### This is the Ticker/On Screen Promotion Server files which can be hosted as Standalone or Dockerized Container


## To Run the server follow the Steps below!

> Step 1 [Clone this Repository]
```
git clone https://github.com/AmoghSaxena/Ticker-Dashboard.git TickerDashboard
```

> Step 2 [Change the Working directory to the cloned directory]
```
cd TickerDashboard
```

###  To Start with it with Docker you can run few Simple Commands

> Step 3 [Build the image of it]
```
docker build -t tickerdashboard:1.0 .
```

> Step 4 [Run the container with the same image]
```
docker run -d --name tickerserver -p 8042:5015 -v tickerdashboard:/var/lib/mysql -v media:/app/media tickerdashboard:1.0
```

> Step 5 [Make Initial Migrations] - MAKE SURE TO WAIT FOR FEW SECONDS SO THAT MYSQL SERVICES CAN START
```
docker exec -it tickerserver /startservices
```

> Step 6 [Run the Cloud Server]
```
docker exec -itd tickerserver /startserver
```

### To Start with it as a Standalone
> Step 3 [Install the Requirements - Make sure you Have Python3.8 +]
```
pip install -r requirements.txt
```

> Step 4 [To perform Migrations]
```
python manage.py makemigrations
```

> Step 5 [To migrate the database]
```
python manage.py migrate
```

> Step 6 [This will run your server on Port 5085]
```
gunicorn --config gunicorn-cfg.py ticker_dashboard.wsgi
```
