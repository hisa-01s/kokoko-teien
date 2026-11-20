import csv, os, re, html, glob, datetime, sys
ROOT = r"C:/Users/user/OneDrive/デスクトップ/heal-place"
SRC = f"{ROOT}/開発用/directory-map_20261119_2333_KW.csv"
BASE = "https://heal-place.com/"
N = {2:"2",3:"３",4:"４",5:"５",6:"６"}
H2KEYS = [f"h2：{N[n]}つ目画像" for n in range(2,7)]

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
    for n in range(2, 7):
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
                   "kw_all": "○" if slug and slug in kw_all else "×"})

FIELDS = ["URL","index","title","KW","vol","第1階層","第2階層","第3階層","階層深さ","sitemap.xml掲載","アイキャッチ掲載",*H2KEYS,"kw_all"]
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
for u in sorted(live - seen):
    notes.append(f"new: {u}")
    out.append({"URL": u, "index": "", "KW": "", "vol": "", **info(u)})

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
dst = f"{ROOT}/開発用/directory-map_{stamp}_KW.csv"
with open(dst, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(out)
print(dst, len(out)); print("\n".join(notes))
from collections import Counter
for k in H2KEYS: print(k, Counter(o[k] for o in out))

# diffs vs old for recomputed columns
old = {r["URL"]: r for r in rows}
for o in out:
    r = old.get(o["URL"])
    if not r: continue
    for k in ["title","sitemap.xml掲載","アイキャッチ掲載","h2：2つ目画像","kw_all","階層深さ"]:
        if r[k] != o[k]: print("changed", o["URL"], k, repr(r[k]), "->", repr(o[k]))
