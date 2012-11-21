#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import numpy
import networkx as nx

class MainHandler(webapp2.RequestHandler):
    
    
    def get(self):
        G=nx.complete_graph(5)
        Au = G
        b = nx.betweenness_centrality(Au)
        e = nx.eigenvector_centrality_numpy(Au)
        c = nx.closeness_centrality(Au)
        d = nx.degree_centrality(Au)
        self.response.write('dette er en test' + str(G.edges()) + " <\b>" + str(b) + str(e) + str(c) + str(d))
        
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
