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


from rdflib import Graph, URIRef, Literal, BNode, RDF
from rdflib.namespace import FOAF, DC


#------------------------------------------ Constants
GA_DOMAIN = "https://orey.github.io/graphapps-V1#"

GA_Node = URIRef(GA_DOMAIN + "Node")
GA_Edge = URIRef(GA_DOMAIN + "Edge")
GA_source = URIRef(GA_DOMAIN + "source")
GA_target = URIRef(GA_DOMAIN + "target")


def enrich_graph_with_navigation(rdfgraph):
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
def usage():
    print('RDF to RDFVIZ utility: Parses the full RDF file and adds unique IDs ' +
          'for displays')
    print('Usage:')
    print('$ python3 rdf2rdfviz.py -i [input_file_or_url] -o [output_dir] (other_options)')
    print('----\nMain options')
    print('=> -i or --input NAME: filename or URL')
    print('=> -o or --output NAME: directory name. Default will be "./outputs/"')
    print('----\nOther options')
    print('=> -f or --format: "xml", "n3", "ntriples" or other format supported')
    print('   by Python rdflib. Default format is "turtle".')
    print('=> -h or --help: usage')

    
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:f:v", [])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    input = None
    outputdir = './outputs'
    myformat = 'turtle'
    verbose = False
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-i", "--input"):
            input = a
        elif o in ("-o", "--output"):
            outputdir = a
        elif o in ("-f", "--format"):
            myformat = a
        else:
            assert False, "unhandled option"

    # Check input
    if input == None:
        #print("Input file or URL cannot be void.")
        usage()
        sys.exit()
    name = build_name(input)
    # Check output dir
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)

    store = Graph()
    result = store.parse(input, format=myformat)
    enrich_graph_with_navigation(store)
    # Dump the rdfgraph into a file
    rdfgraph.serialize(rdf_file, myformat) 



