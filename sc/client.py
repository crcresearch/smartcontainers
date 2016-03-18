# Client.py

import docker
import glob
import os
import scMetadata
import io
import pprint
import re
import tempfile
import tarfile
import provinator
import json
import glob

class scClient(docker.Client):

    def __init__(self, *args, **kwargs):
        super(scClient, self).__init__(*args, **kwargs)

        #Initialize variable and objects
        self.scmd = scMetadata.scMetadata()
        self.provfilepath = "/SmartContainer/"
        self.provfilename = "SCProv.jsonld"
        self.label_prefix = "smartcontainer"

    def commit(self, container, *args, **kwargs):
        #Extends the docker-py commit command to include smartcontainer functions
        #Check if the container being committed has previous provenance information stored in it.
        if self.hasProv(container,self.provfilename,self.provfilepath):
            #Retrieve provenance file from the container
            self.fileCopyOut(container,self.provfilename, self.provfilepath)
            #Append provenance data to file
            self.scmd.appendData(self.provfilename)
            #Copy provenance file back to the container
            self.fileCopyIn(container, self.provfilename, self.provfilepath)
            #Remove the local copy of the provenance file
            os.remove(self.provfilename)
            # #Commit the container changes
            newImage = super(scClient, self).commit(container=container, *args,
                                                    **kwargs)
            #Get the ID of the newly created image
            thisID = newImage['Id']
            #Get the label contents in dictionary form.
            newLabel = self.scmd.labelDictionary(self.label_prefix)
            #Write the label to the new image
            self.put_label_image(thisID, newLabel, *args, **kwargs)

        else:
            pass

    def build(self, *args, **kwargs):
        #path or fileobj must exist. If not, we should abort

        #Build Metadata

        #Execute the build
        generator = super(scClient,self).build(*args, **kwargs)

    def put_label_image(self, image, label, *args, **kwargs):
        #Write the label to the new image
        #Create a new container with the label, commit it and then remove the container.
        newContainer = super(scClient, self).create_container(image=image, command="/bin/sh", labels=label)
        super(scClient, self).commit(container=newContainer, *args, **kwargs)
        super(scClient, self).remove_container(newContainer)

    def fileCopyOut(self, containerid, filename, path):
        #Copies file from container to local machine.
        #File transmits as a tar stream. Saves to local disk as tar.
        #Extracts file for local manipulation.
        tarObj, stats = super(scClient, self).get_archive(container=containerid,path=path + filename)
        with open('temp.tar', 'w') as destination:
            for line in tarObj:
                destination.write(line)
            destination.seek(0)
            thisTar = tarfile.TarFile(destination.name)
            thisTar.extract(filename)
            os.remove('temp.tar')

    def fileCopyIn(self, containerid, filename, path):
        #Copies file from local machine to container.
        #Converts file to temporary tar for transfer.
        with self.simple_tar(filename) as thisTar:
            super(scClient, self).put_archive(containerid, path, thisTar)

    def hasProv(self, containerid, filename, path):
        #Get a directory listing from the target directory inside the container.
        #Examine the directory contents for the provenance file.
        #Return true if found, false if not found.
        execid = super(scClient, self).exec_create(container=containerid, stdout=True, cmd='ls ' + path)
        text   = super(scClient, self).exec_start(exec_id=execid)
        if 'SCProv.jsonld' in text:
            return True
        return False

    def simple_tar(self, path):
        #Creates temporary tar file from file specified in path.
        # Returns tar file.
        # t_dir = tempfile.mkdtemp(prefix='app-')
        f = tempfile.NamedTemporaryFile()
        tar = tarfile.open(mode='w', fileobj=f)

        abs_path = os.path.abspath(path)
        for filex in glob.glob(abs_path):
            if filex:
                archname = re.sub(abs_path,'%s/%s' % (self.provfilepath, path), filex)
                tar.add(abs_path, arcname=archname, recursive=False)

        tar.close()
        f.seek(0)
        return f
