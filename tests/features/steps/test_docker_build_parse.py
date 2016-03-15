from pytest_bdd import given, scenario, then, when

@scenario('../docker_build.feature', 'Smart containers when executing Docker build should store the Maintainer')
def test_smart_containers_when_executing_docker_build_should_store_the_maintainer():
    pass

@given('a Dockerfile containing a maintainer')
def a_dockerfile_containing_a_maintainer():
    """a Dockerfile containing a maintainer."""

@when('it is parsed correctly')
def it_is_parsed_correctly():
    """it is parsed correctly."""

@then('it should execute docker build')
def it_should_execute_docker_build():
    """it should execute docker build."""

@then('it should store the maintainer information in the container')
def it_should_store_the_maintainer_information_in_the_container():
    """it should store the maintainer information in the container."""
