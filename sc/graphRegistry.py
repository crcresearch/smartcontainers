# -*- coding: utf-8 -*-
"""RDFlib Graph Registry for SmartContainers.

This module provides a common interface to all RDFlib graphs created by all
vocabularies. New vocabularies should subclass graphFactory.
"""
import rdflib
import baseVocabulary
import provVocabulary


class VocabularyRegistry(object):

    REGISTRY = {}
    global_context = {}
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
                self.global_context.update(self.REGISTRY[k].context)
            self.built = True

    @classmethod
    def get_json_ld(self):
        if not self.built:
            self.build_graph()
        return self.global_graph.serialize(
            format='json-ld', context=self.global_context)

    @classmethod
    def get_turtle(self):
        if not self.built:
            self.build_graph()
        return self.global_graph.serialize(format='turtle')

    @classmethod
    def add_context(self, key, value):
        if key not in self.context:
            self.global_context[key] = value

# Create instances of registry and register vocabularies
# scVocabRegistry = VocabularyRegistry()
# scProvVocab = provVocabulary.provVocabulary()
# VocabularyRegistry.register(scProvVocab)
