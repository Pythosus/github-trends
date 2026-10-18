from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import pandas as pd
import requests
import re

def clean_readme(raw_text: str) -> str:
    text_no_code = re.sub(r'```[\s\S]*?```', '', raw_text)
    soup = BeautifulSoup(text_no_code, 'html.parser')
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'[*_#`]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def readme_text(url: str) -> str:
    resp = requests.get(url, timeout=10)
    return resp.text

def extract_keywords(text: str, topics: list) -> dict:
    target_vocabulary = list(set([topic.lower() for topic in topics]))
    
    stop_words = {'project', 'open-source', 'license', 'installation', 'docker', 'github', 'repository'}
    
    vectorizer = TfidfVectorizer(
        vocabulary=target_vocabulary,      
        ngram_range=(1, 2),                
        stop_words='english',              
        lowercase=True,
        token_pattern=r'(?u)\b\w[\w-]+\b' 
    )
    vectorizer.stop_words_ = set(vectorizer.get_stop_words()).union(stop_words)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out() 
    scores = tfidf_matrix.toarray()[0]
    
    keyword_scores = dict(zip(feature_names, scores))  #{слово: вес}
    sorted_keywords = {
        k: round(v, 4) for k, v in sorted(keyword_scores.items(), key=lambda item: item[1], reverse=True) if v > 0
    }
    return sorted_keywords
