from segments import Point, Box
from haversine import haversine

box = Box(Point(40.5363713, 0.5739316671, -1),
          Point(40.79886535, 0.9021482, -1))

width = haversine((box.bottom_left.lat, box.bottom_left.lon),
                  (box.bottom_left.lat, box.top_right.lon))
height = haversine((box.bottom_left.lat, box.bottom_left.lon),
                   (box.top_right.lat, box.bottom_left.lon))

print(width * height)