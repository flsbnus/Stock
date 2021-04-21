import pandas as pd
import html5lib
from bs4 import BeautifulSoup as bs
import requests

def get_day_list(item_code, page_no):

"""

 일자별 시세를 페이지별로 수집

 """

    url = f"https://finance.naver.com/item/sise_day.nhn?code={item_code}&page={page_no}"

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'}

    response = requests.get(url, headers=headers)
    html = bs(response.text, "lxml")
    table = html.select("table")
    table = pd.read_html(str(table))
    df_day = table[0].dropna()
    return df_day