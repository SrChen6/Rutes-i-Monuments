import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("ebre.csv", sep=" ", header=0)
x_lst = df['x'].tolist()
y_lst = df['y'].tolist()
plt.plot(x_lst, y_lst, 'ko', markersize=1)
plt.show()
