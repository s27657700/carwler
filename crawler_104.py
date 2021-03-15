import json
import requests
import os 
import time
from bs4 import BeautifulSoup
import jieba
import glob
import pandas as pd
keyword=input("keyword : ")
page=int(input("page : "))
path="./104"
if not os.path.exists(path):
    os.mkdir(path)


for current_page in range(page+1):
    useragent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
    headers={
        "user-Agent":useragent
    }

    url="https://www.104.com.tw/jobs/search/?ro=0&kwop=7&keyword={}&order=15&asc=0&page={}&mode=s&jobsource=2018indexpoc".format(keyword,current_page)
    req=requests.get(url=url,headers=headers)
    res=BeautifulSoup(req.text,"html.parser")
    search=res.find_all("a",class_="js-job-link")
    for i in search:
        title_url="https:"+i['href']
        job_id=title_url[27:32]
        request_url="https://www.104.com.tw/job/ajax/content/{}".format(job_id)
        headers={
        "user-Agent":useragent,
        "Referer":title_url
        }
        
        req=requests.get(url=request_url,headers=headers)
        try:
            jsondata=json.loads(req.text,encoding="utf-8")
            jsondata=jsondata['data']
            job_info=jsondata['header']
            job_opening=job_info['jobName']
            job_company=job_info['custName']
            job_requires=jsondata['condition']
            job_requirements=list()
            for i in job_requires["acceptRole"]["role"]:
                job_requirements.append(i['description'])
            job_detail=jsondata["jobDetail"]['jobDescription']
            job_detail=job_detail.replace("\t","")
            job_detail=job_detail.replace("\r","")
            job_detail=job_detail.replace("\n","")
            job_contact=list()
            for u in jsondata['contact'].values():
                if u != "":
                    job_contact.append(u)
            job_other_requires=job_requires['other']
            job_other_requires=job_other_requires.replace("\t","")
            job_other_requires=job_other_requires.replace("\r","")
            job_other_requires=job_other_requires.replace("\n","")
            with open (path+"/{}.txt".format(job_id),"w",encoding="utf-8")as f :
                f.write(job_opening)
                f.write("\n")
                f.write("--split--")
                f.write("\n")
                f.write(job_company)
                f.write("\n")
                f.write("--split--")
                f.write("\n")
                f.write(title_url)
                f.write("\n")
                f.write("--split--")
                f.write("\n")
                f.write(str(job_contact))
                f.write("\n")
                f.write("--split--")
                f.write("\n")
                f.write(str(job_requirements))
                f.write("\n")
                f.write("--split--")
                f.write("\n")
                f.write(job_detail)
                f.write("\n")
                f.write(job_other_requires)
        except:
            print(request_url)
            continue
    print(current_page)
columns=["職稱","公司","連結","聯絡方式","接受身分","工作內容","python","java","javascript","r語言","linux","mysql","mongodb","nosql","aws","gcp","azure","spark","ai","deep learning","cloud","hadoop"]
job_rows=list()
for g in glob.glob("./104/*.txt"):
    sb=""
    each_file=list()
    my_dict={"python":0,"java":0,"javascript":0,"r語言":0,"linux":0,"mysql":0,"mongodb":0,"nosql":0,"aws":0,"gcp":0,"azure":0,"spark":0,"ai":0,"deep learning":0,"cloud":0,"hadoop":0}
    with open (g,'r',encoding="utf-8") as f:
        each_file=f.read().replace("\n","").split('--split--')

        sb+=each_file[5]       
    sb=jieba.cut(sb,cut_all=True)
    cut_list=list()
    for each_word in sb:
        word_lower=each_word.lower()
        cut_list.append(word_lower)
    for i in cut_list:
        if i in my_dict:
            my_dict[i]=1
        else:
            continue
    for q in my_dict.values():
        each_file.append(q)
    job_rows.append(each_file)
df=pd.DataFrame(data=job_rows,columns=columns)
df.to_csv(r'./{}.csv'.format(keyword),encoding="utf-8")