import requests


def get_eth_spot_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'ethereum',
        'vs_currencies': 'usd'
    }
    response = requests.get(url, params=params)
    eth_price = response.json()['ethereum']['usd']
    return eth_price


def main():
    eth_price = get_eth_spot_price()
    print(f"The current spot price of ETH is {eth_price}")


if __name__ == '__main__':
    main()
