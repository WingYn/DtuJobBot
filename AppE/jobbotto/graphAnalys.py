import community
import numpy
import networkx as nx
import operator
from networkx.readwrite import json_graph

def groupGraph(G, userNodeId):
    """docstring for groupGraph"""
    G.node[userNodeId]['group'] = 0
    Gc = nx.Graph(G)
    Gc.remove_node(userNodeId)
    
    if len(Gc.edges()) < 1:
        partition = {}
        for n in Gc.nodes():
            partition[n] = 1
    else:
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
            bm, cm, dm = CentralityNoself(SG)
            G.node[bm]['central'] =  1
            #G.node[em]['central'] =  2
            G.node[cm]['central'] =  3
            G.node[dm]['central'] =  4
            
    return G, len(set(partition.values()))
    
def CentralityNoself(G):
    """docstring for Centrality"""
    
    b = nx.betweenness_centrality(G)
    #e = nx.eigenvector_centrality_numpy(G)
    c = nx.closeness_centrality(G)
    d = nx.degree_centrality(G)

    #get the max value
    bm = max(b.iteritems(), key=operator.itemgetter(1))[0]
    #em = max(e.iteritems(), key=operator.itemgetter(1))[0]
    cm = max(c.iteritems(), key=operator.itemgetter(1))[0]
    dm = max(d.iteritems(), key=operator.itemgetter(1))[0]
    
    return bm, cm, dm#em, cm, dm
    
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
    
def DrawGraph(G, userNodeId):
    #her
    #userNodeId = 'Sin'
    #G=nx.read_graphml('newGraph.xml')
    G = G.to_undirected()
         
    for n in G.nodes():
        G.node[n]['name'] = n
        G.node[n]['central'] = 0
        
            #jsonGraph = json.dumps(dict(nodes=[G.node[n] for n in G.nodes()],links=[{'source':u,'target':v, 'value':1} for u,v in G.edges()]))
    #G = MainHandler.findCommunity(self, G, 'Sin')
        
    G, numOfGroups = groupGraph(G, userNodeId)
    bm, em, cm, dm = Centrality(G, userNodeId)

        
    G.node[bm]['central'] =  1
    G.node[em]['central'] =  2
    G.node[cm]['central'] =  3
    G.node[dm]['central'] =  4
        
    jsonGraph = json_graph.dumps(G)
    #self.response.out.write
    return ("""<!DOCTYPE html>
    <meta charset="utf-8">
    <style>

    .node {
      stroke: #fff;
      stroke-width: 1.5px;
    }

    .link {
      stroke: #999;
      stroke-opacity: .6;
    }

    </style>
    <body>
    <script src="http://d3js.org/d3.v3.min.js"></script>
    <script>

    var width = 1000,
        height = 1000;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-500)
        .linkDistance(1)
        .linkStrength(0.6)
        .size([width, height]);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);
    
    var jsonGraph = %s

    function drawG(graph) {
      force
          .nodes(graph.nodes)
          .links(graph.links)
          .start();

      var link = svg.selectAll("line.link")
          .data(graph.links)
          .enter().append("line")
          .attr("class", "link")
          .style("stroke-width", function(d) { return Math.sqrt(d.value); });

      var node = svg.selectAll("circle.node")
          .data(graph.nodes)
          .enter().append("circle")
          .attr("class", "node")
          .attr("r", 5)
          .style("fill", function(d) { return color(d.group); })
          .style("stroke", function(d) { return color(d.group + d.central); })
          .style("stroke-width", "4")
          .call(force.drag);

      node.append("title")
          .text(function(d) { return d.name; });

      force.on("tick", function() {
  
        for (var i=0;i<graph.nodes.length;i++)
        {
            if(graph.nodes[i].group == 0){
                graph.nodes[i].x = width / 2;
                graph.nodes[i].y = height / 2;
            }
        }
  
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) {return d.x; })
            .attr("cy", function(d) {return d.y; });
      });
    }

    drawG(jsonGraph);

    </script>""" % jsonGraph)
    