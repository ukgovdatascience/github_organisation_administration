# Creating a GitHub API token JSON

To use this repository, you need to create a JSON file containing your GitHub API personal access token. This is to
compartmentalise the secrets in a separate location on your local system, as an added security precaution.

```{contents}
:local:
:depth: 2
```

## Getting a GitHub personal access token

Follow the instructions [here][github-token] to create a personal access token. You will need to grant `repo` access
rights for your token at Step 7.

Once you have completed Step 9, you can create the JSON file.

## Creating a token JSON file

In your preferred text editor, add the following lines:

```{code-block} json
{
  "username": "<<<YOUR GITHUB USERNAME>>>",
  "token": "<<<YOUR GITHUB PERSONAL ACCESS TOKEN>>>"
}
```

where `<<<YOUR GITHUB USERNAME>>>` is your GitHub username, and `<<<YOUR GITHUB PERSONAL ACCESS TOKEN>>>` is the
personal access token you created in [Step 9](#getting-a-github-personal-access-token).

Save this JSON file with an appropriate name, for example `github_api_token.json`, in a different location to this
repository. [Now you can import the JSON file via the `.secrets` file](#import-json-via-secrets).

## Import JSON via `.secrets`

Once you have [created a token JSON file](#creating-a-token-json-file), open the `.secrets` file in this repository.
Add the following line:

```{code-block} shell
export GITHUB_API_TOKEN=<<<ABSOLUTE PATH TO TOKEN JSON>>>
```

where `<<<ABSOLUTE PATH TO TOKEN JSON>>>` is the absolute path to your token JSON file.

[github-token]: https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token
