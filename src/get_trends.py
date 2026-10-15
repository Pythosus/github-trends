import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime
import config

def get_github_trends() -> list:
    headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    repos = []
    response = requests.get('https://github.com/trending', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for article in soup.find_all('article', class_='Box-row'):
        repo_info = dict()
        h2_art = article.find('h2', class_='h3')

        rep = h2_art.find('a')
        _, owner, repo_info['work_name'] = rep['href'].split('/')
        repo_info['name'] = f'{owner}/{repo_info['work_name']}'

        stars = article.find('div', class_='f6').find('a').get_text()
        repo_info['stars'] = int(str(stars).replace(',', ''))

        repo_info['description'] = article.find('p', class_='col-9').get_text().strip('\n ')

        get_info_from_repo(repo_info)

        repos.append(repo_info)
    return repos

def get_info_from_repo(repo: str):
    headers = {"Authorization": f"Bearer {config.token}"}
    repo_info = requests.get(f'https://api.github.com/repos/{repo['name']}', headers=headers).json()

    repo['topics'] = repo_info.get('topics', [])

    readme_info = requests.get(f'https://api.github.com/repos/{repo['name']}/readme', headers=headers).json()
    repo['raw_readme_url'] = readme_info.get('download_url')


#print(get_github_trends())
