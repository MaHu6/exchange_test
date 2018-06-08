import ccxt

from Utils import set_correct_result, set_error_result

api = {
    "apiKey": "218b48f89f32f121937a8a749ce15f47",
    "secret": "H0Li10A6L3eSiB4RhORNQyNldVGbvYmSZYMORKTFBx9UNB3ifXRJXhJlmcoUXsMt"
}

bitz = ccxt.bitz(api)


# 查询所有币种余额
def query_balance(ccxt_client):
    try:
        fetch_balances = ccxt_client.fetch_balance()
        info = fetch_balances.get("info")

        all_balances = info.get("data")

        return all_balances
    except Exception as e:
        print("Query balance error :" + str(e))
        return


# 根据币种查询账户余额
def query_balance_by_symbol(symbol, ccxt_client):
    try:
        fetch_balances = ccxt_client.fetch_balance()
        info = fetch_balances.get("info")

        all_balances = info.get("data")
        if all_balances.get(symbol):
            return float(all_balances.get(symbol))

        return
    except Exception as e:
        print("Query balance error :" + str(e))
        return


# 下单
# 交易对
# 交易类型
# 交易方向
# 价格
# 数量
# ccxt
def do_order(trade_pair, trade_type, trade_side, price, amount, ccxt_client):
    try:
        if trade_type == "limit":
            if trade_side == "buy":
                order_res = ccxt_client.create_limit_buy_order(trade_pair, amount, price)
            else:
                order_res = ccxt_client.create_limit_sell_order(trade_pair, amount, price)

        else:
            if trade_side == "buy":
                order_res = ccxt_client.create_market_buy_order(trade_pair, amount, price)
            else:
                order_res = ccxt_client.create_market_sell_order(trade_pair, amount, price)

        print(order_res)
        return set_correct_result(order_res)

    except Exception as e:
        print("do_order,trade_pair:" + str(trade_pair) + " trade_side:" + str(trade_side) + " price:" + str(
            price) + " amount:" + str(amount) + " error:" + str(e))

        return set_error_result(str(e))


# 计算手续费
# 交易对
# 交易类型
# 交易方向
# 数量
# 价格
# ccxt
def calculate_fee(symbol, type, side, amount, price, ccxt_client):
    try:
        fee = ccxt_client.calculate_fee(symbol=symbol, type=type, side=side, amount=amount, price=price)

        print("fee:" + str(fee))

        return fee

    except Exception as e:

        print("fee error:" + str(e))
        return


# 查询订单状态
# 交易对
# 订单id
# ccxt
def query_order_by_id(symbol, order_id, ccxt_client):
    try:
        order = ccxt_client.fetch_order(symbol=symbol, id=order_id)

        return order

    except Exception as e:
        print("query order:" + str(order_id) + "status error:" + str(e))
        return


# 根据 订单号撤销订单
# 交易对
# 订单id
# ccxt
def cancel_order_by_num(symbol, order_num, ccxt_client):
    try:

        cancel_res = ccxt_client.cancel_order(id=order_num, symbol=symbol)

        # 撤单成功
        # 查询订单状态，
        order_res = query_order_by_id(symbol=symbol, order_id=cancel_res.get("orderId"), ccxt_client=ccxt_client)
        if order_res:
            status = order_res.get("status")
            if status == "canceled":
                # 撤单成功
                print("cancel order " + order_num + " succeed")

            else:
                # 撤单失败
                print("cancel " + order_num + " failed")

        return

    except Exception as e:
        print("cancel order " + order_num + " exception:" + str(e))
        return


# 根据交易对获取最少数量，价格，成本
# 交易对
# ccxt
def get_limit_info_by_pair(pair, ccxt_client):
    try:

        pair_market_info = ccxt_client.market(pair)
        limit_info = pair_market_info.get("limits")

        return limit_info

    except Exception as e:
        print(e)
        app.logger.debug("get_limit_info_by_pair: " + str(pair) + str(e))
        return


bitz.load_markets()

print(bitz.fetch_markets())
print(query_balance(ccxt_client=bitz))
print(query_balance_by_symbol(symbol="btc", ccxt_client=bitz))
