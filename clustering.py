import pandas as pd
from pandas import DataFrame
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

from raw_graph import plot_csv

def cluster(df: DataFrame, n: int)-> DataFrame:
    """Donat un dataframe amb coordenades i un enter n, retorna les 
    coordenades del cluster amb n coordenades"""
    x_lst = df['x'].tolist() #TODO: Veure si val la pena el .tolist()
    y_lst = df['y'].tolist()
    points = list(zip(x_lst, y_lst))
    kmeans = KMeans(n_clusters=n, random_state=0, n_init="auto").fit(points) #el 100 és subject to change
    labels = kmeans.labels_ #Gives a number for every cluster
    df['cluster'] = labels
    df.to_csv("ebre_clusters.csv", index=False, sep=" ")
    x_clustered, y_clustered = zip(*kmeans.cluster_centers_)
    plt.plot(x_clustered, y_clustered, 'ko', markersize=1)
    df_clustered = pd.DataFrame()
    df_clustered['x'] = x_clustered
    df_clustered['y'] = y_clustered
    df_clustered['num'] = [i for i in range(n)]
    plot_csv(df)
    plot_csv(df_clustered)
    return df_clustered

def main() -> None:
    df = pd.read_csv("ebre2.csv", sep=" ", header=0)
    new_df = cluster(df, 100)
    print("dataframe returned")
    new_df.to_csv("clusters.csv", sep=" ", index=False)
    

if __name__ == "__main__":
    main()