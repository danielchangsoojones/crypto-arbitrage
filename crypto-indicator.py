from bittrex import Bittrex
import time
import json
import requests
from coinbase.wallet.client import Client
import gdax
import matplotlib.pyplot as plt
#import term



t = 720 #number of times to record the rates (right now 12 hours)
loop = 60 #number of seconds per loop (1 min right now)

lines = []
bt = []
cb = []
c = 0
for n in range(t):
    #This is the main loop for the program that determines the number of times it is run
    
    
    #BITTREX
    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)
    history = my_bittrex.get_market_history('ETH-LTC', 5)
    sum = 0
    count = 0
    #print(history['result'][0]['TimeStamp'])
    for trans in range(5):
        sum += history['result'][trans]['Price']
        count += 1    
    price_bittrex = sum/count
    #Gets the last 5 transactions and averages them to get a good indication of price
    
    #COINBASE
    response_LTC = requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot')
    response_ETH = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
    price_coinbase = float(response_LTC.json()['data']['amount'])/float(response_ETH.json()['data']['amount'])
    
    bt.append(price_bittrex)
    cb.append(price_coinbase)
    
    print('\n')
    print('minutes:', c)
    print('CB', price_coinbase)
    print('BT', price_bittrex)
    time.sleep(loop) #Duration between calculation loops
    c += 1
    

lines.append(plt.plot(list(range(len(bt))), bt))
lines.append(plt.plot(list(range(len(cb))), cb))
plt.xlabel('Time')
plt.ylabel('Conversion Rate')
plt.draw()
plt.show()
    
