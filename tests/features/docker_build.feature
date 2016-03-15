Feature: Smart containers handles docker build

    Scenario: Dockerfile is not found
        Given a path that does not contain a Dockerfile
        When smart containers is asked to build it
        Then it should return an error

    Scenario: Dockerfile is found
        Given a path containing a Dockerfile
        When smart containers is asked to build it
        Then it should run docker build
         And it should parse the file to create a dictionary of the steps

    Scenario: Dockerfile contains a maintainer
        Given a Dictionary of steps from a Dockerfile
        When smart containers is asked to process the steps
        Then it should find the maintainer
         And it should look for their ORCID ID
         And it should create a graph
         And it should attach the graph to the container
