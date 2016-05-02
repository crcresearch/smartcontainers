# -*- coding: utf-8 -*-
"""RDFlib Graph Registry for SmartContainers.

This module provides a common interface to all RDFlib graphs created by all
vocabularies. New vocabularies should subclass baseVocabulary.
Since the registry has access to the SmartContainer global provenance graph
it also manages the named graph objects. The design specification is to have
a named graph for each docker state change (build, commit, run). Provenance
 of the named graphs can then be provided by referencing the graph as a quad.
 For more information about RDF 1.1 Datasets and named graphs see:
 https://dvcs.w3.org/hg/rdf/raw-file/default/rdf-dataset/index.html
 http://patterns.dataincubator.org/book/named-graphs.html

 RDFLib Dataset graph object reference:
 https://rdflib.readthedocs.org/en/stable/apidocs/rdflib.html#dataset
"""
import rdflib
from rdflib import URIRef
import baseVocabulary
import provVocabulary


class VocabularyRegistry(object):
    """RDFlib Vocabulary Graph Registry for SmartContainers.

    This module provides a common interface to all RDFlib graphs created by all
    vocabularies. New vocabularies should subclass graphFactory.
    """

    REGISTRY = {}
    global_context = {}
    built = False
    global_graph = rdflib.Dataset(default_union=True)

    def __init__(self, existing_graph=None):
        """Initialize a new registry.

        Args:
         (Optional) existing_graph (turtle): Add an existing global graph
         to the default graph.
        """
        if existing_graph:
            self.global_graph.parse(data=existing_graph, format='turtle')

    # @classmethod
    def get_registry(self):
        """get_registry: Returns the dictionary of all registered vocbularies.

        All of the vocabularies in the graphRegistry store
        their instances in the REGISTRY dictionary. This provides an access
        function for the dictionary.

        Returns:
            REGISTRY (dict): Dictionary of registered vocabularies.

        """
        return dict(self.REGISTRY)

    # @classmethod
    def register(self, vocabulary):
        """register: Register a subclass of baseVocabulary .

        Registration method that registers an instance of a new
        baseVocabulary with the graphRegistry.

        Args:
            vocabulary (baseVocabulary): New vocabulary class to be registered.

        """
        if isinstance(vocabulary, baseVocabulary.baseVocabulary):
            self.REGISTRY[type(vocabulary).__name__] = vocabulary

    # @classmethod
    def build_graph(self):
        """build_graph: Builds a new global graph.

        If the global_graph doesn't exisit, loop through all
        registered vocabularies, build the vocabulary and
        merge the vocabulary graph with the global_graph.
        """
        if not self.built:
            for k in self.REGISTRY:
                print self.REGISTRY[k]
                self.REGISTRY[k].build()
                g = self.global_graph.graph(
                    URIRef('http://www.example.com/gr'))
                g += self.REGISTRY[k].graph
                self.global_context.update(self.REGISTRY[k].context)
            self.built = True

    # @classmethod
    def get_json_ld(self):
        """get_json_ld: Returns JSON-LD serialization of global graph.

        Make sure that the global graph is build and return the JSON-LD
        serialization of the global graph.

        Returns:
            json-ld (str): JSON-LD string object.

        """
        if not self.built:
            self.build_graph()
        return self.global_graph.serialize(
            format='json-ld', context=self.global_context)

    # @classmethod
    def get_turtle(self):
        """get_turtle: Returns TURTLE serialization of global graph.

        Make sure that the global graph is build and return the
        TURTLE (https://www.w3.org/TR/turtle/)
        serialization of the global graph.

        Returns:
            turtle (str): TURTLE string object.

        """
        if not self.built:
            self.build_graph()
        return self.global_graph.serialize(format='turtle')

    # @classmethod
    def add_context(self, key, value):
        """add_context: Register a new JSON-LD context.

        Add new JSON-LD @context entry for the JSON header to the
        global context dictionary.

        Args:
            key (str):    Shortcut identifier for the new JSON-LD context entry.
            value (str): IRI that the shortut key identifies.

        """
        if key not in self.context:
            self.global_context[key] = value

    # @classmethod
    def add_graph(self, existing_graph):
        """add_graph: Add turtle graph into global graph.

        Add an existing graph object to the default global graph using a
        turtle serialzation to parse the graph.

        Args:
            existing_graph (str):    Turtle serialized rdf graph.

        """
        self.global_graph.parse(data=existing_graph, format='turtle')
