import community
import numpy
import networkx as nx

def groupGraph(G, userNodeId):
    """docstring for groupGraph"""
    Gc = nx.Graph(G)
    Gc.remove_node(userNodeId)
    partition = community.best_partition(Gc)
    for nodes in partition.keys():
        G.node[nodes]['group'] = partition[nodes]
    return G