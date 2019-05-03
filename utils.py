#============================================
# File name:      utils.py
# Author:         Olivier Rey
# Date:           December 2018
# License:        GPL v3
# Purpose:        Set of utilities
#============================================
#!/usr/bin/env python3

import rdflib


def print_store(store):
    # Iterate over triples in store and print them out.
    print("--- printing raw triples ---")
    for s, p, o in store:
        print(s, p, o)
    
    # Serialize as XML
    print("--- start: rdf-xml ---")
    print(store.serialize(format="pretty-xml"))
    print("--- end: rdf-xml ---\n")

    # Serialize as Turtle
    print("--- start: turtle ---")
    print(store.serialize(format="turtle"))
    print("--- end: turtle ---\n")

    # Serialize as NTriples
    print("--- start: ntriples ---")
    print(store.serialize(format="nt"))
    print("--- end: ntriples ---\n")
    

def build_name(input):
    '''
    This function takes the input of the command line and tries to build a name
    '''
    temp = input.split('/')[-1]
    if not '\\' in temp:
        return temp
    else:
        return temp.split('\\')[-1]
