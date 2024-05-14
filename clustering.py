from sklearn.cluster import KMeans
import csv
import plotter

def cluster(n: int)-> list[tuple[float, float]]:
    """Donat un dataframe amb coordenades i un enter n, afegeix una columna
    al dataframe corresponent al label del cluster"""
    # Llegir CSV
    with open('ebre.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    coords = [(float(x), float(y)) for x, y, _ in data]

    #Clustering
    kmeans = KMeans(n_clusters=n, random_state=0, n_init="auto").fit(coords)

    #Escriure dades
    for i in range(len(data)):
        data[i].append(kmeans.labels_[i])
    with open('ebre_clusters.csv', 'w', newline='') as f:
        writer =csv.writer(f)
        writer.writerows(data)

    return kmeans.cluster_centers_.tolist()
    

def main() -> None:
    new_df = cluster(100)
    x, y = zip(*new_df)
    plotter.plot_lists(x, y)

if __name__ == "__main__":
    main()