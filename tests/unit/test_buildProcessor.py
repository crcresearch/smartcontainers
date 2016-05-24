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
            base_dir, 'data/Dockerfile')))

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

    def test_parse_maintainer(self):
        second_maintainer = "Nicolas Reed <Nicolas.Reed.102 at nd dot edu>"

        self.assertEqual(self.parsers[0].data["maintainer"], "Kimbro Staken")
        self.assertEqual(self.parsers[1].data["maintainer"], second_maintainer)

    def test_parse_run(self):
        parameter_one = "install -y software-properties-common python curl"
        parameter_two = "cp Schema\ 32/densities.csv "
        parameter_two += "Schema\ 32/autoRegressionParameters.csv "
        parameter_two += "Schema\ 32/scenario_32.xsd /om"

        special_command = self.data_one["run"][1]["special"]
        self.assertIn("apt-get", special_command)
        self.assertEqual(special_command["apt-get"][0], parameter_one)

        self.assertEqual(self.data_two["run"][9]["original"], parameter_two)

    def test_parse_expose(self):
        self.assertEqual(self.data_one["expose"][2], "443")

    def test_parse_from(self):
        from_data_one = self.data_one["from"][0]
        self.assertEqual(from_data_one["string"], "ubuntu")
        self.assertEqual(from_data_one["image"], "ubuntu")
        self.assertEqual(from_data_one["tag"], "latest")

        from_data_two = self.data_two["from"][0]
        self.assertEqual(from_data_two["string"], "ubuntu:14.04")
        self.assertEqual(from_data_two["image"], "ubuntu")
        self.assertEqual(from_data_two["tag"], "14.04")

    def test_parse_label(self):
        data_label = self.data_one["label"]
        description = "This text illustrates that label-values can span multiple lines. And be a real pain!"

        self.assertIn("description", data_label)
        self.assertEqual(data_label["description"], description)
        self.assertIn("empty", data_label)
        self.assertEqual(data_label["empty"], "")

    def test_parse_add(self):
        data_add = self.data_one["add"]

        self.assertIn("dest", data_add[0])
        self.assertEqual(data_add[0]["dest"], "/")
        self.assertIn("src", data_add[1])
        self.assertEqual(data_add[1]["src"][0], "Dockerfile")

    def test_parse_copy(self):
        data_copy = self.data_one["copy"]
        self.assertIn("dest", data_copy[0])
        self.assertEqual(data_copy[0]["dest"], "/")
        self.assertIn("src", data_copy[1])
        self.assertEqual(data_copy[1]["src"][0], "Dockerfile")

    def test_parse_volume(self):
        self.assertEqual(self.data_one["volume"][1], "/test2vol")

        self.assertEqual(len(self.data_two["volume"]), 1)
        self.assertEqual(self.data_two["volume"][0], "/om/scenarios")

    def test_parse_user(self):
        self.assertEqual(self.data_one["user"][0], "root")

    def test_parse_workdir(self):
        self.assertEqual(self.data_two["workdir"][0], "/om")

    def test_parse_arg(self):
        self.assertEqual(self.data_one["arg"][1]["value"], "1")

    def test_parse_stopsignal(self):
        self.assertEqual(self.data_one["stopsignal"], "9")
