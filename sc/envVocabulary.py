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
import platform
import cpuinfo

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

class envVocabulary(baseVocabulary):

    def __init__(self):
        pass

    def build(self):
        ds = self.graph
        self.context = {"ce":
                        "https://raw.githubusercontent.com/Vocamp/ComputationalActivity/master/pattern/ComputationalEnvironment.jsonld"}

        CE = Namespace("http://dase.cs.wright.edu/ontologies/ComputationalEnvironment#")
        CA = Namespace("http://dase.cs.wright.edu/ontologies/ComputationalActivity#")
        DOCKER = Namespace("http://w3id.org/daspos/docker#")
        info = cpuinfo.get_cpu_info()

# ISSUES: We want if the architecture URI's to be created only once on
# build or initial commit. Otherwise, we want to re-read the URI's
#  from the original graph. There are imm

        ds.bind("ce", CE)
        ceuri = URIRef(str(uuid.uuid4()))
        ds.add((ceuri, RDF.type, CE.ComputationalEnvironment))

        osUri = URIRef(str(uuid.uuid4()))
        ds.add((ceuri, CE.hasOperatingSystem, osUri))
        ds.add((osUri, RDFS.label, Literal("linux")))

        processorUri = URIRef(str(uuid.uuid4()))
        ds.add((ceuri, CE.hasHardware, processorUri))

        archUri = URIRef(str(uuid.uuid4()))
        ds.add((processorUri, CE.hasArchitecture,  archUri))
        ds.add((archUri, RDFS.label, Literal("amd64")))
        ds.add((processorUri, CE.hasNumberOfCores,
                Literal("4", datatype=XSD.nonNegativeInteger)))

        # :hasArchitecture
        # :hasNumberOfCores
        # :hasOperatingSystem
        # :hasSize Memory or HD
        # :isAvailable
        # :VirtualMACAddress
