#============================================
# File name:      rdf2graphviz.py
# Author:         Olivier Rey
# Date:           November 2018
# License:        GPL v3
#============================================
#!/usr/bin/env python3

import uuid, rdflib, sys, os, getopt

from rdf_representations import *
from rdf_utils import *

from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import FOAF, DC
from graphviz import Digraph

    
def print_rel_as_box(rel, dot):
    ''''
    This function is adding some extra representation to relationships.
    '''
    dot.node(rel.get_id(),rel.get_name(), shape='box')
    dot.edge(rel.get_source_id(), rel.get_id())
    dot.edge(rel.get_id(), rel.get_target_id())
            

def add_rdf_graph_to_dot(dot, rdfgraph, mode=0):
    '''
    mode=0 (default): prints labels in edges
    mode=1: prints labels in boxes
    mode=2: prints no labels
    '''
    node_dict = {}
    rel_dict  = {}
    for s, p, o in rdfgraph:
        source = add_to_nodes_dict(RDFNode(s),node_dict)
        target = add_to_nodes_dict(RDFNode(o),node_dict)
        add_to_rels_dict(RDFRel(p, source, target),rel_dict)
    for elem in node_dict.values():
        dot.node(*elem.to_dot(), color="blue", fontcolor='blue')
    if mode==1:
        for elem in rel_dict.values():
            print_rel_as_box(elem, dot)
    elif mode==2:
        for elem in rel_dict.values():
            dot.edge(*elem.to_dot(False))
    else:
        for elem in rel_dict.values():
            dot.edge(*elem.to_dot())
    return dot


    
    
def rdf_to_graphviz(store, name='default', mode=0):
    dot = Digraph(comment=name, format='pdf')
    dot.graph_attr['rankdir'] = 'LR'
    add_rdf_graph_to_dot(dot, store, mode)
    dot.render(name + '.dot', view=True)


def usage():
    print('RDF to GraphViz utility')
    print('Usage')
    print('$ python3 rdf2graphviz.py -i [INPUT] -o [OUTPUT] (other_options)')
    print('    * -i [INPUT] or --input [INPUT]: filename or URL')
    print('    * -o [OUTPUT] or --output [OUTPUT]: directory name. Default will be "./tests/"')    
    print('Other options')
    print('    * -f [FORMAT] or --format [FORMAT]: input format, like "xml", "n3", "ntriples", "turtle" or other format supported by Python rdflib. If no format is provided, rdflib will try to parse the file.')
    print('    * -r [RENDERING] or --render [RENDERING]: format supported by Graphviz. Default is "png".')
    print('-h or --help: usage')

        
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:f:r:v", [])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    input = None
    outputdir = './tests'
    myformat = None
    myrendering = 'png'
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
        elif o in ("-r", "--render"):
            myrendering = a
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
    if myformat == None:
        result = store.parse(input, format='turtle')
    else:
        result = store.parse(input, format=myformat)
    dot = Digraph(comment="RDF to Graphviz: " + name, format=myrendering)
    dot.graph_attr['rankdir'] = 'LR'
    add_rdf_graph_to_dot(dot, store, 1)
    dot.render(os.path.join(outputdir,name + '.dot'), view=True)
