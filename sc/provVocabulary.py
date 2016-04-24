# -*- coding: utf-8 -*-
"""W3C Provenance Vocabulary for SmartContainers.

This module provides a populator for the W3C
recommendation PROV-O Ontology  https://www.w3.org/TR/prov-o/
for smart containers. It has a builder for each of the main owl:class
prov:Entity, prov:Activity and prov:Agent.

"""

from baseVocabulary import baseVocabulary
from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
from rdflib.namespace import FOAF
from rdflib.serializer import Serializer
import rdflib.resource
import uuid
import configmanager

# Define some namespaces
PROV = Namespace("http://www.w3.org/ns/prov#")
ORE = Namespace("http://www.openarchives.org/ore/terms/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
DC = Namespace("http://purl.org/dc/terms/")
UUIDNS = Namespace("urn:uuid:")
DOCKER = Namespace("http://w3id.org/daspos/docker#")
# W3C namespace:
POSIX = Namespace("http://www.w3.org/ns/posix/stat#")
ACL = Namespace("http://www.w3.org/ns/auth/acl#")

# DASPOS namespaces
SC = Namespace("https://w3id.org/daspos/smartcontainers#")
CA = Namespace("https://w3id.org/daspos/computationalactivity#")
CE = Namespace("https://w3id.org/daspos/computationalenvironment#")

dockerUseruuid = str(uuid.uuid4())

class provVocabulary(baseVocabulary):

    def __init__(self):
        pass

    def build(self):

        ds = self.graph
        self.context = context = {"prov": "http://www.w3.org/ns/prov#",
                   "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                   "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
                   "xsd": "http://www.w3.org/2001/XMLSchema#",
                   "dc": "http://purl.org/dc/terms"}

        # Need to handle DOI
        # http://bitwacker.com/2010/02/04/dois-uris-and-cool-resolution/

        ds.bind("prov", PROV)
        ds.bind("ore", ORE)
        ds.bind("owl", OWL)
        ds.bind("dc", DC)
        ds.bind("uuidns", UUIDNS)
        ds.bind("docker", DOCKER)
        ds.bind("posix", POSIX)
        ds.bind("acl", ACL)
        ds.bind("sc", SC)
        ds.bind("ca", CA)
        ds.bind("ce", CE)
        ds.bind("foaf", FOAF)

        # Build agent metadata
        self.build_agent(ds)


    def build_agent(self, ds):

        # Get configmager object from configmanager.
        config_graph = configmanager.configmanager.graph

        chuckORIDchuck = URIRef(str(uuid.uuid4()))
        print "Config graph:"
        for s, p, o in config_graph:
            print s, p, o
        for person in config_graph.subjects(RDF.type, FOAF["Person"]):
            print person

    def build_entity(self, ds):
        pass

    def build_activity(self, ds):
        pass
