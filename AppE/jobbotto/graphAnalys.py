import community
import numpy
import networkx as nx
import operator

def groupGraph(G, userNodeId):
    """docstring for groupGraph"""
    G.node[userNodeId]['group'] = 0
    Gc = nx.Graph(G)
    Gc.remove_node(userNodeId)
    partition = community.best_partition(Gc)
    for nodes in partition.keys():
        G.node[nodes]['group'] = partition[nodes] + 1
    
    #For Connected Sub Graphs
    #Gcc=nx.connected_component_subgraphs(Gc)
    Gcc = []
    for com in set(partition.values()) :
        list_nodes = [nodes for nodes in partition.keys()
                                    if partition[nodes] == com]
        Gcc.append(G.subgraph(list_nodes))
        
    
    for SG in Gcc:
        if len(SG.nodes()) > 3:
            bm, em, cm, dm = CentralityNoself(SG)
            G.node[bm]['central'] =  1
            G.node[em]['central'] =  2
            G.node[cm]['central'] =  3
            G.node[dm]['central'] =  4
            
    return G, len(set(partition.values()))
    
def CentralityNoself(G):
    """docstring for Centrality"""
    
    b = nx.betweenness_centrality(G)
    e = nx.eigenvector_centrality_numpy(G)
    c = nx.closeness_centrality(G)
    d = nx.degree_centrality(G)

    #get the max value
    bm = max(b.iteritems(), key=operator.itemgetter(1))[0]
    em = max(e.iteritems(), key=operator.itemgetter(1))[0]
    cm = max(c.iteritems(), key=operator.itemgetter(1))[0]
    dm = max(d.iteritems(), key=operator.itemgetter(1))[0]
    
    return bm, em, cm, dm
    
def Centrality(G, userNodeId):
    """docstring for Centrality"""
    
    b = nx.betweenness_centrality(G)
    e = nx.eigenvector_centrality_numpy(G)
    c = nx.closeness_centrality(G)
    d = nx.degree_centrality(G)
    
    #remove you self
    b[userNodeId] = 0
    e[userNodeId] = 0
    c[userNodeId] = 0
    d[userNodeId] = 0
    
    #get the max value
    bm = max(b.iteritems(), key=operator.itemgetter(1))[0]
    em = max(e.iteritems(), key=operator.itemgetter(1))[0]
    cm = max(c.iteritems(), key=operator.itemgetter(1))[0]
    dm = max(d.iteritems(), key=operator.itemgetter(1))[0]
    
    return bm, em, cm, dm
    