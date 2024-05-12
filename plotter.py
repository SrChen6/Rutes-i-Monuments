import csv
from matplotlib import pyplot as plt

def plot_csv() -> None:
    """Donat un dataframe, retorna el graf de les coordenades"""
    x: list[float] = []
    y: list[float] = []
    with open('ebre3.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    for punt in data:
        x.append(float(punt[0]))
        y.append(float(punt[1]))
    plt.scatter(x, y, color='black', s=1)
    plt.axis('off')
    # plt.savefig(f"C:{Directori}/Ruta{num_ruta}") #Per si es vol auto-save
    plt.show()

def plot_lists(x: list[float], y: list[float]) -> None:
    plt.scatter(x, y, color='black', s=1)
    plt.show()

def main() -> None:
    plot_csv()

if __name__ == "__main__":
    main()