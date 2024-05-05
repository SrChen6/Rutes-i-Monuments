import pandas as pd
from yogi import read
df = pd.read_csv('ebre.csv', sep=" ", header=0)
print(df[df['s'] == 2])
x_lst = df['x'].tolist()
# print(x_lst)