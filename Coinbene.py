# 满币
import datetime
import hashlib
import hmac
import json
from  decimal import Decimal
import requests

from Utils import getMd5Str

API_KEY = "472730ae4e03dd604a8bff48893880de"
SECRET = "1ac1249c9d5f48d6bc6837dbb46dcbe1"


BaseUrl = "https://api.coinbene.com/v1/"

import time

current_milli_time = lambda: int(round(time.time() * 1000))


def getSign(cmds):
    m = hmac.new(bytearray(SECRET), digestmod=hashlib.md5)
    m.update(cmds.encode())
    return m.hexdigest()


def getAllTicker(symbol):
    url = "market/ticker?symbol=" + symbol
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh - CN, zh;q = 0.9, en;q = 0.8, zh - TW;q = 0.7',
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    completed_url = BaseUrl + url
    try:
        s = requests.Session()
        r = s.get(completed_url, verify=False, headers=headers)
        if r.status_code == 200:
            res = r.json()
            print(res)
            return res

        else:
            print("error")
            return

    except Exception as e:
        print(str(e))
        print("end")
        return


# 获取挂单
# 交易对
# 获取挂单档位的数量，默认200  1 到 500
def getOrderBook(symbol, depth=200):
    url = "market/orderbook?symbol=" + symbol + "&depth=" + str(depth)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh - CN, zh;q = 0.9, en;q = 0.8, zh - TW;q = 0.7',
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    completed_url = BaseUrl + url
    try:
        s = requests.Session()
        r = s.get(completed_url, verify=False, headers=headers)
        if r.status_code == 200:
            res = r.json()
            print(res)
            return res

        else:
            print("error")
            return

    except Exception as e:
        print(str(e))
        print("end")
        return


# 获取成交记录
# 交易对
# 获取记录数量，按照时间倒序传输。默认300  1 到 2000
def getTradeRecored(symbol, size=300):
    url = "market/trades?symbol=" + symbol + "&size=" + str(size)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh - CN, zh;q = 0.9, en;q = 0.8, zh - TW;q = 0.7',
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    completed_url = BaseUrl + url
    try:
        s = requests.Session()
        r = s.get(completed_url, verify=False, headers=headers)
        if r.status_code == 200:
            res = r.json()
            print(res)
            return res

        else:
            print("error")
            return

    except Exception as e:
        print(str(e))
        print("end")
        return


# 查询账户余额
def getBalance():
    time_stamp = current_milli_time()

    long_time_stamp = time_stamp - (1000 * 60 * 60 * 8)

    origin_str = "ACCOUNT=EXCHANGE&APIID=" + API_KEY.upper() + "&SECRET="+SECRET.upper()+"&TIMESTAMP=" + str(long_time_stamp)
    print(origin_str)
    sign = getMd5Str(origin_str)
    print(sign)

    payload = {
        "apiid": API_KEY,
        "account": "exchange",
        "timestamp": int(long_time_stamp),
        "sign": sign
    }

    url = "trade/balance"

    headers = {

        'Content-Type': 'application/json'

    }
    completed_url = BaseUrl + url
    try:
        s = requests.Session()
        r = s.post(completed_url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            res = r.json()
            if res.get("status") == "ok":
                print(res)
                return res
            else:
                print(float(long_time_stamp) - float(res.get("timestamp")))
                print(res)
                return


        else:
            print(r.text())
            print("error")
            return

    except Exception as e:
        print(str(e))
        print("end")
        return


# 下单
# 交易对 ABTETH
# 交易类型 buy-limit/sell-limit	限价买入 / 限价卖出
# 下单价格
# 下单数量
def doOrder(symbol, type, price, quantity):
    time_stamp = current_milli_time()

    long_time_stamp = time_stamp - (1000 * 60 * 60 * 8)

    origin_str = "APIID=" + API_KEY.upper() + "&PRICE=" + str(price) + "&QUANTITY=" + str(
        quantity) + "&SECRET=" + SECRET.upper() + "&SYMBOL=" + symbol.upper() + "&TIMESTAMP=" + str(
        long_time_stamp) + "&TYPE=" + type.upper()
    print(origin_str)
    sign = getMd5Str(origin_str)

    payload = {
        "apiid": API_KEY,
        "price": float(price),
        "quantity": float(quantity),
        "symbol": symbol,
        "type": type,
        "timestamp": int(long_time_stamp),
        "sign": sign
    }
    print(sign)
    print(payload)

    url = "trade/order/place"

    headers = {

        'Content-Type': 'application/json'

    }
    completed_url = BaseUrl + url
    try:
        s = requests.Session()
        r = s.post(completed_url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            res = r.json()
            if res.get("status") == "ok":
                print(res)
                return res
            else:
                print(float(long_time_stamp) - float(res.get("timestamp")))
                print(res)
                return


        else:
            print(r.text())
            print("error")
            return

    except Exception as e:
        print(str(e))
        print("end")
        return


# 查询委托
def getOrderInfo(orderid):
    time_stamp = current_milli_time()

    long_time_stamp = time_stamp - (1000 * 60 * 60 * 8) + 1200

    origin_str = "APIID=" + API_KEY.upper() + "&ORDERID=" + str(orderid) + "&TIMESTAMP=" + str(long_time_stamp)
    print(origin_str)
    sign = getMd5Str(origin_str)

    payload = {
        "apiid": API_KEY,
        "orderid": str(orderid),
        "timestamp": int(long_time_stamp),
        "sign": sign
    }

    url = "trade/order/info"

    headers = {

        'Content-Type': 'application/json'

    }
    completed_url = BaseUrl + url
    try:
        s = requests.Session()
        r = s.post(completed_url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            res = r.json()
            if res.get("status") == "ok":
                print(res)
                return res
            else:
                print(float(long_time_stamp) - float(res.get("timestamp")))
                print(res)
                return


        else:
            print(r.text())
            print("error")
            return

    except Exception as e:
        print(str(e))
        print("end")
        return


# 撤单
def cancelOrder(orderid):
    time_stamp = current_milli_time()

    long_time_stamp = time_stamp - (1000 * 60 * 60 * 8) + 1200

    origin_str = "APIID=" + API_KEY.upper() + "&ORDERID=" + str(orderid) + "&TIMESTAMP=" + str(long_time_stamp)
    print(origin_str)
    sign = getMd5Str(origin_str)

    payload = {
        "apiid": API_KEY,
        "orderid": str(orderid),
        "timestamp": int(long_time_stamp),
        "sign": sign
    }

    url = "trade/order/cancel"

    headers = {

        'Content-Type': 'application/json'

    }
    completed_url = BaseUrl + url
    try:
        s = requests.Session()
        r = s.post(completed_url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            res = r.json()
            if res.get("status") == "ok":
                print(res)
                return res
            else:
                print(float(long_time_stamp) - float(res.get("timestamp")))
                print(res)
                return


        else:
            print(r.text())
            print("error")
            return

    except Exception as e:
        print(str(e))
        print("end")
        return


# 查询当前委托
def getOpenOrders(symbol):
    time_stamp = current_milli_time()

    long_time_stamp = time_stamp - (1000 * 60 * 60 * 8) + 1200

    origin_str = "APIID=" + API_KEY.upper() + "&SYMBOL=" + symbol.upper() + "&TIMESTAMP=" + str(long_time_stamp)
    print(origin_str)
    sign = getMd5Str(origin_str)

    payload = {
        "apiid": API_KEY,
        "symbol": str(symbol),
        "timestamp": int(long_time_stamp),
        "sign": sign
    }
    print(sign)

    url = "trade/order/open-orders"

    headers = {

        'Content-Type': 'application/json'

    }
    completed_url = BaseUrl + url
    try:
        s = requests.Session()
        r = s.post(completed_url, headers=headers, data=json.dumps(payload))
        if r.status_code == 200:
            res = r.json()
            if res.get("status") == "ok":
                print(res)
                return res
            else:
                print(float(long_time_stamp) - float(res.get("timestamp")))
                print(res)
                return


        else:
            print(r.text())
            print("error")
            return

    except Exception as e:
        print(str(e))
        print("end")
        return

getAllTicker("all")

doOrder("btcusdt", "buy-limit",10000.00, 100.00)

getOrderBook(symbol="ABTETH",depth=300)
getTradeRecored(symbol="ABTETH",size=300)

getBalance()


