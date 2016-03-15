Feature: Docker Build Capture
    Scenario: Smart containers should parse a Dockerfile
        Given a Dockerfile
        When it is parsed
        Then it should extract important information

    Scenario: Smart containers when executing Docker build should store the Maintainer
        Given a parsed Docker file
        When it contains a maintainer
        Then it should execute docker build
        And it should store the maintainer information in the container
