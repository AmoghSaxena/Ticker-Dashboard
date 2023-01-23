from ticker_dashboard.settings import BASE_DIR
from datetime import datetime,timedelta
from ticker_dashboard.celery import app
import os

BASE_DIR+='/logs/'
today_date=datetime.now()
today_date-=timedelta(days=90)

def clearLogs(file,updatefile):
    file=file.readlines()
    for i in file:
        date_obj=datetime.strptime(i.split(' ')[1],'%Y-%m-%d')
        if date_obj>today_date:
            updatefile.write(i)
@app.task
def filereader():
    for path in os.listdir(BASE_DIR):
        if os.path.isfile(os.path.join(BASE_DIR, path)) and 'celery' not in path:
            file1=BASE_DIR+path
            file2=BASE_DIR+'temp.log'
            print(file1)
            clearLogs(open(file1,'r'),open(file2,'w'))
            os.rename(file2, file1)
    
    if os.path.exists(BASE_DIR+'temp.log'):
        os.remove(BASE_DIR+'temp.log')