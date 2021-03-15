import requests
from bs4 import BeautifulSoup
import time
import os
import pandas as pd
import random
# from  pymongo import MongoClient
# conn = MongoClient("mongodb://root:666666@2.tcp.ngrok.io:17528/")
# db=conn['toyota']
# col=db.autostar
path='./autostar'
if not os.path.exists(path):
    os.mkdir(path)
url="https://www.autostar.com.tw/p1_buy.php"
headers={
    "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"   ,
    'referer': 'https://www.autostar.com.tw/p1_buy.php'
}
n=int(input("page : "))
car_info_list=[]
car_data=["auto_brand","auto_model","auto_gas_tpye","auto_displacement","auto_color","auto_build_year","auto_mileage","auto_img","auto_price"]
for page in range(32,n+1):
    data={
    'Page': page,#換頁改這個
    'PageA': "",
    'PageB': "",
    'Keyword': "",
    'Keywords': '',
    'Class1': '19',
    'Class2': '',
    'Class4': '',
    'strCountry':'' ,
    'StartDate': '',
    'EndDate': '',
    'Price': '',
    'PriceFlag': '',
    'Milage_Check': '',
    'CheckPaper': '',
    'Record': '',
    'CarNumber':'' ,
    'area':''
    }

    req=requests.post(url=url,headers=headers,data=data)
    res=BeautifulSoup(req.text,'html.parser')
    title_url=res.find_all('ul',class_="list photo clearfix")
    for i in title_url:
        item_url="https://www.autostar.com.tw/"+i.a['href']
        item_id=i.a['href'][30:]
        req=requests.get(url=item_url,headers=headers)
        res=BeautifulSoup(req.text,'html.parser')
        photo_url=res.find_all("p")
        cartype=res.find_all('li',class_="active")
        cartype=cartype[-1].text
        car_info=res.find('ul',class_="specification")
        car_info=car_info.text.split("\n")[1:-1]
        car_info[0]=car_info[0][-2:]
        car_info[1]=car_info[1][2:]
        car_info[2]=car_info[2][-2:]
        car_info[3]=car_info[3][-4:]
        car_info[4]=car_info[4][2:]
        car_info[5]=car_info[5][4:].replace("年",".").replace("月","")
        car_info[6]=car_info[6][4:]
        car_info_img="autostar_"+str(cartype)+"_"+str(item_id)
        price=res.find("strong",class_="red")
        price=price.text
        car_info.append(car_info_img)
        car_info.append(price)
        car_info_list.append(car_info)
        # col.insert({car_info_img:{
        # "auto_brand":car_info[0],
        # "auto_model":car_info[1],
        # "auto_gas_tpye":car_info[2],
        # "auto_displacement":car_info[3],
        # "auto_color":car_info[4],
        # "auto_build_year":car_info[5],
        # "auto_mileage":car_info[6],
        # "auto_img":car_info_img,
        # "auto_price":price
        # }
        # })
        for u in range(len(photo_url)):
            if photo_url[u].img != None:
                photo="https://www.autostar.com.tw/"+photo_url[u].img['src']
                
                if photo[-3:]=="jpg":
                    req=requests.get(url=photo,headers=headers)
                    print("page : ",page,"  ",cartype,item_id,req)
                    print(photo)
                    img=req.content
                    img_name="autostar_"+str(cartype)+"_"+str(item_id)+"_"+str(u)
                    with open (path+"/{}.jpg".format(img_name),'wb')as f :
                        f.write(img)
                    sleeptime=random.randint(1,3)
                    print("wait time : ",sleeptime,"  img : ",u)
                    time.sleep(sleeptime)
                    print("ok")
                else:
                    continue
        # print('page : ',page,cartype,item_id)
        # print(car_info)
        sleeptime2=random.randint(5,10)
        print('wait time :',sleeptime2)
        time.sleep(sleeptime2)
        print("ok")
    print("change page change page change page change page change page change page ")
# print(car_info_list)
# df=pd.DataFrame(data=car_info_list,columns=car_data)
# df.to_csv(r"autostar_toyota.csv",encoding="utf-8")