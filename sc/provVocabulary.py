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

        # Build agent metadata
        self.build_agent(ds)


    def build_agent(self, ds):
        # Add human Agent info
        ds.add((UUIDNS[dockerUseruuid], RDF.type, PROV.Person))
        ds.add((UUIDNS[dockerUseruuid], RDF.type, FOAF.Person))
        # Not sure if I'm happy with strong statement.
        ds.add((UUIDNS[dockerUseruuid], OWL.sameAs, chuckORIDchuck))
        # Add account info from config, this should include ORCID
        ds.add((UUIDNS[dockerUseruuid], FOAF.account, chuckORID))
        # User name and hostname info should go here from docker host or from "Dashboard system"
        ds.add((UUIDNS[dockerUseruuid], FOAF.account, URIRef("cvardema@ssh://crcfe.crc.nd.edu")))
        ds.add((UUIDNS[dockerUseruuid], FOAF.givenName, Literal("Charles") ) )
        ds.add(( UUIDNS[dockerUseruuid], FOAF.familyName, Literal("Vardeman II") ) )


    def build_entity(self, ds):
        pass

    def build_activity(self, ds):
        pass
