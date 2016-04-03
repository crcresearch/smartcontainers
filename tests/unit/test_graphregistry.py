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
    for k in graphRegistry.scVocabRegistry.REGISTRY:
        print(k)

    graphRegistry.scVocabRegistry.build_graph()

if __name__ == "__main__":
    pytest.main([__file__, '--color=yes', '-s' ])
