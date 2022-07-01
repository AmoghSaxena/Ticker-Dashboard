from celery import shared_task
import subprocess

@shared_task(bind=True)
def test_fun(self):
    command = ['notify-send Hello']
    #,'sshpass -p 1 ssh -p7010 -X -o StrictHostKeyChecking=no guest@172.22.12.62 start-ticker']
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

@shared_task(bind=True)
def celery_beat_name(self):
    command = ['sshpass -p 1 ssh -p7010 -X -o StrictHostKeyChecking=no guest@172.22.12.62 ticker-birthday']
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)