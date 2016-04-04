from rdflib import Literal, BNode, Namespace, URIRef, Graph, Dataset, RDF, RDFS, XSD
from rdflib.namespace import FOAF
from rdflib.serializer import Serializer
import rdflib.resource
import uuid

#  Create a default dataset graph.
ds = Dataset(default_union=True)

# J SON-LD serializer requires an explicit context.
#  https://github.com/RDFLib/rdflib-jsonld
#  context = {"@vocab": "http://purl.org/dc/terms/", "@language": "en"}

context = {"prov": "http://www.w3.org/ns/prov#",
           "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
           "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
           "xsd": "http://www.w3.org/2001/XMLSchema#",
           "dc": "http://purl.org/dc/terms"}

# Define some namespaces
PROV = Namespace("http://www.w3.org/ns/prov#")
ORE = Namespace("http://www.openarchives.org/ore/terms/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
DC = Namespace("http://purl.org/dc/terms/")
UUIDNS = Namespace("urn:uuid:")
DOCKER = Namespace("http://w3id.org/daspos/docker#")
# W3C namespace:
POSIX = Namespace("http://www.w3.org/ns/posix/stat#")
ACL = Namespace("http://www.w3.org/ns/auth/acl#")

# DASPOS namespaces
SC = Namespace("https://w3id.org/daspos/smartcontainers#")
CA = Namespace("https://w3id.org/daspos/computationalactivity#")
CE = Namespace("https://w3id.org/daspos/computationalenvironment#")


# Need to handle DOI
# http://bitwacker.com/2010/02/04/dois-uris-and-cool-resolution/

ds.bind("prov", PROV)
ds.bind("ore", ORE)
ds.bind("owl", OWL)
ds.bind("dc", DC)
ds.bind("uuidns", UUIDNS)
ds.bind("docker", DOCKER)
ds.bind("posix", POSIX)
ds.bind("acl", ACL)
ds.bind("sc", SC)
ds.bind("ca", CA)
ds.bind("ce", CE)

default_graph = ds


# image_name = cmd_string.rsplit(' ', 1) [1]
# image_id = self.get_imageID(image_name)
# self.set_image(image_id)
# label = self.get_label()
# run_time = str(datetime.datetime.now())
# host_name = socket.gethostname()
# this_user = os.getlogin()
# prev_container = self.get_prev_container()
# docker_path = str(self.location)
# docker_version = self.get_docker_version()
# hash = random.getrandbits(32)
# prev_label = self.get_label()
# print "hash value: %08x" % hash
# subprocess.Popen(cmd_string, shell=True, stdin=None,
# stdout=None, stderr=None, close_fds=True)
# time.sleep(1)
# container_id = self.get_containerID(image_name)
# print 'CID:' + container_id
# print 'commit'


# Generate URI's for docker instance
dockerEntityuuid = str(uuid.uuid4())
dockerActivityuuid = str(uuid.uuid4())
### WARNING WARNING this needs to be generated and stored in the config.
dockerUseruuid = str(uuid.uuid4())

# Add entity triples first
ds.add((UUIDNS[dockerEntityuuid], RDF.type, PROV.Entity))
ds.add((UUIDNS[dockerEntityuuid], RDF.type, DOCKER.Entity))
ds.add((UUIDNS[dockerEntityuuid], PROV.wasGeneratedBy,
        UUIDNS[dockerActivityuuid]))
ds.add((UUIDNS[dockerEntityuuid], DOCKER.hasImageID, Literal("ImageIDString")))

# Add activity triples next including computational activity.
ds.add((UUIDNS[dockerActivityuuid], RDF.type, PROV.Activity))
ds.add((UUIDNS[dockerActivityuuid], RDF.type, CA.compuatationalActivity))
# Need sublcass of docker related activities
ds.add((UUIDNS[dockerActivityuuid], RDF.type, DOCKER.commitActivity))
ds.add((UUIDNS[dockerActivityuuid], DOCKER.hasCommand, DOCKER.commitOperation))
ds.add((UUIDNS[dockerActivityuuid], DOCKER.hasContainerID, Literal("blahID")))
ds.add((UUIDNS[dockerActivityuuid],
        DOCKER.hasContainerTag, Literal("GreatContainer")))
ds.add((UUIDNS[dockerActivityuuid],
        PROV.startedAtTime, Literal("2015-11-10T01:30:00Z",
                                    datatype=XSD.dateTime)))
ds.add((UUIDNS[dockerActivityuuid],
        PROV.endedAtTime, Literal("2015-11-10T03:40:00Z",
                                  datatype=XSD.dateTime)))


# For a provisioning activity, we need the docker workflow in doing the previsioning plus


# Computational Environment






# Add agent info last. Docker is a software agent actingOnBelhalfof
ds.add((SC.sc, RDF.type, PROV.SoftwareAgent ))
ds.add((SC.sc, SC.hasVersion, Literal("0.0.1")))
ds.add((DOCKER.docker, PROV.actedOnBehalfOf, SC.sc ))
ds.add( (DOCKER.docker, RDF.type, PROV.SoftwareAgent ) )
ds.add( (DOCKER.docker, RDFS.label, Literal("Docker: https://www.docker.com/")))
ds.add( (DOCKER.docker, RDFS.seeAlso, URIRef(u"https://www.docker.com/")))
# This need to be put somewhere
ds.add( (DOCKER.docker, DOCKER.hasVersion, Literal("Docker version 1.9.1, build a34a1d5")))
ds.add( (SC.sc, PROV.actedOnBehalfOf, UUIDNS[dockerUseruuid]))
# If docker calls another software agent, we need to specifiy that here.


### WARNING --- DANGER --- DANGER --- WARNING
# Chuck's orcid ID as an example, this needs to get poked in from
# the config graph.

chuckORIDchuck = URIRef("http://orcid.org/000-0003-4901-6059")
chuckORID = URIRef("http://orcid.org/000-0003-4901-6059/")

# Add human Agent info
ds.add( ( UUIDNS[dockerUseruuid], RDF.type, PROV.Person))
ds.add( ( UUIDNS[dockerUseruuid], RDF.type, FOAF.Person))
# Not sure if I'm happy with strong statement.
ds.add( ( UUIDNS[dockerUseruuid], OWL.sameAs, chuckORIDchuck))
# Add account info from config, this should include ORCID
ds.add( ( UUIDNS[dockerUseruuid], FOAF.account, chuckORID))
# User name and hostname info should go here from docker host or from "Dashboard system"
ds.add( ( UUIDNS[dockerUseruuid], FOAF.account, URIRef("cvardema@ssh://crcfe.crc.nd.edu")))
ds.add( ( UUIDNS[dockerUseruuid], FOAF.givenName, Literal("Charles") ) )
ds.add( ( UUIDNS[dockerUseruuid], FOAF.familyName, Literal("Vardeman II") ) )





# Main function just prints the graph right now for testing:
def main():
    print "--- start: turtle ---"
    print ds.serialize(format="turtle")
    print "--- end: turtle ---\n"
    print "-- start: json-ld ---"
    print ds.serialize(format='json-ld', context=context, indent=4)
    print "--- end: json-ld ---"

if __name__ == "__main__":
    main()

def get_json_ld():
    return ds.serialize(format='json-ld', context=context, indent=4)

def get_commit_data():
    return ds.serialize(format='json-ld', context=context, indent=4)

def get_commit_label():
    return ds.serialize(format='json-ld', context=context, indent=4)
