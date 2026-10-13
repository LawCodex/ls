"""Lesotho: download the legislation published on the Government of Lesotho portal (https://www.gov.ls):
the Constitution of Lesotho and the Acts uploaded to the portal's media library (found through the portal's
public WordPress REST API, /wp-json/wp/v2/media?search=...).
Cache: _raw/ls/. Usage: python ls_fetch.py
"""
import json
import os
import re
import sys

import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ls_text import fetch, UA  # noqa: E402

RAW = os.environ.get("LS_RAW", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_raw", "ls"))
API = "https://www.gov.ls/wp-json/wp/v2/media?per_page=100&search=%s&mime_type=application/pdf&_fields=id,title,source_url,date"


def main():
    items, seen = [], set()
    for q in ("constitution", "act"):
        for m in requests.get(API % q, headers={"User-Agent": UA}, timeout=120).json():
            t = re.sub(r"&#8211;", "-", m["title"]["rendered"]).replace("_", " ").strip()
            if not (re.search(r"(?i)\bconstitution\b", t) or re.search(r"\bAct\b", t)) or re.search(r"(?i)contract|press|advert", t):
                continue
            key = re.sub(r"\W+", " ", t.lower()).strip()
            if key in seen:
                continue
            seen.add(key)
            items.append({"title": t, "url": m["source_url"], "date_uploaded": m["date"][:10]})
    for it in items:
        name = re.sub(r"[^A-Za-z0-9]+", "_", it["title"])[:100] + ".pdf"
        it["file"] = fetch(it["url"], os.path.join(RAW, "pdf", name), delay=3, check_pdf=True, timeout=300)
        print("ok " if it["file"] else "FAIL", it["title"])
    json.dump(items, open(os.path.join(RAW, "index.json"), "w"), indent=1)


if __name__ == "__main__":
    os.makedirs(RAW, exist_ok=True)
    main()
