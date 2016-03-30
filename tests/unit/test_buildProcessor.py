# -*- coding: utf-8 -*-
"""Tests for Smart Containers buildProcessor.

Tests for Smart Containers buildProcessor.
This module provides functions for processing Build commands.
"""
import os
import unittest

from sc import buildProcessor


class BuildProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.build_processor = buildProcessor.buildProcessor()
        self.result = self.build_processor.processDF('unit/data/Dockerfile.txt')

    def test_processDF(self):
        # Process the test data file, and check that the return is 0,
        #  indicating that no errors were encountered.
        self.assertEqual(self.result, 0)
