# -*- coding: utf-8 -*-
"""Test code for provVocabylary for SmartContainers.

This module provides tests for the W3C prov-o ontology.
"""
import json
import pytest
from rdflib import Namespace, URIRef, RDF, RDFS, Literal
import uuid
from sc import baseVocabulary
from sc import provVocabulary

tstuuid = str(uuid.uuid4())
uuidurn = "urn:uuid:"+tstuuid


def test_create_graph():
    vocab = provVocabulary.provVocabulary()
    vocab.build()

if __name__ == "__main__":
    pytest.main([__file__, '--color=yes', '-s'])
