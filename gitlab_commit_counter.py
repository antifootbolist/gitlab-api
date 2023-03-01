import requests
from datetime import datetime, timedelta

# Задаем параметры запроса к API GitLab
gitlab_url = "https://gitlab.example.com/api/v4"
private_token = "YOUR_PRIVATE_TOKEN"
repository_url = "https://gitlab.example.com/namespace/repository"
start_date = datetime.now() - timedelta(days=365)  # Данные за последний год

# Отправляем запрос на получение списка коммитов
response = requests.get(
    f"{gitlab_url}/projects/{repository_url}/repository/commits",
    headers={"PRIVATE-TOKEN": private_token},
    params={"since": start_date.isoformat()},
)

# Обрабатываем полученный ответ и считаем количество коммитов за каждый день
commits_per_day = {}
for commit in response.json():
    commit_date = datetime.fromisoformat(commit["created_at"][:-1])  # Преобразуем дату в формат datetime
    commit_day = commit_date.date()
    if commit_day in commits_per_day:
        commits_per_day[commit_day] += 1
    else:
        commits_per_day[commit_day] = 1

# Считаем среднее количество коммитов в день
days = (datetime.now().date() - start_date.date()).days
average_commits_per_day = sum(commits_per_day.values()) / days

# Выводим результат
print(f"Среднее количество коммитов в день за последний год: {average_commits_per_day}")
