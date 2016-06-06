# -*- coding: utf-8 -*-
"""Smart Containers Docker API Client.

This module extends the docker-py package to provide the ability to add
metadata to docker containers. It is meant to be a drop-in replacement  the
docker-py package Client module. Existing methods that change the state of a
conainer are implimented to also write the provenance associated with that
state change.
"""


import docker
import glob
import json
import re
import os
import scMetadata
import tempfile
import tarfile
import buildProcessor


class scClient(docker.Client):
    """scClient Class extends Docker-py Client class and Docker API."""

    def __init__(self, *args, **kwargs):
        """Initialize docker-py client with standard arguments.

        Sets smartcontainer metadata path and docker label key.
        """
        super(scClient, self).__init__(*args, **kwargs)

        # Initialize variable and objects
        self.scmd = scMetadata.scMetadata()
        self.provfilepath = "/SmartContainer/"
        self.provfilename = "SCProv.jsonld"
        self.label_prefix = "smartcontainer"

    def commit(self, container, *args, **kwargs):
        """Docker Commit that also updates a smart container object.

        Args:
            container: Container ID

        Returns: Nothing.

        """
        # Extends the docker-py commit command to include
        #              smartcontainer functions
        # Check if the container being committed has previous
        #                     provenance information stored in it.
        if self.hasProv(container, self.provfilename, self.provfilepath):
            # Retrieve provenance file from the container
            self.fileCopyOut(container, self.provfilename, self.provfilepath)
            # Append provenance data to file
            self.scmd.appendData(self.provfilename)
            # Copy provenance file back to the container
            self.fileCopyIn(container, self.provfilename, self.provfilepath)
            # Remove the local copy of the provenance file
            os.remove(self.provfilename)
            # Commit the container changes
            newImage = super(scClient, self).commit(container=container, *args,
                                                    **kwargs)
            # Get the ID of the newly created image
            thisID = newImage['Id']
            # Get the label contents in dictionary form.
            newLabel = self.scmd.labelDictionary(self.label_prefix)
            # Write the label to the new image
            self.put_label_image(thisID, newLabel, *args, **kwargs)

        else:
            super(scClient, self).commit(container, *args, **kwargs)

    def build(self, *args, **kwargs):
        """build; Docker Build for smartcontainers.

        Args:
            image: Image ID
            label: Label string to write to the container

        Returns: Nothing.

        """
        # Build Metadata
        # Instanciate the build processor
        BP = buildProcessor.buildProcessor()

        # path or fileobj must exist. If not, we let the docker-py interface handle any error reporting
        if "path" in kwargs and kwargs['path'] != None:
            BP.processDF(kwargs['path'])
        elif "fileobj" in kwargs and kwargs['fileobj'] != None:
            BP.processFO(kwargs['fileobj'])

        Id = ""

        generator = None
        try:
            # Execute the build
            generator = super(scClient, self).build(*args,  **kwargs)
        except TypeError:
            raise
        else:
            response = [line for line in generator]
            final_line = response[len(response)-1]

            # Handle strange case of two lines in generated last line
            lines = final_line.split("\r\n")
            if len(lines) > 1:
                if len(lines[0]) == 0:
                    final_line = lines[1]
                else:
                    final_line = lines[0]

            fJson = json.loads(final_line)
            if "Successfully built" in fJson['stream']:
                Id = fJson['stream'].split(' ')[2].strip()

            for line in super(scClient, self).images():
                fullID = line['Id'].replace("sha256:", "")
                if fullID.startswith(Id):
                    return fullID
            return ""
        finally:
            if "fileobj" in kwargs:
                kwargs["fileobj"].close()

    def put_label_image(self, image, label, *args, **kwargs):
        """Write a new label to a new image.

        Args:
            image: Image ID
            label: Label string to write to the container

        Returns: Nothing.

        """
        # Write the label to the new image
        # Create a new container with the label,
        #    commit it and then remove the container.

        newContainer = super(scClient, self).create_container(
            image=image, command="/bin/sh", labels=label)
        super(scClient, self).commit(container=newContainer, *args, **kwargs)
        super(scClient, self).remove_container(newContainer)

    def fileCopyOut(self, containerid, filename, path):
        """Copy file from container to the local machine.

        Args:
            containerid: Container ID
            filename: Name of file to be copied in.
            path: Path in the container where file should be copied.
        Returns: Nothing.

        """
        # Copies file from container to local machine.
        # File transmits as a tar stream. Saves to local disk as tar.
        # Extracts file for local manipulation.
        tarObj, stats = super(scClient,
                              self).get_archive(container=containerid,
                                                path=path + filename)
        with open('temp.tar', 'w') as destination:
            for line in tarObj:
                destination.write(line)
            destination.seek(0)
            thisTar = tarfile.TarFile(destination.name)
            thisTar.extract(filename)
            os.remove('temp.tar')

    def fileCopyIn(self, containerid, filename, path):
        """Copy file from local machine to container.

            Creates tar file for transfer.

        Args:
            containerid: Container ID
            filename: Name of file to be copied in.
            path: Path in the container where file should be copied.
        Returns: Nothing.

        """
        # Copies file from local machine to container.
        # Converts file to temporary tar for transfer.
        with self.simple_tar(filename) as thisTar:
            super(scClient, self).put_archive(containerid, path, thisTar)

    def hasProv(self, containerid, filename, path):
        """Check for Smart Container directory inside container.

        Args:
            containerid: Container ID
            filename: Name of file to be copied in.
            path: Path in the container where file should be copied.
        Returns: Nothing.

        """
        # Get a directory listing from the
        #      target directory inside the container.
        # Examine the directory contents for the provenance file.
        # Return true if found, false if not found.
        execid = super(scClient, self).exec_create(container=containerid,
                                                   stdout=True,
                                                   cmd='ls ' + path)
        text = super(scClient, self).exec_start(exec_id=execid)
        if 'SCProv.jsonld' in text:
            return True
        return False

    def simple_tar(self, path):
        """Create tarfile.

        Args:
            path: Path to file object.

        Returns: Nothing.

        """
        # Creates temporary tar file from file specified in path.
        # Returns tar file.
        # t_dir = tempfile.mkdtemp(prefix='app-')
        f = tempfile.NamedTemporaryFile()
        tar = tarfile.open(mode='w', fileobj=f)

        abs_path = os.path.abspath(path)
        for filex in glob.glob(abs_path):
            if filex:
                archname = re.sub(abs_path,
                                  '%s/%s' % (self.provfilepath, path), filex)
                tar.add(abs_path, arcname=archname, recursive=False)

        tar.close()
        f.seek(0)
        return f

    def infect_image(self, image, *args, **kwargs):
        """Create new smart container from image.

        Args:
            image: Image ID

        Returns:
            image: New image ID of the Smart Container. If already a Smart
        Container returns None.

        """
        # Look for the smart container label, if it exists return none
        myInspect = super(scClient, self).inspect_image(image)
        labels = myInspect['ContainerConfig']['Labels']
        if labels is not None:
            if self.label_prefix in myInspect['ContainerConfig']['Labels']:
                return None

        # Get label contents in dictionary form
        newlabel = self.scmd.labelDictionary(self.label_prefix)

        # Get new container from image.
        newContainer = super(scClient, self).create_container(image=image,
                                                              command="/bin/sh",
                                                              labels=newlabel)
        ContainerID = str(newContainer['Id'])
        super(scClient, self).start(ContainerID)

        # Get metadata.
        self.scmd.appendData(self.provfilename)

        # Copy file into container.
        self.fileCopyIn(newContainer, self.provfilename, "/")
        # Remove local copy of provenance file
        os.remove(self.provfilename)

        # Commit the container changes
        if 'path' in kwargs:
            del kwargs['path']

        tName = ""
        if 'tag' in kwargs:
            tName = kwargs['tag']
            del kwargs['tag']

        newImage = super(scClient, self).commit(container=ContainerID, *args,
                                                **kwargs)
        # Update Tag
        if tName is not "":
            repository = ""
            tag = ""

            parts = tName.split(":")
            repository = parts[0]
            if len(parts) is 1:
                tag = "latest"
            else:
                tag = parts[1]

            super(scClient, self).tag(image=str(newImage['Id']).replace("sha256:", ""), repository=repository, tag=tag)

        # Stop container
        super(scClient, self).stop(ContainerID)
        super(scClient, self).remove_container(ContainerID)
        newImageID = str(newImage['Id'])
        return newImageID

    def get_label_image(self, imageID):
        """Get Smart Container Metadata Label from image.

        Args:
            imageID: Id for image that label is requested

        Returns:
            metadata: Label String in JSON-LD

        """
        # Look for the smart container label, if it exists return none
        myInspect = super(scClient, self).inspect_image(imageID)
        labels = myInspect['ContainerConfig']['Labels']
        if labels is not None:
            # print json.dumps(labels, ensure_ascii=False, sort_keys=True, indent=4,
            #                 separators=(',', ':')).encode('utf8')
            return json.dumps(labels)
        return None

    def get_label_container(self, containerID):
        """Get Smart Container Metadata Label from a container.

        Args:
            containerID (TODO): Container ID
        Returns:
            metadata: Label String in JSON-LD

        """
        pass
