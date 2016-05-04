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
dockerActivityuuid = str(uuid.uuid4())
dockerEntityuuid = str(uuid.uuid4())

class provVocabulary(baseVocabulary):

    def __init__(self):
        pass

    def build(self):

        ds = self.graph
        self.context = {"prov": "http://www.w3.org/ns/prov#",
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
        self.build_entity(ds)
        self.build_activity(ds)


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
            orcid_account = URIRef(person_entities[0]+"#orcid-id")
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
            ds.add(( orcid_person, FOAF.account, orcid_account))
            ds.add(( orcid_person, FOAF.givenName, givenName_literal))
            ds.add(( orcid_person, FOAF.familyName, familyName_literal))

        # Add agent info last. Docker is a software agent actingOnBelhalfof
        ds.add((SC.sc, RDF.type, PROV.SoftwareAgent ))
        ds.add((SC.sc, SC.hasVersion, Literal("0.0.1")))
        ds.add((DOCKER.docker, PROV.actedOnBehalfOf, SC.sc ))
        ds.add( (DOCKER.docker, RDF.type, PROV.SoftwareAgent ) )
        ds.add( (DOCKER.docker, RDFS.label, Literal("Docker: https://www.docker.com/")))
        ds.add( (DOCKER.docker, RDFS.seeAlso, URIRef(u"https://www.docker.com/")))
        # This need to be put somewhere
        ds.add( (DOCKER.docker, DOCKER.hasVersion, Literal("Docker version 1.9.1, build a34a1d5")))
        ds.add( (SC.sc, PROV.actedOnBehalfOf, UUIDNS[dockerUseruuid]))





    def build_entity(self, ds):
        ds.add((UUIDNS[dockerEntityuuid], RDF.type, PROV.Entity))
        ds.add((UUIDNS[dockerEntityuuid], RDF.type, DOCKER.Entity))
        ds.add((UUIDNS[dockerEntityuuid], PROV.wasGeneratedBy,
        UUIDNS[dockerActivityuuid]))
        ds.add((UUIDNS[dockerEntityuuid], DOCKER.hasImageID, Literal("ImageIDString")))



    def build_activity(self, ds):
        ds.add((UUIDNS[dockerActivityuuid], RDF.type, PROV.Activity))
        ds.add((UUIDNS[dockerActivityuuid], RDF.type, CA.compuatationalActivity))
        # Need sublcass of docker related activities
        ds.add((UUIDNS[dockerActivityuuid], RDF.type, DOCKER.commitActivity))
        ds.add((UUIDNS[dockerActivityuuid], DOCKER.hasCommand, DOCKER.commitOperation))
        ds.add((UUIDNS[dockerActivityuuid], DOCKER.hasContainerID, Literal("blahID")))
        ds.add((UUIDNS[dockerActivityuuid],
                DOCKER.hasContainerTag, Literal("GreatContainer")))
        ds.add((UUIDNS[dockerActivityuuid],
                PROV.startedAtTime, Literal("2015-11-10T01:30:00Z",
                                            datatype=XSD.dateTime)))
        ds.add((UUIDNS[dockerActivityuuid],
                PROV.endedAtTime, Literal("2015-11-10T03:40:00Z",
                                          datatype=XSD.dateTime)))
