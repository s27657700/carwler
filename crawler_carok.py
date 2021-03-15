import requests
from bs4 import BeautifulSoup
import time
import os
# from  pymongo import MongoClient
# conn = MongoClient("mongodb://root:666666@2.tcp.ngrok.io:17528/")
# db=conn['toyota']
# col=db.carok
path='./carok'
if not os.path.exists(path):
    os.mkdir(path)
import random
import pandas as pd

car_info_list=[]
car_data=['auto_brand','auto_type','auto_color','auto_door_num','auto_passenger','auto_gearshift','auto_gas_type','auto_model','auto_displacement','auto_build_year','auto_view','auto_img','auto_price']
# car_data=['廠牌','類別','顏色','車門數','乘客數','排檔方式','燃料','車型','排氣量','年分','瀏覽數','圖名','價錢']
n=int(input("page : "))
for j in range(40,n+1):
    url="http://www.carok.com.tw/buy/carList?page_status=on&multi_area_no=&car_brand=Toyota&car_model=0&car_color=&car_price_range=0&car_cc_range=&car_start_year=&car_end_year=&guarantee3=&warranty3=&warranty5=&no_taxi=&mileage_guarantee=&car_guarantee=&price_guarantee=&car_keyword=&car_recommend=&car_type=&car_price_guarantee=&original_warranty=&order_type=car_refresh_date&order_mode=desc&page={}".format(j)
    headers={
        "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"   
    }
    #要換頁改網址最後面的page
    req=requests.get(url=url,headers=headers)
    res=BeautifulSoup(req.text,'html.parser')
    title_url=res.find_all("div",class_="col-info")
    for i in range(int(len(title_url)/2)):
        item_url="http://www.carok.com.tw"+title_url[i].a['href']
        item_id=title_url[i].a['href'][-5:]
        req=requests.get(url=item_url,headers=headers)
        res=BeautifulSoup(req.text,'html.parser')
        photo_url=res.find_all('figure',class_='figure')
        car_info=res.find('td',class_="txt4-16b")
        car_info=car_info.text.replace(" ","").split("\n\n")
        car_info[0]=car_info[0][4:]
        car_info[1]=car_info[1][3:]
        car_info[2]=car_info[2][3:]
        car_info[3]=car_info[3][4:]
        car_info[4]=car_info[4][4:]
        car_info[5]=car_info[5][5:]
        car_info[6]=car_info[6][4:]
        car_info[7]=car_info[7][3:]
        car_info[8]=car_info[8][4:]
        car_info[9]=car_info[9][3:]
        car_info[10]=car_info[10][4:].replace("\n","")   
        cartype=car_info[7]
        # price=res.find("td",class_="txt5-28")
        # price=price.text
        # car_img="carok_"+str(cartype)+"_"+str(item_id) 
        # car_info.append(car_img)
        # car_info.append(price)
        # if len(car_info)>13:
        #     car_info.remove(car_info[-3])
        # car_info_list.append(car_info)
        # col.insert({car_img:{
        #     'auto_brand':car_info[0],
        #     'auto_type':car_info[1],
        #     'auto_color':car_info[2],
        #     'auto_door_num':car_info[3],
        #     'auto_passenger':car_info[4],
        #     'auto_gearshift':car_info[5],
        #     'auto_gas_type':car_info[6],
        #     'auto_model':car_info[7],
        #     'auto_displacement':car_info[8],
        #     'auto_build_year':car_info[9],
        #     'auto_view':car_info[10],
        #     'auto_img':car_img,
        #     'auto_price':price
        # }

        # })
        for u in range(len(photo_url)):
            photo="http://www.carok.com.tw"+photo_url[u].img['src']            
            req=requests.get(url=photo,headers=headers)
            print('carok '+"page : ",j,"  ",cartype,item_id,req)
            print(photo)
            img=req.content
            item_name="carok_"+str(cartype)+"_"+str(item_id)+"_"+str(u)
            with open (path+"/{}.jpg".format(item_name),'wb') as f:
                f.write(img)   
            sleeptime=random.randint(3,7)
            print("wait time : ",sleeptime,"  img : ",u)
            # time.sleep(sleeptime)
            print("OK")   
        # print("carok ",'page : ',j,cartype,item_id)
        # print(car_info)
        sleeptime2=random.randint(3,7)
        print("wait time : ",sleeptime2)
        # time.sleep(sleeptime2)
        print("ok")
    print("change page change page change page change page change page change page change page")
# print(car_info_list)
# df=pd.DataFrame(data=car_info_list,columns=car_data)
# df.to_csv(r"carok_toyota.csv",encoding="utf-8")