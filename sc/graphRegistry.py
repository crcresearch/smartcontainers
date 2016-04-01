# -*- coding: utf-8 -*-
"""RDFlib Graph Factory for SmartContainers.

This module provides a common interface to all RDFlib graphs created by all
vocabularies. New vocabularies should subclass graphFactory.
"""
import rdflib
import abc
#  Create a default dataset graph.
# ds = Dataset(default_union=True)

# J SON-LD serializer requires an explicit context.
#  https://github.com/RDFLib/rdflib-jsonld
#  context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}

context = {"prov": "http://www.w3.org/ns/prov#",
           "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
           "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
           "xsd": "http://www.w3.org/2001/XMLSchema#",
           "dc": "http://purl.org/dc/terms"}

class RegistryHolder(type):

    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = type.__new__(cls, name, bases, attrs)
        """
            Here the name of the class is used as key but it could be any class
            parameter.
        """
        cls.REGISTRY[new_cls.__name__] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)


class BaseRegisteredClass:
    __metaclass__ = RegistryHolder
    """
        Any class that will inherits from BaseRegisteredClass will be included
        inside the dict RegistryHolder.REGISTRY, the key being the name of the
        class and the associated value, the class itself.
    """
    pass
