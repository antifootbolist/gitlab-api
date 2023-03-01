# Project Description

This project is a Python script that accesses the GitLab API and calculates the average number of commits per day for a given interval in a specific repository.

## How to Use

To use the script, you need to have a private token for accessing the GitLab API. You also need to install the requests library (if it is not already installed) using the command:

```commandline
pip install requests
```

To run the script, you need to run the `gitlab_commit_counter.py` file with the following command-line arguments:

```commandline
python gitlab_commit_counter.py <gitlab_url> <private_token> <repository_url> <interval>
```

- `<gitlab_url>` - URL of the GitLab server
- `<private_token>` - private token for accessing the GitLab API
- `<repository_url>` - link to the repository in the format `namespace/repository`
- `<interval>` - the interval for which to calculate the average number of commits. It can be specified in the format `n[d|m|y]`, where `n` is the number of days, months, or years, `d` is for days, `m` is for months, and `y` is for years.

For example, to calculate the average number of commits for the last year in the repository `my-namespace/my-repo` on the GitLab server `https://gitlab.example.com` with private token `my-private-token`, you need to execute the following command:

```commandline
python gitlab_commit_counter.py https://gitlab.com my-private-token my-namespace/my-repo 1y
```
