import pandas as pd
from yogi import read
df = pd.read_csv('data.csv', sep=" ", header=0)
print(df['x'])
