from decimal import Decimal
from trade.order_data import client


def create_quoted_order(symbol, side, quoteOrderQty):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quoteOrderQty=quoteOrderQty
        )

        symbol_info = client.get_symbol_info(symbol)
        base_asset = symbol_info['baseAsset']

        quantity_filled = Decimal(order['executedQty'])

    except Exception as e:
        print(f'Ошибка {e}')
        quantity_filled = Decimal('0')
        base_asset = 'UNKNOWN'

    return quantity_filled, base_asset


def create_base_order(symbol, side, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )

        quantity_filled = Decimal(order['executedQty'])

    except Exception as e:
        print(f'Ошибка {e}')
        quantity_filled = Decimal('0')

    return quantity_filled
