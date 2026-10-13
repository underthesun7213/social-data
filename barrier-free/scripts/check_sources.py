"""Fetch every cited source_url and check whether each row's numbers appear in the page.

Usage: python3 barrier-free/scripts/check_sources.py CACHE_DIR
Output: barrier-free/verification/source_check.csv

A number "appears" if it is found in the page text in any common format
(94.3 / 94,3 / 1,089 / 1 089 / 1089). This is a mechanical first pass: a hit
does not prove the number means the same thing, and a miss can mean the page is
JavaScript-rendered or the number is computed from the source.
"""
import concurrent.futures as cf
import csv
import hashlib
import html
import os
import re
import subprocess
import sys
import urllib.request

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}


def fetch(url, cache):
    path = os.path.join(cache, hashlib.sha1(url.encode()).hexdigest())
    if os.path.exists(path + ".txt"):
        return open(path + ".status").read(), open(path + ".txt", encoding="utf-8").read()
    status, text = "error", ""
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=45) as r:
            body, ctype, status = r.read(), r.headers.get("Content-Type", ""), str(r.status)
        if body[:4] == b"%PDF" or "pdf" in ctype:
            open(path + ".pdf", "wb").write(body)
            text = subprocess.run(["pdftotext", "-layout", path + ".pdf", "-"],
                                  capture_output=True, text=True, timeout=120).stdout
        else:
            raw = body.decode(r.headers.get_content_charset() or "utf-8", errors="replace")
            raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
            text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    except urllib.error.HTTPError as e:
        status = str(e.code)
    except Exception as e:  # network errors, timeouts, bad PDFs
        status = f"error:{type(e).__name__}"
    open(path + ".status", "w").write(status)
    open(path + ".txt", "w", encoding="utf-8").write(text)
    return status, text


def numbers(value):
    """Significant numbers in a value cell, ignoring bare years and tiny integers."""
    out = []
    for m in re.findall(r"\d[\d,]*(?:\.\d+)?", value):
        n = m.replace(",", "")
        if re.fullmatch(r"(19|20)\d\d", n) or (n.isdigit() and int(n) < 10):
            continue
        out.append(n)
    return out


def variants(n):
    whole, _, frac = n.partition(".")
    grouped = f"{int(whole):,}"
    v = {n, grouped + ("." + frac if frac else ""), grouped.replace(",", " ") + ("." + frac if frac else ""),
         grouped.replace(",", ".") + ("," + frac if frac else "")}
    if frac:
        v.add(whole + "," + frac)
    return v


def found(n, text):
    return any(re.search(r"(?<![\d.,])" + re.escape(v) + r"(?![\d])", text) for v in variants(n))


def main(cache):
    os.makedirs(cache, exist_ok=True)
    rows = list(csv.DictReader(open(os.path.join(BASE, "all_indicators.csv"), encoding="utf-8")))
    counter = {}
    for r in rows:
        counter[r["source_file"]] = counter.get(r["source_file"], 0) + 1
        r["row_id"] = f"{r['source_file'].replace('_indicators.csv', '')}:{counter[r['source_file']]}"
    urls = sorted({r["source_url"] for r in rows if r["source_url"].startswith("http")})
    with cf.ThreadPoolExecutor(12) as ex:
        pages = dict(zip(urls, ex.map(lambda u: fetch(u, cache), urls)))
    out = []
    for r in rows:
        status, text = pages.get(r["source_url"], ("no_url", ""))
        nums = numbers(r["value"])
        hits = [n for n in nums if text and found(n, text)]
        if not text.strip():
            match = "열람불가"
        elif not nums:
            match = "수치없음"
        else:
            match = "전부" if len(hits) == len(nums) else ("일부" if hits else "없음")
        out.append({"row_id": r["row_id"], "country": r["country"], "indicator": r["indicator"],
                    "value": r["value"], "http_status": status, "text_chars": len(text),
                    "numbers": " ".join(nums), "found": " ".join(hits), "match": match,
                    "source_url": r["source_url"]})
    with open(os.path.join(BASE, "verification", "source_check.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    from collections import Counter
    print(Counter(o["match"] for o in out))


if __name__ == "__main__":
    main(sys.argv[1])
