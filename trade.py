# Importing the API and instantiating the REST client according to our keys
from alpaca.trading.client import TradingClient
import json
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import time

# JSON file
f = open ('config.json', "r")
  
# Reading from file
keys = json.loads(f.read())

API_KEY = keys["API_KEY"]
SECRET_KEY = keys["Secret"]

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

# Getting account information and printing it
account = trading_client.get_account()
for property_name, value in account:
  print(f"\"{property_name}\": {value}")


# Setting parameters for our buy order

print("###########################")
while (True):
    positions = trading_client.get_all_positions()
    for position in positions:
        if position.symbol == 'BTCUSD':
            curr = round(float(position.current_price),3)
            avg = round(float(position.avg_entry_price), 3)
            diff = round(curr/avg, 5)
            if curr > avg*1.05:
                market_order_data = MarketOrderRequest(
                      symbol="BTC/USD",
                      qty=0.001,
                      side=OrderSide.SELL,
                      time_in_force=TimeInForce.GTC
                )
                market_order = trading_client.submit_order(market_order_data)
                print("Status: SOLD US${} to BTCUSD@{} | AVG: {} | DIFF: {}".format(0.001*curr , curr , avg, diff))

            elif curr < avg*0.95:
                market_order_data = MarketOrderRequest(
                      symbol="BTC/USD",
                      qty=0.001,
                      side=OrderSide.BUY,
                      time_in_force=TimeInForce.GTC
                )
                market_order = trading_client.submit_order(market_order_data)
                print("Status: BUY US${} to BTCUSD@{} | AVG: {} | DIFF: {}".format(0.001*curr , curr , avg, diff))
            else:
                print("Status: No Actions | BTCUSD@{} | AVG: {} | DIFF: {} ".format(curr, avg, diff))
    time.sleep(60)
