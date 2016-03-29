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

        self.data_one = self.parsers[0].data
        self.data_two = self.parsers[1].data

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

    def test_parse_maintainer(self):
        second_maintainer = "Nicolas Reed <Nicolas.Reed.102 at nd dot edu>"

        self.assertEqual(self.parsers[0].data["maintainer"], "Kimbro Staken")
        self.assertEqual(self.parsers[1].data["maintainer"], second_maintainer)

    def test_parse_run(self):
        parameter_one = "install -y python-software-properties python"
        parameter_two = "cp Schema\ 32/densities.csv "
        parameter_two += "Schema\ 32/autoRegressionParameters.csv "
        parameter_two += "Schema\ 32/scenario_32.xsd /om"

        special_command = self.data_one["run"][0]["special"]
        self.assertIn("apt-get", special_command)
        self.assertEqual(special_command["apt-get"][0], parameter_one)

        self.assertEqual(self.data_two["run"][9]["original"], parameter_two)

    def test_parse_expose(self):
        self.assertEqual(self.data_one["expose"][2], "443")
