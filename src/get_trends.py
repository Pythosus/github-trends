import requests
from bs4 import BeautifulSoup
from datetime import timedelta, datetime

def get_github_trends() -> dict:
    headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    repos = {}
    response = requests.get('https://github.com/trending', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    sp = soup.find_all('h2')
    print(sp)


get_github_trends()
