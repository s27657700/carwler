import requests
from bs4 import BeautifulSoup
import time
import os
import json
import random
import pandas as pd
from  pymongo import MongoClient
conn = MongoClient("mongodb://root:666666@2.tcp.ngrok.io:17528/")
db=conn['toyota']
col=db.ocar
path='./toyota'
if not os.path.exists(path):
    os.mkdir(path)
headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}
n=int(input("page : "))
car_info_list=[]
car_data=['auto_brand','auto_model','auto_engine_num','auto_build_year','auto_color','auto_displacement','auto_mileage','auto_origin','auto_location','auto_price','auto_img']
# car_data=['廠牌','車款','車身號碼','年份','顏色','排氣量','里程數','產地','地區','售價','圖名']
for i in range(1,n+1):
    url="http://www.ocar.com.tw/sell/search.php?cartype=5&cartool=5&brand=7722&cars=&car=&carlist_4=&carlist_1=&mincaryear=&maxcaryear=&carlist_5=&carlist_6=&carlist_7=&carlist_8=&carlist_9=&motorlist_9=&carlist_10=&areaid=&areaid2=&kw=&catid=7722&page={}".format(i)
    req=requests.get(url=url,headers=headers)
    res=BeautifulSoup(req.text,'html.parser')
    title_url=res.find_all("div",class_="detail-thumb")#內文網址
    for j in title_url:
        item_id=j.a['href'][-5:]
        item_url=j.a['href']
        req=requests.get(url=item_url,headers=headers)
        res=BeautifulSoup(req.text,'html.parser')
        photo_url=res.find_all('img',height="45")
        cartype=res.find('div', class_="pos")
        cartype=cartype.text.split("»")[3]
        carinfo=res.find("table",class_='left_box_table')
        carinfo=carinfo.text
        carinfo=carinfo.replace("\n\n","").replace("\xa0","").split("\n")
        car_info=[]
        for r in range(len(carinfo)):
            if r % 2 !=0:
                car_info.append(carinfo[r])
        car_info=car_info[0:-4]      
        if len(cartype)>16:
            cartype=cartype.split(" ")[4]
            car_info.insert(1,cartype)
        price=res.find('td',class_='f_b f_orange')
        price=price.text .replace('\xa0','')
        car_img="ocar_"+str(cartype)+"_"+str(item_id)       
        car_info.append(car_img)
        if len(car_info)<11:
            car_info.insert(9,price)
        print(car_info)
        if len(car_info)>11:
            car_info[1]=car_info[1]+car_info[2]
            car_info.remove(car_info[2])        
        col.insert({car_img:{
            'auto_brand':car_info[0],
            'auto_model':car_info[1],
            'auto_engine_num':car_info[2],
            'auto_build_year':car_info[3],
            'auto_color':car_info[4],
            'auto_displacement':car_info[5],
            'auto_mileage':car_info[6],
            'auto_origin':car_info[7],
            'auto_location':car_info[8],
            'auto_price':car_info[9],
            'auto_img':car_info[10]
        }
        })
        # for u in range(len(photo_url)):
        #     photo=photo_url[u]['src']
        #     req=requests.get(url=photo)
        #     print(cartype,item_id,req)
        #     print(photo)
        #     img=req.content
        #     item_name="ocar_"+str(cartype)+"_"+str(item_id)+"_"+str(u)
        #     with open (path+"/{}.jpg".format(item_name),'wb')as f:
        #         f.write(img)
        #     sleeptime=random.randint(1,3)
        #     print("wait time: ",sleeptime,"  img: ",u)
        #     time.sleep(sleeptime)            
        #     print("OK")
        car_info_list.append(car_info)
        print('o_car ','page : ',i,cartype,item_id)
        sleeptime2=random.randint(3,5)
        print("wait time : ",sleeptime2)
        time.sleep(sleeptime2)
        print('ok')
    print("change page change page change page change page change page change page change page change page ")
df=pd.DataFrame(data=car_info_list,columns=car_data)
df.to_csv(r"o_car.csv",encoding='utf-8')