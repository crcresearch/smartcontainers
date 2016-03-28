# -*- coding: utf-8 -*-
"""Tests for Smart Containers buildProcessor.

Tests for Smart Containers buildProcessor.
This module provides functions for processing Build commands.
"""
import os
import unittest

from sc import buildProcessor


base_dir = os.path.dirname(os.path.abspath(__file__))


class BuildProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.processors = [
            buildProcessor.buildProcessor(),
            buildProcessor.buildProcessor()
        ]
        self.results = []

        self.results.append(self.processors[0].processDF(os.path.join(
            base_dir, 'data/Dockerfile.txt')))

        self.results.append(self.processors[1].processDF(os.path.join(
            base_dir, 'data/openmalaria/Dockerfile')))

    def test_processDF(self):
        # Process the test data file, and check that the return is 0,
        #  indicating that no errors were encountered.
        self.assertEqual(self.results[0], 0)
        self.assertEqual(self.results[1], 0)
