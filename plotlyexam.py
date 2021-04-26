import plotly.express as px # express 통해서 그리기

df = px.data.iris()
df.head()

fig = px.scatter(df, x="sepal_width", y="sepal_length",
                 hover_data=['petal_width'], # 참고할 데이터 추가
                 title='Iris Data - Scatter Plot' # 그래프 타이틀 지정
                )
fig.show()