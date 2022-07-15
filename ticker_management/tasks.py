from celery import shared_task
import subprocess

@shared_task(bind=True)
def callticker(self,command):
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# @shared_task(bind=True)
# def celery_beat_name(self):
#     command = ['sshpass -p 1 ssh -p7010 -X -o StrictHostKeyChecking=no guest@172.22.12.62 ticker-birthday']
#     subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)