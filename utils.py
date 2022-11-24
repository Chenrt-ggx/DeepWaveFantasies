import json
import socket
import base64
import requests

from urllib.parse import urlparse, parse_qs

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.loads(file.read())


def get_user_info() -> (str, str):
    def decode(text: str) -> str:
        return base64.b64decode(text.encode()).decode()

    try:
        '''
        auth.json：
            共计两个字段
            username 为用户名的 base64 编码结果
            password 为用户密码的 base64 编码结果
        '''
        with open('auth.json', 'r', encoding='utf-8') as auth:
            content = json.loads(auth.read())
            username, password = content.get('username'), content.get('password')
        return decode(username), decode(password)
    except IOError:
        print('error: auth file failed to open')
        exit(1)
    except AttributeError:
        print('error: username or password not exist')
        exit(1)
    except json.decoder.JSONDecodeError:
        print('error: json file failed to parse')
        exit(1)


def get_info_str(username: str, password: str, ip: str, acid: int) -> str:
    return json.dumps({
        'username': username,
        'password': password,
        'ip': ip,
        'acid': acid,
        'enc_ver': config['request']['ver']
    })


def get_ip() -> str:
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.connect(('8.8.8.8', 80))
    return soc.getsockname()[0]


def get_acid() -> int:
    try:
        request = requests.get('https://gw.buaa.edu.cn', verify=False)
        param = parse_qs(urlparse(request.url).query)
        if param.get('ac_id') is not None and len(param['ac_id']) == 1:
            return int(param['ac_id'][0])
    except ValueError:
        pass
    return 1


def test_connect() -> bool:
    try:
        requests.get('https://www.baidu.com')
        return True
    except OSError:
        pass
    return False
