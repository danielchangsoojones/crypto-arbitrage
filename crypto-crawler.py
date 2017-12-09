from bittrex import Bittrex
import time
import json
import requests
from coinbase.wallet.client import Client
import gdax
#import term


#STARTING HOLDINGS TO SIMULATE
holdings = {'ETH': 1}
confirming = []
graph = []


def buyLTC(quant, price):
    change = quant*(price + price*0.0025)
    holdings['ETH'] = holdings['ETH'] - change
    confirming.append({'type': 'LTC', 'amount': quant, 'time': 12})#number of loops necessary to confirm
    print("bought LTC with ETH", quant)
    return change

def sellLTC(quant, price):
    change = quant
    holdings['LTC'] = holdings['LTC'] - change
    
    confirming.append({'type': 'ETH', 'amount': quant*(price - price*0.015), 'time': 30})
    print("trying to sell")#number of loops necessary to confirm
    print("Sold LTC for ETH", quant)
    return change
    
def updateConf():
    counter = 0
    for el in confirming:
        if el['time'] == 0:
            holdings[confirming[counter]['type']] = confirming[counter]['amount']
            confirming.pop(counter)
            graph.append(holdings['ETH'])
        else:
            confirming[counter]['time'] = confirming[counter]['time'] - 1
        counter += 1    
    
c = 0
for n in range(1000):
    #This is the main loop for the program that determines the number of times it is run
    
    
    #BITTREX
    my_bittrex = Bittrex(None, None)  # or defaulting to v1.1 as Bittrex(None, None)
    history = my_bittrex.get_market_history('ETH-LTC')
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
    price_coinbase = float(response_ETH.json()['data']['amount'])/float(response_LTC.json()['data']['amount'])
    price_coinbase = 1/price_coinbase
    
    
    
    include = (price_bittrex + price_bittrex*0.0025)
    if (price_coinbase - price_coinbase*0.0025) > include:
        
        try:
            if holdings['ETH'] > 0:
                if holdings['ETH'] < 0.0001:
                    holdings['ETH'] = 0
                else:   
                    buyLTC(holdings['ETH']/include , price_bittrex)
        except:
            None
        try:
            if holdings['LTC'] > 0:
                if holdings['LTC'] < 0.0001:
                    holdings['LTC'] = 0
                else:                   
                    sellLTC(holdings['LTC'], price_coinbase)
        except:
            None
    updateConf()
    print('\n')
    print('minutes:', c)
    print('CB', price_coinbase)
    print('BT', price_bittrex)
    print(confirming)  
    print(holdings)
    time.sleep(4) #Duration between calculation loops
    c += 1
    


    
