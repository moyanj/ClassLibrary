import hashlib
import json
from urllib.parse import quote

import requests as rep


def rjson(path):
    f = open(path, encoding='UTF-8')
    return json.load(f)


def json_text_analysis(data):
    return json.loads(data)


def rfile(path):
    f = open(path, encoding='UTF-8')
    return f.read()


def get_net_md5(data):
    chinese = quote(data, 'utf-8')
    temp = rep.get("https://v.api.aa1.cn/api/api-md5/go.php?act=%E5%8A%A0%E5%AF%86&md5={}".format(chinese))
    temp1 = temp.text
    md5 = temp1.split(":")[1]
    return md5


def get_md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()
