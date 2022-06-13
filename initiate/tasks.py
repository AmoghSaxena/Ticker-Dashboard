from __future__ import absolute_import, unicode_literals
from datetime import datetime
import os
import subprocess
from celery import shared_task

@shared_task(name = 'print_time')
def print_time():
    print('Hello time: ',datetime.now())

@shared_task(name = 'execute_command')
def execute_command():
    command = ["notify-send hello",'ping -c 8.8.8.8']
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
