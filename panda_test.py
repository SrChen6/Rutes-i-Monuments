import pandas as pd
from yogi import read
df = pd.DataFrame([], columns=['x', 'y', 't', 's'])
series = pd.Series([9.0,8.0,7.0,6.0], index=df.columns)
df.loc[len(df.index)] = series
print(df)
while True:
    df.loc[len(df.index)] = [1.0, 2.0, 3.0, 4.0]
    if len(df.index) > 100:
        df.to_csv("data.csv", sep=" ", header=False, index=False)
        break
