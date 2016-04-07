# -*- coding: utf-8 -*-
"""Test code for RDFlib Graph Factory for SmartContainers.

This module provides a common interface to all RDFlib graphs created by all
vocabularies. New vocabularies should subclass graphFactory.
"""
import json
import pytest
from rdflib import Namespace, URIRef, RDF, RDFS, Literal
import uuid
from sc import baseVocabulary

tstuuid = str(uuid.uuid4())
uuidurn = "urn:uuid:"+tstuuid


class Vocabulary1(baseVocabulary.baseVocabulary):
    def build(self):
        self.context = {"prov": "http://www.w3.org/ns/prov#"}
        PROV = Namespace("http://www.w3.org/ns/prov#")
        chuckORIDchuck = URIRef("http://orcid.org/000-0003-4901-6059")
        self.graph.add((chuckORIDchuck, RDF.type, PROV.Person))


class Vocabulary2(baseVocabulary.baseVocabulary):
    def build(self):
        self.context = {"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}
        UUIDNS = Namespace("urn:uuid:")
        self.graph.bind("uuidns", UUIDNS)
        self.graph.add((UUIDNS[tstuuid], RDFS.label, Literal(
            "Docker: https://www.docker.com/")))


def test_create_graph():
    """Create new graphFactory Object"""
    from sc import graphRegistry

    PROV = Namespace("http://www.w3.org/ns/prov#")
    tstregistry = graphRegistry.VocabularyRegistry()

    vocab1 = Vocabulary1()
    tstregistry.register(vocab1)
    vocab2 = Vocabulary2()
    tstregistry.register(vocab2)

    tstregistry.build_graph()
    # Check assertions in global graph store
    assert (URIRef("http://orcid.org/000-0003-4901-6059"),
            RDF.type, PROV.Person) in tstregistry.global_graph
    assert (URIRef(uuidurn),
            RDFS.label,  Literal(
                "Docker: https://www.docker.com/")) in tstregistry.global_graph
    # Check Serialization
    jsongraph = json.loads(tstregistry.get_json_ld())
    assert '@context' in jsongraph


if __name__ == "__main__":
    pytest.main([__file__, '--color=yes', '-s'])
