#============================================
# File name:      rdf2rdfviz.py
# Author:         Olivier Rey
# Date:           May 12 2019
# License:        GPL v3
# Purpose:        Transforms rdf representations into
#                 representable rdf
#============================================
#!/usr/bin/env python3

import rdflib, getopt, sys, os

from rdf_representations import *
from rdf_utils import *


from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import FOAF, DC


#------------------------------------------ Constants
GA_DOMAIN = "https://github.com/orey/graphapps/graphapps-grammar#"

GA_Node = URIRef(GA_DOMAIN + "Node")
GA_Edge = URIRef(GA_DOMAIN + "Edge")
GA_source = URIRef(GA_DOMAIN + "source")
GA_target = URIRef(GA_DOMAIN + "target")



def add_rdf_graph_to_rdfviz(rdfgraph):
    '''
    Creates a RDF file from the RDF file with the RDF decorations that
    enable to make the graph representable.
    '''
    node_dict = {}
    rel_dict = {}
    # First: insert the graph in dictionaries to provide them with IDs
    for s, p, o in rdfgraph:
        source = add_to_nodes_dict(RDFNode(s),node_dict)
        target = add_to_nodes_dict(RDFNode(o),node_dict)
        add_to_rels_dict(RDFRel(p, source, target),rel_dict)
    # Enrich for each unique node by 2 triples, one being the visualizer
    for elem in node_dict.values():
        node = URIRef(GA_DOMAIN + elem.get_id())
        rdfgraph.add((node, RDF.type, GA_Node))
        rdfgraph.add((node, RDF.value, elem.get_rdf()))
    # Enrich for each unique edge by 4 triples, one being the visualizer
    for elem in rel_dict.values():
        edge = URIRef(GA_DOMAIN + elem.get_id())
        rdfgraph.add((edge, RDF.type, GA_Edge))
        rdfgraph.add((edge, GA_source, URIRef(GA_DOMAIN + elem.get_source_id())))
        rdfgraph.add((edge, GA_target, URIRef(GA_DOMAIN + elem.get_target_id())))
        rdfgraph.add((edge, RDF.value, elem.get_rdf()))
    return rdfgraph

# toto: implement the rest
