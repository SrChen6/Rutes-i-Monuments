import pandas as pd
from pandas import DataFrame
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

def cluster(df: DataFrame, n: int)-> DataFrame:
    """Donat un dataframe amb coordenades i un enter n, retorna les 
    coordenades del cluster amb n coordenades"""
    x_lst = df['x'].tolist()
    y_lst = df['y'].tolist()
    points = list(zip(x_lst, y_lst))
    kmeans = KMeans(n_clusters=n, random_state=0, n_init="auto").fit(points) #el 100 és subject to change
    x_clustered, y_clustered = zip(*kmeans.cluster_centers_)
    plt.plot(x_clustered, y_clustered, 'ko', markersize=1)
    #TODO: acabar aquesta funció tal que retorni el dataframe del clustered

def main() -> None:
    df = pd.read_csv("ebre.csv", sep=" ", header=0)
    cluster(df, 100)

if __name__ == "__main__":
    main()