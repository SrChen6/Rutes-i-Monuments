import pandas as pd
from yogi import read
df = pd.read_csv('data.csv', sep=" ", header=0)
print(df['x'])
x_lst = df['x'].tolist()
print(x_lst)