from matplotlib import pyplot as plt

def main() -> None:
    coord = pd.read_csv("ebre_clusters.csv", sep=" ", header=0)
    clust = pd.read_csv("clusters.csv", sep=" ", header=0)
    #TODO: crear una funció que, donats unes coords i uns clusters, retorni els camins que uneixen clusters