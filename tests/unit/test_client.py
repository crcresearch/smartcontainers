# -*- coding: utf-8 -*-
"""Tests for Smart Containers Docker API Client.

Testing for Smart Containers Client.
This module extends the docker-py package to provide the ability to add
metadata to docker containers. It is meant to be a drop-in replacement  the
docker-py package Client module. Existing methods that change the state of a
conainer are implimented to also write the provenance associated with that
state change.
"""

import tarfile
import time
import os


def test_simple_tar(createClient):
    """Tarfile creation.

    Create tarfile from sample file and assert that resultant file
    is a tarfile.
    """
    # Create the smartcontainer client
    # Create a test file to be turned into a tar
    with open('tempprov.txt', 'a') as provfile:
        provfile.write('This is the data for the tar file test.')
    # Call the simple tar function and test the result
    thisfile = createClient.simple_tar('tempprov.txt')
    assert tarfile.is_tarfile(thisfile.name)


def test_fileCopyIn(createClient, pull_docker_image):
    """File Copy into container from image.

    Create a new test container and copy tarfile into container.
    """
    newContainer = createClient.create_container(image=pull_docker_image,
                                                 command="/bin/sh", tty=True)
    ContainerID = str(newContainer['Id'])
    createClient.start(ContainerID)
    with open('SCProv.jsonld', 'a') as provfile:
        provfile.write('This is the data for the tar file test.')
    createClient.fileCopyIn(ContainerID, 'SCProv.jsonld', '/')
    assert createClient.hasProv(ContainerID, 'SCProv.jsonld', '/SmartContainer')
    time.sleep(1)
    createClient.stop(ContainerID)
    createClient.remove_container(ContainerID)
    os.remove('SCProv.jsonld')


def test_fileCopyOut(createClient, pull_docker_image):
    """File Copy out of container.

    Create a new test container and copy directory out of container
    as a tarfile.
    """
    newContainer = createClient.create_container(image=pull_docker_image,
                                                 command="/bin/sh", tty=True)
    ContainerID = str(newContainer['Id'])
    createClient.start(ContainerID)
    with open('SCProv.jsonld', 'a') as provfile:
        provfile.write('This is the data for the tar file test.')
    createClient.fileCopyIn(ContainerID, 'SCProv.jsonld', '/')
    createClient.fileCopyOut(ContainerID, 'SCProv.jsonld', '/SmartContainer/')
    assert os.path.isfile('SCProv.jsonld')
    time.sleep(1)
    createClient.stop(ContainerID)
    createClient.remove_container(ContainerID)
    os.remove('SCProv.jsonld')


def test_put_label_image(createClient, pull_docker_image):
    """Add label to docker image.

    Add a label to a test image file and assert the label exists.
    """
    myLabel = {'smartcontainer': '{"author":"Scott B. Szakonyi"}'}
    createClient.put_label_image(image=pull_docker_image,
                                 repository="phusion/baseimage",
                                 tag="tester", label=myLabel)
    # The new image created should be image[0]'s id
    image_list = createClient.images()
    image_id = image_list[0]['Id']
    myInspect = createClient.inspect_image(image_id)
    assert 'Szakonyi' in str(myInspect)
    createClient.remove_image(image_id)


def test_infect_image(createClient, pull_docker_image):
    """TODO: Create new Smart Container from docker image ID.

    First create a new smart container from fixture image. Next make
    sure that if the smart container already exists we don't overwrite the
    existing smart container.
    """
    imageID = str(createClient.inspect_image(pull_docker_image)['Id'])
    imageID = imageID.replace('sha256:', '')
    sc_image = createClient.infect_image(image=imageID)

    # Test creation of existing smart container -- it's a twofur
    existing_sc_image = createClient.infect_image(image=sc_image)
    assert existing_sc_image == None
    # Cleanup image after ourselves
    createClient.remove_image(sc_image)
    # image_list = createClient.images()
    # We assume that if this operation is successful it will be on
    # top of the image list.
    # image_id = image_list[0]['Id']


def test_infect_container(createClient, pull_docker_image):
    """TODO: Create new Smartcontainer from container ID."""
    pass


def test_get_label_image(createClient, pull_docker_image):
    """Get JSON label from imageID."""
    imageID = str(createClient.inspect_image(pull_docker_image)['Id'])
    imageID = imageID.replace('sha256:', '')
    sc_image = createClient.infect_image(image=imageID)
    json_str = createClient.get_label_image(imageID=sc_image)
    assert 'smartcontainer' in str(json_str)
    # print json_str
    createClient.remove_image(sc_image)
