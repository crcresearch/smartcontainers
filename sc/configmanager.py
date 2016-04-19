"""Configuration manager for reading and writing SC configuration files."""

import simplejson as json
import os

__author__ = 'cwilli34'


# noinspection PyBroadException,PyBroadException
class ConfigManager(object):
    """ Configuration File Creator """

    def __init__(self, filename='sc.config'):
        """Initialize

        Parameters
        ----------
        :param filename: string
            For renaming the configuration file name.  Default value.

        Returns
        -------
        :returns: none
        """
        self.filename = filename

        if os.environ.get('SC_HOME'):
            self.config_path = os.getenv('SC_HOME')
        else:
            os.environ['SC_HOME'] = os.environ['HOME'] + '/.sc/'
            self.config_path = os.getenv('SC_HOME')

    def write_config(self):
        """Write the configuration file
           Writes the configuration file to the SC directory, or program home directory

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns: none
        """
        if os.path.exists(self.config_path):
            # Open existing file, read and write
            ctgfile = open(self.config_path + self.filename, 'w+')
        else:
            # Create config file, write
            os.mkdir(self.config_path)
            ctgfile = open(self.config_path + self.filename, 'w')

        try:
            ctgfile.write(str(self.config_obj))
            # ctgfile.write(json.dumps(self.config_obj, indent=4, sort_keys=True))
            ctgfile.close()
            print('The configuration file has been created.')
        except:
            print('An unexpected error has occurred.  The configuration file could not be created.')
            ctgfile.close()

    def read_config(self):
        """Read the configuration file.  The configuration file is in a Turtle syntax format and
            is intended for RDF graph creation.  The 'result' returned will be parsed as RDF

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns message: string
            If the configuration file does not exist, return error string
        """
        # g = rdflib.Graph()
        if not os.path.exists(self.config_path):
            # If the directory does not exist, we cannot read it.
            message = 'Directory does not exist. Cannot read file.'
            return message
        elif not os.path.exists(self.config_path + self.filename):
            # If the file does not exist, we cannot read it.
            message = 'File does not exist. Cannot read file.'
            return message
        else:
            # Open existing file, read and write
            ctgfile = open(self.config_path + self.filename, 'r')
            # Variable data is not used (This is for customizing the script later for future configuration).
            try:
                contents = ctgfile.read()
                self.config_object = contents
                ctgfile.close()
                message = 'File was read successfully.'
                return message
            except:
                ctgfile.close()
                message = 'File could not be read.  Please try again.'
                return message
