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

        self.parsers = [
            self.processors[0].PU,
            self.processors[1].PU
        ]

    def test_processDF(self):
        # Process the test data file, and check that the return is 0,
        #  indicating that no errors were encountered.
        self.assertEqual(self.results[0], 0)
        self.assertEqual(self.results[1], 0)

    def test_check_steps(self):
        second_step = "RUN apt-get --yes update && apt-get --yes upgrade"

        self.assertEqual(self.parsers[0].steps[0], "FROM ubuntu")
        self.assertEqual(self.parsers[1].steps[2], second_step)

    def test_write_out_data(self):
        self.parsers[0].write_out_data(os.path.join(base_dir,
            "data/data1.json"))

        self.parsers[1].write_out_data(os.path.join(base_dir,
            "data/data2.json"))

        self.assertTrue(os.path.isfile(os.path.join(base_dir,
            "data/data1.json")))
        self.assertTrue(os.path.isfile(os.path.join(base_dir,
            "data/data2.json")))
