import requests
import gpxpy

#TODO: canviar el nom del csv tal que sigui més flexible

def importer(box: str) -> None:
    """Donades unes coordenades en la forma esquina inferior dret, esquina
    esquina superior esquerra, descarreva el .csv amb les dades:
    longitud, latitud, temps, nombre de ruta"""
    num_seg = 0
    started = False
    page = 0
    f = open("ebre.csv", "w")
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
                        f.write(f"{p1.longitude},{p1.latitude},{num_seg}")
                        f.write("\n")
                num_seg += 1
        print(f"finished importing page {page}")                
        page += 1
        #TODO: passar la llista a csv

    print("finished importing")
    f.close()

def main() -> None:
    BOX_EBRE = "0.5739316671,40.5363713,0.9021482,40.79886535"
    importer(BOX_EBRE)


if __name__ == "__main__":
    main()