from m5stack import *
from m5ui import *
from uiflow import *
import urequests
import json


def setFont():
  #lcd.clear()
  #setScreenColor(0x006600)
  lcd.setRotation(1)
  lcd.font(lcd. FONT_Default)
  #lcd.font(lcd.FONT_Small)
  #lcd.setTextColor(0xffffff,0x006600)

def redBackDrop():
  lcd.clear()
  setFont()
  setScreenColor(0xf80b0b)
  lcd.setTextColor(0xffffff,0xf80b0b)
  
def greenBackDrop():
  lcd.clear()
  setFont()
  setScreenColor(0x009900)
  lcd.setTextColor(0xffffff,0x009900)

def displayContent(symbol,price, marketcap,block):
    lcd.print(str(symbol), 60, 5)
    lcd.print("Price : $" + str(price), 5, 20)
    lcd.print("M.Cap: $" + str(marketcap) + " Bn", 5, 35)  
    if str(symbol) == 'BTC':
      lcd.print("1$     : " + str(round(1/(price/100000000))) + " Sat", 5, 50)
      lcd.print("Block : " + str(block) + "", 5, 65)


def getAPI():
  result = dict()
  try:
    # Replace 'X-CMC_PRO_API_KEY' with your coinmarketcap API
    req = urequests.request(method='GET', url='https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=BTC,ETH,LTC', headers={'X-CMC_PRO_API_KEY':'XXXXXXXXXXXXXXX','Accept':'application/json'})
    req1 = urequests.request(method='GET', url='https://mempool.space/api/blocks/tip/height')
    BTCPrice = round(json.loads((req.text))["data"]["BTC"]["quote"]["USD"]["price"],2)
    BTCMarketCap = round(json.loads((req.text))["data"]["BTC"]["quote"]["USD"]["market_cap"]/1000000000,2)
    BTCBlock = req1.text
    
    ETHPrice = round(json.loads((req.text))["data"]["ETH"]["quote"]["USD"]["price"],2)
    ETHMarketCap = round(json.loads((req.text))["data"]["ETH"]["quote"]["USD"]["market_cap"]/1000000000,2)
    
    result['btcprice'] = BTCPrice
    result['btcmarketcap'] = BTCMarketCap
    result['block'] = BTCBlock
    result['ethprice'] = ETHPrice
    result['ethmarketcap'] = ETHMarketCap
    
    return result
  except:
    setScreenColor(0xff0000)
    lcd.print("Can't fetch API",5,30)
    result['btcprice'] = 0
    result['btcmarketcap'] = 0
    result['block'] = 0
    result['ethprice'] = 0
    result['ethmarketcap'] = 0
    return result
   
while True:
  result = getAPI()
  redBackDrop()
  displayContent('BTC', result['btcprice'],result['btcmarketcap'],result['block'])
  wait(150)
  greenBackDrop()
  displayContent('ETH', result['ethprice'],result['ethmarketcap'],result['block'])
  wait(150)