import json
import time
import websocket
from psycopg2 import Error
from db.connection import get_connection, put_connection


def on_close(ws, close_status_code, close_msg):
    print("Соединение закрыто")


def on_open(ws):
    print("Соединение открыто")


def main(ws, msg):
    time_start = time.time()
    tickers = json.loads(msg)
    rows = []

    for ticker in tickers:
        symbol = str(ticker['s'])
        price = float(ticker['c'])
        row = (price, symbol)
        rows.append(row)

    if len(rows) == len(tickers):
        query = put_data(rows)
        rows.clear()
        print(f"Обновлено {query} пар, Время: {round(time.time() - time_start, 3)} сек")


def put_data(rows):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.executemany("UPDATE currency_pair SET price = %s WHERE symbol = %s", rows)
        connection.commit()
        return len(rows)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        cursor.close()
        put_connection(connection)


if __name__ == "__main__":
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/!ticker@arr",
                                on_open=on_open,
                                on_message=main,
                                on_close=on_close)
    ws.run_forever()
