# Average count of commits

This project is a Python script that accesses the GitLab API and calculates the average number of commits per day for a given interval in a specific repository.

## How to Use

To use the script, you need to have a private token for accessing the GitLab API and export its value by exporting variable GITLAB_TOKEN

You also need to install some libraries (if it is not already installed) using the command:

```commandline
pip install -r requirements.txt
```

To run the script, you need to run the `gitlab_commit_counter.py` file with the following command-line arguments:

```commandline
python gitlab_commit_counter.py <gitlab_url> <repo_path> <start_date> <end_date>
```

- `<gitlab_url>` - URL of the GitLab server
- `<repo_path>` - link to the repository in the format `group_name/repo_name`
- `<start_date>` - start date of the interval for which to calculate the average number of commits
- `<end_date>` - end date of the interval for which to calculate the average number of commits

For example, to calculate the average number of commits in October last year in the repository `my_group/my_repo` on the GitLab server `https://gitlab.example.com` you need to execute the following command:

```commandline
export GITLAB_TOKEN=***
python gitlab_commit_counter.py https://gitlab.com my-group/my-repo 2022-10-01 2022-10-31
```
