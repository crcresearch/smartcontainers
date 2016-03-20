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
import re
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


class DockerNotFoundError(RuntimeError):
    """Exception raised for missing docker command.

    Attributes:
        msg -- explaination of error
    """

    def __init__(self, msg):
        """Exception message Docker not Found Error."""
        msg = "Please make sure docker is installed and in your path."
        self.arg = msg


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

    def __init__(self):
        """Init has no arguments.

        The __init__ method will attempt to find the docker command line
        and attempt to setup docker-py to connect to the docker client backend.
        The connection variables will be stored in self.
        """
        self.location = None              #: Path to docker command line.
        self.docker_host = None           #: Docker host environment variable.
        self.docker_cert_path = None      #: Docker cert path environment variable.
        self.docker_machine_name = None   #: Docker machine name env variable.
        self.docker_socket_file = None    #: Path to docker socket file.
        self.dcli = None                  #: docker-py client object.

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
        socket_path = "/var/run/docker.socket"
        has_docker_socket_file = os.path.exists(socket_path)
        if has_docker_socket_file:
            mode = os.stat(socket_path).st_mode
            isSocket = stat.S_ISSOCK(mode)
            if isSocket:
                self.docker_socket_file = "unix://" + socket_path
        # Sanity check docker environment to see that we either have
        # docker machine env vars or a running docker server with
        # a socket file.
        if not ((self.docker_host and self.docker_machine_name and
                self.docker_cert_path) or not (has_docker_socket_file)):
            raise DockerNotFoundError("Make docker server is started or env"
                                      "variables for docker-machine are set.")
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
        # #print self.dcli.info()
        elif (self.docker_socket_file):
            self.dcli = client.scClient(base_url=self.docker_socket_file,
                                        version="auto")

        # Assert dcli is not none;
        if self.dcli is not None:
            raise DockerNotFoundError("Docker Client cannot find server.")
        # TODO: test for dcli to make sure it can talk to client.

    def get_location(self):
        """Get path to docker executable.
        
        """
        return self.location

    def sanity_check(self):
        """sanity_check checks existence and executability of docker."""
        if self.location is None:
            self.find_docker()
        self.check_docker_version()
        self.check_docker_connection()

    def check_docker_version(self, min_version=min_docker_version):
        """check_docker_version makes sure docker is of a min version."""
        output = get_stdout('docker --version')
        # in docker 1.7.1 version is at 2 position in returned string
        version = output.split()[2]
        # remove comma from out put if in string
        if ',' in version:
            version = version[:-1]
        if self.ver_cmp(version, min_version) < 0:
            raise DockerInsuficientVersionError(
                "Please  make sure docker is greater than %s" % min_version)

    def check_docker_connection(self):
        output = get_stdout('docker images')
        # This checks if we can get a connection to the remote docker
        # server. It assumes the output of the "docker images"" command is
        # of the form: "Get http:///var/run/docker.sock/v1.19/images/json: dial
        # unix /var/run/docker.sock: no such file or directory. Are you trying
        # to connect to a TLS-enabled daemon without TLS?"
        if 'IMAGE ID' not in output:
            raise DockerServerError("Docker cannot connect to daemon")

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

    def capture_command(self):
        pass

    def capture_cmd_build(self,cmd_string):
        output = capture_stdout(cmd_string)
        #print output.stdout
        #print 'build'
        #pass

    def capture_cmd_commit(self, cmd_string):
        pass


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



# Each image has a metadata record. This returns a list of all label
# strings contained in the metadata.
    def get_metadata(self):
        docker_command = str(self.location) + ' inspect ' + self.imageID
        p = Command(docker_command, stdout=Capture(buffer_size=-1))
        p.run()
        # Testing directly in the string works if the output is only
        # one line.
        # if 'No such image' in p.stdout:
        # raise DockerImageError
        # data = [json.loads(str(item)) for item in p.stdout.readline().strip().split('\n')]
        json_block = []
        line = p.stdout.readline()
        while (line):
            if 'no such image' in line:
                raise DockerImageError
            # Stupid sarge appears to add a blank line between
            # json statements. This checks for a blank line and
            # cycles to the next line if it is blank.
            if re.match(r'^\s*$', line):
                line = p.stdout.readline()
                continue
            json_block.append(line)
            line = p.stdout.readline()
        s = ''.join(json_block)
        s = s[1:-2]
        self.metadata = s


    def set_image(self, image):
        """set_image
            sets docker image id to docker object.
            :param image: image id
            """
        self.imageID = image


    def set_command(self, command):
        """set_command
            sets the docker command to docker object
            :param command: docker command
            """
        if len(command) > 0:
            self.command = command
        else:
            raise DockerInputError("Invalid Command")

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
