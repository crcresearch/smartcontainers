import pytest
import os
from sys import platform as _platform

# Test code that discovers docker command
# This is a bad hack right now
# The correct way should be monkeypatch fixtures
# http://holgerkrekel.net/2009/03/03/monkeypatching-in-unit-tests-done-right/
def test_DockerCli():
    from sc import dockercli
   

    oldenv = os.environ.copy()
    # Test location first
    oldpath = os.environ["PATH"]
    with pytest.raises(dockercli.DockerNotFoundError):
        # check that exceptions are being raised.
        os.environ["PATH"] = "NULL"
        dockertester2 = dockercli.DockerCli()
    os.environ["PATH"] = oldpath
    # Test environment variables on MacOS
    if _platform == "darwin":
        docker_host = os.environ["DOCKER_HOST"]
        with pytest.raises(dockercli.DockerNotFoundError):
            os.environ.clear()
            dockertester = dockercli.DockerCli()
        os.environ.update(oldenv)
        dockertester.check_docker_connection()
    if _platform == "linux":
        dockertester = dockercli.DockerCli()
    dockertester3 = dockercli.DockerCli()
    assert dockertester3.location is not None

# def test_docker_version():
#     from sc import dockercli
#    with pytest.raises(dockercli.DockerInsuficientVersionError):
#        # This will fail if docker ever gets to version 100
#        dockertester = dockercli.DockerCli()
#        dockertester.check_docker_version("100.100.100")

# def test_check_docker_connection():
#    from sc import dockercli
#    dockertester = dockercli.DockerCli()
#    if _platform == "darwin":
#        docker_host = os.environ["DOCKER_HOST"]
#        with pytest.raises(dockercli.DockerServerError):
#            os.environ["DOCKER_HOST"] = "tcp://127.0.0.1:1000"
#            dockertester.check_docker_connection()
#        os.environ["DOCKER_HOST"] = docker_host
#        dockertester.check_docker_connection()
#    else:
#        dockertester.check_docker_connection()

# Test all sanity checks to make sure docker is there.
# def test_sanity():
#    from sc import dockercli
#    dockertester = dockercli.DockerCli('help')
#    dockertester.sanity_check()

# This test should pass through since we don't capture the
# provenance of help.
# def test_do_command_simple():
#    from sc import dockercli
#    dockertester = dockercli.DockerCli('--help')
#    dockertester.do_command()

# def test_do_command_run():
#    from sc import dockercli
#    dockertester = dockercli.DockerCli('run /usr/bin/uname')
#    dockertester.do_command()

# Tests function that returns the current image id for
# "phusion/baseimage"
# def test_get_imageID(pull_docker_image):
#    from sc import dockercli
#    dockertester = dockercli.DockerCli('images')
#    imageID = dockertester.get_imageID(pull_docker_image)
#    # assert imageID == "e9f50c1887ea"

# def test_put_label_image(pull_docker_image):
#    from sc import dockercli
#    dockertester = dockercli.DockerCli('images')
#    imageID = dockertester.get_imageID(pull_docker_image)
#    dockertester.set_image(imageID)
#    label = '{"Description":"A containerized foobar","Usage":"docker run --rm example/foobar [args]","License":"GPL","Version":"0.0.1-beta","aBoolean":true,"aNumber":0.01234,"aNestedArray":["a","b","c"]}'
#    dockertester.put_label_image(label)

# def test_docker_get_metadata(pull_docker_image):
#    from sc import dockercli
#    dockertester = dockercli.DockerCli('images')
#    imageID = dockertester.get_imageID(pull_docker_image)
#    dockertester.set_image(imageID)
#    label = dockertester.get_metadata()

# def test_docker_get_label(pull_docker_image):
#    from sc import dockercli
#    dockertester = dockercli.DockerCli('images')
#    imageID = dockertester.get_imageID(pull_docker_image)
#    dockertester.set_image(imageID)
#    #label = dockertester.get_label(imageID)
