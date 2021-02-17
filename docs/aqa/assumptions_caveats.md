# Assumptions and caveats log

This log contains a list of assumptions and caveats used in this analysis.

```{contents}
:local:
:depth: 1
```

## Definitions

Assumptions are RAG-rated according to the following definitions for quality and impact<sup>1</sup>:

<!-- Using reStructuredText table here, otherwise the raw Markdown is greater than the 120-character line width -->
```{eval-rst}
+-------+------------------------------------------------------+-------------------------------------------------------+
| RAG   | Assumption quality                                   | Assumption impact                                     |
+=======+======================================================+=======================================================+
| GREEN | Reliable assumption, well understood and/or          | Marginal assumptions; their changes have no or        |
|       | documented; anything up to a validated & recent set  | limited impact on the outputs.                        |
|       | of actual data.                                      |                                                       |
+-------+------------------------------------------------------+-------------------------------------------------------+
| AMBER | Some evidence to support the assumption; may vary    | Assumptions with a relevant, even if not critical,    |
|       | from a source with poor methodology to a good source | impact on the outputs.                                |
|       | that is a few years old.                             |                                                       |
+-------+------------------------------------------------------+-------------------------------------------------------+
| RED   | Little evidence to support the assumption; may vary  | Core assumptions of the analysis; the output would be |
|       | from an opinion to a limited data source with poor   | drastically affected by their change.                 |
|       | methodology.                                         |                                                       |
+-------+------------------------------------------------------+-------------------------------------------------------+
```
<sup><sup>1</sup> With thanks to the Home Office Analytical Quality Assurance team for these definitions.</sup>

## Assumptions and caveats

The log contains the following assumptions and caveats:

<!-- Use reStructuredText contents directive to generate a local contents -->
```{contents}
:local:
:depth: 1
```

### Assumption 1: Functions and documentation limited to getting repositories, contributors, teams, and setting team permissions for main purpose of project

- **Quality**: GREEN
- **Impact**: GREEN

The main aim of this work is to prevent accidental loss of admin privileges to GitHub organisation repositories when an
individual contributor leaves the organisation. It does this by setting a GitHub organisation team's permissions
wholesale across a number of organisation repositories.

In some specialised cases, we may want to find a limited set of organisation repositories which have a specific
contributor(s), before setting the team permissions. This is why functions to get contributor and team information has
been added.

As such, all the functions and documentation are limited to this purpose, although they could be conceivably extended
and/or used for ulterior purposes.

### Assumption 2: `get_items_for_all_repos.py`, `get_items_for_repo.py` functions limited to main purpose of project

- **Quality**: GREEN
- **Impact**: GREEN

Following on from [another assumption](#assumption-1-functions-and-documentation-limited-to-getting-repositories-contributors-teams-and-setting-team-permissions-for-main-purpose-of-project),
the functions in the `get_items_for_all_repos.py`, `get_items_for_repo.py` scripts in the `src/make_data` folder do not
accept attribute names that require further arguments or keyword arguments, as this is not required for the main
purpose of this project.
