#============================================
# File name:      rdf_representations.py
# Author:         Olivier Rey
# Date:           December 2018
# License:        GPL v3
# Purpose:        This file contains the representations
#                 of rdf objects in order to be able
#                 to visualize them in graph
#============================================
#!/usr/bin/env python3

import uuid, rdflib

MAX_STRING_LENGTH = 40

def analyze_uri(uri):
    tokens = uri.split('/')
    if 'http:' in tokens or 'https:' in tokens:
        domain = tokens[2].split('.')[-2]
        mtype  = tokens[-1]
        return domain + ':' + mtype 
    else:
        print('Strange URI: ' + str(uri))
        return str(uri)

    
class Numbering:
    def __init__(self):
        self.number = 0
    def get_next_number(self):
        self.number += 1
        return self.number

    
class RDFNode():
    '''
    This class is managing the representation of a RDF node.
    '''
    def __init__(self, ident, numbering=None):
        # The default system is a uuid system which is converted to int when needed
        # but when using an external numbering system, we have directly an int
        self.numbering = None
        if numbering == None:
            # IDs should be strings because that can cause problems if they are not
            self.id = 'ID_' + str(uuid.uuid4())
        else:
            self.numbering = numbering
            self.id = 'ID_' + str(numbering.get_next_number())
        self.name = "void"
        # Keep a reference to the original RDF concept for later
        self.ident = ident
        if not isinstance(ident, rdflib.term.Identifier):
            raise TypeError("Unrecognized type: " + str(type(ident)))
        if type(ident) == rdflib.term.URIRef:
            self.name = analyze_uri(ident.toPython())
        elif type(ident) == rdflib.term.BNode \
          or type(ident) == rdflib.term.Literal:
            value = str(ident.toPython())
            if len(value) > MAX_STRING_LENGTH:
                self.name = value[0:MAX_STRING_LENGTH] + '...'
            else:
                self.name = value
        else:
            raise TypeError("Unrecognized type: " + str(type(ident)))
    def to_dot(self):
        return str(self.id), str(self.name)
    def to_gml(self):
        if self.numbering == None:
            return self.id.int, str(self.name)
        else:
            return self.id, str(self.name)
    def get_name(self):
        return self.name
    def get_id(self):
        # Should be a string
        return self.id
    def get_int_id(self):
        if self.numbering == None:        
            return self.id.int
        else:
            return self.id
    def get_rdf(self):
        return self.ident


class RDFRel(RDFNode):
    '''
    This class is representing the representation of a relationship. It is an extension of RDFNode.
    '''
    def __init__(self, ident, source, target, numbering=None):
        RDFNode.__init__(self, ident, numbering)
        if type(source) != RDFNode:
            raise TypeError("Unrecognize type: " + str(type(source)))
        elif type(target) != RDFNode:
            raise TypeError("Unrecognize type: " + str(type(target)))
        self.source = source
        self.target = target
    def to_dot(self, label=True):
        # returns the label to print
        if label:
            return self.source.get_id(), self.target.get_id(), str(self.name)
        else: # returns only the link
            return self.source.get_id(), self.target.get_id()
    def to_gml(self):
        return self.source.get_int_id(), self.target.get_int_id(), str(self.name)
    def get_source_id(self):
        return self.source.get_id()
    def get_target_id(self):
        return self.target.get_id()

    
def add_to_nodes_dict(rdfnode, node_dict):
    '''
    Helper function to build the dict of node representations
    We suppose that the parser will create an instance of node for each parse triple
    '''
    name = rdfnode.get_name()
    if name in node_dict:
        print("Info: same node won't be written in the dictionary")
        return node_dict[name]
    else:
        node_dict[name] = rdfnode
        return node_dict[name]

    
def add_to_rels_dict(rdfrel, rel_dict):
    '''
    Helper function to build the dictionnary of relationship representations
    We suppose that all relationships are unique, even if they have the same label
    '''
    rel_dict[rdfrel.get_id()] = rdfrel
    
