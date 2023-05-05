import json
import requests as requests
from psycopg2 import Error
from cryptocurrency_data import triplets_coins
from db.connection import get_connection, put_connection
from trade.order_data import wait_for_asset_balance, order_prepair

url = 'https://api.binance.com/api/v3/ticker/24hr'
response = requests.get(url)


def get_transaction():
    data = json.loads(response.text)
    transaction_list = []
    for item in data:
        symbol = item['symbol']
        trade_count = float(item['count'])
        point = (trade_count, symbol)
        transaction_list.append(point)

    return add_transaction(transaction_list)


def add_transaction(transaction_list):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.executemany("UPDATE currency_pair SET transaction = %s WHERE symbol = %s", transaction_list)
        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        cursor.close()
        put_connection(connection)


def get_triplets(triplets_coins):
    chain = []
    for symbols in triplets_coins:
        chain.extend(symbols)
        if len(chain) == len(symbols):
            result = query_triplets(chain)
            calculate_triplets(chain, result)
            chain.clear()


def query_triplets(chain):
    db_connection = get_connection()
    cursor = db_connection.cursor()
    try:
        price_pr = "SELECT symbol, price, transaction FROM currency_pair WHERE symbol IN %s"
        cursor.execute(price_pr, (tuple(chain),))
        res_query = cursor.fetchall()
        result = sorted(res_query, key=lambda x: chain.index(x[0]))
        return result

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        cursor.close()
        put_connection(db_connection)


def calculate_triplets(chain, result):
    transaction = result[1][2]
    if transaction > 14000:
        count = wait_for_asset_balance('USDT')

        pr1_size = count / result[0][1]
        pr1_res = pr1_size - pr1_size * 0.001

        pr2_size = pr1_res / result[1][1]
        pr2_res = pr2_size - pr2_size * 0.001

        pr3_size = result[2][1] * pr2_res
        pr3_res = pr3_size - pr3_size * 0.001

        profit_money = pr3_res - count
        profit_percentage = profit_money / count * 100

        if profit_percentage > 0.1:
            operation = order_prepair(chain)
            print(operation)


get_triplets(triplets_coins)
get_transaction()
