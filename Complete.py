import pandas as pd
import html5lib
from bs4 import BeautifulSoup as bs
import requests
import numpy as np

import plotly.offline as pyo
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

font_path=r'C:\Users\user\NanumGothic.ttf'
fontprop=fm.FontProperties(fname=font_path,size=18)


headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}


code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드','업종','상장일']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code','대표자명':'CEO'})




# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌
# KEC의 일자데이터 url 가져오기
item_name = '삼성전자'
df = pd.DataFrame()

#20페이지 불러오기
for page in range(3,28):
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
df['date'] = pd.to_datetime(df['date'])
# 일자(date)를 기준으로 오름차순 정렬
df = df.sort_values(by=['date'], ascending=True)
#df=df.sort_values(by=['xf'],ascending=True)
print(df['date'].dtype)
print(df['date'])
print(df)
df=df.reset_index(drop=True)
print(df['date'])
print(df)


#그래프그리기
trace1=go.Scatter(x=df.date,y=df.open,name=item_name)
#trace2=go.Scatter()
data=[trace1]
layout=go.Layout(title=item_name+' 주가')
fig=go.Figure(data=data,layout=layout)
pyo.iplot(fig)

xf=[]

for i in range(0,5000):
    xf.append(i)

column=['xf']
df1=pd.DataFrame(xf,columns=column)
df=pd.concat([df,df1],axis=1).dropna()
#df = df.sort_values(by=['date'], ascending=True)
print(df)
#X=xf #date 형식변환

#선형회귀 그래프
X=df[['xf']].values.reshape(-1,1) #행(row)의 위치에 -1을 넣고 열의 값을 지정해주면 변환될 배열의 행의 수는 알아서 지정
y=df[['open']]
print(df['date'].dtype)

X_train,X_test,y_train,y_test=train_test_split(X,y)

line_fitter=LinearRegression()
line_fitter.fit(X_train,y_train)

plt.title(item_name+' 주가예측 그래프',fontproperties=fontprop)
plt.plot(X_train,y_train,'o')
plt.plot(X_train,line_fitter.predict(X_train))
plt.ylabel('시가',fontproperties=fontprop)
#plt.xticks(X,df['date'])


print("기울기 : ",line_fitter.coef_)
print("절편 : ",line_fitter.intercept_)

print("30일뒤 예상 가격 : ",line_fitter.predict([[269]]))
#print("훈련세트 점수: {:.2f}".format(line_fitter.score(X_train,y_train)))
#print("테스트세트 점수: {:.2f}".format(line_fitter.score(X_test,y_test)))

plt.show()