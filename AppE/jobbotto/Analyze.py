import os
import re
import networkx as nx
import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np
import pylab as P
import community



def reFormatFile(File):
    """docstring for reFormatFile"""
    links = []
    comun = {}
    G = nx.Graph()
    f1 = open(File, 'r')
    #f2 = open(File + 'cytoscape.txt', 'w')
    #f2.write('gruppe')
    for line in f1:
        g = re.findall(r'.+\t.+\t([0-9]+)',line)[0]
        c = comun.get(g, 0)
        c = c + 1
        comun[g] = c
    
    f1.close()
    for t in comun.keys():
            if comun[t] < 3:
                   del(comun[t])
    f1 = open(File, 'r')
    for line in f1:
        print('lol')
        fromNode = re.findall(r'(.+)\t[^0-9]+.*\t[0-9]+',line)[0]
        toNode = re.findall(r'.+\t(.+)\t[0-9]+',line)[0]
        g = re.findall(r'.+\t.+\t([0-9]+)',line)[0]
        if g in comun.keys():
            G.add_edge(fromNode,toNode, gruppe=int(g))
        
        
    f1.close()
    
    return G, comun
   
def linkclustering():
    """docstring for link-clustering"""

    D, dd= reFormatFile('edgeList_D_maxS0.257143_maxD0.112986.edge2comm.txt')
    M, mm = reFormatFile('edgeList_M_maxS0.250000_maxD0.109111.edge2comm.txt')

    return M, mm, D, dd

def make_A_and_Au(G):
    """docstring for fname"""
    A = G
    Au = A.to_undirected(reciprocal=True)
    return A, Au
    
def subNetworks(Au):
    """docstring for subNetworks"""
    M = Au.subgraph([w for w in Au if Au.node[w]['com'] == 'Marvel'])
    D = Au.subgraph([w for w in Au if Au.node[w]['com'] == 'DC'])
    return M, D
    
    
def MvsD(A, Au, M, D):
    """docstring for MvsD"""
    #Calculate the number of nodes
    print("Number of nodes in A  : " + str(len(A.nodes())))
    print("Number of nodes in Au : " + str(len(Au.nodes())))
    #Calculate the number of links
    print("Number of links in A  : " + str(len(A.edges())))
    print("Number of links in Au : " + str(len(Au.edges())))
    t = nx.average_clustering(Au)
    print("network clustering coefficient for Au : " + str(t))
    print("")
    #Calculate the number of nodes
    print("Number of nodes in M  : " + str(len(M.nodes())))
    print("Number of nodes in D : " + str(len(D.nodes())))
    t = nx.average_clustering(M)
    print("network clustering coefficient for M  : " + str(t))
    t = nx.average_clustering(D)
    print("network clustering coefficient for D : " + str(t))
    
    
    MavgD = float(sum(M.degree().values()))/float(len(M.nodes()))
    print("Connectivity M : " + str(MavgD))
    DavgD = float(sum(D.degree().values()))/float(len(D.nodes()))
    print("Connectivity D : " + str(DavgD))
    
    pass
    
def Degreedistribution(A, Au):
    """docstring for Degreedistribution"""
    
    # fig = plt.figure()
    # ax = fig.add_subplot(111)
    # n, bins, patches = ax.hist(Au.degree().values(), 50, normed=1, facecolor='green', alpha=0.75)
    # 
    # bincenters = 0.5*(bins[1:]+bins[:-1])
    # 
    # ax.set_xlabel('Degrees')
    # ax.set_ylabel('Probability')
    # #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
    # ax.set_xlim(0, 50)
    # ax.set_ylim(0, 0.25)
    # ax.grid(True)
    # 
    # plt.show()
    
    AuDegrees = {}
    for d in Au.degree().values():
        c = AuDegrees.get(d, 0)
        c = c + 1
        AuDegrees[d] = c
        
    x0 = Au.degree().values()
    x1 = A.in_degree().values()
    x2 = A.out_degree().values()
    
    print(str(sum(x0)))
    P.figure()
    
    n, bins, patches = P.hist( [x0, x1,x2], 20, histtype='bar')
    #P.xlim([0, 200])
    #P.ylim([0, 0.5])
    P.show()
    
    return AuDegrees
    
def Centrality(Au):
    """docstring for Centrality"""
    b = nx.betweenness_centrality(Au)
    e = nx.eigenvector_centrality_numpy(Au)
    c = nx.closeness_centrality(Au)
    d = nx.degree_centrality(Au)
    return b, e, c, d

def ironspiderbatsuper(A, Au):
    """docstring for ironspiderbatsuper"""
    print "& Iron_Man 	& Spider-Man 	& Batman & Superman	\\"
    i =   Au.degree()['Iron Man']
    s =   Au.degree()['Spider-Man']
    b =   Au.degree()['Batman']
    su =  Au.degree()['Superman']
    
    print 'Au degree & ' + str(i) + ' & '+ str(s) + ' & '+ str(b) + ' & '+ str(su) + ' \\'
                     
    i =   A.in_degree()['Iron Man']
    s =   A.in_degree()['Spider-Man']
    b =   A.in_degree()['Batman']
    su =  A.in_degree()['Superman']
    
    print 'A in degree & ' + str(i) + ' & '+ str(s) + ' & '+ str(b) + ' & '+ str(su) + ' \\'
    
    i =   A.out_degree()['Iron Man']
    s =   A.out_degree()['Spider-Man']
    b =   A.out_degree()['Batman']
    su =  A.out_degree()['Superman']
    
    print 'A out degree & ' + str(i) + ' & '+ str(s) + ' & '+ str(b) + ' & '+ str(su) + ' \\'
    pass
    
def fname(b, e, c, d):
    """docstring for fname"""
    max1 = max2 = max3 = 0
    maxk1 = maxk2 = maxk3 = ''
    for k in b:
        v = b[k]
        if v > max1:
            max1 = v
            maxk1 = k
    
    mb = maxk1 + ' : ' + str(max1)
    max1 = max2 = max3 = 0
    maxk1 = maxk2 = maxk3 = ''
    for k in e:
        v = e[k]
        if v > max1:
            max1 = v
            maxk1 = k
    me = maxk1 + ' : ' + str(max1)
    max1 = max2 = max3 = 0
    maxk1 = maxk2 = maxk3 = ''
    for k in c:
        v = c[k]
        if v > max1:
            max1 = v
            maxk1 = k
    
    mc = maxk1 + ' : ' + str(max1)
    max1 = max2 = max3 = 0
    maxk1 = maxk2 = maxk3 = ''
    for k in d:
        v = d[k]
        if v > max1:
            max1 = v
            maxk1 = k
    
    md = maxk1 + ' : ' + str(max1)

    print mb +' & ' + me +' & ' + mc +' & '+ md +' \\\\'
    pass
    
def edgeListToFile(M, D):
    """docstring for edgeListToFile"""
    f = open('edgeList_M.txt','w')
    for g in M.edges():
        f.write(g[0] + '\t' + g[1] +'\n')
        
    f.close()
    
    f = open('edgeList_D.txt','w')
    for g in D.edges():
        f.write(g[0] + '\t' + g[1] +'\n')
        
    f.close()
    
    pass
    
def partitionToFile(G):
    """docstring for partitionToFile"""
    G = nx.connected_component_subgraphs(Au)[0]
    partition = community.best_partition(G)
    
    f = open('nodeAtt.txt','w')
    for g in G.edges():
        f.write(g + '\t=\t' + str(partition[g]) + '\n')
        
    f.close()

    pass
    
def partition(G):
    partition = community.best_partition(G)
    gp = {}
    for i in partition.values():
        c = gp.get(i, 0)
        c = c + 1
        gp[i] = c
    rg = {}    
    for i in gp.keys():
        if gp[i] < 6:
               del(gp[i])
               rg[i] = 1
               
    for i in partition.keys():
        if partition[i] in rg:
            del(partition[i])
            
    return partition, gp, rg
    
def reDoNetworkBasedOnEdges(G):
    gp = {}
    for e in G.edges():
        i = G.edge[e]['gruppe']
        c = gp.get(i, 0)
        c = c + 1
        gp[i] = c
    
    for i in gp.keys():
        if gp[i] < 6:
               del(gp[i])
               
    for e in G.edges():
        i = G.edge[e]['gruppe']
        if i not in gp:
            G.remove
    return G

def anyInWronGroupe(Au, partition):
    gp = {}
    for i in partition.keys():
        c = gp.get(partition[i], [])
        c.append(i)
        gp[partition[i]] = c
        
    for i in gp:
        t = gp[i][0]
        for n in gp[i]:
            if Au.node[t]['com'] != Au.node[n]['com']:
                print(str(i) + ' ' + t +' : '+ Au.node[t]['com'] + '  ;: ' + n + ' : ' + Au.node[n]['com'] )
    
    pass
def lol():
    """docstring for lol"""
    gColor = [
          '#0000FF','#FAEBD7','#00FFFF','#7FFFD4','#F5F5DC','#FFE4C4',
          '#FFEBCD','#8A2BE2','#A52A2A','#DEB887','#5F9EA0','#7FFF00','#D2691E','#FF7F50','#6495ED',
          '#DC143C','#00FFFF','#00008B','#008B8B','#B8860B','#A9A9A9','#006400','#BDB76B','#8B008B','#556B2F',
          '#FF8C00','#9932CC','#8B0000','#E9967A','#8FBC8F','#483D8B','#2F4F4F','#00CED1','#9400D3','#FF1493',
          '#00BFFF','#696969','#1E90FF','#B22222','#228B22','#FF00FF','#DCDCDC','#E0E0E0','#FFD700',
          '#DAA520','#808080','#008000','#ADFF2F','#CC5500','#FF69B4','#CD5C5C','#4B0082','#F0E68C',
          '#E6E6FA','#7CFC00','#ADD8E6','#F08080','#E0FFFF','#FAFAD2','#D3D3D3','#90EE90',
          '#FFB6C1','#FFA07A','#20B2AA','#87CEFA','#778899','#B0C4DE','#00FF00','#32CD32','#FAF0E6',
          '#FF00FF','#800000','#66CDAA','#0000CD','#BA55D3','#9370D8','#3CB371','#7B68EE','#00FA9A','#48D1CC',
          '#C71585','#191970','#FFE4E1','#FFE4B5','#FFDEAD','#000080','#FDF5E6','#808000','#6B8E23',
          '#FFA500','#FF4500','#DA70D6','#EEE8AA','#98FB98','#AFEEEE','#D87093','#FFEFD5','#FFDAB9','#CD853F',
          '#FFC0CB','#DDA0DD','#B0E0E6','#800080','#BC8F8F','#4169E1','#8B4513','#FA8072','#F4A460','#2E8B57',
          '#A0522D','#C0C0C0','#87CEEB','#6A5ACD','#708090','#00FF7F','#4682B4','#D2B48C',
          '#008080','#D8BFD8','#FF6347','#40E0D0','#EE82EE','#F5DEB3','#A86363','#F5F5F5','#9ACD32',
          ]
          
    G = nx.Graph()
    G.add_nodes_from(gColor)
    pos = nx.spring_layout(G)
    for n in G.nodes():
        nx.draw_networkx_nodes(G, pos, [n], node_size = 500,
                                          node_color = n)
        
    nx.draw_networkx_labels(G,pos, font_size = 8)
    plt.show()          
    pass
    
def drawGCommunity(G,pm ):
    """docstring for drawGCommunity"""
    gColor = [
          '#0000FF','#FAEBD7','#00FFFF','#7FFFD4','#F5F5DC','#FFE4C4',
          '#FFEBCD','#8A2BE2','#A52A2A','#DEB887','#5F9EA0','#7FFF00','#D2691E','#FF7F50','#6495ED',
          '#DC143C','#00FFFF','#00008B','#008B8B','#B8860B','#A9A9A9','#006400','#BDB76B','#8B008B','#556B2F',
          '#FF8C00','#9932CC','#8B0000','#E9967A','#8FBC8F','#483D8B','#2F4F4F','#00CED1','#9400D3','#FF1493',
          '#00BFFF','#696969','#1E90FF','#B22222','#228B22','#FF00FF','#DCDCDC','#E0E0E0','#FFD700',
          '#DAA520','#808080','#008000','#ADFF2F','#CC5500','#FF69B4','#CD5C5C','#4B0082','#F0E68C',
          '#E6E6FA','#7CFC00','#ADD8E6','#F08080','#E0FFFF','#FAFAD2','#D3D3D3','#90EE90',
          '#FFB6C1','#FFA07A','#20B2AA','#87CEFA','#778899','#B0C4DE','#00FF00','#32CD32','#FAF0E6',
          '#FF00FF','#800000','#66CDAA','#0000CD','#BA55D3','#9370D8','#3CB371','#7B68EE','#00FA9A','#48D1CC',
          '#C71585','#191970','#FFE4E1','#FFE4B5','#FFDEAD','#000080','#FDF5E6','#808000','#6B8E23',
          '#FFA500','#FF4500','#DA70D6','#EEE8AA','#98FB98','#AFEEEE','#D87093','#FFEFD5','#FFDAB9','#CD853F',
          '#FFC0CB','#DDA0DD','#B0E0E6','#800080','#BC8F8F','#4169E1','#8B4513','#FA8072','#F4A460','#2E8B57',
          '#A0522D','#C0C0C0','#87CEEB','#6A5ACD','#708090','#00FF7F','#4682B4','#D2B48C',
          '#008080','#D8BFD8','#FF6347','#40E0D0','#EE82EE','#F5DEB3','#A86363','#F5F5F5','#9ACD32',
          ]
    
    count = 0
    for c in pm.keys():
        pm[c] = gColor[count]
        count = count + 1
    #first compute the best partition
    #drawing
    pos = nx.spring_layout(G)

    for e in G.edges() :
        nx.draw_networkx_edges(G, pos, [e], width = 4,
                                    edge_color = pm[str(G.edge[e[0]][e[1]]['gruppe'])])
    
    supN = 'Superman'
    restN = []
    for n in G.nodes():
        if n == 'Superman':
            supN = n
        else:
            restN.append(n)
            
    nx.draw_networkx_nodes(G, pos, [supN], node_size = 30,
                                node_color = '#f8f8ff')
    nx.draw_networkx_nodes(G, pos, restN, node_size = 10,
                                node_color = '#000000')
    plt.show()
    return
#Basic stats. Calculate the number of nodes, links (in both directed and undirected networks), network clustering coefficient for the superhero network. What are the differences between the two networks A and Au? What does the results tell you about reciprocity? Use M and D to explain which fantasy universe is bigger, and which is better connected; explain your answers.