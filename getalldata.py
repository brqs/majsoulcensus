#!/usr/bin/python
# -*- coding:utf-8 -*-
import json
import pandas as pd
import time
import datetime
import string
import requests
import re
import string
with open("data.json",'r',encoding="utf-8") as load_f:
    load_dict = json.load(load_f)
#解析json文件
timelist=[]
for data_time in load_dict:
    timelist= timelist+[data_time["time"]]
levellist=[]
for data_level in load_dict:
    levellist= levellist+[data_time["level"]]
#获取时间数组
dict = {}
for key in timelist:
    dict[key] = dict.get(key, 0) + 1 
timeamountlist_key = list(dict) 
timeamountlist_value = list(dict.values()) 
timeamountlist=[list(t) for t in zip(timeamountlist_key,timeamountlist_value)]
#输出时间数量二维数组
date=time.strftime("%Y%m%d", time.localtime())
#获取当前时间
timeArray=time.strptime(date,"%Y%m%d")
timeStamp=(time.mktime(timeArray))   
end_time = time.strftime('%Y-%m-%d',time.localtime(timeStamp))
start_year = int(time.strftime('%Y',time.localtime(timeStamp))) - 1
month_day = time.strftime('%m-%d',time.localtime(timeStamp))
start_time = '{}-{}'.format(start_year,month_day)
#获取一年前时间 
timeamountlistfrist= timeamountlist_key[0]
punctuation_string = string.punctuation
for i in punctuation_string:
    timeamountlistfrist = timeamountlistfrist.replace(i, '')
date_A= timeamountlistfrist
dayA= datetime.datetime.strptime(date_A, '%Y%m%d')
delta=datetime.timedelta(days=1)
dayB=dayA-delta
#获取前一天时间
start = start_time
end = dayB
year_dateslist = pd.date_range(start,end).strftime("%Y-%m-%d").to_list()
dayamount=400
zerohelp=[0]*dayamount
year_zerohelptlist=[list(t) for t in zip(year_dateslist,zerohelp)]
#生成全零辅助二维列表
yearlist=year_zerohelptlist+timeamountlist
daterange=[start ,timeamountlist_key[-1] ]
#生成日历二维列表
trendlist=[]
for data_trend in load_dict:
    trendlist= trendlist+[data_trend["variation"]]
#获取变化量数组
poweramount=len(trendlist)
powervariation=[]
for i in range(poweramount):
    powervariationi = sum(trendlist[:i+1]) 
    powervariation.append(powervariationi)
#计算累计变化量
powerstandar=743#雀力初记基准量
powervariationhelp=[powerstandar]*poweramount
powerlist=[]
for i in range(len(powervariationhelp)):
    new_value=powervariationhelp[i]+powervariation[i]
    powerlist.append(new_value)
#雀力数组对应相加
url = 'https://hesifan.top/PaipuAnalyzeResult.html'
r = requests.get(url=url)
content = r.text
result = re.findall('.*DATA.*DATA = ({"#1R":0.283951.*?};).*BASEDATA.*?',
                    content, re.S)

resultstr= result[0]
#获取网页数据
webdatamain=resultstr[0:6120]+'}'
webdatamaindict=eval(webdatamain)
webdatahule=resultstr[6131:7169]
webdatahuledict=eval(webdatahule)
webdatachong=resultstr[7184:8202]
webdatachongdict=eval(webdatachong)
level=str(levellist[0])
#切片处理字符串，转化字典处理
sortlist=[ { "value": webdatamaindict["#1R"], "name": '一位' },{ "value": webdatamaindict["#2R"], "name": '二位' },{ "value": webdatamaindict["#3R"], "name": '三位' },{ "value": webdatamaindict["#4R"], "name": '四位' }]
alldit = {
    'level1': level[0:2],
    'level2': level[2:4],
   'dateranges': daterange,
   'calendarlist': yearlist,
   'trendlist': trendlist,
   'powerlist': powerlist,
   'sortlist': sortlist,
   'totalgame': webdatamaindict["TOTALGAME"],
   'totalround': webdatamaindict["TOTALROUND"],
   'hupair': webdatamaindict["HULER"],
   'fulur':webdatamaindict["FULUR"],
   'lizhir':webdatamaindict["REACHR"],
   'dadainp':webdatamaindict["HULEP"],
   'fangchongr':webdatamaindict["CHONGR"],
   'liujur':webdatamaindict["LIUJUR"],
   'chongdianp':webdatamaindict["CHONGP"],
   'zimor':webdatamaindict["ZIMOR"],
   'liujutingpair':webdatamaindict["LIUJUTENPAIR"],
   'hulexuns':webdatamaindict["HULECC"],
   'hulexuns':webdatamaindict["#A"],
}
with open('./alldata.json', 'w') as jsonfile:
    json.dump(alldit, jsonfile)




