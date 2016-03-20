# -*- coding: utf-8 -*-
"""Docker Command Line Interface Module.

This module provides the interface to the docker command line utility. Commands
that need to be processed by smartcontainers are intercepted and sent to
docker-py client API for processing. All other commands are sent to the docker
command line client. This is a cheat to avoid having to reimpliment the entire
docker command line arguments even though only a subset of these commands need
to be processed for provenance.
"""
from __future__ import unicode_literals
from util import which
import io
import os
import os.path
import requests
import stat
import subprocess

import docker.tls as tls

import client

# We need to docker version greater than 1.6.0 to support
# the label functionality.
min_docker_version = '1.6.0'

# Default docker commands that sc can handle.
snarf_docker_commands = ['commit', 'build', 'stop', 'run']
# Default docker label key where smart container graph is stored.
smart_container_key = 'sc'


class Error(Exception):
    """Base exception for client module."""


class DockerNotFoundError(RuntimeError):
    """Exception raised for missing docker command.

    Attributes:
        msg -- explaination of error
    """

    def __init__(self, msg):
        """Exception message Docker not Found Error."""
        msg = "Please make sure docker is installed and in your path."
        self.arg = msg


class DockerDaemonConnectionError(Error):
    """Raised if the docker client can't connect to the docker daemon."""


class DockerInsuficientVersionError(RuntimeError):
    """Exception raised for wrong version of docker command.

    We require a minimimum version of the docker command line interface
    that supports labels as run time arguments.

    """

    def __init__(self, msg):
        """Exception for incompatable docker command line version."""
        msg = "Please make sure docker is greater than %s" % min_docker_version
        self.arg = msg


class DockerServerError(RuntimeError):
    """Exception for no docker server connection.

    This exception can be raised for ether the command line client not
    conncting to server backend or for the docker-py not able to find
    either a docker socket file or the envrionment variables for
    docker-machine.

    """

    def __init__(self, msg):
        """Set exception message for no server connection.

        Args:
            msg (str): Message for paticular server error.
        """
        msg = "Cannot connect to server"
        self.arg = msg


class DockerCli:
    """Docker Command Line interface class.

    This class provides a wrapper for directing docker commands to either the docker
    command line client or to the smart containers docker-py client wrapper for
    metadata and provenance processing.
    """

    location = None              #: Path to docker command line.
    docker_host = None           #: Docker host environment variable.
    docker_cert_path = None      #: Docker cert path environment variable.
    docker_machine_name = None   #: Docker machine name env variable.
    docker_socket_file = None    #: Path to docker socket file.
    dcli = None                  #: docker-py client object.
    docker_machine = False       #: Using Docker machine instead of sockets.

    def __init__(self):
        """Init has no arguments.

        The __init__ method will attempt to find the docker command line
        and attempt to setup docker-py to connect to the docker client backend.
        The connection variables will be stored in self.
        """
        # Find docker command line location
        location = which("docker")
        if location is None:
            raise DockerNotFoundError("Please make sure docker is installed "
                                      "and in your path")
        self.location = location

        # Find docker-machine environment variables
        self.docker_host = os.getenv("DOCKER_HOST")
        self.docker_cert_path = os.getenv("DOCKER_CERT_PATH")
        self.docker_machine_name = os.getenv("DOCKER_MACHINE_NAME")

        # Look for linux docker socket file
        socket_path = "/var/run/docker.sock"
        has_docker_socket_file = os.path.exists(socket_path)
        if has_docker_socket_file:
            mode = os.stat(socket_path).st_mode
            isSocket = stat.S_ISSOCK(mode)
            if isSocket:
                self.docker_socket_file = "unix://" + socket_path
        if not ((self.docker_host and
                self.docker_cert_path and
                self.docker_machine_name) or
                has_docker_socket_file):
            raise DockerNotFoundError("Couldn't find socket file or"
                                      "Environment variables for docker.")

        # Setup the docker client connections based on what we've found.
        if (self.docker_host and self.docker_machine_name and
                self.docker_cert_path):
            tls_config = tls.TLSConfig(
                client_cert=(os.path.join(self.docker_cert_path, 'cert.pem'),
                             os.path.join(self.docker_cert_path, 'key.pem')),
                ca_cert=os.path.join(self.docker_cert_path, 'ca.pem'),
                verify=True,
                assert_hostname=False
            )
        # # Replace tcp: with https: in docker host.
            docker_host_https = self.docker_host.replace("tcp", "https")
            self.dcli = client.scClient(base_url=docker_host_https,
                                        tls=tls_config, version="auto")
            self.docker_machine = True
        # #print self.dcli.info()
        elif (self.docker_socket_file):
            self.dcli = client.scClient(base_url=self.docker_socket_file,
                                        version="auto")

        # Assert dcli is not none;
        if self.dcli is None:
            raise DockerNotFoundError("Docker Client cannot find server.")
        # Test for dcli to make sure it can talk to client.
        # self.test_docker_version()
        # self.test_docker_connection()

    def check_docker_connection(self):
        """check_docker_connection: Docker connections.

        Checks both the command line docker and docker-py client can
        communicate with docker server.

        Raises:
            DockerServerError: Docker cannot connect to server.

        """
        try:
            res = subprocess.Popen([self.location, 'images'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            output, error = res.communicate()
        except OSError as e:
            print "OSError > ", e.errno
            print "OSError > ", e.strerror
            print "OSError > ", e.filename
        #
        # This checks if we can get a connection to the remote docker
        # server. It assumes the output of the "docker images"" command is
        # of the form: "Get http:///var/run/docker.sock/v1.19/images/json: dial
        # unix /var/run/docker.sock: no such file or directory. Are you trying
        # to connect to a TLS-enabled daemon without TLS?"
        if 'IMAGE ID' not in output:
            raise DockerDaemonConnectionError("Docker cannot connect to daemon")

        # Check dcli can connect to server.
        try:
            self.dcli.ping()
        except requests.exceptions.ConnectionError:
            raise DockerDaemonConnectionError(
                'Couldn\'t connect to the docker daemon using the specified '
                'environment variables. Please check the environment variables '
                'DOCKER_HOST, DOCKER_CERT_PATH and DOCKER_TLS_VERIFY are set '
                'correctly. If you are using boot2docker, make sure you have run '
                '"$(docker-machine env)"')

    def check_docker_version(self, min_version=min_docker_version):
        """check_docker_version: makes sure docker is of a min version."""
        try:
            res = subprocess.Popen([self.location, '--version'],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
            output, error = res.communicate()
        except OSError as e:
            print "OSError > ", e.errno
            print "OSError > ", e.strerror
            print "OSError > ", e.filename
        # in docker 1.7.1 version is at 2 position in returned string
        version = output.split()[2]
        # remove comma from out put if in string
        if ',' in version:
            version = version[:-1]
        if self.ver_cmp(version, min_version) < 0:
            raise DockerInsuficientVersionError(
                "Please  make sure docker is greater than %s" % min_version)

    def do_command(self, command):
        """do_command is main entry point for capturing docker commands"""
        # First run the command and capture the output.
        # For efficiency this should probably change such that
        # if a command doesn't have a capture handler we execute
        # the command uncaptured. Most commands are going to be captured
        # for provenance, so this efficiency concern is probably moot.

        if self.location is None:
            self.find_docker()
        cmd_string = str(self.location) + ' ' + self.command
        capture_flag = False

        for name in snarf_docker_commands:
            if name in self.command:
                if name == 'build':
                    self.capture_cmd_build(cmd_string) #Captures information from logs.
                    capture_flag = True
                elif name == 'commit':
                    self.capture_cmd_commit(cmd_string)
                    capture_flag = True
                elif name == 'run':
                    #Execute some procedure
                    capture_flag = True
                elif name == 'stop':
                    #Execute some procedure
                    capture_flag = True
        if not capture_flag:
            #print 'here'
            subprocess.call(cmd_string, shell=True)


    def get_docker_version(self):
        docker_version = None
        docker_command = str(self.location) + " version --format '{{.Server.Version}}'"
        output = capture_stdout(docker_command)
        for line in io.TextIOWrapper(output.stdout):
            docker_version = line
        return docker_version

    def get_image_info(self):
        docker_command = str(self.location) + ' images'
        output = capture_stdout(docker_command)
        if self.imageID is not None:
            for line in io.TextIOWrapper(output.stdout):
                if self.imageID in repr(line):
                    repository = line.split()[0]
                    tag = line.split()[1]
            return repository, tag
        else:
            raise DockerImageError


    # Function to compare sematic versioning
    # See http://zxq9.com/archives/797 for explaination
    # and http://semver.org/ for information on semantic versioning
    def ver_tuple(self, z):
        return tuple([int(x) for x in z.split('.') if x.isdigit()])

    def ver_cmp(self, a, b):
        return cmp(self.ver_tuple(a), self.ver_tuple(b))

    def infect(self, image):
        """

        Args:
            image (TODO): ImageID

        Returns: TODO

        """
        self.dcli.infect(image)
