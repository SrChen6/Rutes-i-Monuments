import simplekml
import path_builder

G = path_builder.cluster_paths()

kml = simplekml.Kml()

kml.newpoint(name="UPC", coords=[(2.112347, 41.388725)])

lin = kml.newlinestring(
    name="Camí",
    description="Un caminet per la UPC",
    coords=[
        (2.11117435152314, 41.3872344661771),
        (2.112543023293298, 41.38807192338636),
        (2.113186629350088, 41.3877564559475),
        (2.113580383823295, 41.38790501339351),
        (2.113638683576819, 41.38819670380168),
        (2.113130671445338, 41.3884676474094),
        (2.114012520479633, 41.38919524414038),
        (2.112873821172967, 41.39003242064307),
        (2.109970958003426, 41.38801346749829),
        (2.11117435152314, 41.3872344661771),
    ],
)
lin.style.linestyle.color = "ff0000ff"  # Red
lin.style.linestyle.width = 5

kml.save("upc.kml")