import requests
import argparse
import os
from datetime import datetime


def get_project_id(gitlab_url, repo_path, gitlab_token):
    """
    Return project ID based on request:
        https://{gitlab_url}/api/v4/projects/{project_path}
    :param gitlab_url: base URL to GitLab (https://gitlab.com)
    :param repo_path: project path (group-name/repo-name)
    :param gitlab_token: personal assess token
    :return: Project ID
    """

    url = gitlab_url + "/api/v4/projects/" + repo_path.replace('/', '%2F')
    headers = {"PRIVATE-TOKEN": gitlab_token}
    response = requests.get(url, headers=headers)

    project_id = response.json()["id"]

    return project_id


def get_average_commits(gitlab_url, repo_path, start_date, end_date, gitlab_token):
    """
    Return number of commits in project based on request:
        https://{gitlab_url}/api/v4/projects/{project_id}/repository/commits
    :param gitlab_url: base URL to GitLab (https://gitlab.com)
    :param repo_path: project path (group-name/repo-name)
    :param start_date: start date of interval
    :param end_date: end date of interval
    :param gitlab_token: personal assess token
    :return: Number of commits
    """

    # Change format of start and end dates
    start_date_fmt = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date_fmt = datetime.strptime(end_date, "%Y-%m-%d").date()
    print(f"Start date: {start_date_fmt}\nEnd date: {end_date_fmt}")

    # Find GitLab project ID
    project_id = get_project_id(gitlab_url, repo_path, gitlab_token)

    # Request commits page by page (Fix pagination issue)
    commits = []
    page = 1
    per_page = 100
    while True:
        url = gitlab_url + "/api/v4/projects/" + str(project_id) + "/repository/commits"
        headers = {"PRIVATE-TOKEN": gitlab_token}
        params = {
            'since': start_date,
            'until': end_date,
            'page': page,
            'per_page': per_page,
            'all': True
        }
        response = requests.get(url, headers=headers, params=params)

        response.raise_for_status()
        page_commits = response.json()
        if not page_commits:
            break
        commits.extend(page_commits)
        page += 1

    # Handle the response of the request and count number of commits per day
    commits_per_day = {}  # Dict to store dates and count of commits
    for commit in commits:
        # Get date of commit by transforming 2021-08-08T22:01:37.000+03:0
        commit_day = datetime.strptime(commit["created_at"][:-1].split('T')[0], '%Y-%m-%d').date()
        if commit_day in commits_per_day:
            commits_per_day[commit_day] += 1
        else:
            commits_per_day[commit_day] = 1

    # Define max number of commits
    max_value = max(commits_per_day.values())
    max_key = max(commits_per_day, key=commits_per_day.get)
    print(f"Max number of commits was: {max_value} in {max_key}")

    print(f"Total number of commits in period: {sum(commits_per_day.values())}")

    # Count of days in period between start day and end day
    days = end_date_fmt - start_date_fmt
    print(f"Number of days in period: {days.days}")
    average_commits_per_day = sum(commits_per_day.values()) / days.days

    return average_commits_per_day


if __name__ == "__main__":
    # Get token from env
    gitlab_token = os.getenv("GITLAB_TOKEN")

    # Get parameters from arguments of the script
    parser = argparse.ArgumentParser(description="Calculate average number of commits in a GitLab "
                                                 "repository for a given period")
    parser.add_argument("gitlab_url", type=str, help="base URL of GitLab server")
    parser.add_argument("repo_path", type=str, help="repository URL in the format group-name/repo-name")
    parser.add_argument("start_date", type=str, help="start date of the period in the format YYYY-MM-DD")
    parser.add_argument("end_date", type=str, help="end date of the period in the format YYYY-MM-DD")
    args = parser.parse_args()

    # Calculate average count of commits
    average_commits = get_average_commits(args.gitlab_url, args.repo_path, args.start_date, args.end_date, gitlab_token)

    # Print count to stdout
    print(f"Average number of commits per day: {round(average_commits, 1)}")
