import pandas as pd
from yogi import read

df = pd.DataFrame([[read(float) for _ in range(4)] for _ in range(3)], columns=['x', 'y', 't', 's'])
df.to_csv("data", sep=" ", columns=False, index=False)
print(df)