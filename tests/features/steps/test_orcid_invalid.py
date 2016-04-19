from pytest_bdd import given, scenario, then, when

@scenario('../orcid.feature', 'Attempt to create a configuration from invalid credentials')
def test_attempt_to_create_a_configuration_from_invalid_credentials():
    pass

@given('a <credential>')
def a_credential(credential):
    return credential

@when('it is an invalid orcid credential')
def it_is_an_invalid_orcid_credential(a_credential):
    """it is an invalid orcid credential."""

@then('it should return an error')
def it_should_return_an_error(a_credential):
    """it should return an error."""
