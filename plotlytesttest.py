import pandas as pd
import html5lib
from bs4 import BeautifulSoup as bs
import requests
import numpy as np

import plotly.offline as pyo
import plotly.graph_objs as go
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}


code_df = pd.read_html('C:\\Users\\user\\Downloads\\stockdata.xls', header=0)[0]

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)



# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드','업종','상장일']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code','대표자명':'CEO'})



# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌
# KEC의 일자데이터 url 가져오기
item_name = 'KEC'
df = pd.DataFrame()
#20페이지 불러오기
for page in range(1,21):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False).lstrip()

    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code)
    url='{url}&page={page}'.format(url=url,page=page)
    print(url)




    response = requests.get(url, headers=headers)
    print("요청 URL = {}".format(url))



    html = bs(response.text, "lxml")

    html_table = html.select("table")
    len(html_table)

# html에서 찾은 table 태그를 pandas 로 읽어옵니다.

    table = pd.read_html(str(html_table))



    df=df.append(table[0],ignore_index=True)
    df=df.dropna()




#한글로 컬럼을 바꿈
df=df.rename(columns={'날짜':'date','종가':'close','전일비':'diff',
                      '시가':'open','고가':'high','저가':'low','거래량':'volume'})
df[['close', 'diff', 'open', 'high', 'low', 'volume']] \
    = df[['close', 'diff', 'open', 'high', 'low', 'volume']].astype(int)
# 컬럼명 'date'의 타입을 date로 바꿔줌
#df['date'] = pd.to_datetime(df['date'])
# 일자(date)를 기준으로 오름차순 정렬
df = df.sort_values(by=['date'], ascending=True)

print(df[['date']])

#그래프그리기
trace1=go.Scatter(x=df.date,y=df.open,name=item_name)
data=[trace1]
layout=go.Layout(title=item_name+' 주가')
fig=go.Figure(data=data,layout=layout)
pyo.iplot(fig)

X=df[['date']] #date 형식변환
y=df[['open']]

line_fitter=LinearRegression()
line_fitter.fit(X.values.reshape(-1,1),y)
plt.plot(X,y,'o')
plt.plot(X,line_fitter.predict(X.values.reshape(-1,1)))
plt.show()