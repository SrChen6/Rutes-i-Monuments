# Rutes-i-Monuments
Made by: Martí Gil, Haokang Chen

## Description
These programs are the [second task for Algoritmics and Programming II](https://github.com/jordi-petit/ap2-rutes-i-monuments-2024).

The project consists in obtaining information about routes in a certain region that hikers upload to the web to then create a graph of the common paths taken by all of them. Furthermore, there is an option to look for nearby monuments and find the shortest path to get there from a certain location. All of these graphs will be exported to a PNG and a KML file that the user can upload to [Google Earth](https://www.google.es/intl/es/earth/index.html).

The routes are downloaded from [OpenStreetMap](https://www.openstreetmap.org/#map=12/41.3823/2.1279) and the monuments are imported from [Catalunya Medieval](https://www.catalunyamedieval.es/). 

All the graph processing is done with [NetworkX](https://networkx.org/documentation/stable/tutorial.html). The exportations are done with [StaticMap](https://github.com/komoot/staticmap/blob/master/README.md) for the PNG file and [Simplekml](https://simplekml.readthedocs.io/en/latest/) for the KML file.

Mode details about the implementation will be given in [Development](#development).

## Requirements

This project uses the following python libraries:
- [requests](https://pypi.org/project/requests/): to request importations from the web.
- [gpxpy](https://pypi.org/project/gpxpy/): to import the gpx data from OpenStreetMap.
- [csv](https://docs.python.org/3/library/csv.html): to read and write .csv files.
- [staticmap](https://developers.google.com/maps/documentation/maps-static/overview?hl=es-419): to export the graph to a PNG file.
- [networkx](https://networkx.org/documentation/stable/reference/index.html): to create and edit graphs.
- [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html): to create clusters on the graph.
- [haversine](https://pypi.org/project/haversine/): To calculate distances on Earth's surface.
- [simplekml](https://simplekml.readthedocs.io/en/latest/): do create a kml file.

Furthermore, some library stubs should be installed to minimize the errors that `Mypy` detects. Some of them are the following:

**AQUI FALTA ACABAR DE TROBAR LES LIBRARY STUBS**



Install "import" library stubs

``
pip install types-requests
``

Install "staticmaps" library stubs
``

## Usage

To start the program, please enter the command `python3 main.py` in your terminal. The following text should appear:

**AQUI FALTA UNA IMATGE DEL TERMINAL**

Now, a set of real numbers have to be written. They correspond to the latitude and longitude of the west, south, east and north boundaries of the region that will be worked on. For example, for _Girona_, these numbers are **`AQUI FALTEN ELS NUMEROS PER GIRONA`**

After writing a name for this region, an image will appear that shows the most common routes that hikers take. This image will be automatically saved in the folder along with a KML file. This KML file can be uploaded to [Google Earth](https://www.google.es/intl/es/earth/index.html) following [these steps](https://support.google.com/mymaps/answer/3024836?hl=en&co=GENIE.Platform%3DDesktop).

**AQUI FALTA UNA IMATGE D'EXEMPLE DE PNG I KML**

Finally, the user will be asked if he wants the location of the nearby monuments along with the shortest path to get there. As before, an image will appear which contains a dot with the user's location, the location of some nearby monuments and a route to get to them.

**AQUI FALTA UNA IMATGE DELS MONUMENTS**


## Development

### Storing data

The data imported form [OpenStreetMap](https://www.openstreetmap.org/#map=12/41.3823/2.1279) will be stored in a `.csv` file, and all it's treatments will be done with the module [segments.py](segments.py).

### Graph making



**FALTEN COSETES**

### Exporting to PNG
One must imagine Sisyphus happy.

### Exporting to KML
One must imagine Sisyphus happy.

### Downloading monuments
One must imagine Sisyphus happy.

### Showing monument paths
One must imagine Sisyphus happy.
