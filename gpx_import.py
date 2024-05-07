import requests
import gpxpy
import pandas as pd

def importer(box: str) -> None:
    """Donades unes coordenades en la forma esquina inferior dret, esquina
    esquina superior esquerra, descarreva el .csv amb les dades:
    longitud, latitud, temps, nombre de ruta"""
    df = pd.DataFrame([], columns=['x', 'y', 't', 's'])
    num_seg = 0
    started = False
    page = 0
    while True:
        url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={box}&page={page}"
        response = requests.get(url)
        gpx_content = response.content.decode("utf-8")
        gpx = gpxpy.parse(gpx_content)

        if len(gpx.tracks) == 0:
            break
        for track in gpx.tracks:
            for segment in track.segments:
                if all(point.time is not None for point in segment.points):
                    segment.points.sort(key=lambda p: p.time)  # type: ignore
                    for i in range(len(segment.points)):
                        p1 = segment.points[i]
                        if not started:
                            print("started importing")
                            started= True
                        df.loc[len(df)] = pd.Series([p1.longitude, p1.latitude, p1.time, num_seg], index=df.columns)
                num_seg += 1
        print(f"finished importing page {page}")                
        page += 1
        df.to_csv("ebre2.csv", sep=" ", index=False)
    print("finished importing")

def main() -> None:
    BOX_EBRE = "0.5739316671,40.5363713,0.9021482,40.79886535"
    importer(BOX_EBRE)

if __name__ == "__main__":
    main()