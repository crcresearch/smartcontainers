Feature: ORCID Management
  In order to link the container to a specific user we need an ID to link to. http://orcid.org/ was selected for this.

  Scenario: Attempt to create configuration from valid credentials
    Given a <credential>
    When it is a valid orcid credential
    Then it should create a config file

    Examples: Vertical
      | credential | 0000-0001-5663-6903 | jsweet@nd.edu |

  Scenario: Attempt to create a configuration from invalid credentials
    Given a <credential>
    When it is an invalid orcid credential
    Then it should return an error

    Examples: Vertical
      | credential | 9000-0001-5663-6903 | jsweet@ndedu |
