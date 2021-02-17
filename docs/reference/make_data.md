# Data generation

These `src` package functions generate data.

<!-- Functions should be referenced in the `src.__init__.py` -->
```{eval-rst}
.. currentmodule:: src
```

## GitHub repositories

```{eval-rst}
.. autosummary::
    :toctree: api/

    find_organisation_repos

```

## GitHub teams

```{eval-rst}
.. autosummary::
    :toctree: api/

    add_team_with_permissions_to_all_repositories
    add_team_with_permissions_to_repository
    check_team_added_already

```

## Helper functions

```{eval-rst}
.. autosummary::
    :toctree: api/

    extract_attribute_from_dict_of_paginated_lists
    extract_attribute_from_paginated_list_elements
    get_items_for_all_repos
    get_items_for_repo

```
