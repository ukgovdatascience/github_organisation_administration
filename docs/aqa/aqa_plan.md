# Analytical quality assurance plan

This analytical quality assurance (AQA) plan outlines our implementation of the [Aqua Book][aqua-book] for this
project. Further resources related to the Aqua Book can be found [here][aqua-book-resources].

This is a **living** document, and should be updated and/or modified as necessary, e.g. if new tasks not listed here
become relevant to project success, please add them to this plan.

```{contents}
:local:
:depth: 1
```

## General

- Security
  - Pre-commit hooks should be installed
    - No secrets, Jupyter notebook outputs, or large files should be version-controlled
  - Credentials should be stored in a location external to this repository
  - All major attempts to prevent unintentional access to the credentials should be taken
  - Details about the credentials file location, GitHub organisation, and teams involved should be kept secret
- Version control
  - All code should be version-controlled using Git and GitHub
  - No code should be merged into the `main` branch without approved peer review
- Documentation should be up-to-date
  - Docstrings for all functions and classes
  - Build in Sphinx where relevant
  - README's are up-to-date
  - Add suitable assumptions and caveats

## Build

- Modularised code as much as possible
- Testing
  - All functions should be tested using [pytest][pytest], and pass their tests
  - Must have at least 90% code coverage for code within the `src` folder

[aqua-book]: https://www.gov.uk/government/publications/the-aqua-book-guidance-on-producing-quality-analysis-for-government
[aqua-book-resources]: https://www.gov.uk/government/collections/aqua-book-resources
[pytest]: https://docs.pytest.org/
