# Creating a GitHub API token

To use this repository, you need to create a GitHub API personal access token, and store it with the untracked
`.secrets` file. This ensures your token is not accidentally version-controlled alongside your code.

```{contents}
:local:
:depth: 2
```

## Getting a GitHub personal access token

Follow the instructions [here][github-token] to create a personal access token. You will need to grant `repo` access
rights for your token at Step 7.

Once you have completed Step 9, you can add it to the `.secrets` file; remember to copy this token before closing your
browser window, otherwise you will have to start the process again.

## Adding your token to `.secrets`

Once you have [obtained your GitHub personal acccess token](#getting-a-github-personal-access-token), open the
`.secrets` file in this repository. Add the following line:

```{code-block} shell
export GITHUB_API_KEY=<<<YOUR GITHUB PERSONAL ACCESS TOKEN>>>
```

where `<<<YOUR GITHUB PERSONAL ACCESS TOKEN>>>` is your token. Save the file, and update the loaded environment
variables by running the following code in your Terminal:

```{code-block} shell
direnv allow
```

More details on loading environment variables can be found [here][docs-env-variables]

[docs-env-variables]: ./loading_environment_variables.md
[github-token]: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token
