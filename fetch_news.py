import requests
import json
import os
import concurrent.futures # 병렬 처리를 위한 모듈 (파이썬 내장)

# GitHub Secrets에서 키를 가져옵니다 (보안 유지)
CLIENT_ID = os.environ.get("NAVER_CLIENT_ID")
CLIENT_SECRET = os.environ.get("NAVER_CLIENT_SECRET")

keywords = ['IT', '경제', '부동산', 'AI', '주식', '날씨', '테크', '신재생', '풍력']
news_data = {}

def fetch_news(query):
    """
    특정 키워드에 대한 뉴스를 가져오는 함수
    """
    api_url = f"https://openapi.naver.com/v1/search/news.json?query={query}&display=15&sort=date"
    headers = {"X-Naver-Client-Id": CLIENT_ID, "X-Naver-Client-Secret": CLIENT_SECRET}
    
    try:
        # timeout을 설정하여 무한 대기 방지 (5초)
        res = requests.get(api_url, headers=headers, timeout=5)
        res.raise_for_status() # 200 OK가 아니면 예외 발생
        return query, res.json().get('items', [])
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return query, []

# [핵심 변경] ThreadPoolExecutor를 사용하여 병렬 요청 수행
# max_workers=10 : 최대 10개까지 동시에 작업 (키워드가 9개니 한 번에 다 처리됨)
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    # executor.map은 순서를 보장하지 않을 수 있으므로, future 객체로 관리
    future_to_url = {executor.submit(fetch_news, kw): kw for kw in keywords}
    
    for future in concurrent.futures.as_completed(future_to_url):
        kw, items = future.result()
        news_data[kw] = items

# 결과를 news.json 파일로 저장 (기존과 동일)
with open("news.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, ensure_ascii=False, indent=4)
