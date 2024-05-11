from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import csv

from raw_graph import plot_csv

def cluster(n: int)-> list[tuple[int, int]]:
    """Donat un dataframe amb coordenades i un enter n, retorna les 
    coordenades del cluster amb n coordenades"""
    x: list[float] = []
    y: list[float] = []
    with open('ebre3.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    # de martí: jo aquí faria
    # coords = [(x, y) for x, y, _, _ in data]
    for punt in data:
        x.append(float(punt[0]))
        y.append(float(punt[1]))
    plt.scatter(x, y, color='black', s=1)
    plt.show()
    coords = list(zip(x, y))
    kmeans = KMeans(n_clusters=n, random_state=0, n_init="auto").fit(coords)
    print(kmeans.cluster_centers_)
    x_cl, y_cl = zip(*kmeans.cluster_centers_)
    plt.scatter(x_cl, y_cl, color='black', s=1)
    plt.show()


    # x_lst = df['x'].tolist() #TODO: Veure si val la pena el .tolist()
    # y_lst = df['y'].tolist()
    # points = list(zip(x_lst, y_lst))
    # kmeans = KMeans(n_clusters=n, random_state=0, n_init="auto").fit(points) #el 100 és subject to change
    # labels = kmeans.labels_ #Gives a number for every cluster
    # df['cluster'] = labels
    # df.to_csv("ebre_clusters.csv", index=False, sep=" ")
    # x_clustered, y_clustered = zip(*kmeans.cluster_centers_)
    # plt.plot(x_clustered, y_clustered, 'ko', markersize=1)
    # df_clustered = pd.DataFrame()
    # df_clustered['x'] = x_clustered
    # df_clustered['y'] = y_clustered
    # df_clustered['num'] = [i for i in range(n)]
    # plot_csv(df)
    # plot_csv(df_clustered)
    # return df_clustered

def main() -> None:
    new_df = cluster(100)
    print("clusters returned")
    print(new_df)

if __name__ == "__main__":
    main()