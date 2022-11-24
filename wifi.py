import sys
import json
import time
import urllib3
import datetime

from core import login
from utils import get_user_info, test_connect

urllib3.disable_warnings()

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.loads(file.read())


def do_login() -> bool:
    if test_connect():
        print(str(datetime.datetime.now()) + ': already login')
        return True
    username, password = get_user_info()
    for i in range(config['run']['retry']):
        login_info = login(username, password)
        stat = login_info.get('suc_msg') is not None and login_info['suc_msg'] == 'login_ok'
        if stat:
            print(str(datetime.datetime.now()) + ': login successfully')
            return True
        else:
            print(str(datetime.datetime.now()) + ': login retrying')
            time.sleep(1)
    print(str(datetime.datetime.now()) + ': login failed')
    return False


def keep_login() -> None:
    while True:
        if not do_login():
            print(str(datetime.datetime.now()) + ': keep login failed')
        time.sleep(config['run']['interval'])


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'login':
        print(do_login())
        exit(0)
    if len(sys.argv) == 2 and sys.argv[1] == 'test':
        print(test_connect())
        exit(0)
    if len(sys.argv) == 2 and sys.argv[1] == 'keep':
        keep_login()
        exit(0)
    print('usage:')
    print('\tpython wifi.py login: ' + ' ' * 4 + 'login BUAA-WiFi')
    print('\tpython wifi.py test: ' + ' ' * 5 + 'test BUAA-WiFi connection')
    print('\tpython wifi.py keep: ' + ' ' * 5 + 'keep BUAA-WiFi connected')
