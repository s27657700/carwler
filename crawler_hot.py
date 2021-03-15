import requests
from bs4 import BeautifulSoup
import time
import os
import json
import pandas as pd
import random
path='./toyota'
if not os.path.exists(path):
    os.mkdir(path)
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    'Referer': 'https://www.hotcar.com.tw/SSAPI45/proxyPage/proxyPage.html',
    'Origin': 'https://www.hotcar.com.tw',
    'Host': 'www.hotcar.com.tw',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    "Content-Type": "application/json;charset=UTF-8"
}
url="https://www.hotcar.com.tw/SSAPI45/API/SPRetB?Token=VfaU%2BLJXyYZp7Nr3mFhCQtBfZ%2FrL2AQmOjkOW4W1uZVumEKn0wIHcD%2FRsdkmgB8di2Y9HFgUS%2F7HFxHm4m9eACLvfBCTdBEGoGqcd6RDUeZNSwlOrVeFarS9bEalGyz6"
data={
    "SPNM":"CWA050Q1_2018",
    "SVRNM":["HOTCARAPP"],
    "PARMS":["https://www.hotcar.com.tw","https://www.hotcar.com.tw/image/nophoto.png","","",0,0,"","",0,0,"","","","","","","toyota","","","","",""]
    
}
car_data=["廠牌","類型","型號","顏色",'排氣量','年分','排檔','里程','車輛所在地','圖名','價錢']
req=requests.post(url=url,headers=headers,json=data)
# res=BeautifulSoup(req.text,'html.parser')
data_list=req.json()
data_list=data_list['DATA']['Table1']
car_info_list=[]
print(data_list[3])
for i in data_list:
    car_info=[]
    photo_url=i['PHOTOSTR'].split(',')
    tseqno=i['TSEQNO']
    cartype=i['CARTYPENM']
    car_produce=i["BRANDNM"]
    car_color=i['CCORLORNM']
    car_location=i['CITYNM']
    car_geartype=i['GEARTYPE']
    car_mileage=i["KM1"]
    car_price=i['SALAMT1']
    car_born=i['CARYM']
    car_displacement=i['CCNUM_R']
    car_class=i['BODYTYPENM']
    img_name="hot_"+cartype+"_"+str(tseqno)
    car_info.append(car_produce)
    car_info.append(car_class)
    car_info.append(cartype)
    car_info.append(car_color)
    car_info.append(car_displacement)
    car_info.append(car_born)
    car_info.append(car_geartype)
    car_info.append(car_mileage)
    car_info.append(car_location)
    car_info.append(img_name)
    car_info.append(car_price)
    car_info_list.append(car_info)
    for u in range(len(photo_url)):
        req=requests.get(url=photo_url[u])
        img=req.content
        print(cartype,tseqno,req)
        print(photo_url[u])
        photoname="hot_"+cartype+"_"+str(tseqno)+"_"+str(u)
        with open (path+'/{}.jpg'.format(photoname),'wb')as f:
            f.write(img)
        sleeptime=random.randint(1,3)
        print("wait time : ",sleeptime,"  img : ",u)
        time.sleep(sleeptime)
        print("ok")
