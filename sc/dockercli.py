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
import getopt
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
        """do_command: main entry point for capturing docker commands.

        Commands that don't require provenance capture and annotation are
        passed verbatim to the docker client command line utility. All other
        commands are parsed and passed to the scClient docker-py client which
        executes the equivalent docker command line and and processes the
        provenance metadata.

        Args:
            command (str): Docker command line string.

        """
        # First run the command and capture the output.
        # For efficiency this should probably change such that
        # if a command doesn't have a capture handler we execute
        # the command uncaptured. Most commands are going to be captured
        # for provenance, so this efficiency concern is probably moot.

        cmd_string = str(self.location) + ' ' + command
        capture_flag = False

        for name in snarf_docker_commands:
            if name in command:
                if name == 'build':
                    capture_flag = True
                    build_args = self.capture_cmd_build(cmd_string)
                    try:
                        default = self.dcli.build(**build_args)
                        self.dcli.infect_image(default, **build_args)
                    except TypeError as error:
                        print(error)
                        # Did not pass a path/fileobj.
                        # Run native docker build command
                        #  (probably a --help, or similar).
                        capture_flag = False
                elif name == 'commit':
                    self.capture_cmd_commit(cmd_string)
                    capture_flag = True
        if not capture_flag:
            subprocess.call(cmd_string, shell=True)

    def capture_cmd_commit(self, cmd_string):
        """TODO: Docstring for capture_cmd_commit.

        Args:
            cmd_string (TODO): TODO

        Returns: TODO

        """
        print cmd_string
        pass

    # Native docker to docker-py options.
    option_mapping = {
        "quiet": "quiet",
        "q": "quiet",
        "t": "tag",
        "no-cache": "nocache",
        "pull": "pull",
        "rm": "rm",
        "force-rm": "forcerm",
        "cpu-shares": "container_limits",
        "cpuset-cpus": "container_limits",
        "memory": "container_limits",
        "memory-swap": "container_limits",
    }
    # Default values for some options.
    value_mapping = {
        "quiet": True,
        "nocache": True,
        "pull": True,
        "forcerm": False,
        "container_limits": {},
        "rm": True,
        "tag": "",
    }
    # Native docker to docker-py container limits.
    container_limits_mapping = {
        "cpu-shares": "cpushares",
        "cpuset-cpus": "cpusetcpus",
        "memory": "memory",
        "memory-swap": "memswap",
    }
    arg_short_options = ["f", "m", "t"]
    no_arg_short_options = ["h", "q"]
    arg_long_options = ["build-arg", "cgroup-parent", "cpu-shares",
        "cpu-period", "cpu-quota", "cpuset-cpus", "cpuset-mems",
        "disable-content-trust", "file", "isolation", "label", "memory",
        "memory-swap", "shm-size", "rm", "tag", "ulimit"]
    no_arg_long_options = ["force-rm", "help", "no-cache", "pull", "quiet"]

    def capture_cmd_build(self, command):
        """Captures and parses the native docker build command.

        Args:
            command (str): String containing 'build' and options.

        Returns:
            (dict): Build data to pass to docker-py.

        """
        short_options = "".join([option + ":" for option in self.arg_short_options])
        long_options = [option + "=" for option in self.arg_long_options]

        short_options += "".join(self.no_arg_short_options)
        long_options.extend(self.no_arg_long_options)

        command_arguments = command.split()[2:]  # Ignore 'docker' and 'build'.
        try:
            opts, args = getopt.gnu_getopt(command_arguments, short_options,
                                           long_options)
        except getopt.GetoptError as error:
            print str(error)
            raise error

        short_options = self.arg_short_options + self.no_arg_short_options
        long_options = self.arg_long_options + self.no_arg_long_options
        data = {}

        # Need to have a valid path to a Dockerfile.
        if args != None and len(args) > 0 and os.path.isdir(args[0]):
            data["path"] = args[0]
        else:
            return data

        # Parse out the build options and arguments.
        for o, a in opts:
            option = o.replace("-", "", 2)
            if option in self.option_mapping:
                option_value = self.option_mapping[option]

                if option_value not in self.value_mapping:
                    continue

                if option in short_options:
                    data[option_value] = a
                elif option in long_options:
                    if type(self.value_mapping[option_value]) == dict:
                        if option_value not in data:
                            data[option_value] = {}

                        argument = a
                        inner_arg = self.container_limits_mapping[option]
                        if inner_arg != "cpusetcpus":
                            argument = int(argument)
                        data[option_value][inner_arg] = argument
                    else:
                        data[option_value] = self.value_mapping[option_value]
            elif option == "file" or option == "f":
                file_obj = open(a)
                data["fileobj"] = file_obj
                del data["path"]

        return data

    def ver_tuple(self, z):
        """ver_tuple: Version Tuple.

        Versioning tuple parser for semantic versioning.
        Note:
            See http://zxq9.com/archives/797 for explaination.
            See http://semver.org/ for info on semantic versioning.
        Args:
            z (str): String containing semantic version.
        Returns:
            tuple: Tuple of the form Major, Minor and Patch.

        """
        return tuple([int(x) for x in z.split('.') if x.isdigit()])

    def ver_cmp(self, a, b):
        """ver_cmp: Semantic Version Comparison.

        Compares two tuples containing semantic version of the form
        Major, Minor and Patch.

        Args:
            a,b (str): Strings containing semantic versions to be compared.
        Returns:
            cmp: Result of python builtin cmp function.
                 Returns -1 if x < y, returns 0 if x == y and 1 if x > y
        """
        return cmp(self.ver_tuple(a), self.ver_tuple(b))

    def infect(self, image):
        """infect: Infect docker image with Provenance.

        Args:
            image (TODO): ImageID

        Returns: TODO

        """
        print("Result" + self.dcli.infect_image(image))
