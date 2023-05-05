import time
from binance import Client

from env import API_KEY, API_SECRET
from trade.trade_order import create_quoted_order, create_base_order

api_key = API_KEY
api_secret = API_SECRET

client = Client(api_key, api_secret)


def wait_for_asset_balance(asset):
    while True:
        balance = client.get_asset_balance(asset=asset)
        if float(balance['free']) > 0:
            break
        time.sleep(2)
    return float(balance['free'])


def order_prepair(chain):
    fst_symbol, sec_symbol, thd_symbol = chain[0], chain[1], chain[2]

    balance = wait_for_asset_balance('USDT')
    op1_trade, base_asset, quote_asset = create_quoted_order(fst_symbol, 'BUY', str(balance))

    quantity = wait_for_asset_balance(str(base_asset))
    op2_trade, base_asset, quote_asset = create_quoted_order(sec_symbol, 'BUY', str(quantity))

    quantity2 = wait_for_asset_balance(str(base_asset))

    op3_trade = create_base_order(thd_symbol, 'SELL', str(quantity2))
    print(op3_trade)
    balance_pf = wait_for_asset_balance('USDT')
    return balance_pf
