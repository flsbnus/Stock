import pandas as pd
x=[]
for i in range(0,204):
    x.append(i)

print(x)
column=['xf']
df=pd.DataFrame(x,columns=column)
print(df)
df=df.rename(columns={'0':'xf'})
print(df)