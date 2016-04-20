
# -*- coding: utf-8 -*-
"""Tests for Docker Command Line Interface Module.

This module provides the interface to the docker command line utility. Commands
that need to be processed by smartcontainers are intercepted and sent to
docker-py client API for processing. All other commands are sent to the docker
command line client. This is a cheat to avoid having to reimpliment the entire
docker command line arguments even though only a subset of these commands need
to be processed for provenance.
"""
import pytest
import os
from sys import platform as _platform

from sc import dockercli


# Test code that discovers docker command
# This is a bad hack right now
# The correct way should be monkeypatch fixtures
# http://holgerkrekel.net/2009/03/03/monkeypatching-in-unit-tests-done-right/
def test_DockerCli():
    """Test DockerCli docker initializetion."""
    oldenv = os.environ.copy()
    # Test location first
    oldpath = os.environ["PATH"]
    with pytest.raises(dockercli.DockerNotFoundError):
        # check that exceptions are being raised.
        os.environ["PATH"] = "NULL"
        dockercli.DockerCli()
    os.environ["PATH"] = oldpath
    # Test environment variables on MacOS
    if _platform == "darwin":
        with pytest.raises(dockercli.DockerNotFoundError):
            os.environ.clear()
            dockercli.DockerCli()
        os.environ.update(oldenv)
        # dockertester.check_docker_connection()
    if _platform == "linux":
        dockercli.DockerCli()
    dockertester3 = dockercli.DockerCli()
    assert dockertester3.location is not None


class TestDockerCli:
    """Test docker commands."""

    @classmethod
    def setup_class(cls):
        cls.docker_cli = dockercli.DockerCli()

    def test_check_docker_connection(self):
        """Test that docker returns something useful."""
        self.docker_cli.check_docker_connection()

    def test_docker_version(self):
        """Test docker version tester works for an incorrect version."""
        with pytest.raises(dockercli.DockerInsuficientVersionError):
            # This will fail if docker ever gets to version 100
            self.docker_cli.check_docker_version("100.100.100")

    # This test should pass through since we don't capture the
    # provenance of help.
    def test_do_command_simple(self):
        """Test simple docker command to pass through."""
        self.docker_cli.do_command('--help')

    def test_do_command_commit(self, createClient, pull_docker_image):
        """TODO: Docstring for test_do_command_commit.

        Returns: TODO

        """
        newContainer = createClient.create_container(image=pull_docker_image,
                                                     command="/bin/sh", tty=True)
        ContainerID = str(newContainer['Id'])
        createClient.start(ContainerID)
        cmd_str = 'commit ' + ContainerID
        self.docker_cli.do_command(cmd_str)
        createClient.stop(ContainerID)
        createClient.remove_container(ContainerID)

    # def test_do_command_run(self):
    #    self.docker_cli.do_command()

    def test_do_command_build(self):
        """Test docker build command."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        docker_file_path = os.path.join(base_dir, "data/openmalaria/")
        build_command = 'build {} --cpu-shares 2 --cpuset-cpus 0,1 --rm=true'.format(docker_file_path)
        self.docker_cli.do_command(build_command)
