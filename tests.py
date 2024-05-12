import networkx as nx
from matplotlib import pyplot as plt

# Create an empty graph
G = nx.Graph()

# Define a node as a tuple
node = [(1.3,2.4), (-4.3,-5.2)]
print("is executing")
# Add the tuple as a node
G.add_nodes_from(node)

nx.draw_networkx(G)
plt.show()