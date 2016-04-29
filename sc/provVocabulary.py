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
        ds.bind("foaf", FOAF)

        # Build agent metadata
        self.build_agent(ds)


    def build_agent(self, ds):

        # Get configmager object from configmanager.
        config_graph = configmanager.configmanager.graph
        person_entities = []
        familyName_entities = []
        givenName_entities = []

        for person in config_graph.subjects(RDF.type, FOAF["Person"]):
            person_entities.append(person)
        # This assumes that the first person property is either the ORCID or SC person identifier
        if person_entities:
            orcid_person = URIRef(person_entities[0])
            # Now find the literals for this URIRef
            for familyName in config_graph.objects(
                    orcid_person, FOAF["familyName"]):
                familyName_entities.append(familyName)
            if familyName_entities:
                familyName_literal = rdflib.Literal(familyName_entities[0])
            for givenName in config_graph.objects(
                    orcid_person, FOAF["givenName"]):
                givenName_entities.append(givenName)
            if givenName_entities:
                givenName_literal = rdflib.Literal(givenName_entities[0])
            # Build the triples Now
            ds.add(( orcid_person, RDF.type, PROV.Person))
            ds.add(( orcid_person, RDF.type, FOAF.Person))
            # Add account info from config, this should include ORCID
            # ds.add(( orcid_person, FOAF.account, chuckORID))
            # User name and hostname info should go here from docker host or from "Dashboard system"
            ds.add(( orcid_person, FOAF.account, URIRef("cvardema@ssh://crcfe.crc.nd.edu")))
            ds.add(( orcid_person, FOAF.givenName, givenName_literal))
            ds.add(( orcid_person, FOAF.familyName, familyName_literal))

            print ds.serialize(format='turtle')



    def build_entity(self, ds):
        pass

    def build_activity(self, ds):
        pass
