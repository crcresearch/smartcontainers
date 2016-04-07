# -*- coding: utf-8 -*-
"""Tests for SC command line execution.

This module tests that the sc command as setup from setup.py
executes correctly and returns the help useage. This is meant to
to be a quick and dirty test to make sure that there isn't a depenency
version conflict that prevents the command line script wrapper from
functioning.
"""
from __future__ import unicode_literals
from subprocess import check_output


def test_sc():
    """Test SC command execution."""
    result = run_cmd("sc")
    assert 'Usage:' in result
    print result


def run_cmd(cmd):
    """Run a shell command `cmd` and return its output."""
    return check_output(cmd, shell=True).decode('utf-8')
