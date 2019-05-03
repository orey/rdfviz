#============================================
# File name:      tests.py
# Author:         Olivier Rey
# Date:           December 2018
# License:        GPL v3
#============================================
#!/usr/bin/env python3

import unittest, os, sys

from rdflib import Graph, BNode, Literal
from rdflib.namespace import RDF, FOAF, DC
from graphviz import Digraph

sys.path.insert(0, '/home/olivier/Documents/github/rdfviz')
#from rdfviz.rdf_utils import *
#from rdfviz.rdf2gml import *
#from rdfviz.rdf2graphviz import *
from rdfviz import *


class TestRdf2Graphviz(unittest.TestCase):
    def test_graphviz_with_basic_data(self):
        try:
            store = Graph()

            # Bind a few prefix, namespace pairs for pretty output
            store.bind("dc", DC)
            store.bind("foaf", FOAF)

            # Create an identifier to use as the subject for Donna.
            donna = BNode()

            # Add triples using store's add method.
            store.add((donna, RDF.type, FOAF.Person))
            store.add((donna, FOAF.nick, Literal("donna", lang="foo")))
            store.add((donna, FOAF.name, Literal("Donna Fales")))
    
            #print_store(store)
    
            # Dump store
            if not os.path.exists('./tests'):
                os.makedirs('./tests')
            store.serialize("./tests/test_a1.rdf", format="pretty-xml", max_depth=3)
    
            dot = Digraph(comment='Test_a1')
            add_rdf_graph_to_dot(dot, store)
            dot.render('./tests/test_a1.dot', view=True)
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)
    
    def test_graphviz_with_online_data(self):
        try:
            store = Graph()
            result = store.parse("http://www.w3.org/People/Berners-Lee/card")
            print_store(store)

            # Dump store
            if not os.path.exists('./tests'):
                os.makedirs('./tests')
            store.serialize("./tests/test_a2.rdf", format="turtle")
    
            dot = Digraph(comment='Test_a2')
            add_rdf_graph_to_dot(dot, store)
            dot.render('./tests/test_a2.dot', view=True)
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)

    def test_graphviz_with_rdf_syntax(self):
        try:
            store = Graph()
            result = store.parse('./resources/22-rdf-syntax-ns.ttl', format='turtle')
            print_store(store)

            if not os.path.exists('./tests'):
                os.makedirs('./tests')

            dot = Digraph(comment='test_a3')
            dot.graph_attr['rankdir'] = 'LR'
            add_rdf_graph_to_dot(dot, store, 1)
            dot.render('./tests/test_a3.dot', view=True)
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)

    def test_graphviz_with_simplified_rdf_syntax(self):
        try:
            store = Graph()
            result = store.parse('./resources/22-rdf-syntax-ns-simplified.ttl', format='turtle')
            print_store(store)

            if not os.path.exists('./tests'):
                os.makedirs('./tests')

            dot = Digraph(comment='test_a4')
            dot.graph_attr['rankdir'] = 'LR'
            add_rdf_graph_to_dot(dot, store, 1)
            dot.render('./tests/test_a4.dot', view=True)
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)

    def test_graphviz_with_full_rdf(self):
        try:
            store = Graph()
            result = store.parse('./resources/rdf-rdfs.ttl', format='turtle')
            print_store(store)

            if not os.path.exists('./tests'):
                os.makedirs('./tests')

            dot = Digraph(comment='test_a5')
            dot.graph_attr['rankdir'] = 'LR'
            add_rdf_graph_to_dot(dot, store, 1)
            dot.render('./tests/test_a5.dot', view=True)
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)


class TestRdf2Gml(unittest.TestCase):
    def test_gml_basic(self):
        try:
            store = Graph()

            if not os.path.exists('./tests'):
                os.makedirs('./tests')

            result = store.parse('./resources/22-rdf-syntax-ns-simplified.ttl', format='turtle')
            add_rdf_graph_to_gml('./tests/test_b1.gml', store)
            self.assertTrue(True)
        except Exception as e:
            print(e)
            self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
    
