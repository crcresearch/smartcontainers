Feature: Smart containers handles Docker build

    Scenario: Dockerfile is not found
        Given a path that does not contain a Dockerfile
        When smart containers is asked to build it
        Then it should return an error

    Scenario: Dockerfile is found
        Given a path containing a Dockerfile
        When smart containers is asked to build it
        Then it should run Docker build
        Then it should parse the file to create a dictionary of the steps

    Scenario: Dockerfile contains a maintainer
        Given a Dictionary of steps from a Dockerfile
        When smart containers is asked to process the steps
        Then it should find the maintainer
        Then it should look for their ORCID ID
        Then it should create a graph
        Then it should attach the graph to the container
