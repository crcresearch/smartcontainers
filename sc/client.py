import docker


class scClient(docker.Client):
    def __init__(self, *args, **kwargs):
         super(scClient, self).__init__(*args, **kwargs)
         print "Baking a smart cake"


    def info(self):
        print "Now we can have an awesome smart cake"
        super(scClient,self).info()



