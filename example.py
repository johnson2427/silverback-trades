import websocket
import json

from collections import deque
from datetime import datetime


prices_50 = deque(maxlen=50)


def calculate_time_weighted_moving_average(prices):
    if len(prices) < 2:
        return None

    total_weighted_price = 0
    total_time_delta = 0

    for i in range(1, len(prices)):
        price_i, time_i = prices[i]
        price_prev, time_prev = prices[i - 1]

        # Time difference (in seconds) between the two prices
        time_diff = (time_i - time_prev).total_seconds()

        # Area under the curve for each step
        total_weighted_price += ((price_prev + price_i) / 2) * (time_diff) 

        # Total time passed between points
        total_time_delta += time_diff

    return total_weighted_price / total_time_delta


# WebSocket message handler
def on_message(ws, message):
    current_time = datetime.now()
    data = json.loads(message)

    # Check if the message contains ticker data (ignore system messages like subscription status)
    if isinstance(data, list) and len(data) > 1:
        # Kraken sends ticker data as the second item in the list
        ticker_data = data[1]

        # Extract the current price from the 'c' key (last trade price)
        eth_price = ticker_data.get('c', [None])[0]  # 'c' is the last trade price
        if eth_price:
            eth_price = float(eth_price)
            print(f"Real-time ETH price: ${eth_price:.2f} at {current_time}")

            # Add the price to the deque for 50 MA calculation
            prices_50.append((eth_price, current_time))

            # Calculate the 50-period moving average
            ma_50 = calculate_time_weighted_moving_average(prices_50)

            # Print the 50-period moving average if there are enough prices
            if ma_50:
                print(f"50-period Moving Average: ${ma_50:.2f}")


# On connection opened
def on_open(ws):
    print("Connection opened")
    
    # Subscribe to the ETH/USD ticker channel
    subscribe_message = {
        "event": "subscribe",
        "pair": ["ETH/USD"],
        "subscription": {
            "name": "ticker"
        }
    }
    ws.send(json.dumps(subscribe_message))


# On connection closed
def on_close(ws):
    print("Connection closed")


# On error
def on_error(ws, error):
    print(f"Error occurred: {error}")

def main():
    # Kraken WebSocket URL
    websocket_url = "wss://ws.kraken.com/"
    
    # Create WebSocket connection
    ws = websocket.WebSocketApp(
        websocket_url,
        on_message=on_message,
        on_open=on_open,
        on_close=on_close,
        on_error=on_error,
    )
    
    # Run WebSocket forever to listen for messages
    ws.run_forever()

if __name__ == '__main__':
    main()
