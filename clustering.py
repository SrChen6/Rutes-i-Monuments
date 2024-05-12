from sklearn.cluster import KMeans
import csv
import plotter

def cluster(n: int)-> list[tuple[float, float]]:
    """Donat un dataframe amb coordenades i un enter n, afegeix una columna
    al dataframe corresponent al label del cluster"""
    with open('ebre3.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    coords = [(float(x), float(y)) for x, y, _ in data]

    # x, y = zip(*coords)
    # plotter.plot_lists(x, y)

    kmeans = KMeans(n_clusters=n, random_state=0, n_init="auto").fit(coords)

    # for i in range(len(data)):
    #     data[i].append(kmeans.labels_[i])
    # with open('ebre_clusters.csv', 'w', newline='') as f:
    #     writer =csv.writer(f)
    #     writer.writerows(data)

    # x_cl, y_cl = zip(*kmeans.cluster_centers_)
    # plotter.plot_lists(x_cl, y_cl)
    return kmeans.cluster_centers_.tolist()
    

def main() -> None:
    new_df = cluster(100)
    print("clusters returned")

if __name__ == "__main__":
    main()