# -*- coding: utf-8 -*-
"""Tests for Smart Containers parsingUtility.

Tests for Smart Containers parsingUtility.
This module provides utility functions for parsing commands.
It is primarily used by the buildProcessor, but may include
other functionality if needed.
"""

from sc import parsingUtility as pClass
P = pClass.parsingUtility()

def test_getCommand():
    #Checks that getCommand appropriately returns the first word as the command
    cmd = P.getCommand('RUN Phusion/BaseImage')
    assert cmd == 'RUN'

def test_parseCommand():
    #TODO this test needs to be fleshed out once actually processing is available.
    cmd = P.parseCommand('RUN Phusion/BaseImage')
    assert 1 == 1