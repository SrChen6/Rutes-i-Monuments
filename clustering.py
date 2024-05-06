import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv("ebre.csv", sep=" ", header=0)

num_ruta = 6
df = df[df['s'] == num_ruta]
print(df)
x_lst = df['x'].tolist()
y_lst = df['y'].tolist()
points = list(zip(x_lst, y_lst))
kmeans = KMeans(n_clusters=5, random_state=0, n_init="auto").fit(points) #el 100 és subject to change
x_clustered, y_clustered = zip(*kmeans.cluster_centers_)
plt.plot(x_clustered, y_clustered, 'ko', markersize=1) #ko == negre
plt.savefig(f"C:/Users/haoka/vscode/AP2/Projectes/Rutes-i-Monuments/RutesEbre/RutaClust{num_ruta}")
plt.show()
print("Image saved")
   