#============================================
# File name:      rdf2gml.py
# Author:         Olivier Rey
# Date:           December 2018
# License:        GPL v3
# Purpose:        Transforms rdf representations into gml
#============================================
#!/usr/bin/env python3

import rdflib, getopt, sys, os

#from . import rdf_representations
from rdf_representations import *

#from . import utils
from utils import *


from rdflib import Graph, Literal, BNode, RDF
from rdflib.namespace import FOAF, DC


def filter_name(name):
    return name.replace('&', 'and')

def create_gml_node_string(id, name):
    return 'node [\n  id ' + str(id) + '\n  label "' + filter_name(name) + '"\n]\n'


def create_gml_rel_string(sourceid, targetid, name):
    return 'edge [\n  label "' + filter_name(name) + '"\n' \
           '  source ' + str(sourceid) + '\n  target '+ str(targetid) + '\n]\n'
    

def add_rdf_graph_to_gml(gmlfilename, rdfgraph):
    '''
    Creates a GML file from the RDF file with the same assumptions
    than the graphviz visual representation.
    Can be used with Gephi
    '''
    node_dict = {}
    rel_dict = {}
    #numbering = rdf_representations.Numbering()
    numbering = Numbering()
    f = open(gmlfilename, 'w')
    f.write('graph [\n')
    for s, p, o in rdfgraph:
        source = add_to_nodes_dict(RDFNode(s,numbering),node_dict)
        target = add_to_nodes_dict(RDFNode(o,numbering),node_dict)
        add_to_rels_dict(RDFRel(p, source, target,numbering),rel_dict)
    for elem in node_dict.values():
        f.write(create_gml_node_string(*elem.to_gml()))
    for elem in rel_dict.values():
        f.write(create_gml_rel_string(*elem.to_gml()))
    f.write(']\n')
    f.close()

    
def usage():
    print('RDF to GML utility')
    print('Usage:')
    print('$ python3 rdf2gml.py -i [input_file_or_url] -o [output_dir] (other_options)')
    print('----\nMain options')
    print('=> -i or --input NAME: filename or URL')
    print('=> -o or --output NAME: directory name. Default will be "./tests/"')
    print('----\nOther options')
    print('=> -f or --format: "xml", "n3", "ntriples" or other format supported')
    print('   by Python rdflib. Default format is "n3".')
    print('=> -h or --help: usage')

    
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hi:o:f:v", [])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    input = None
    outputdir = './tests'
    myformat = 'n3'
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
    add_rdf_graph_to_gml(os.path.join(outputdir,name + '.gml'), store)
    

