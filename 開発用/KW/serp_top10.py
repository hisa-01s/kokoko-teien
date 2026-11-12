import csv
import os
import re
import sys

import requests

API_URL = "https://google.serper.dev/search"
TOP_N = 10
OUTPUT_DIR = "serp_results"

def search_google(keyword, api_key):
    """Serper.dev経由でGoogle検索し、上位の結果を返す"""
    headers = {
        'X-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    payload = {'q': keyword, 'gl': 'jp', 'hl': 'ja', 'num': TOP_N}
    response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json().get('organic', [])[:TOP_N]

def save_csv(keyword, results):
    """検索結果をCSVに保存し、保存先のパスを返す"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = re.sub(r'[<>:"/\\|?*\s]+', '_', keyword)[:50] + '.csv'
    path = os.path.join(OUTPUT_DIR, filename)
    # Excelで文字化けしないようBOM付きで保存
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['rank', 'url', 'title'])
        for rank, item in enumerate(results, 1):
            writer.writerow([rank, item.get('link', ''), item.get('title', '')])
    return path

def main():
    if len(sys.argv) < 2:
        print('使い方: python serp_top10.py キーワード')
        print('例: python serp_top10.py 枯山水 作り方')
        sys.exit(1)

    api_key = os.environ.get('SERPER_API_KEY')
    if not api_key:
        print('エラー: 環境変数 SERPER_API_KEY が設定されていません。')
        sys.exit(1)

    keyword = ' '.join(sys.argv[1:])
    print(f'検索中: {keyword}')
    try:
        results = search_google(keyword, api_key)
    except requests.RequestException as e:
        print(f'エラー: {e}')
        sys.exit(1)

    if not results:
        print('検索結果がありませんでした。')
        sys.exit(1)

    for rank, item in enumerate(results, 1):
        print(f"{rank:2d}. {item.get('link', '')}")
        print(f"    {item.get('title', '')}")

    path = save_csv(keyword, results)
    print(f'\n完了！{path} に保存しました。')

if __name__ == "__main__":
    main()
