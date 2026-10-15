from sklearn.feature_extraction.text import TfidVectorizer
import pandas as pd
import re

def clean_markdown(text: str) -> str:
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'[*_#`]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_keywords(text: str, topics: list) -> dict:
    pass
