import json
import pandas as pd
import urllib.parse
import numpy as np
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import time
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
    #data.to_excel(str(category)+'.xlsx', index=False,encoding='utf8')     #寫入excel 工作表 xlsx檔
    return data #回傳data表
