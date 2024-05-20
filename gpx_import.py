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
    f = open("girona.csv", "w")
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

    print("finished importing")
    f.close()

def main() -> None:
    BOX = "2.7359,41.9199,2.9031,42.0350"
    importer(BOX)

if __name__ == "__main__":
    main()