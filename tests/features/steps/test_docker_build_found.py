from pytest_bdd import given, scenario, then, when

@scenario('../docker_build.feature', 'Dockerfile is found')
def test_dockerfile_is_found():
    pass

@given('a path containing a Dockerfile')
def a_path_containing_a_dockerfile():
    """a path containing a Dockerfile."""

@when('smart containers is asked to build it')
def smart_containers_is_asked_to_build_it():
    """smart containers is asked to build it."""

@then('it should run Docker build')
def it_should_run_docker_build():
    """it should run Docker build."""

@then('it should parse the file to create a dictionary of the steps')
def it_should_parse_the_file_to_create_a_dictionary_of_the_steps():
    """it should parse the file to create a dictionary of the steps."""
