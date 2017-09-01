from django.shortcuts import render
from django.http import HttpResponse
import json
import time
import sys
import requests
import re

class Coin():
    def __init__(self, name, price, volume):
        self.price = 0
        self.volume = 0
        self.priceList = [0, 0, 0, 0, 0]
        self.volumeList = [0, 0, 0, 0, 0]
        self.diffPriceList = [0, 0, 0, 0, 0]
        self.diffVolumeList = [0, 0, 0, 0, 0]
        self.diffPriceRateList = [0, 0]
        self.diffVolumeRateList = [0, 0]
        self.name = name
        self.priceList[4] = "%9.8f" % price
        self.volumeList[4] = "%9.8f" %volume
        self.price = price
        self.volume = volume
        print("Append Name : " + self.name  + ", price : " + str(self.priceList[4]) + ", volume : " + str(self.volumeList[4]))

    def addCoinData(self, price, volume):
        for i in range(0, 4):
            self.priceList[i] = self.priceList[i+1]
            self.volumeList[i] = self.volumeList[i+1]
#            if(i < 3):
#                self.diffPriceList[i] = self.diffPriceList[i+1]
#                self.diffVolumeList[i] = self.diffVolumeList[i+1]
#                self.diffPriceRateList[i] = self.diffPriceRateList[i+1]
#                self.diffVolumeRateList[i] = self.diffVolumeRateList[i+1]

        self.priceList[4] = "%9.8f" % price
        self.volumeList[4] = "%9.8f" %volume

        self.diffPriceList[0] = "%9.8f" % (float(self.priceList[4]) - float(self.priceList[2]))
        self.diffVolumeList[0] = "%5.2f" % (float(self.volumeList[4]) - float(self.volumeList[2]))
        self.diffPriceList[1] = "%9.8f" % (float(self.priceList[4]) - float(self.priceList[0]))
        self.diffVolumeList[1] = "%5.2f" % (float(self.volumeList[4]) - float(self.volumeList[0]))
#        self.diffPriceList[4] = "%9.8f" % (float(self.priceList[4]) - float(self.priceList[0]))
#        self.diffVolumeList[4] = "%5.2f" % (float(self.volumeList[4]) - float(self.volumeList[0]))

        if(float(self.priceList[2]) != 0 and float(self.volumeList[2]) != 0):
            self.diffPriceRateList[0] = "%5.2f" % ((float(self.priceList[4]) - float(self.priceList[2])) / float(self.priceList[2]) * 100 )
            self.diffVolumeRateList[0] = "%5.2f" % ((float(self.volumeList[4]) - float(self.volumeList[2])) / float(self.volumeList[2]) * 100 )
        else:
            self.diffPriceRateList[0] = 0
            self.diffVolumeRateList[0] = 0

        if(float(self.priceList[0]) != 0 and float(self.volumeList[0]) != 0):
            self.diffPriceRateList[1] = "%5.2f" % ((float(self.priceList[4]) - float(self.priceList[0])) / float(self.priceList[0]) * 100 )
            self.diffVolumeRateList[1] = "%5.2f" % ((float(self.volumeList[4]) - float(self.volumeList[0])) / float(self.volumeList[0]) * 100 )
        else:
            self.diffPriceRateList[1] = 0
            self.diffVolumeRateList[1] = 0

    def coinVolume30min(c):
                return float(c.diffVolumeList[0])

    def coinVolume60min(c):
            return float(c.diffVolumeList[1])

    def coinVolumeRate30min(c):
            return float(c.diffVolumeRateList[0])

    def coinVolumeRate60min(c):
        return float(c.diffVolumeRateList[1])

coinList = []
url = "https://bittrex.com/api/v1.1/public/getmarketsummaries"

# Create your views here.
def showlist(request):
    for coin in coinList :
        print("Name : " + coin.name + ", price : " + str(coin.price) + ", volume : " + str(coin.volume))
    return render(request, 'super.html', {'coins': coinList})

def returnTicker(request):
    global coinList
    voluem30minList = []
    voluem60minList = []
    voluemRate30minList = []
    voluemRate60minList = []
    topCoinvoluem30minList = []
    topCoinvoluem60minList = []
    topCoinvoluemRate30minList = []
    topCoinvoluemRate60minList = []
#  for coin in coinList :
#        print("Name : " + coin.name + ", price : " + str(coin.price) + ", volume : " + str(coin.volume))
    for coinVolume in coinList:
        if(float(coinVolume.volumeList[4]) > 100 and coinVolume.name.find("USDT") < 0):
            topCoinvoluem30minList.append(coinVolume)
            topCoinvoluem60minList.append(coinVolume)
            topCoinvoluemRate30minList.append(coinVolume)
            topCoinvoluemRate60minList.append(coinVolume)

    topCoinvoluem30minList.sort(key=Coin.coinVolume30min)
    topCoinvoluem30minList.reverse()

    topCoinvoluem60minList.sort(key=Coin.coinVolume60min)
    topCoinvoluem60minList.reverse()

    topCoinvoluemRate30minList.sort(key=Coin.coinVolumeRate30min)
    topCoinvoluemRate30minList.reverse()

    topCoinvoluemRate60minList.sort(key=Coin.coinVolumeRate60min)
    topCoinvoluemRate60minList.reverse()

    for i in range(0, 5):
        voluem30minList.append(topCoinvoluem30minList[i])
        voluem60minList.append(topCoinvoluem60minList[i])
        voluemRate30minList.append(topCoinvoluemRate30minList[i])
        voluemRate60minList.append(topCoinvoluemRate60minList[i])



    return render(request, 'super.html', {'voluem30minLists': voluem30minList, 'voluem60minLists': voluem60minList, 'voluemRate30minLists': voluemRate30minList, 'voluemRate60minLists': voluemRate60minList,})
#  return HttpResponse(json.dumps(json.loads(jsonString), indent=4), content_type="application/json")
  #return json.loads(ret.read())

def return24Volume():
    while True:
        checkVoluem()
#       for data in coinData[check]:
#       print("Name : " + data.name + ", price : " + str(data.price) + ", volume : " + str(data.volume))
        time.sleep(900)
#        time.sleep(10)
    return HttpResponse("1")

def initcheckVoluem():
    global coinList

    s = requests.get(url)
    dict = s.json()
    #print(dict["result"])
    for item in dict["result"]:
        if(item["MarketName"].find("BTC") >= 0):
            coinList.append(coin(item["MarketName"],item["Last"],item["BaseVolume"]))

def checkVoluem():
    global coinList
    coinSave = 0

    s = requests.get(url)
    dict = s.json()
    #print(dict["result"])
    for item in dict["result"]:
        if(item["MarketName"].find("BTC") >= 0):
            coinSave = 0
            for coin in coinList:
                if(coin.name == item["MarketName"]):
                    print("Add Name : " + item["MarketName"] + ", price : " + str(item["Last"]) + ", volume : " + str(item["BaseVolume"]))
                    coin.addCoinData(item["Last"], item["BaseVolume"])
                    coinSave = 1

            if(coinSave == 0):
                #print("Append Name : " + item["MarketName"] + ", price : " + str(item["Last"]) + ", volume : " + str(item["BaseVolume"]))
                #tempCoin.addCoinData(item["Last"], item["BaseVolume"])
                coinList.append(Coin(item["MarketName"],item["Last"],item["BaseVolume"]))








"""
def returnOrderBook (self, currencyPair):
  return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

def returnMarketTradeHistory (self, currencyPair):
  return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair})
"""
