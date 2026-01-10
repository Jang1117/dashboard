import requests
import json
import os

# GitHub Secrets에서 키를 가져옵니다 (보안 유지)
CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")

keywords = ['IT', '경제', '부동산']
news_data = {}

def fetch_news(query):
    api_url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=15&sort=date"
    headers = {"X-Naver-Client-Id": CLIENT_ID, "X-Naver-Client-Secret": CLIENT_SECRET}
    res = requests.get(api_url, headers=headers)
    return res.json().get('items', [])

for kw in keywords:
    news_data[kw] = fetch_news(kw)

# 결과를 news.json 파일로 저장
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)
