import pandas as pd
from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
columns = ["Name", "Marks"]
df = pd.read_csv("ebre.csv", sep=" ", header=0)
x_lst = df['x'].tolist()
y_lst = df['y'].tolist()
plt.plot(x_lst, y_lst, 'ro', markersize=1)
plt.show()
