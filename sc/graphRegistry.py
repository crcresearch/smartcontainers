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
import graphManager
import provVocabulary
import envVocabulary
# Create instances of registry and register vocabularies
scVocabRegistry = graphManager.VocabularyRegistry()
scProvVocab = provVocabulary.provVocabulary()
scVocabRegistry.register(scProvVocab)

scEnvVocabulary = envVocabulary.envVocabulary()
scVocabRegistry.register(envVocabulary)
