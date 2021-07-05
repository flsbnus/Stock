import pandas as pd
import matplotlib
import sklearn


df = pd.read_csv("economy.csv", parse_dates =["date"], index_col ="date")
df = df.dropna()
df.head()
df.info