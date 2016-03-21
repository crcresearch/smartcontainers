import pytest
from pytest_bdd import given, scenario, then, when

@pytest.mark.skip(reason="Currently not implemented")
@scenario('../docker_build.feature', 'Dockerfile contains a maintainer')
def test_dockerfile_contains_a_maintainer():
    pass

@given('a Dictionary of steps from a Dockerfile')
def a_dictionary_of_steps_from_a_dockerfile():
    """a Dictionary of steps from a Dockerfile."""

@when('smart containers is asked to process the steps')
def smart_containers_is_asked_to_process_the_steps():
    """smart containers is asked to process the steps."""

@then('it should find the maintainer')
def it_should_find_the_maintainer():
    """it should find the maintainer."""

@then('it should look for their ORCID ID')
def it_should_look_for_their_orcid_id():
    """it should look for their ORCID ID."""

@then('it should create a graph')
def it_should_create_a_graph():
    """it should create a graph."""

@then('it should attach the graph to the container')
def it_should_attach_the_graph_to_the_container():
    """it should attach the graph to the container."""
