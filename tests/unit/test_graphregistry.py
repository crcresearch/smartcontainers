# -*- coding: utf-8 -*-
"""Test code for RDFlib Graph Factory for SmartContainers.

This module provides a common interface to all RDFlib graphs created by all
vocabularies. New vocabularies should subclass graphFactory.
"""
import pytest


def test_create_graph():
    """Create new graphFactory Object"""
    from sc import graphRegistry
    print("Before subclassing: ")
    for k in graphRegistry.VocabularyRegistry.REGISTRY:
        print(k)

    class sampleVocabulary(graphRegistry.BaseVocabulary):
        def __init__(self, *args, **kwargs):
            pass

    print("After subclassing: ")
    for k in graphRegistry.VocabularyRegistry.REGISTRY:
        print(k)

if __name__ == "__main__":
    pytest.main([__file__, '--color=yes', '-s' ])
