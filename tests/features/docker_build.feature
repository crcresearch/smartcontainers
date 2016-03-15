Feature: Docker Build Capture
    Scenario: Smart containers when executing Docker build should store the Maintainer
        Given a Dockerfile containing a maintainer
        When it is parsed correctly
        Then it should execute docker build
        And it should store the maintainer information in the container
