"""Class that receives an Orcid ID and Python requests to lookup user data and
   output to Turtle syntax.  It also finds an Orcid ID for basic search terms
   and email address searches.
"""

import orcid
import requests
import click

# noinspection PyBroadException
class OrcidManager(object):
    """Class for OrcidManager"""

    def __init__(self, query=None, orcid_id=None, orcid_email=None, sandbox=True):
        """Initialize

        Parameters
        ----------
        :param orcid_id: string
            Needs orcid_id to perform a request by orcid_id.
        :param orcid_email: string
            Needs an email address to perform a request by email.
        """
        self.api = orcid.SearchAPI(False)
        if orcid_email:
            self.data = self.basic_search(orcid_email)
            self.orcid_id = self.get_id()
        elif query:
            self.basic_search(query)
            self.orcid_id = self.select_id()
        else:
            self.orcid_id = orcid_id

        if self.orcid_id is not None:
            try:
                self.url = self.api._endpoint_public + '/' + self.orcid_id
                self.headers = {'Accept': 'text/turtle'}
                self.turtle_config = None
            except:
                print('Orcid ID or email is invalid.  Please try again.')
                exit()

    def get_id(self):
        """Get the Orcid_id from the email search

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns orcid_id[0]: string
            returns the Orcid ID from the email search
        """
        if not self.data:
            print('No data was found.')
        else:
            orcid_id = self.data.keys()
            return orcid_id[0]

    def get_turtle(self):
        """Get the user information in a Turtle syntax

        Parameters
        ----------
        :param: None

        Returns
        -------
        :returns self.turtle_config.text: string
            user data in a text format with Turtle syntax
        """
        self.turtle_config = requests.get(self.url, headers=self.headers)
        if (self.turtle_config.status_code == 404) or (self.turtle_config.status_code == 500):
            print('Orcid ID not found.  Please try again.')
            exit()
        else:
            print(str(self.url) + ", Status: " +
                  str(self.turtle_config.status_code))
            return self.turtle_config.content

    def select_id(self):
        """ Function for initializing a search for an orcid id, and then creates a RDF
            configuration file automatically.

        Parameters
        ----------
        :param query: string
            Query built from user input.

        Returns
        -------
        :returns: no return.
        """

        # Initialize and populate all variables and dictionaries
        actual_total = self.actual_total_results
        total_results = self.total_results

        # Print results
        self.print_basic_alt()

        # Print total results if actual results are above 100
        if total_results < actual_total:
            print('Actual Total Results: {}'.format(actual_total))
            print('')

        # Get list of Orcid ID's from results
        id_list = self.orcid_id

        # Return ID if only one result was found
        if total_results == 1:
            orcid_id = id_list[0]
            return orcid_id
        # If no results are found
        elif total_results == 0:
            print("No results where found. Please try again.\n")
            orcid_id = None
            return orcid_id

        # Allow user to select Orcid profile if multiple results are found
        else:
            id_dict = dict()
            # Get list of Orcid ID's and correspond count with ID
            for i, d in enumerate(id_list):
                id_dict[i + 1] = d

            selected = None
            while not selected:
                try:
                    selected = click.prompt('Select the result # of the record (Type "N" for another search, '
                                            '"Exit" to abort)')
                    print("")
                    orcid_id = id_dict[int(selected)]
                    return orcid_id
                except KeyError:
                    print('That is not a valid selection.  Please try again.\n')
                    selected = None
                except ValueError:
                    if selected in ('N', 'n'):
                        return None
                    elif selected in ('exit', 'Exit', 'EXIT'):
                        exit()
                    else:
                        print('That is not a valid selection.  Please try again.\n')
                        selected = None

    def basic_search(self, query):
        """Basic search based on search terms entered by user to find an Orcid ID.
        Parameters
        ----------
        :param query: string
            A phrase, or group of search terms with boolean operators for lucene search
        Returns
        -------
        :returns self.s_dict: dict type
            Records with minimal information based on search terms used.
        """
        search_results = self.api.search_public(query, start=0, rows=100)
        results = search_results.get('orcid-search-results', None)
        self.actual_total_results = results.get('num-found', 0)
        result = results.get('orcid-search-result', None)

        # Actual results versus displayed results
        if self.actual_total_results > 99:
            self.total_results = 100
        else:
            self.total_results = self.actual_total_results

        # Only last name, first name, Orcid ID, and email will be displayed for
        # each record
        for p in range(self.total_results):
            try:
                f_name = result[p][
                    'orcid-profile']['orcid-bio']['personal-details']['given-names']['value']
            except TypeError:
                pass
            try:
                l_name = result[p][
                    'orcid-profile']['orcid-bio']['personal-details']['family-name']['value']
            except TypeError:
                pass
            try:
                contact_details = result[p][
                    'orcid-profile']['orcid-bio'].get('contact-details', None)
            except AttributeError:
                pass

            if contact_details is None:
                self.s_dict.update(
                    {
                        result[p]['orcid-profile']['orcid-identifier']['path']:
                            {
                                'f_name': f_name,
                                'l_name': l_name
                        }
                    }
                )
            else:
                email = contact_details.get('email', None)

                if email is None or email == []:
                    self.s_dict.update(
                        {
                            result[p]['orcid-profile']['orcid-identifier']['path']:
                                {
                                    'f_name': f_name,
                                    'l_name': l_name
                            }
                        }
                    )
                else:
                    l = dict()
                    for k, e in enumerate(email):
                        c = e.get('value')
                        l[k + 1] = c

                    self.s_dict.update(
                        {
                            result[p]['orcid-profile']['orcid-identifier']['path']:
                                {
                                    'f_name': f_name,
                                    'l_name': l_name,
                                    'email': l
                            }
                        }
                    )

        # To just get a list of Orcid ID's without any other profile
        # information
        self.orcid_id = self.s_dict.keys()

        return self.s_dict

        # For testing ###
        # results = self.api.search_public(query)
        # pp(results)


def print_basic_alt(self):
    """Print basic search results for better user readability (Alternative Format).
    Parameters
    ----------
    :param: None
    Returns
    -------
    :returns: None
    """
    result_text = \
        Fore.YELLOW + \
        Style.BRIGHT + \
        "Search Results: " + \
        Fore.RESET + \
        '(' + \
        str(self.total_results) + \
        ' Total)' + \
        Style.RESET_ALL
    result_warning_text = \
        Fore.RED + \
        Style.BRIGHT + \
        "You have a lot of results!!\n" + \
        Fore.RESET + \
        "Please modify or add more search terms to narrow your results.\n" + \
        Style.RESET_ALL

    print(result_text + '\n')
    if self.total_results > 30:
        print(result_warning_text)

    for i, p in enumerate(self.s_dict):
        email = self.s_dict[p].get('email')
        l_name = self.s_dict[p].get('l_name')
        f_name = self.s_dict[p].get('f_name')

        id_text = p
        l_name_text = l_name
        f_name_text = f_name
        count = \
            Fore.MAGENTA + \
            Style.BRIGHT + \
            'Result: ' + \
            Fore.RESET + \
            Fore.YELLOW + \
            str(i + 1) + \
            Fore.RESET + \
            Style.RESET_ALL

        email_list = []

        if email is not None:
            for e in email:
                email_list.insert(e, email[e])

        print(count +
              ', ' +
              id_text +
              ', ' +
              f_name_text +
              ' ' +
              l_name_text +
              (' (' if email_list else '') +
              ', '.join(email_list) +
              (') ' if email_list else ''))
    print("" + Style.RESET_ALL)
