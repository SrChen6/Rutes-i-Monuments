import pandas as pd
from matplotlib import pyplot as plt
from pandas import DataFrame

def plot_csv(df: DataFrame) -> None:
    """Donat un dataframe, retorna el graf de les coordenades"""
    x_lst = df['x'].tolist()
    y_lst = df['y'].tolist()
    plt.scatter(x_lst, y_lst, color='black', s=1)
    plt.axis('off')
    # plt.savefig(f"C:{Directori}/Ruta{num_ruta}") #Per si es vol auto-save
    plt.show()


def main() -> None:
    df = pd.read_csv("ebre.csv", sep=" ", header=0)
    plot_csv(df)

if __name__ == "__main__":
    main()