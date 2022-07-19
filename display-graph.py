import networkx as nx
from pyvis.network import Network
import json
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--graph", default="graph.json", type=str,
                    help="path to the json file for the graph")
args = parser.parse_args()
data = json.load(open(args.graph, "r"))
G = nx.Graph(data)
print(G)
net = Network(notebook=False)
net.from_nx(G)
net.show("example.html")
