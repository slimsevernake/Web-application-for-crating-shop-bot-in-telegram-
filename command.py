from collections import deque
import sys
import os
import requests
import json
import env_file
import subprocess

env = env_file.get()
PROTOCOL = 'http'


# import django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "viber_bot.settings")
# django.setup()
# from bot.models import *


def backup_create():
    """ Create database backup """
    command = "python ./manage.py dumpdata " \
        "--exclude auth.permission " \
        "--exclude contenttypes " \
        "--exclude sessions.session " \
        "--exclude subscribers.vibersubscribers " \
        "--exclude subscribers.telegramsubscribers " \
        "--exclude subscribers.vibermessage " \
        "--exclude subscribers.telegrammessage " \
        "--exclude subscribers.replyhelp " \
        "--exclude subscribers.helpmessage " \
        "--indent 4 > db.json"
    os.system("rm db.json")
    os.system(command)


def db_backup_load(filename="db.json"):
    """ load database info from file """
    command = f"python ./manage.py loaddata {filename}"
    os.system(command)


def db_init():
    """ Use migrate """
    command = f"python ./manage.py makemigrations"
    os.system(command)
    command = f"python ./manage.py migrate"
    os.system(command)


def create_admin(name="Admin", email="Admin@mail.com"):
    """ run to server """
    command = f"python manage.py createsuperuser --username {name} --email {email}"
    os.system(command)


def run():
    db_init()
    """ run to server """
    command = f"python ./manage.py runserver {env.get('SITE_HOST')}:{env.get('SITE_PORT')} --noreload"
    os.system(command)


def clean():
    """ delete all __pycache__ """
    command = f'find . | grep -E "(pycache|\.pyc|\.pyo$)" | xargs rm -rf'
    os.system(command)


def setup_viber_dev():
    launch_ngrok()
    public_url = get_url()
    set_viber_webhook(domain=public_url)


def setup_telegram_dev():
    launch_ngrok()
    public_url = get_tel_url()
    set_telegram_webhook(domain=public_url)


def launch_ngrok(protocol: str=None, port: int=None):
    protocol = PROTOCOL if not protocol else protocol
    port = env.get('SITE_PORT') if not port else port
    command = f"ngrok {protocol} {port} > /dev/null &"
    res = os.system(command)


def get_tel_url():
    data = subprocess.check_output("curl -s http://localhost:4040/api/tunnels", shell=True)
    b = data.decode('utf-8')
    data = json.loads(b)
    public_url = f"{data['tunnels'][0]['public_url']}/tele_prod/"
    print(public_url)
    return public_url


def get_url():
    data = subprocess.check_output("curl -s http://localhost:4040/api/tunnels", shell=True)
    b = data.decode('utf-8')
    data = json.loads(b)
    public_url = f"{data['tunnels'][0]['public_url']}/viber_prod/"
    print(public_url)
    return public_url


def set_viber_webhook(domain: str, token=None) -> None:
    if not token:
        token = env.get('VIBER_TOKEN')
    print(token)
    print(domain)
    hook = "https://chatapi.viber.com/pa/set_webhook"
    headers = {"X-Viber-Auth-Token": token, "Content-Type": "application/json"}
    sen = dict(url=domain, event_types=["subscribed",
        "unsubscribed",
        "conversation_started",
        "delivered",
        "failed",
        "message",
        "seen"
        ])
    result = requests.post(hook, json.dumps(sen), headers=headers)
    print(result.json())


def set_telegram_webhook(domain: str, token=None) -> None:
    print(domain)
    telegram_url = "https://api.telegram.org/bot%s/%s?url=%s" % (env.get('TELEGRAM_TOKEN'), 'setWebhook', domain)
    result = requests.get(telegram_url)
    print(result)


def static():
    command = f"python manage.py collectstatic"
    os.system(command)


def deploy():
    db_init()
    print("DB init OK")
    db_backup_load()
    print("DB load OK")
    create_admin()
    print("DB create_admin OK")
    static()
    print("Static collection OK")
    run()


if __name__ == "__main__":
    db_backup_load("db2.json")
