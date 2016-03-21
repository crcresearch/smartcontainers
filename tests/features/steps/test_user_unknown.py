import pytest
from pytest_bdd import given, scenario, then, when

@pytest.mark.skip(reason="Currently not implemented")
@scenario('../user.feature', 'An unknown user starts Smart Containers')
def test_an_unknown_user_starts_smart_containers():
    """An unknown user starts Smart Containers."""

@given('an unknown user')
def an_unknown_user():
    """an unknown user."""

@when('it is given to smart containers on start')
def it_is_given_to_smart_containers_on_start():
    """it is given to smart containers on start."""

@then('it should create an RDF graph')
def it_should_create_an_rdf_graph():
    """it should create an RDF graph."""

@then('it should contain a blank node for the unknown user')
def it_should_contain_a_blank_node_for_the_unknown_user():
    """it should contain a blank node for the unknown user."""

@then('it should contain a has account node containing the username and hostname')
def it_should_contain_a_has_account_node_containing_the_username_and_hostname():
    """it should contain a has account node containing the username and hostname."""
