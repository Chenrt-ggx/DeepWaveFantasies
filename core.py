import time
import json
import requests

from utils import get_info_str, get_acid, get_ip
from crypto import get_md5, get_sha1, get_base64, x_encode

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.loads(file.read())


def do_request(url: str, params: dict, times: int) -> dict:
    callback = config['request']['jquery'] + '_' + str(times)
    resp = requests.get(url, params={'callback': callback, **params}, headers={
        'User-Agent': config['request']['ua']
    }, verify=False)
    return json.loads(resp.text[len(callback) + 1: -1])


def get_ip_token(username: str) -> (str, str):
    times = int(time.time() * 1000)
    res = do_request('https://gw.buaa.edu.cn/cgi-bin/get_challenge', {
        'username': username,
        'ip': get_ip(),
        '_': times
    }, times - 2)
    return res['client_ip'], res['challenge']


def login(username: str, password: str) -> dict:
    acid = get_acid()
    ip, token = get_ip_token(username)
    info, hmd5 = get_info_str(username, password, ip, acid), get_md5(password, token)
    info = get_base64(x_encode(info, token))
    times = int(time.time() * 1000)
    chkstr = token + username + token + hmd5 + token + str(acid) + token + ip
    chkstr += token + str(config['misc']['n']) + token + str(config['misc']['type']) + token + '{SRBX1}' + info
    return do_request('https://gw.buaa.edu.cn/cgi-bin/srun_portal', {
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': acid,
        'ip': ip,
        'chksum': get_sha1(chkstr),
        'info': '{SRBX1}' + info,
        'n': config['misc']['n'],
        'type': config['misc']['type'],
        'os': config['misc']['os'],
        'name': config['misc']['name'],
        'double_stack': '0',
        '_': times
    }, times - 2)
