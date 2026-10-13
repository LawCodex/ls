"""Lesotho: convert the downloaded PDFs to Markdown (scans without a text layer are skipped, no OCR).
Usage: python ls_convert.py <repo_dir>"""
import datetime
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ls_text import pdf_text, clean_pages, structure, write_md, slug, text_quality  # noqa: E402

RAW = os.environ.get("LS_RAW", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_raw", "ls"))
TODAY = datetime.date.today().isoformat()


def main(repo):
    for it in json.load(open(os.path.join(RAW, "index.json"))):
        if not it.get("file"):
            continue
        pages, _ = pdf_text(it["file"])
        full = "\n".join(pages)
        if len(re.sub(r"\s", "", full)) < 2000 or text_quality(full) < 0.75:
            print("SKIP (scan, no text layer):", it["title"])
            continue
        if "Constitution" in it["title"]:
            title = "Constitution of Lesotho"
            path = os.path.join(repo, "constitution", "constitution-of-lesotho.md")
            meta = {"title": title, "type": "constitution", "date": "1993-04-02", "status": "unknown"}
        else:
            title = it["title"]
            y = re.search(r"(19|20)\d\d", title)
            path = os.path.join(repo, "acts", slug(title) + ".md")
            meta = {"title": title, "type": "act", "year": y.group(0) if y else "", "status": "unknown"}
        meta.update({"jurisdiction": "ls", "language": "en", "source": it["url"], "retrieved": TODAY})
        write_md(path, meta, title, structure(clean_pages(pages), "en"))
        print("written", path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
