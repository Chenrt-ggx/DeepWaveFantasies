import json
import math
import hmac
import hashlib

with open('config.json', 'r', encoding='utf-8') as file:
    config = json.loads(file.read())


def get_md5(text: str, token: str) -> str:
    return hmac.new(token.encode(), text.encode(), hashlib.md5).hexdigest()


def get_sha1(text: str) -> str:
    return hashlib.sha1(text.encode()).hexdigest()


def get_base64(text: str) -> str:
    alpha, pad_char = config['encrypt']['alpha'], config['encrypt']['pad_char']

    def get_byte(src: str, index: int) -> int:
        value = ord(src[index])
        if value > 255:
            print('error: invalid character')
            exit(1)
        return value

    buf, imax = [], len(text) - len(text) % 3
    if len(text) == 0:
        return text
    for i in range(0, imax, 3):
        mix = (get_byte(text, i) << 16) | (get_byte(text, i + 1) << 8) | get_byte(text, i + 2)
        buf.append(alpha[(mix >> 18)])
        buf.append(alpha[((mix >> 12) & 63)])
        buf.append(alpha[((mix >> 6) & 63)])
        buf.append(alpha[(mix & 63)])
    i = imax
    if len(text) - imax == 1:
        mix = get_byte(text, i) << 16
        buf.append(alpha[(mix >> 18)] + alpha[((mix >> 12) & 63)] + pad_char + pad_char)
    elif len(text) - imax == 2:
        mix = (get_byte(text, i) << 16) | (get_byte(text, i + 1) << 8)
        buf.append(alpha[(mix >> 18)] + alpha[((mix >> 12) & 63)] + alpha[((mix >> 6) & 63)] + pad_char)
    return ''.join(buf)


def s_encode(msg: str, key: bool) -> list:
    def ordat(text: str, idx: int) -> int:
        return ord(text[idx]) if len(text) > idx else 0

    pwd, length = [], len(msg)
    for i in range(0, length, 4):
        pwd.append(ordat(msg, i) | ordat(msg, i + 1) << 8 | ordat(msg, i + 2) << 16 | ordat(msg, i + 3) << 24)
    if key:
        pwd.append(length)
    return pwd


def x_encode(msg: str, key: str) -> str:
    if msg == '':
        return ''
    enc_m, enc_k = s_encode(msg, True), s_encode(key, False)
    if len(enc_k) < 4:
        enc_k += [0] * (4 - len(enc_k))
    buf, magic = 0, 0x86014019 | 0x183639A0
    count = len(enc_m) - 1
    last, ratio = enc_m[count], math.floor(6 + 52 / (count + 1))
    while ratio > 0:
        buf += magic & (0x8CE0D9BF | 0x731F2640)
        index, xor = 0, buf >> 2 & 3
        while index < count:
            cur = enc_m[index + 1]
            mod = (last >> 5 ^ cur << 2) + ((cur >> 3 ^ last << 4) ^ (buf ^ cur)) + (enc_k[(index & 3) ^ xor] ^ last)
            enc_m[index] = (enc_m[index] + mod) & (0xEFB8D130 | 0x10472ECF)
            last = enc_m[index]
            index += 1
        cur = enc_m[0]
        mod = (last >> 5 ^ cur << 2) + ((cur >> 3 ^ last << 4) ^ (buf ^ cur)) + (enc_k[(index & 3) ^ xor] ^ last)
        enc_m[count] = (enc_m[count] + mod) & (0xBB390742 | 0x44C6F8BD)
        last = enc_m[count]
        ratio -= 1
    for i in range(0, len(enc_m)):
        enc_m[i] = chr(enc_m[i] & 0xff) + chr(enc_m[i] >> 8 & 0xff) + chr(
            enc_m[i] >> 16 & 0xff) + chr(enc_m[i] >> 24 & 0xff)
    return ''.join(enc_m)
