# -*- coding: utf-8 -*-
"""Test code for envVocabulary for SmartContainers.

This module provides tests for the ComputationalEnvironment ontology.
"""
import json
import pytest
from rdflib import Namespace, URIRef, RDF, RDFS, Literal
import uuid
from sc import baseVocabulary
from sc import envVocabulary

tstuuid = str(uuid.uuid4())
uuidurn = "urn:uuid:"+tstuuid


def test_create_graph():
    vocab = envVocabulary.envVocabulary()
    vocab.build()
    print vocab.graph.serialize(format='turtle')

if __name__ == "__main__":
    pytest.main([__file__, '--color=yes', '-s'])
