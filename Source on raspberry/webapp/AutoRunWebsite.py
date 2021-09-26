import os,sys

os.system("systemctl restart webapp_doan.uwsgi.service")

os.system("python3 /home/pi/Desktop/NLP_Class/code_assistant.py")