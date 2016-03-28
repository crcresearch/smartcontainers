# -*- coding: utf-8 -*-
"""Tests for Smart Containers buildProcessor.

Tests for Smart Containers buildProcessor.
This module provides functions for processing Build commands.
"""
import os
from sc import buildProcessor
P = buildProcessor.buildProcessor()

def test_processDF():
    #Process the test data file, and check that the return is 0,
    #indicating that no errors were encountered.
    result = P.processDF('unit/data/Dockerfile.txt')
    assert result == 0