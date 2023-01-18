import base64
import subprocess
import os

try:
    username = subprocess.check_output(['cat', '/app/admin_user']).decode().strip()
    password = subprocess.check_output(['cat', '/app/admin_pass']).decode().strip()
except:
    username = "testuser"
    password = "testpass"


tmp = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode()
os.system(f"echo {tmp} > /app/auth_token_api")