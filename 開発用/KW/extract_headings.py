"""指定URLのページから title / h2〜h5 を抽出する

使い方:
  python extract_headings.py https://example.com/a https://example.com/b
      → URLを直接指定（結果は画面に表示）
  python extract_headings.py kw_all/eye_fatigue
      → ディレクトリ内の URL.txt を読み込み、結果を同じディレクトリの
         headings_YYYYMMDD.txt に保存
  python extract_headings.py kw_all/eye_fatigue/URL.txt
      → URL.txt を直接指定（保存先は URL.txt と同じディレクトリ）

オプション:
  -o FILE   結果の保存先を指定（URL直接指定時も保存できる）
"""
import argparse
import os
import sys
from datetime import date

import requests
from bs4 import BeautifulSoup

HEADING_TAGS = ['h2', 'h3', 'h4', 'h5']

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/130.0 Safari/537.36'
}


def clean(text):
    return ' '.join(text.split())


def extract(url):
    """URLから title と h2〜h5（出現順）を取得する"""
    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    title = clean(soup.title.get_text()) if soup.title else ''

    for tag in soup(['script', 'style', 'noscript', 'template']):
        tag.decompose()

    # 本文領域にh2があればそこを優先（サイドバー等の見出しを除外）
    root = soup.body or soup
    for candidate in (soup.find('article'), soup.find('main')):
        if candidate and candidate.find('h2'):
            root = candidate
            break

    headings = []
    for h in root.find_all(HEADING_TAGS):
        text = clean(h.get_text())
        if text:
            headings.append((h.name, text))
    return title, headings


def format_result(url, title, headings):
    lines = [f'URL: {url}', f'title: {title}']
    for name, text in headings:
        indent = '   ' * (int(name[1]) - 2)
        lines.append(f'{indent}{name}: {text}')
    return '\n'.join(lines)


def read_url_file(path):
    with open(path, encoding='utf-8-sig') as f:
        return [line.strip() for line in f if line.strip().startswith('http')]


def resolve_targets(args):
    """引数からURLリストとデフォルト保存先を決める"""
    urls, out = [], None
    for arg in args:
        if arg.startswith('http'):
            urls.append(arg)
        elif os.path.isdir(arg):
            urls += read_url_file(os.path.join(arg, 'URL.txt'))
            out = out or os.path.join(arg, f'headings_{date.today():%Y%m%d}.txt')
        elif os.path.isfile(arg):
            urls += read_url_file(arg)
            out = out or os.path.join(os.path.dirname(arg) or '.',
                                      f'headings_{date.today():%Y%m%d}.txt')
        else:
            print(f'スキップ（URL・ファイル・ディレクトリではない）: {arg}', file=sys.stderr)
    return urls, out


def main():
    parser = argparse.ArgumentParser(description='ページの title / h2〜h5 を抽出')
    parser.add_argument('targets', nargs='+', help='URL / URL.txt / URL.txtを含むディレクトリ')
    parser.add_argument('-o', '--output', help='結果の保存先ファイル')
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

    urls, default_out = resolve_targets(args.targets)
    if not urls:
        sys.exit('URLが見つかりませんでした。')
    out_path = args.output or default_out

    blocks = []
    for i, url in enumerate(urls, 1):
        print(f'[{i}/{len(urls)}] {url[:80]}', file=sys.stderr)
        try:
            title, headings = extract(url)
            block = format_result(url, title, headings)
        except requests.RequestException as e:
            block = f'URL: {url}\nエラー: {e}'
        blocks.append(f'#{i:02d}\n{block}')

    result = ('\n\n' + '=' * 60 + '\n\n').join(blocks) + '\n'
    if out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f'\n保存しました: {out_path}', file=sys.stderr)
    else:
        print(result)


if __name__ == '__main__':
    main()
