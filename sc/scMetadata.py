# -*- coding: utf-8 -*-
"""Smart Containers Metadata Interface.

This module provides an interface for the Client to the metadata
objects that need to writen to a label or inside of a container.
"""
import graphRegistry
import re
import ast


class scMetadata:
    def __init__(self):
        pass

    def appendData(self, filepath):
        # Appends provinator data to the file passed in
        with open(filepath, 'a') as provfile:
            provfile.write(graphRegistry.scVocabRegistry.get_json_ld())

    def labelDictionary(self, label_prefix):
        # Returns the label as a dictionary
        # Get the label information from provinator
        provOutput = graphRegistry.scVocabRegistry.get_json_ld()
        # Remove any formatting characters
        provOutput = re.sub('[\t\r\n\s+]', '', provOutput)
        # Add the label prefix
        newLabel = "{'" + label_prefix + "':'" + provOutput + "'}"
        # Evaluate the string to create the dictionary
        newLabel = ast.literal_eval(newLabel)
        # Return the dictionary
        return newLabel
