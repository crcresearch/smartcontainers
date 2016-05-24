import click
import os
import rdflib
from rdflib import Literal, Namespace
from rdflib.namespace import FOAF
import uuid
from configmanager import ConfigManager
from orcidmanager import OrcidManager
from orcidprofilesearch import orcid_search
from dockercli import DockerCli

# from ._version import __version__

# Set sandbox variable
sandbox = True


class Settings(object):
    def __init__(self, home=None, debug=False):
        self.home = os.path.abspath(home or '.')
        self.debug = debug

graph = rdflib.Graph()
config_file = ConfigManager()

@click.group()
@click.version_option()
@click.pass_context
def cli(ctx):
    """Smartcontainers for software and data preservation.
    Smartcontainers provides a mechanism to add metadata to Docker
    containers as a JSON-LD label. The metadata is contextualized using
    W3C recommended PROV-O and ORCID IDs to capture provenance information.
    The sc command wraps the docker commandline interface and passes any
    docker command line parameters through to docker. Any command that changes
    the state of the container is recorded in a prov graph and attached to the resultant
    image.
    """

    # Ignore config loading if we intend to create an orcid config
    if ctx.args[0] == "config" and ctx.args[1] == "orcid":
        return

    Success = False
    while not Success:
        result = config_file.read_config()
        if 'Configuration does not exist.' in result:
            print("User configuration needs to be initialized")
            selected = None
            while not selected:
                try:
                    selected = click.prompt('Do you have an ORCID profile (Y/N)')
                    if selected.lower() == 'y' or selected.lower() == 'yes':
                        config_by_search()
                        continue

                    if selected.lower() == 'n' or selected.lower() == 'no':
                        print("Please provide some basic information:")
                        query = {
                            'first_name': click.prompt(
                                'Please enter a first name', default='',
                                show_default=False
                            ),
                            'last_name': click.prompt(
                                'Please enter a last name', default='',
                                show_default=False
                            )
                        }
                        dockerUseruuid = str(uuid.uuid4())
                        UUIDNS = Namespace("urn:uuid:")
                        config_file.graph.bind("foaf", FOAF)
                        config_file.graph.add( ( UUIDNS[dockerUseruuid], FOAF.givenName, Literal(query['first_name']) ) )
                        config_file.graph.add( ( UUIDNS[dockerUseruuid], FOAF.familyName, Literal(query['last_name']) ) )

                        config_file.config_obj = config_file.graph.serialize(format='turtle')
                        config_file.write_config()
                except KeyError:
                    print('That is not a valid selection.  Please try again.\n')
        else:
            Success = True
            graph = config_file.graph


@cli.group()
@click.option('--config', '-c', help='Run configure command')
def config(config):
    """Configure smartcontainers. Run sc config to get subcommand options for configuring

    :param config: string
    """

    pass


# We may have to manually handle --help and pass it to docker
@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('command', nargs=-1, type=click.UNPROCESSED)
def docker(command):
    """Execute a docker command.
    Example: sc docker run <container id>

    :param command: string
    """
    cmd = ""
    for i in range(len(command)):
        cmd += command[i] + " "

    processdocker = DockerCli()
    processdocker.do_command(cmd)


@cli.command()
@click.argument('image')
def search(image):
    """Search for information in docker metadata.

    :param image: string
    """
    pass


@cli.command()
@click.argument('image')
def printlabel(image):
    """Print Metadata label from container."""
    processdocker = DockerCli("info")
    this_label = processdocker.get_label(image)
    print this_label


@cli.command()
@click.argument('image')
def publish(image):
    """Publish a image to a public repository.

    :param image: string
    """
    pass


@cli.command()
def preserve():
    """Preserve workflow to container using umbrella."""
    pass

@cli.command()
@click.argument('image')
def infect(image):
    """Provenance should be contagious. Create smartcontainer image from
    existing image. """
    processdocker = DockerCli()
    processdocker.infect(image)

#  Orcid Commands  ################################
#  cwilli34
@config.command()
@click.option('-i', default=None, help='Search for an Orcid profile by Orcid ID.')
@click.option('-e', default=None, help='Search for an Orcid profile by email.')
def orcid(i, e):
    """Create a config file, based on an Orcid ID.

    :param i: string
        (Optional) Option to enter Orcid ID if known
    :param e: string
        (Optional) Option to enter Orcid email if known
    """
    # Make sure sandbox variable is set correctly in cli.py before testing
    if i:
        config_by_id(i)
    elif e:
        config_by_email(e)
    elif i is None and e is None:
        config_by_search()
    else:
        print('You have not selected a viable option.')


def config_by_search():
    """Create a RDF Graph configuration file by searching for Orcid user."""
    orcid_profile = orcid_search(sandbox=False)
    if orcid_profile is not None:
        orcid_manager = OrcidManager(sandbox=False, orcid_id=orcid_profile)
        turtle_data = orcid_manager.get_turtle()
        config_file = ConfigManager()
        config_file.config_obj = turtle_data
        config_file.write_config()
    else:
        print("Sorry, ORCID returned no resutls for that user information.")


def config_by_id(orcid_id):
    """Create a RDF Graph configuration file by Orcid ID.

    :param orcid_id: string
        Orcid ID used for the configuration file ID and to create the configuration file.
    """
    # Make sure sandbox variable is set correctly in cli.py before testing
    orcid_profile = OrcidManager(orcid_id=orcid_id, sandbox=False)
    turtle_data = orcid_profile.get_turtle()
    config_file = ConfigManager()
    config_file.get_config(_id=orcid_profile.orcid_id, _data=turtle_data)
    config_file.write_config()


def config_by_email(email):
    """Create a RDF Graph configuration file by Orcid email.

    :param email: string
        Orcid email address used to create a configuration file.
    """
    # Make sure sandbox variable is set correctly in cli.py before testing
    email = 'email:' + email
    orcid_profile = OrcidManager(orcid_email=email, sandbox=False)
    turtle_data = orcid_profile.get_turtle()
    config_file = ConfigManager()
    config_file.get_config(_id=orcid_profile.orcid_id, _data=turtle_data)
    config_file.write_config()

#  End Orcid  ###############################
if __name__ == '__main__':
    cli()
