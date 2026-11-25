import csv, os, re, html, glob, datetime, sys
ROOT = r"C:/Users/user/OneDrive/デスクトップ/heal-place"
SRC = f"{ROOT}/開発用/directory-map_20261125_2215_KW.csv"
BASE = "https://heal-place.com/"
N = {1:"1",2:"2",3:"３",4:"４",5:"５",6:"６"}
H2KEYS = [f"h2：{N[n]}つ目画像" for n in range(1,7)]

rows = list(csv.DictReader(open(SRC, encoding="utf-8-sig")))
sitemap = open(f"{ROOT}/sitemap.xml", encoding="utf-8").read()
sm_urls = set(re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap))
kw_all = set(os.listdir(f"{ROOT}/開発用/KW/kw_all"))

# 301 map from .htaccess
redir = {}
for line in open(f"{ROOT}/.htaccess", encoding="utf-8", errors="ignore"):
    m = re.match(r"\s*Redirect(?:Match)?\s+(?:301|permanent)\s+(\S+)\s+(\S+)", line)
    if m:
        src, dst = m.groups()
        if not dst.startswith("http"): dst = BASE.rstrip("/") + dst
        redir[BASE.rstrip("/") + src.replace("^", "").replace("$", "")] = dst

# all live pages
pages = [""]
for p in glob.glob(f"{ROOT}/column/**/index.html", recursive=True) + glob.glob(f"{ROOT}/contents/**/index.html", recursive=True):
    rel = os.path.relpath(os.path.dirname(p), ROOT).replace("\\", "/")
    pages.append(rel + "/")
live = {BASE + p for p in pages}

def info(url):
    rel = url[len(BASE):]
    s = open(f"{ROOT}/{rel}index.html", encoding="utf-8").read()
    m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = html.unescape(m.group(1).strip()) if m else ""
    parts = [x for x in rel.strip("/").split("/") if x]
    l1 = parts[0] if parts else "(トップ)"
    l2 = parts[1] if len(parts) > 1 else ""
    l3 = parts[2] if len(parts) > 2 else ""
    eye = re.search(r'<figure class="eyecatch">\s*<img[^>]*src="([^"]+)"', s)
    eyefile = os.path.basename(eye.group(1)) if eye else ""
    if eyefile and not os.path.exists(f"{ROOT}/asset/image/{eyefile}"): eyefile += "(ファイルなし)"
    h2 = [m.start() for m in re.finditer(r"<h2[\s>]", s)]
    h2imgs = {}
    for n in range(1, 7):
        key = f"h2：{N[n]}つ目画像"
        if len(parts) < 3 or len(h2) < n: h2imgs[key] = "-"; continue
        sec = s[h2[n-1]: h2[n] if len(h2) > n else len(s)]
        im = re.search(r'<img[^>]*src="([^"]+)"', sec)
        if im and os.path.exists(os.path.normpath(os.path.join(ROOT, rel, im.group(1)))): h2imgs[key] = "○"
        elif im: h2imgs[key] = "×(ファイルなし)"
        else: h2imgs[key] = "×"
    slug = l3 or l2
    return dict(title=title, 第1階層=l1, 第2階層=l2, 第3階層=l3, 階層深さ=str(len(parts)),
                **{"sitemap.xml掲載": "○" if url in sm_urls else "×",
                   "アイキャッチ掲載": "○" if eye else "×",
                   **h2imgs,
                   "kw_all": "○" if slug and slug in kw_all else "×",
                   "kw_allファイル": chr(10).join(sorted(os.listdir(f"{ROOT}/開発用/KW/kw_all/{slug}"))) if slug and slug in kw_all else "-"})

FIELDS = ["URL","index","title","KW","vol","第1階層","第2階層","第3階層","sitemap.xml掲載","アイキャッチ掲載",*H2KEYS,"kw_allファイル"]
out, seen, notes = [], set(), []
for r in rows:
    url = r["URL"]; idx = r["index"]
    if url not in live and url in redir:
        notes.append(f"moved: {url} -> {redir[url]}"); url = redir[url]; idx = ""
    if url not in live:
        notes.append(f"missing (dropped): {url}"); continue
    if url in seen: continue
    seen.add(url)
    out.append({"URL": url, "index": idx, "KW": r["KW"], "vol": r["vol"], **info(url)})
# KW/vol for new pages, as supplied by the user (merged KWs newline-joined in one cell)
NEWKW = {
    "column/hobby/embroidery_howto/": [("刺繍のやり方", "14800")],
    "column/hobby/kansai_onsen/": [("温泉日帰り関西", "12100")],
    "column/culture/goshuincho_popular/": [("人気御朱印帳", "8100"), ("御朱印帳 レア", "2900"), ("寺の御朱印帳", "720")],
    "column/life/kizukai/": [("気遣いとは", "6600")],
    "column/hobby/puraban_keyholder/": [("プラ板キーホルダー", "6600")],
    "column/life/time_kill/": [("時間つぶし", "5400")],
    "column/culture/hana_kotoba/": [("花の意味", "5400")],
    "column/life/bag_storage/": [("カバン　収納", "18100"), ("かばん収納", "18100")],
    "column/life/xmas_gift1000/": [("1000円プレゼント クリスマス", "2400")],
    "column/culture/kiyomizu_goshuin/": [("清水寺 の 御朱印", "8100")],
    "column/life/sink_storage/": [("キッチンした収納", "12100")],
    "column/life/xmas_card/": [("クリスマス手作りカード", "14800")],
    "column/life/laundry_fold/": [("洗濯物　たたみ方", "1900")],
    "column/hobby/easy_sewing/": [("簡単裁縫", "880")],
    "column/culture/season_change/": [("季節の移ろい", "880")],
    "column/life/hyakkin_storage/": [("100 均 収納", "6600")],
    "column/hobby/tokyo_spots/": [("東京 有名な場所", "4400")],
}
for u in sorted(live - seen):
    notes.append(f"new: {u}")
    kws = NEWKW.get(u[len(BASE):], [])
    out.append({"URL": u, "index": "", "KW": chr(10).join(k for k, v in kws), "vol": chr(10).join(v for k, v in kws), **info(u)})

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
dst = f"{ROOT}/開発用/directory-map_{stamp}_KW.csv"
with open(dst, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, FIELDS, extrasaction="ignore"); w.writeheader(); w.writerows(out)
print(dst, len(out)); print("\n".join(notes))
from collections import Counter
for k in H2KEYS: print(k, Counter(o[k] for o in out))

# diffs vs old for recomputed columns
old = {r["URL"]: r for r in rows}
for o in out:
    r = old.get(o["URL"])
    if not r: continue
    for k in ["title","sitemap.xml掲載","アイキャッチ掲載",*H2KEYS,"kw_allファイル"]:
        if r[k] != o[k]: print("changed", o["URL"], k, repr(r[k]), "->", repr(o[k]))
