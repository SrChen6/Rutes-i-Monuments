import pandas as pd
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

df = pd.read_csv("ebre.csv", sep=" ", header=0)

x_lst = df['x'].tolist()
y_lst = df['y'].tolist()
points = list(zip(x_lst, y_lst))
kmeans = KMeans(n_clusters=100, random_state=0, n_init="auto").fit(points)
x_clustered, y_clustered = zip(*kmeans.cluster_centers_)
plt.plot(x_clustered, y_clustered, 'ko', markersize=1)
plt.show()
