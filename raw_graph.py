import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv("ebre.csv", sep=" ", header=0)
num_ruta = 10
df = df[df['s'] == num_ruta]
x_lst = df['x'].tolist()
y_lst = df['y'].tolist()
plt.plot(x_lst, y_lst, 'ko', markersize=1)
plt.savefig(f"C:/Users/haoka/vscode/AP2/Projectes/Rutes-i-Monuments/RutesEbre/Ruta{num_ruta}")
plt.show()
