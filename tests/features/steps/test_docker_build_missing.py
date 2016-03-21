import pytest
from pytest_bdd import given, scenario, then, when

@pytest.mark.skip(reason="Currently not implemented")
@scenario('../docker_build.feature', 'Dockerfile is not found')
def test_dockerfile_is_not_found():
    pass

@given('a path that does not contain a Dockerfile')
def a_path_that_does_not_contain_a_dockerfile():
    """a path that does not contain a Dockerfile."""

@when('smart containers is asked to build it')
def smart_containers_is_asked_to_build_it():
    """smart containers is asked to build it."""

@then('it should return an error')
def it_should_return_an_error():
    """it should return an error."""
