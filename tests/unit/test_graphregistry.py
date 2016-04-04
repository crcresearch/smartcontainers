# -*- coding: utf-8 -*-
"""Test code for RDFlib Graph Factory for SmartContainers.

This module provides a common interface to all RDFlib graphs created by all
vocabularies. New vocabularies should subclass graphFactory.
"""
import pytest


def test_create_graph():
    """Create new graphFactory Object"""
    from sc import graphRegistry
    from sc import baseVocabulary

    tstregistry = graphRegistry.VocabularyRegistry()

    class Vocabulary1(baseVocabulary.baseVocabulary):
        def build(self):
            print "Building test registry"

    vocab1 = Vocabulary1()
    tstregistry.register(vocab1)

    print("Before subclassing: ")
    for k in tstregistry.REGISTRY:
        print(k)

    tstregistry.build_graph()

if __name__ == "__main__":
    pytest.main([__file__, '--color=yes', '-s'])
