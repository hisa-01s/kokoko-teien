from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote_plus, urlparse
import csv
import os
import re
import sys
import time

TOP_N = 10
MAX_PAGES = 3
CAPTCHA_WAIT = 180
OUTPUT_DIR = "serp_results"

def wait_for_results(driver):
    """検索結果の表示を待つ。CAPTCHAが出た場合は手動で解くまで待機する"""
    if '/sorry/' in driver.current_url:
        print(f'CAPTCHAが表示されました。ブラウザで解いてください（最大{CAPTCHA_WAIT}秒待機）')
        try:
            WebDriverWait(driver, CAPTCHA_WAIT).until(lambda d: '/sorry/' not in d.current_url)
        except TimeoutException:
            return False
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#search'))
        )
    except TimeoutException:
        return False
    return True

def extract_results(driver):
    """検索結果ページから自然検索のURLとタイトルを取得する"""
    results = []
    for h3 in driver.find_elements(By.CSS_SELECTOR, '#search a h3'):
        link = h3.find_element(By.XPATH, './ancestor::a[1]')
        url = link.get_attribute('href') or ''
        title = h3.text.strip()
        host = urlparse(url).netloc
        if not title or not url.startswith('http') or host.endswith('google.com'):
            continue
        results.append({'url': url, 'title': title})
    return results

def search_google(driver, keyword):
    """1ページ目から順に開き、上位TOP_N件を集める"""
    results = []
    seen = set()
    for page in range(MAX_PAGES):
        url = f'https://www.google.com/search?q={quote_plus(keyword)}&hl=ja&gl=jp&start={page * 10}'
        driver.get(url)
        if not wait_for_results(driver):
            break
        for item in extract_results(driver):
            if item['url'] not in seen:
                seen.add(item['url'])
                results.append(item)
        if len(results) >= TOP_N:
            break
        time.sleep(3)
    return results[:TOP_N]

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
            writer.writerow([rank, item['url'], item['title']])
    return path

def main():
    if len(sys.argv) < 2:
        print('使い方: python serp_browser.py キーワード')
        print('例: python serp_browser.py 枯山水 作り方')
        sys.exit(1)

    keyword = ' '.join(sys.argv[1:])
    print(f'検索中: {keyword}')
    driver = webdriver.Chrome()
    try:
        results = search_google(driver, keyword)
    except WebDriverException:
        print('エラー: ブラウザが途中で閉じられたため、取得を中止しました。')
        sys.exit(1)
    finally:
        try:
            driver.quit()
        except WebDriverException:
            pass

    if not results:
        print('検索結果を取得できませんでした。')
        sys.exit(1)

    for rank, item in enumerate(results, 1):
        print(f"{rank:2d}. {item['url']}")
        print(f"    {item['title']}")

    path = save_csv(keyword, results)
    print(f'\n完了！{path} に保存しました。')

if __name__ == "__main__":
    main()
