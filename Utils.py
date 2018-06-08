# 设置处理后正确的返回值
import hashlib

import requests


def set_correct_result(data):
    return {'status': 1, 'data': data}


# 设置处理后不正确的返回值
def set_error_result(data):
    return {'status': 0, 'data': data}


# md5 加密
def getMd5Str(origin_str):
    # 创建md5对象
    hl = hashlib.md5()
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(origin_str.encode(encoding='utf-8'))
    return hl.hexdigest()


# post
def doPost(url, payload):
    try:
        r = requests.post(url=url, data=payload)
        try:
            print(r.json())
            return r.json()

        except Exception as e:
            print(e)
            return

    except Exception as e:
        print(e)
        return
