import pandas as pd
from yogi import read

df = pd.DataFrame([[1.0, 2.0, 3.0, 4.0] for _ in range(3)], columns=['x', 'y', 't', 's'], dtype='float')
series = pd.Series(pd.Series([9.0,8.0,7.0,6.0], index=df.columns, dtype='float'))
df = df.append(series, ignore_index=True)
print(df.tail())