import requests
from bs4 import BeautifulSoup
import time
import os
import json
import random
import pandas as pd
from pymongo import MongoClient
conn = MongoClient("mongodb://root:666666@2.tcp.ngrok.io:17528/")
db=conn['toyota']
col=db['toyota2hand']
path='./toyota'
if not os.path.exists(path):
    os.mkdir(path)
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
n=int(input("page : "))
car_data=['auto_brand','auto_color','auto_build_year','auto_is_warranty','auto_phone','auto_mileage','auto_displacement','auto_location','auto_price','auto_img']
# car_data=['車款','顏色','年分','保固','業務電話','里程數','排氣量','車輛所在地','售價','圖名']
car_info_list=[]
for j in range(0,n):
    page=j*16
    url="https://www.toyotacpo.com.tw/Home/List?IsEnable=True&Sort=ID&Order=desc&Limit=16&Offset={}".format(page)
    #換頁調整網址後面的offset數字
    req=requests.get(url=url,headers=headers)
    res=BeautifulSoup(req.text,'html.parser')
    title_url=res.find_all('a',class_='card-item flex-none')
    for i in title_url:
        each_url='https://www.toyotacpo.com.tw/'+i['href']
        item_id=i['href'][13:18]
        req=requests.get(url=each_url,headers=headers)
        res=BeautifulSoup(req.text,'html.parser')
        cartype=res.find("h1", class_="section-title flex items-center")
        cartype=cartype.text.split(" ")[0]
        photo_url=res.find_all('div',class_='swiper-slide preview_slide')
        carinfo=res.find("div",class_='data-wrap')
        carinfo=carinfo.text
        carinfo=carinfo.replace(" ","").replace("\n\n\n","").replace("\n\n","").replace("：","").replace("\r",'').split("\n")
        carinfo[0]=carinfo[0][2:]
        carinfo[1]=carinfo[1][2:]
        carinfo[2]=carinfo[2][2:]
        carinfo[3]=carinfo[3][2:]
        carinfo[4]=carinfo[4][3:]
        carinfo[5]=carinfo[5][3:]
        carinfo[6]=carinfo[6][2:-2]
        car_info=[]
        car_info.append(cartype)
        for i in carinfo:
            car_info.append(i)
        car_img="toyota2_"+str(cartype)+"_"+str(item_id)
        car_info.append(car_img)
        if len(car_info)>10:
            car_info.remove(car_info[8])
        col.insert({car_img:{
        'auto_brand':car_info[0],
        'auto_color':car_info[1],
        'auto_build_year':car_info[2],
        'auto_is_warranty':car_info[3],
        'auto_phone':car_info[4],
        'auto_mileage':car_info[5],
        'auto_displacement':car_info[6],
        'auto_location':car_info[7],
        'auto_price':car_info[8],
        'auto_img':car_info[9]}
        })
        print(car_info)
        for u in range(len(photo_url)):
            if photo_url[u] != None:
                photo="https://www.toyotacpo.com.tw"+photo_url[u].img['src']
                req=requests.get(url=photo,headers=headers)
                print("page : ",j+1,cartype,item_id,req)
                print(photo)
                img=req.content
                img_name="toyota2_"+str(cartype)+"_"+str(item_id)+"_"+str(u)
                with open (path+"/{}.jpg".format(img_name),'wb')as f:
                    f.write(img)
                sleeptime=random.randint(3,5)
                print("wait time : ",sleeptime,"img : ",u)
                time.sleep(sleeptime)
                print("OK")
            else:
                pass
        car_info_list.append(car_info)
    print("change page change page change page change page change page change page change page change page change page change page ")            

df=pd.DataFrame(data=car_info_list,columns=car_data)
df.to_csv(r"toyota2hand.csv",encoding='utf-8')
