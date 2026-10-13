import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime

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
        repo_info['url'] = f'https://github.com/{owner}/{repo_info['work_name']}'
        
        repos.append(repo_info)
    return repos

def get_text_from_repo(url):
    pass

get_github_trends()
