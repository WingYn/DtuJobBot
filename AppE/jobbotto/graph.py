import webapp2
import community
import numpy
import graphAnalys as ga
import networkx as nx
from django.utils import simplejson as json
from networkx.readwrite import json_graph

class MainHandler(webapp2.RequestHandler): 
     
    def get(self):
        G=nx.read_graphml('g.xml')
        for n in G.nodes():
            G.node[n]['name'] = n
        #jsonGraph = json.dumps(dict(nodes=[G.node[n] for n in G.nodes()],links=[{'source':u,'target':v, 'value':1} for u,v in G.edges()]))
        #G = MainHandler.findCommunity(self, G, 'Sin')
        G = ga.groupGraph(G, 'Sin')    
        jsonGraph = json_graph.dumps(G)
        self.response.out.write("""<!DOCTYPE html>
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

var width = 960,
    height = 500;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-120)
    .linkDistance(30)
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
      .call(force.drag);

  node.append("title")
      .text(function(d) { return d.name; });

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  });
}

drawG(jsonGraph);

</script>""" % jsonGraph)
        
app = webapp2.WSGIApplication([
    ('/graph', MainHandler)
], debug=True)
