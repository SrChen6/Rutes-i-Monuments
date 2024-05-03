import requests
import gpxpy

BOX_EBRE = "0.5739316671,40.5363713,0.9021482,40.79886535"

page = 0

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
                    print(p1.latitude, p1.longitude, p1.time, "-", p2.latitude, p2.longitude, p2.time)
    page += 1