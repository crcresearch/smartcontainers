import pytest
from pytest_bdd import given, scenario, then, when

@pytest.mark.skip(reason="Currently not implemented")
@scenario('../user.feature', 'A known user with an ORCID ID starts Smart Containers')
def test_a_known_user_with_an_orcid_id_starts_smart_containers():
    """A known user with an ORCID ID starts Smart Containers."""

@given('a valid orcid id')
def a_valid_orcid_id():
    """a valid orcid id."""

@when('it is given to smart containers on start')
def it_is_given_to_smart_containers_on_start():
    """it is given to smart containers on start."""

@then('it should create an RDF graph')
def it_should_create_an_rdf_graph():
    """it should create an RDF graph."""

@then('it should contain the user\'s ORCID information')
def it_should_contain_the_users_orcid_information():
    """it should contain the user's ORCID information."""
