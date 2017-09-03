from django.shortcuts import render
from django.http import HttpResponse
import json
import time
import sys
import requests
import re
import datetime

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
        self.volumeList[4] = "%5.2f" %volume
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
        self.volumeList[4] = "%5.2f" %volume

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

class CoinRec():
    def __init__(self, name, price, volume):
        self.name = name
        self.dectprice = price
        self.dectvolume = volume
        self.count = 24
        self.targprice = "%9.8f" % (float(price) * 0.9)
        self.lastprice = price
        self.lastvolume = volume
        self.buysig = 0

    def resetCoinRec(self, price, volume):
        self.count = 24
        self.lastprice = price
        self.lastvolume = volume
        temp = (float(self.lastprice) - float(self.targprice)) / float(self.targprice) * 100
        if( temp < 3 ):
            self.buysig = 1

    def checkCoinRec(self):
        check = self.count
        self.count = check - 1

coinList = []
coinRecList = []
url = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
timecheck = 1
voluem60minList = []
voluemRate60minList = []
run = 0

# Create your views here.
def returnRecommand(request):
    global coinRecList
    global timecheck

    return render(request, 'super0.html', {'time':timecheck, 'coinRecLists': coinRecList})

    return HttpResponse("1")

def returnTicker(request):
    global timecheck
    global voluem60minList
    global voluemRate60minList

    return render(request, 'super.html', {'time':timecheck, 'voluem60minLists': voluem60minList, 'voluemRate60minLists': voluemRate60minList,})
#    return render(request, 'super.html', {'voluem30minLists': voluem30minList, 'voluem60minLists': voluem60minList, 'voluemRate30minLists': voluemRate30minList, 'voluemRate60minLists': voluemRate60minList,})
#  return HttpResponse(json.dumps(json.loads(jsonString), indent=4), content_type="application/json")
  #return json.loads(ret.read())

def return24Volume():
    global run

    if(run == 0):
        run = 1
        print("run is 0")
    else:
        print("run is 1")
        return HttpResponse("1")

    while True:
        checkVolume()
        rankVolume()
        checkRec()
#       for data in coinData[check]:
#       print("Name : " + data.name + ", price : " + str(data.price) + ", volume : " + str(data.volume))
        time.sleep(900)
#        time.sleep(10)

    return HttpResponse("1")

def checkVolume():
    global coinList
    global timecheck
    coinSave = 0

    timecheck = datetime.datetime.now()
    s = requests.get(url)
    dict = s.json()
    #print(dict["result"])
    print("checkVolume")
    for item in dict["result"]:
        if(item["MarketName"].find("BTC") >= 0):
            coinSave = 0
            for coin in coinList:
                if(coin.name == item["MarketName"]):
                    #print("Add Name : " + item["MarketName"] + ", price : " + str(item["Last"]) + ", volume : " + str(item["BaseVolume"]))
                    coin.addCoinData(item["Last"], item["BaseVolume"])
                    coinSave = 1

            if(coinSave == 0):
                #print("Append Name : " + item["MarketName"] + ", price : " + str(item["Last"]) + ", volume : " + str(item["BaseVolume"]))
                #tempCoin.addCoinData(item["Last"], item["BaseVolume"])
                coinList.append(Coin(item["MarketName"],item["Last"],item["BaseVolume"]))

def rankVolume():
    global coinList
    global voluem60minList
    global voluemRate60minList

    voluem60minList = []
    voluemRate60minList = []
#    topCoinvoluem30minList = []
    topCoinvoluem60minList = []
#    topCoinvoluemRate30minList = []
    topCoinvoluemRate60minList = []

#  for coin in coinList :
#        print("Name : " + coin.name + ", price : " + str(coin.price) + ", volume : " + str(coin.volume))
    for coinVolume in coinList:
        if(float(coinVolume.volumeList[4]) > 150 and coinVolume.name.find("USDT") < 0):
#            topCoinvoluem30minList.append(coinVolume)
            topCoinvoluem60minList.append(coinVolume)
#            topCoinvoluemRate30minList.append(coinVolume)
            topCoinvoluemRate60minList.append(coinVolume)

#    topCoinvoluem30minList.sort(key=Coin.coinVolume30min)
#    topCoinvoluem30minList.reverse()

    topCoinvoluem60minList.sort(key=Coin.coinVolume60min)
    topCoinvoluem60minList.reverse()

#    topCoinvoluemRate30minList.sort(key=Coin.coinVolumeRate30min)
#    topCoinvoluemRate30minList.reverse()

    topCoinvoluemRate60minList.sort(key=Coin.coinVolumeRate60min)
    topCoinvoluemRate60minList.reverse()

    for i in range(0, 10):
        voluem60minList.append(topCoinvoluem60minList[i])
        voluemRate60minList.append(topCoinvoluemRate60minList[i])
#        voluem30minList.append(topCoinvoluem30minList[i])
#        voluemRate30minList.append(topCoinvoluemRate30minList[i])

def checkRec():
    global voluem60minList
    global voluemRate60minList
    global coinRecList
    coinSave = 0

    print("checkCoinRec")
    for coinRec in coinRecList:
        coinRec.checkCoinRec()
        #print("Add coinRec Name : " + coinRec.name + "coin count : " + str(coinRec.count))
        if (coinRec.count == 0):
            coinRecList.remove(coinRec)

    print("add coinQec volume")
    for coinVolume in voluem60minList:
        if(float(coinVolume.diffVolumeList[0]) > 30 or float(coinVolume.diffVolumeList[1]) > 50 ):
            coinSave = 0
            for coin in coinRecList:
                if(coin.name == coinVolume.name):
                    print("reset 1 : " + coin.name + ", 2 : " + coinVolume.name)
                    #print("Add coinRec Name : " + coinVolume.name)
                    coin.resetCoinRec(coinVolume.priceList[4], coinVolume.volumeList[4])
                    coinSave = 1

            if(coinSave == 0):
                print("volume Append "  + coinVolume.name)
                coinRecList.append(CoinRec(coinVolume.name,coinVolume.priceList[4],coinVolume.volumeList[4]))

    print("add coinQec volumeRate")
    for coinVolumeRate in voluemRate60minList:
        if(float(coinVolumeRate.diffVolumeRateList[0]) > 7 or float(coinVolumeRate.diffVolumeRateList[1]) > 15 ):
            coinSave = 0
            for coin in coinRecList:
                if(coin.name == coinVolumeRate.name):
                    print("reset 1 : " + coin.name + ", 2 : " + coinVolumeRate.name)
                    #print("Add coinRec Name : " + coinVolumeRate.name)
                    coin.resetCoinRec(coinVolumeRate.priceList[4], coinVolumeRate.volumeList[4])
                    coinSave = 1

            if(coinSave == 0):
                print("volumeRate Append : " + coinVolumeRate.name)
                coinRecList.append(CoinRec(coinVolumeRate.name,coinVolumeRate.priceList[4],coinVolumeRate.volumeList[4]))


"""
def returnOrderBook (self, currencyPair):
  return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

def returnMarketTradeHistory (self, currencyPair):
  return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair})
"""
