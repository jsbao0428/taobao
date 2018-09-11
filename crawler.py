import json
import pandas as pd
import urllib.parse
import numpy as np
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
def get_data(date):
    file = open('city_dict.json','r')
    city_list=json.loads(file.read())
    file.close()
    data = pd.DataFrame([[0,0,0,0,0,0]],columns=['觀測時間(LST)ObsTime','氣溫(℃)Temperature','降水量(mm)Precp','降水時數(hr)PrecpHour','測站','地區'])
    count = 0
    for key,value in city_list.items():
        count += 1
        loc=urllib.parse.quote(value[0])#把文字轉換成 URL編碼
        print(key,value[0],value[2],loc,count,str(date))
        table = pd.read_html('https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station='+key+'&stname='+loc+'&datepicker='+str(date),encoding='utf8')[1]
        table.columns = table.iloc[1:2].values[0]
        table = table.drop(index=[0,1]).reset_index(drop=True)
        table = table[['觀測時間(LST)ObsTime','氣溫(℃)Temperature','降水量(mm)Precp','降水時數(hr)PrecpHour']]
        for i in table.columns:
            table[i] = pd.to_numeric(table[i], errors='coerce')#pd.to_numeric(list Series array tuple,errors=‘ignore’, ‘raise’, ‘coerce’) coerce如果轉換失敗就填NAN
        table['測站'] = value[0]
        table['地區'] = value[2]
        data = data.append(table,ignore_index=True)
    data=data.drop(index=0)
    data['日期'] = data['觀測時間(LST)ObsTime'].map(lambda x: datetime.strptime(str(date)+' '+str(x-1),'%Y-%m-%d %H'))
    return data
def combine_everyday_data(date_list):
    data = pd.DataFrame([[0,0,0,0,0,0,0]],columns=['觀測時間(LST)ObsTime','氣溫(℃)Temperature','降水量(mm)Precp','降水時數(hr)PrecpHour','測站','地區','日期'])
    for day in date_list:
        data_by_day = get_data(day)
        data = data.append(data_by_day)
        time.sleep(5)
    data=data.drop(index=0)
    data.to_csv('weather_data.csv',index=False)
    return data
def taobao_top_n(category,n=100):
    data = pd.DataFrame([[0,0,0,0,0,0,0,0,0,0,0]],columns=['category','title','raw_title','view_sales','comment_count','view_price','item_loc','nick','pic_url','detail_url','comment_url'])
    #設立一個空的dataframe 並給予first row 不然不能append or concat
    cat = urllib.parse.quote(category)
    #把文字轉換成 URL編碼
    n = int(n)
    #不換int的話 可能會出錯
    for page in range(0,n,12):#用12去切 因為每次回傳是12筆
        html = urlopen('https://s.taobao.com/api?_ksTS=1536551069935_254&callback=jsonp255&ajax=true&m=customized&stats_click=search_radio_all:1&q='+str(cat)+'&imgfile=&initiative_id=staobaoz_20180910&bcoffset=-1&js=1&s='+str(page+1)+'&sort=sale-desc&ie=utf8&rn=ee8573c87fb38de8cefc97dbf202f3eb')
        #s參數代表從第幾個開始查詢 回傳12個產品
        bsObj = BeautifulSoup(html) #用bs解析
        m = re.search('jsonp255\((.*?)\);',bsObj.text)#用regular expression 去掉前後多餘的 剩下json字串 //re.search(pattern,str)會找出所有匹配的結果
        m.group(1)#group(0) 是整個字串匹配的結果 ex:jsonp255(XXXXX), group(1)是第一個pattern (.*?) 所匹配到的結果
        jd = json.loads(m.group(1))#將json字串 轉成 dictionary // load用來處理文件 loads用來處理字串 //dump or dumps 將dict轉成json字串 這樣就可將dict寫成檔案
        df = pd.DataFrame(jd['API.CustomizedApi']['itemlist']['auctions'])#變成dict後用key選出想要的value
        df=df[['category','title','raw_title','view_sales','comment_count','view_price','item_loc','nick','pic_url','detail_url','comment_url']]
        data = data.append(df)#不斷將新資料附加到data
    data.reset_index(drop=True,inplace=True)#重設索引 並刪除本來的索引 drop=True
    data = data.iloc[1:n+1]#刪除多餘的row
    data.to_excel(str(category)+'.xlsx', index=False,encoding='utf8')     #寫入excel 工作表 xlsx檔
    return data #回傳data表
