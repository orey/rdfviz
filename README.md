# 2 RDF visualization tools

## rdf2gml

This utility converts Turtle files into GML.

### Dependencies:

  * `rdflib`
  
### Usage

```
$ python3 rdf2gml.py
```

## rdf2graphviz

### Dependencies:

  * `rdflib`
  * `graphviz`

Warning: on top of `graphviz` Python3 package, you must have installed [Graphviz](http://graphviz.org/).

On Debian:

```
$ su root
$ apt install graphviz
```

### Usage

```
$ python3 rdf2graphviz.py
```

## Design notes

### Structure of files

![Files](https://github.com/orey/rdfviz/blob/master/design/design.png)

## rdf2graphviz comments

### Mapping web semantic concepts to graphs

We face 2 structural differences between graph and semantic web RDF.

#### 1. Edges are not edges

To be able to display triples, we have to take some options. In RDF, the predicate can be itself the subject or the object of other triples. That means that the predicate is not an "edge" in the graph sense of the term.

Moreover, in pure RDF, if we have ```d1:s1 d2:p d3:o1 .``` and ```d1:s2 d2:p d3:o2 .```, "d2:p" is one and only one object whereas 2 triples are using it.

So we must find a convention of representation.

### 2. Emulating a knowledge graph into a graph

In a standard graph representation, we will choose to focus on nodes and to use "d2:p" as a label of both ```d1:s1 -> d3:o1``` and ```d1:s2 -> d3:o2``` relationships. That's the first option of representation that we have chosen to implement.

The second option that we have chosen to represent is creating a box around each of the relations. In that case "d2:p" will appear in several boxes between the nodes of the subject and the node of the subject.

This way of representing is not perfect because:

  * "d2:p" will be represented several times whereas in the real knowledge graph, it exists only once.
  * If, in the same knowledge graph, we have something like ```d2:p d4:q d5:r .``` (case of "d2:p" being a subject to another triple) or "d2:p" is the object of another triple, "d2:p" will also appear as a node (on top of being potentially labels or rectangles in relationships).

In a way, we chose to "emulate" the knowledge graph in a graph considering as primary objects "subject" and "object" and as secondary objects "predicate" - except when a predicate becomes subject or object.

Technically that means that the representation of the knowledge graph will ensure node unicity (subject/object used in several triples) but will create graphical instances of the same predicate if need be.

Concretely:

  * BNode instances and Literal instances are considered unique nodes;
  * URIRef is instanciated for each edge.

