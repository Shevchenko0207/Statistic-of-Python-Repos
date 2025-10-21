import os # Додано для доступу до змінних середовища
import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

# 1. Отримання GITHUB_TOKEN зі змінних середовища
token = os.environ.get("GITHUB_TOKEN")
headers = {}
if token:
    headers["Authorization"] = f"token {token}"
    print("Using GITHUB_TOKEN for API request.")
else:
    print("GITHUB_TOKEN not found. Using anonymous request (low rate limit).")

# URL запиту залишається незмінним
url = "https://api.github.com/search/repositories?q=language:python&sort=stars"

# 2. Виконання запиту з автентифікацією
# Передача заголовків (headers) у запит
r = requests.get(url, headers=headers)
print("Status code:", r.status_code)

# Якщо запит не вдався, вивести помилку та вийти
if r.status_code != 200:
    print(f"Error: API request failed with status code {r.status_code}.")
    # Вивести текст помилки, якщо він є у відповіді
    try:
        error_dict = r.json()
        print("API Error Response:", error_dict)
    except requests.exceptions.JSONDecodeError:
        print("API Error Response Text:", r.text)
    
    # Вихід із кодом 1, щоб позначити невдачу в Actions
    exit(1)


response_dict = r.json()
print("Total repositories:", response_dict["total_count"])

repo_dicts = response_dict["items"]
print("Number of items:", len(repo_dicts))

names, stars, plot_dicts = [], [], []
for repo_dict in repo_dicts:
    names.append(repo_dict["name"])
    stars.append(repo_dict["stargazers_count"])

    plot_dict = {
        "value": repo_dict["stargazers_count"],
        # Додано перевірку, щоб уникнути помилок, якщо опис відсутній
        "label": repo_dict["description"] or "No description provided", 
        "xlink": repo_dict["html_url"],
    }
    plot_dicts.append(plot_dict)

my_style = LS("#333366", base_style=LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 18
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000
# НОВИЙ РЯДОК: Вимикає відображення додаткових міток (включаючи заголовок діаграми) у тултіпах
my_config.show_minor_labels = False 

chart = pygal.Bar(my_config, style=my_style)
chart.title = "Most-Starred Python Projects on GitHub"
chart.x_labels = names
chart.add("", plot_dicts)
chart.render_to_file("python_repos.svg")
