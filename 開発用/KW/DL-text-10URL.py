import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import os
import csv
import sys

def get_page_content(url):
    """URLからページの本文を取得する"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 不要な要素を削除
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 
                         'aside', 'form', 'iframe', 'noscript']):
            tag.decompose()
        
        # 本文を取得（優先順位: article > main > body）
        content = soup.find('article') or soup.find('main') or soup.find('body')
        
        if content:
            text = content.get_text(separator='\n', strip=True)
            # 連続する空行を1つにまとめる
            text = re.sub(r'\n{3,}', '\n\n', text)
            return text
        return "本文を取得できませんでした。"
    
    except requests.RequestException as e:
        return f"エラー: {e}"

def sanitize_filename(url):
    """URLから安全なファイル名を生成"""
    parsed = urlparse(url)
    name = parsed.netloc + parsed.path
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    return name[:50] + '.txt'

URLS = [
    "https://kanbe-zouen.com/blog/column/165327",
    "https://www.niwaishi.co.jp/blog/%E8%87%AA%E5%AE%85%E3%81%AB%E6%9E%AF%E5%B1%B1%E6%B0%B4%E3%81%AE%E5%9D%AA%E5%BA%AD%E3%82%92%E3%81%A4%E3%81%8F%E3%82%8B%EF%BC%81%E3%81%9D%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9%E3%82%92%E3%81%94%E7%B4%B9-2/",
    "https://niwasekai.com/articles/zen-dry-rock-garden-sand-pattern",
    "https://t23m-navi.jp/magazine/housing/karesansui/",
    "https://nippon-teien.com/2020/07/11/how-to-make-japanese-garden-part1/",
    "https://www.japanesegardenlife.com/%E3%80%90%E5%88%9D%E5%BF%83%E8%80%85%E5%90%91%E3%81%91%E3%80%91%E6%9E%AF%E5%B1%B1%E6%B0%B4%E3%81%AE%E4%BD%9C%E3%82%8A%E6%96%B9%E3%81%A8%E9%81%93%E5%85%B7%E3%83%BB%E5%B0%8F%E3%82%B9%E3%83%9A%E3%83%BC/",
    "https://note.com/sgk2005/n/n3d335d7febcb"
]

def load_urls(csv_path):
    """serp_top10.pyが出力したCSVからURLを読み込む"""
    with open(csv_path, encoding='utf-8-sig', newline='') as f:
        return [row['url'] for row in csv.DictReader(f) if row['url']]

def main():
    # CSVを指定した場合はそのURLを、指定がなければURLSを処理する
    urls = load_urls(sys.argv[1]) if len(sys.argv) > 1 else URLS
    print("=" * 50)
    print("URL本文抽出ツール（リスト指定版）")
    print("=" * 50)
    print(f"{len(urls)}件のURLを処理中...")
    output_dir = "extracted_texts"
    os.makedirs(output_dir, exist_ok=True)
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] {url[:60]}...")
        content = get_page_content(url)
        filename = os.path.join(output_dir, f"{i:02d}_{sanitize_filename(url)}")
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write("=" * 50 + "\n\n")
            f.write(content)
        print(f"  → 保存: {filename}")
    print(f"\n完了！{output_dir}フォルダに保存しました。")

if __name__ == "__main__":
    main()
