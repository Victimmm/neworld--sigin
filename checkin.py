"""
@File : checkin.py
@Author : Liaoweiming
@Date : 2024/6/1 0:20
"""
import requests
import re
import json
import os


def check_in(cookies):
    check_in_url = "https://neworld.cloud/user/checkin"
    check_headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Content-Length": "0",
        "Cookie": cookies,
        "Origin": "https://neworld.cloud",
        "Priority": "u=1, i",
        "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    response_checkin = requests.post(check_in_url, headers=check_headers, verify=False)
    #打印utf8的返回值
    print(json.loads(response_checkin.content.decode('utf-8'))['msg'])
    # print(response_checkin.text)


def login(user, password):
    url = 'https://neworld.cloud/auth/login'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': '_pk_id.1.86b2=9c41cc0eac5d13af.1684203936.; intercom-id-sh7mjuq3=b559e5c3-1f87-4f32-92a4-ea64a84c82ef; intercom-device-id-sh7mjuq3=88077d2f-4636-4e2e-8317-c2be2ca5e4dc; intercom-session-sh7mjuq3=',
        'Origin': 'https://neworld.cloud',
        'Referer': 'https://neworld.cloud/auth/login',
        'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }


    data = {
        'code': '',
        'email': user,
        'passwd': password,
        'fingerprint': '28a6103abe67ae368d0be9b612fc72db'
    }

    response = requests.post(url, headers=headers, data=data, verify=False)
    # 将Set-Cookie头拆分为单个cookie条目
    entries = response.headers.get('Set-Cookie')
    keys_to_extract = ["uid", "key", "email", "expire_in", "ip", "ip_hash"]

    # 创建一个正则表达式模板，匹配每个目标键值对
    cookie_pattern = r'(?P<key>' + '|'.join(keys_to_extract) + r')=([^;]+)'

    # 使用正则表达式查找所有匹配的键值对
    matches = re.findall(cookie_pattern, entries)
    # 将匹配的结果转换成字典
    cookie_dict = {key: value.strip() for key, value in matches}

    return cookie_dict



# 环境变量中读取数据，包含账号密码，和登陆页面测试
user = os.environ["USERNAME"]
password = os.environ["PASSWORD"]


add_cookies = {"intercom-device-id-sh7mjuq3": "88077d2f-4636-4e2e-8317-c2be2ca5e4dc", "intercom-id-sh7mjuq3": "b559e5c3-1f87-4f32-92a4-ea64a84c82ef", "_pk_id.1.86b2": "9c41cc0eac5d13af.1684203936."}
cookies = login(user, password)
cookies.update(add_cookies)
result = "; ".join([f"{key}={value}" for key, value in cookies.items()])
check_in(result)
