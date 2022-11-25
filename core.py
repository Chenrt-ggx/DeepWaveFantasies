import time
import json
import random
import requests

from utils import get_info_str, get_acid_cookies, get_ip
from crypto import get_md5, get_sha1, get_base64, x_encode

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.loads(file.read())


def do_request(url: str, params: dict, times: int, cookies: dict) -> dict:
    callback = config['request']['jquery'] + '_' + str(times)
    proxies = None if not config['proxies']['enable'] else {
        'http': config['proxies']['http'],
        'https': config['proxies']['https']
    }
    resp = requests.get(url, params={'callback': callback, **params}, headers={
        'User-Agent': config['request']['ua']
    }, verify=False, cookies=cookies, proxies=proxies)
    return json.loads(resp.text[len(callback) + 1: -1])


def get_ip_token(username: str, cookies: dict) -> (str, str):
    times = int(time.time() * 1000)
    res = do_request('https://gw.buaa.edu.cn/cgi-bin/get_challenge', {
        'username': username,
        'ip': get_ip(),
        '_': times
    }, times - random.randint(1, 5), cookies)
    return res['client_ip'], res['challenge']


def get_login_info(token: str, username: str, hmd5: str, acid: int, ip: str, info: str,
                   n: int or str, kind: int or str, cookies: dict) -> dict:
    times = int(time.time() * 1000)
    chkstr = token + username + token + hmd5 + token + str(acid) + token + ip
    chkstr += token + str(n) + token + str(kind) + token + '{SRBX1}' + info
    return do_request('https://gw.buaa.edu.cn/cgi-bin/srun_portal', {
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': acid,
        'ip': ip,
        'chksum': get_sha1(chkstr),
        'info': '{SRBX1}' + info,
        'n': n,
        'type': kind,
        'os': config['misc']['os'],
        'name': config['misc']['name'],
        'double_stack': '0',
        '_': times
    }, times - random.randint(1, 5), cookies)


def login(username: str, password: str) -> dict:
    acid, cookies = get_acid_cookies()
    ip, token = get_ip_token(username, cookies)
    info, hmd5 = get_info_str(username, password, ip, acid), get_md5(password, token)
    n, kind = config['misc']['n'], config['misc']['type']
    return get_login_info(token, username, hmd5, acid, ip, get_base64(x_encode(info, token)), n, kind, cookies)
