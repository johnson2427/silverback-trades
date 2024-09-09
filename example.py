import requests
import time
from collections import deque


def get_eth_spot_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'ethereum',
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    eth_price = response.json()['ethereum']['usd']
    return eth_price


def calculate_moving_average(prices: deque, period: int):
    if len(prices) < period:
        return None
    return sum(prices) / period


prices_200 = deque(maxlen=20)
prices_100 = deque(maxlen=10)


def main():
    while True:
        price = get_eth_spot_price()
        print(f"Latest ETH Price: {price}")

        prices_200.append(price)
        prices_100.append(price)

        ma_200 = calculate_moving_average(prices_200, 20)
        ma_100 = calculate_moving_average(prices_100, 10)

        if ma_200:
            print(f"200-period Moving Average: {ma_200}")

        if ma_100:
            print(f"100-period Moving Average: {ma_100}")

        time.sleep(5)


if __name__ == '__main__':
    main()
