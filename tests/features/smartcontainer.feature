Feature: Smart Container General Features

    Scenario: A user creates a smart container from an existing container
        Given A container ID
        When  Smart containers is called with the command line argument
        Then it should initialize the container with smart container metadata
        And it should contain the correct JSON-LD metadata

    Scenario: A user wants to print smart image metadata 
        Given An image ID
        When  Smart containers is called with the command line argument
        Then it should print the JSON-LD metadata attched to the image 
        And it should contain the correct JSON-LD metadata
