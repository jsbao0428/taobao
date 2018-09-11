import pandas as pd,numpy as np,sklearn as sk
raw_data = pd.read_csv('C:\\Users\\kevin.huang\\Downloads\\fs.csv',parse_dates=['grass_date','start_time','sold_out_time'])#parse_dates=[欄位,] 先將這些欄位轉成時間格式
raw_data = raw_data.drop_duplicates()#去重複
raw_data.reset_index(inplace=True)
need = ['promotionid','itemid','Category','Sub_Category','L3_Category','promotion_price','discount_percent','fs_stock_sold_item_level','user_item_limit','start_time','sold_out_time']
df = raw_data[need]
df['week_day'] = df['start_time'].apply(lambda x: x.isoweekday())#日期資料.weekday() 回傳0~6, 日期資料.isoweekday() 1~7
#增加星期欄位
df['is_holiday'] = df['week_day'].apply(lambda x: 1 if x == (7|6) else 0)
#增加是否為假日

df['start_time'][0].day #datetime.day 回傳 日 #year,hour
df['start_time'][0].date()#datetim.date() 回傳年月日
date_list = list(set(df['start_time'].apply(lambda x: x.date())))
#DataFrame.set_index(column label or list of column labels / arrays,drop=True)
#datetime.strftime(時間文字格式) 將時間轉成文字
#datetime.strptime(時間文字,'%Y-%m-%d %H<時間文字格式>') 將文字轉成時間
#Timestamp is the pandas equivalent of python’s Datetime