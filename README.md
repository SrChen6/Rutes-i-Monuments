# Rutes-i-Monuments
Made by: Martí Gil, Haokang Chen

## Description
These programs are the [second task for Algoritmics and Programming II](https://github.com/jordi-petit/ap2-rutes-i-monuments-2024).

The project consists in obtaining information about routes in a certain region that hikers upload to the web to then create a graph of the common paths taken by all of them. Furthermore, there is an option to look for nearby monuments and find the shortest path to get there from a certain location. All of these graphs will be exported to a PNG and a KML file that the user can upload to [Google Earth](https://www.google.es/intl/es/earth/index.html).

The routes are downloaded from [OpenStreetMap](https://www.openstreetmap.org/#map=12/41.3823/2.1279) and the monuments are imported from [Catalunya Medieval](https://www.catalunyamedieval.es/). 

All the graph processing is done with [NetworkX](https://networkx.org/documentation/stable/tutorial.html). The exportations are done with [StaticMap](https://github.com/komoot/staticmap/blob/master/README.md) for the PNG file and [Simplekml](https://simplekml.readthedocs.io/en/latest/) for the KML file.


## Requirements

Install "import" library stubs

``
pip install types-requests
``

Install "staticmaps" library stubs
``


## Development decisions