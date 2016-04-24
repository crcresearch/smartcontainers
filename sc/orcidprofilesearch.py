"""CLI program that allows the user to input keywords for a basic search of the
    Orcid API.  It uses the OrcidManager class to find the Orcid ID and data.
"""
from requests import RequestException
import orcid
import click

def orcid_search(sandbox):
    """Get the Orcid_id from the email search

    Parameters
    ----------
    :param sandbox: boolean
        Should the sandbox be used. True (default) indicates development mode.

    Returns
    -------
    :returns orcid.orcid_Id: string
        Returns the Orcid ID from a basic search by user.
    """
    # Prompt and get search terms
    print('* You can leave fields blank *')
    query = {
        'first_name': click.prompt(
            'Please enter a first name', default='', show_default=False
        ),
        'last_name': click.prompt(
            'Please enter a last name', default='', show_default=False
        ),
        'email': click.prompt(
            'Please enter an email', default='', show_default=False
        ),
        'keywords': click.prompt(
            'Please enter some keywords (like country, department or institution)', default='', show_default=False
        )
    }
    print('')

    search_terms = ""
    if query['first_name']:
        search_terms += 'given-names:' + query['first_name']
    if query['last_name']:
        if len(search_terms) > 0:
            search_terms += " AND "
        search_terms += 'family-name:' + query['last_name']
    if query['email']:
        if len(search_terms) > 0:
            search_terms += " AND "
        search_terms += 'email:' + query['email']
    if query['keywords']:
        if len(search_terms) > 0:
            search_terms += " AND "
        search_terms += query['keywords']

    api = orcid.SearchAPI(False)
    try:
        results = api.search_public(search_terms).get(
            'orcid-search-results', None)
    except RequestException as e:
    # Here the error should be handled. As the exception message might be
    # too generic, additional info can be obtained by:
        print(e.response.text)
    # The response is a requests Response instance.

    print results
    if results is None:
        return None
    if results.get('num-found') == 0:
        return None
    result = results.get('orcid-search-result', None)

    return result[0]['orcid-profile']['orcid-identifier']['path']
