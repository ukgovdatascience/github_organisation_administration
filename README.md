# `GitHub Organisation Administration`

Use GitHub REST API v3 to do administration tasks within a GitHub organisation. The main aim of this project is prevent
accidental access loss to organisation repositories when individuals leave the organisation by programatically adding,
and setting team permissions across multiple repositories.

> ℹ️ Where this documentation refers to the **root folder** we mean where this README.md is located.

- [Getting started](#getting-started)
  - [Requirements](#requirements)
- [Required secrets and credentials](#required-secrets-and-credentials)
- [Licence](#licence)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Getting started

> ⚠️ You can only complete tasks where your GitHub username has organisation owner and/or repository administrator
> privileges.

> ❗️ Some actions, such as setting team permissions can be **destructive**. Take care when using them!

To get started, make sure your system meets the [requirements](#requirements), and you have
[set up all secrets, and credentials](#required-secrets-and-credentials).

This project heavily leverages the [`PyGithub` package][pygithub], and has wrapped functions around different methods.
The advantage of these wrapped functions is that they leverage multiprocessing to speed up the API requests, as well as
providing convenience functions for GitHub organisation administration.

All functions can be imported directly from the `src` package, and documentation is available in the Reference section
of the [Sphinx documentation](#viewing-the-documentation).

The functions can:

- Find all repositories in a GitHub organisation (`src.find_organisation_repos`)
- Get information from a PyGithub single repositories (`src.get_items_for_repo`)
- Get information from a PyGithub paginated list of repositories (`src.get_items_for_all_repos`)
- Extract a specific attribute from a PyGithub paginated list of information
  (`src.extract_attribute_from_dict_of_paginated_lists`)

Here is an example of getting the names of all contributors across all organisation repositories:

> ⚠️ Note that, because the `name` attribute is not in the [API response][github-contributors] for getting repository
contributors, PyGithub will send another API GET request for each contributor to obtain their name!

```python
from github import Github
from src import extract_attribute_from_dict_of_paginated_lists, find_organisation_repos, get_items_for_all_repos
import os

# Instantiate the github.Github class to gain access to GitHub REST APIv3 via your GitHub personal access token
g = Github(os.getenv("GITHUB_API_KEY"), per_page=100)

# Get all the repositories for your GitHub organisation
organisation_repositories = find_organisation_repos(g, os.getenv("GITHUB_ORGANISATION"))

# Get all the contributors for these repositories
organisation_contributors = get_items_for_all_repos(g, "get_contributors", organisation_repositories)

# Show the contributors names in each repository
extract_attribute_from_dict_of_paginated_lists(organisation_contributors, "name")
```

For more information, see the example notebooks in the [`notebooks`][notebooks] folder.

### Requirements

- A `.secrets` file with the [required secrets and credentials](#required-secrets-and-credentials)
- [Load environment variables][docs-loading-environment-variables] from `.envrc`
- Python 3.8 or later with a virtual environment set up
- All packages from [`requirements.txt`][requirements] installed in your environment
  - For ease, open your terminal and run the Make command `make requirements`, which will install package requirements
    as well as [pre-commit hooks][docs-pre-commit-hooks] to prevent committing of secrets, Jupyter notebook outputs,
    and large files

## Required secrets and credentials

To run this project, you need a `.secrets` file with secrets/credentials as environmental variables; see the
[documentation][docs-loading-environment-variables-secrets] for further guidance. The secrets/credentials should have
the following environment variable name(s):

| Secret/credential              | Environment variable name | Description                                                 |
|--------------------------------|---------------------------|-------------------------------------------------------------|
| GitHub personal access token   | `GITHUB_API_KEY`          | See [here][docs-github-token] for further information       |
| GitHub organisation name       | `GITHUB_ORGANISATION`     | The GitHub organisation name, e.g. `ukgovdatascience`       |
| GitHub organisation admin team | `GITHUB_ADMIN_TEAM_SLUG`  | The GitHub team name that should have repo admin privileges |

Once you've added these environment variables to `.secrets` you will need to
[load them via `.envrc`][docs-loading-environment-variables].

## Viewing the documentation

To build the documentation locally, open your Terminal, and enter the following command:

```shell
make docs
```

You can then access the documentation by opening `docs/_build/index.html` in your preferred web browser.

## Licence

Unless stated otherwise, the codebase is released under the MIT License. This covers both the codebase and any sample
code in the documentation. The documentation is © Crown copyright and available under the terms of the Open Government
3.0 licence.

## Contributing

If you want to help us build, and improve `GitHub Organisation Administration`, view our
[contributing guidelines][contributing].

## Acknowledgements

This project structure is based on the [`govcookiecutter`][govcookiecutter] template project.

[contributing]: ./CONTRIBUTING.md
[govcookiecutter]: https://github.com/ukgovdatascience/govcookiecutter
[docs-github-token]: docs/user_guide/creating_github_api_token.md
[docs-loading-environment-variables]: ./docs/user_guide/loading_environment_variables.md
[docs-loading-environment-variables-secrets]: ./docs/user_guide/loading_environment_variables.md#storing-secrets-and-credentials
[docs-pre-commit-hooks]: ./docs/contributor_guide/pre_commit_hooks.md
[github-contributors]: https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#list-repository-contributors
[notebooks]: ./notebooks
[pre-commit]: https://pre-commit.com/
[pygithub]: https://pygithub.readthedocs.io/
[requirements]: ./requirements.txt
