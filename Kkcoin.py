import time
import json
import requests
from collections import OrderedDict

from OpenSSL.crypto import load_privatekey, FILETYPE_PEM, sign
from base64 import b64encode, b64decode

BASE_URL = 'https://api.kkcoin.com'


class KK_REST:

    def __init__(self, api_key, api_secret, password):
        self.api_key = api_key
        self.api_secret = api_secret
        self.password = password.encode()

    def sign(self, payload):
        private_key = load_privatekey(FILETYPE_PEM, self.api_secret, self.password)

        signature = sign(private_key, payload, 'sha256')

        return b64encode(signature).decode()

    def trade(self, symbol, order_type, order_op, price, amount):
        path = '/rest/trade'
        request_url = BASE_URL + path

        payload = OrderedDict([
            ('amount', str(amount)),
            ('orderop', order_op),
            ('ordertype', order_type),
            ('price', str(price)),
            ('symbol', symbol)])

        nonce = str(int(time.time()))
        sigPayload = 'trade' + json.dumps(payload, separators=(',', ':')) + nonce
        signature = self.sign(sigPayload)
        print(sigPayload)
        print(signature)

        return requests.post(
            request_url,
            headers={
                'KKCOINAPIKEY': self.api_key,
                'KKCOINSIGN': signature,
                'KKCOINTIMESTAMP': nonce
            },
            data=payload
        ).json()

    def balance(self):
        path = '/rest/balance'
        request_url = BASE_URL + path

        payload = []

        nonce = str(int(time.time()))
        sigPayload = 'balance' + json.dumps(payload) + nonce
        signature = self.sign(sigPayload)
        print(sigPayload)
        print(signature)

        return requests.get(
            request_url,
            headers={
                'KKCOINAPIKEY': self.api_key,
                'KKCOINSIGN': signature,
                'KKCOINTIMESTAMP': nonce
            }
        ).json()

    def openorders(self, symbol):
        path = '/rest/openorders'
        request_url = BASE_URL + path

        payload = OrderedDict([
            ('symbol', symbol)])

        nonce = str(int(time.time()))
        sigPayload = 'openorders' + json.dumps(payload, separators=(',', ':')) + nonce
        signature = self.sign(sigPayload)

        return requests.get(
            request_url,
            headers={
                'KKCOINAPIKEY': self.api_key,
                'KKCOINSIGN': signature,
                'KKCOINTIMESTAMP': nonce
            },
            params=payload
        ).json()

    def cancelorder(self, order_num):
        path = '/rest/cancel'
        request_url = BASE_URL + path

        payload = OrderedDict([
            ('id', str(order_num))
        ])

        nonce = str(int(time.time()))
        sigPayload = 'trade' + json.dumps(payload, separators=(',', ':')) + nonce
        signature = self.sign(sigPayload)
        print(sigPayload)
        print(signature)

        return requests.post(
            request_url,
            headers={
                'KKCOINAPIKEY': self.api_key,
                'KKCOINSIGN': signature,
                'KKCOINTIMESTAMP': nonce
            },
            data=payload
        ).json()


# 此处需要计算机生成密钥 具体步骤参见 https://github.com/KKCoinEx/api-wiki/wiki/Auth-D1.-generate-key-pair
# 运行时需要把 api_key，api_secret，password 替换
api_key = 'f5b40efb2b35305b4ac821e1ce8247e1'
api_secret = open('/Users/simahu/Project/Janlent/newNET/ssh/private.pem').read()

password = '111111'  # RSA private key password

kk_rest = KK_REST(api_key, api_secret, password)

symbol = 'KK_ETH'
order_type = 'LIMIT'
order_op = 'BUY'
price = 0.001
amount = 1000

result = kk_rest.trade(symbol, order_type, order_op, price, amount)
print("trade res : ")
print(result)

result = kk_rest.balance()
print("balance res : ")
print(result)

cancel_res = kk_rest.cancelorder(1245)
print("cancelorder res : ")
print(cancel_res)

openorders_res = kk_rest.openorders(symbol=symbol)
print("openorders_res res : ")
print(openorders_res)
