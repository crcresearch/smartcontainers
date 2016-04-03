# -*- coding: utf-8 -*-
"""RDFlib Graph Registry for SmartContainers.

This module provides a common interface to all RDFlib graphs created by all
vocabularies. New vocabularies should subclass graphFactory.
"""
import rdflib
import baseVocabulary
import provVocabulary

#  Create a default dataset graph.
# ds = Dataset(default_union=True)

# J SON-LD serializer requires an explicit context.
#  https://github.com/RDFLib/rdflib-jsonld
#  context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}

context = {"prov": "http://www.w3.org/ns/prov#",
           "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
           "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
           "xsd": "http://www.w3.org/2001/XMLSchema#",
           "dc": "http://purl.org/dc/terms"}

class VocabularyRegistry(object):

    REGISTRY = {}
    built = False
    global_graph = rdflib.Dataset(default_union=True)
    def __init__(self):
        pass

    @classmethod
    def get_registry(self):
        return dict(self.REGISTRY)

    @classmethod
    def register(self, vocabulary):
        if isinstance(vocabulary, baseVocabulary.baseVocabulary):
            self.REGISTRY[type(vocabulary).__name__] = vocabulary

    @classmethod
    def build_graph(self):
        if not self.built:
            for k in self.REGISTRY:
                print self.REGISTRY[k]
                self.REGISTRY[k].build()
                self.global_graph += self.REGISTRY[k].graph
            self.built = True

    @classmethod
    def get_json_ld(self):
        if not self.built:
            self.build_graph()
        pass

# Create instances of registry and register vocabularies
scVocabRegistry = VocabularyRegistry()
scProvVocab = provVocabulary.provVocabulary()
VocabularyRegistry.register(scProvVocab)
