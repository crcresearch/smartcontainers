from pytest_bdd import given, scenario, then, when

@scenario('../orcid.feature', 'Attempt to create configuration from valid credentials')
def test_attempt_to_create_configuration_from_valid_credentials():
    pass

@given('a <credential>')
def a_credential(credential):
    return credential

@when('it is a valid orcid credential')
def it_is_a_valid_orcid_credential(a_credential):
    """it is a valid orcid credential"""

@then('it should create a config file')
def it_should_create_a_config_file(a_credential):
    """it should create a config file."""
