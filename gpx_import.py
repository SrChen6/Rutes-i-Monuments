import requests
import gpxpy
import pandas as pd


BOX_EBRE = "0.5739316671,40.5363713,0.9021482,40.79886535"

page = 0
datos = pd.DataFrame([], columns=['x', 'y', 't', 's'])
df = pd.DataFrame(datos, dtype=float)
num_seg = 0

started = False
while True:
    url = f"https://api.openstreetmap.org/api/0.6/trackpoints?bbox={BOX_EBRE}&page={page}"
    response = requests.get(url)
    gpx_content = response.content.decode("utf-8")
    gpx = gpxpy.parse(gpx_content)

    if len(gpx.tracks) == 0:
        break
    for track in gpx.tracks:
        for segment in track.segments:
            if all(point.time is not None for point in segment.points):
                segment.points.sort(key=lambda p: p.time)  # type: ignore
                for i in range(len(segment.points) - 1):
                    p1, p2 = segment.points[i], segment.points[i + 1]
                    if not started:
                        print("started importing")
                        started= True
                    df.loc[len(df.index)] = pd.Series([p1.longitude, p1.latitude, p1.time, num_seg], index=df.columns)
        num_seg += 1
    print(f"finished importing page {page}")                
    page += 1
    df.to_csv("ebre.csv", sep=" ", index=False)
print("finished importing")
    
#this was written in main branch