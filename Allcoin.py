import hashlib

import requests

key = "e94da6c19fa648b29cae9584767fdd67406f82e24c99ddc38ad68a906ae214f6"
secret = "5b0f-c3e02-27a61-2148-4865"


# 用户余额信息
def getBalance():
    url = "https://www.allcoin.com/Api_User/userBalance"
    payload = {
        "api_key": key,
        "sign": getMd5Str("api_key=" + key + "&secret_key=" + secret)
    }
    r = doPost(url=url, payload=payload)
    if r:
        if r.get("code") == 0:
            print(r.get("data"))
            return r.get("data")
        else:
            print("getCoinTrade error")
            print(r.get("msg"))
            return

    else:
        print("getCoinTrade error")


# 下单
# 币种比如 btc2ckusd , ltc2btc ,mcc2cnet(注意:数字2前面代表币名，2后面是币对应的交易区)
# 买卖类型 (buy sale)
# 价格
# 数量
def doOrder(symbol, type, price, number):
    url = "https://www.allcoin.com/Api_Order/coinTrust"
    # sign = "api_key=xxx&number=xxx&price=xxx&symbol=xxx&type=xxx&secret_key=你的私钥"
    sign_str = "api_key=" + key + "&number=" + str(number) + "&price=" + str(
        price) + "&symbol=" + symbol + "&type=" + type + "&secret_key=" + secret

    sign = getMd5Str(sign_str)
    payload = {
        "api_key": key,
        "symbol": symbol,
        "type": type,
        "price": price,
        "number": number,
        "sign": sign,
    }
    r = doPost(url=url, payload=payload)
    if r:
        if r.get("code") == 0:
            print(r.get("order_id"))
            return r.get("order_id")
        else:
            print("doOrder error")
            print(r.get("msg"))
            return

    else:
        print("doOrder error")
        return

# 撤销挂单
# 币种比如 btc2ckusd , ltc2btc ,mcc2cnet(注意:数字2前面代表币名，2后面是币对应的交易区)
# 订单ID
def cancel_order(symbol, order_id):
    url = "https://www.allcoin.com/Api_Order/cancel"

    # sign = md5('api_key=xxx&order_id=xxx&symbol=xxx&secret_key=你的私钥'))
    sign_origin = "api_key=" + key + "&order_id=" + str(order_id) + "&symbol=" + symbol + "&secret_key=" + secret
    sign = getMd5Str(sign_origin)

    payload = {
        "api_key": key,
        "symbol": symbol,
        "order_id": order_id,
        "sign": sign,
    }

    r = doPost(url=url, payload=payload)
    if r:
        if r.get("code") == 0:
            print(r.get("data"))
            return r.get("data")
        else:
            print("cancel order error")
            print(r.get("msg"))
            return

    else:
        print("cancel order error")


# 获取委托单信息
# 币种比如 btc2ckusd , ltc2btc ,mcc2cnet(注意:数字2前面代表币名，2后面是币对应的交易区)
# 委托单id
def getOrderInfo(symbol, trust_id):
    url = "https://www.allcoin.com/Api_Order/orderInfo"
    # sign = md5('api_key=xxx&symbol=btc2ckusd&trust_id=123&secret_key=你的私钥'))
    sign_origin = "api_key=" + key + "&symbol=" + symbol + "&trust_id=" + str(trust_id) + "&secret_key=" + secret
    sign = getMd5Str(sign_origin)

    payload = {
        "api_key": key,
        "symbol": symbol,
        "trust_id": trust_id,
        "sign": sign,
    }

    r = doPost(url=url, payload=payload)
    if r:
        if r.get("code") == 0:
            print(r.get("data"))
            return r.get("data")
        else:
            print("getOrderInfo error")
            print(r.get("msg"))
            return

    else:
        print("getOrderInfo error")


# 获取市场深度信息
# 币种比如 btc2ckusd , ltc2btc ,mcc2cnet(注意:数字2前面代表币名，2后面是币对应的交易区
def getDepth(symbol):
    url = "https://www.allcoin.com/Api_Order/depth"

    payload = {
        "symbol": symbol,
    }

    r = doPost(url=url, payload=payload)
    if r:
        if r.get("code") == 0:
            print(r.get("data"))
            return r.get("data")
        else:
            print("getDepth error")
            print(r.get("msg"))
            return

    else:
        print("getDepth error")


#

# 获取所有币种价格列表
def getPriceList():
    url = "https://www.allcoin.com/Api_Market/getPriceList"
    r = doGet(url)
    if r:
        print(r)
        return r
    else:
        print("get price list error")


# 获取币种交易行情,
# 参数：交易区，币名（全部小写）
def getCoinTrade(part, coin):
    payload = {
        "part": part,
        "coin": coin
    }
    url = "https://www.allcoin.com/Api_Market/getCoinTrade"
    r = doPost(url=url, payload=payload)
    if r:
        print(r)
        return r

    else:
        print("getCoinTrade error")


# get
def doGet(url):
    try:
        r = requests.get(url)
        try:
            return r.json()

        except Exception as e:
            print(e)
            return

    except Exception as e:
        print(e)
        return


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


# md5 加密
def getMd5Str(origin_str):
    # 创建md5对象
    hl = hashlib.md5()
    # 此处必须声明encode
    # 若写法为hl.update(str)  报错为： Unicode-objects must be encoded before hashing
    hl.update(origin_str.encode(encoding='utf-8'))
    return hl.hexdigest()


getDepth(symbol="eth2btc")
getBalance()
