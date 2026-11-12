import csv
import re
from collections import Counter
import os
import sys

# 除外ワード
EXCLUDE = set([
    '千社札', 'とは', 'の', 'が', 'に', 'を', 'は', 'と', 'で', 'も', 'や', 'から', 'まで', 'より', 'へ',
    'そして', 'また', 'または', 'など', 'その', 'この', 'あの', 'それ', 'これ', 'あれ', 'ため', 'ので', 'が'
])

# ファイルのBOMやバイナリ先頭を見てエンコーディング自動判別
def auto_open(filename):
    with open(filename, 'rb') as f:
        raw = f.read(4096)
    if raw.startswith(b'\xff\xfe'):
        enc = 'utf-16'
    elif raw.startswith(b'\xfe\xff'):
        enc = 'utf-16'
    elif raw.startswith(b'\xef\xbb\xbf'):
        enc = 'utf-8-sig'
    else:
        try:
            raw.decode('utf-8')
            enc = 'utf-8'
        except Exception:
            try:
                raw.decode('cp932')
                enc = 'cp932'
            except Exception:
                enc = 'shift-jis'
    return open(filename, encoding=enc)

# ディレクトリ指定（引数 or カレント）
def main(target_dir):
    os.chdir(target_dir)
    # キーワード抽出
    keywords = set()
    for fname in ['00_02.csv', '00_03.csv', '00_04.csv']:
        if not os.path.exists(fname):
            continue
        with auto_open(fname) as f:
            reader = csv.reader(f)
            header = next(reader, None) or []
            # 「キーワード」列（00_04は「キーワード/質問」）のみ対象
            kw_idx = next((i for i, h in enumerate(header) if h.strip().startswith('キーワード')), 0)
            for row in reader:
                if len(row) <= kw_idx:
                    continue
                for word in re.split(r'[\s　]+', row[kw_idx].replace('"', '')):
                    if not word or word in EXCLUDE or word.isdigit():
                        continue
                    # 半角1文字（英字・記号）はノイズとして除外
                    if len(word) == 1 and word.isascii():
                        continue
                    # ひらがな1文字（助詞・接続的な語）は除外
                    if len(word) == 1 and 'ぁ' <= word <= 'ゖ':
                        continue
                    keywords.add(word)
    # 00_01.csvから見出し・本文列を抽出
    headline_list = []
    if os.path.exists('00_01.csv'):
        with auto_open('00_01.csv') as f:
            reader = csv.reader(f)
            header = next(reader, None) or []
            # 「見出し」列のみ対象（タイトル・URL等は除外）
            h_idx = header.index('見出し') if '見出し' in header else len(header) - 1
            for row in reader:
                if len(row) > h_idx:
                    headline_list.append(row[h_idx])
    # キーワードごとにカウント
    counter = Counter()
    for kw in keywords:
        for headline in headline_list:
            counter[kw] += headline.count(kw)
    # 結果を01_01.csvに出力
    with open('01_01.csv', 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['キーワード', 'カウント'])
        for kw, cnt in sorted(counter.items(), key=lambda x: -x[1]):
            writer.writerow([kw, cnt])

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('Usage: python count_kw_all.py <target_dir>')
