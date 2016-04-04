# -*- coding: utf-8 -*-
"""RDFlib Graph Factory for SmartContainers.

This module provides a common interface to all RDFlib graphs created by all
vocabularies. New vocabularies should subclass graphFactory.
"""
from abc import ABCMeta, abstractmethod
import rdflib


class baseVocabulary(object):
    __metaclass__ = ABCMeta
    """
        Any class that will inherits from BaseRegisteredClass will be included
        inside the dict RegistryHolder.REGISTRY, the key being the name of the
        class and the associated value, the class itself.
    """
    graph = rdflib.Dataset(default_union=True)
    context = {}
    namespace = []
    @abstractmethod
    def build(self):
        pass
