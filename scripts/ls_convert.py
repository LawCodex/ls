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
    import hashlib
    hashes = set()
    for it in json.load(open(os.path.join(RAW, "index.json"))):
        if not it.get("file"):
            continue
        pages, _ = pdf_text(it["file"])
        full = "\n".join(pages)
        h = hashlib.sha1(full.encode()).hexdigest()
        if h in hashes:
            continue
        hashes.add(h)
        if it.get("archived") and re.search(r"(?i)\bbill\b|memorandum|explanatory|expl\w*natory", full[:1500]):
            print("SKIP (Bill version, not the enacted Act):", it["title"])
            continue
        if len(re.sub(r"\s", "", full)) < 2000 or text_quality(full) < 0.75:
            print("SKIP (scan, no text layer):", it["title"])
            continue
        if "Constitution" in it["title"]:
            title = "Constitution of Lesotho"
            path = os.path.join(repo, "constitution", "constitution-of-lesotho.md")
            meta = {"title": title, "type": "constitution", "date": "1993-04-02", "status": "unknown"}
        else:
            head = [x.strip() for x in full.splitlines() if x.strip()][:12]
            num = re.search(r"(?i)\bACT\s+NO\.?\s*(\d+)\s*(?:OF\s*)?((?:19|20)\d\d)", " ".join(head))
            tl = next((x for x in head if re.search(r"(?i)\bACT\b", x) and not re.match(r"(?i)^(ACT NO|Supplement|An Act)", x)
                       and len(x) < 120), it["title"])
            title = re.sub(r"\s+", " ", tl).strip()
            mc = re.search(r"may be cited as the (.+?\bAct,? (?:19|20)\d\d)", title)
            if mc:
                title = mc.group(1)
            title = re.sub(r"(?i)\s+No\.?\s*\d+\s+of\s+((?:19|20)\d\d)$", r" \1", title)
            title = title.title() if title.isupper() else title
            title = re.sub(r"\b(And|Of|The|To|For)\b", lambda m: m.group(1).lower(), title)
            title = title[:1].upper() + title[1:]
            y = re.search(r"(19|20)\d\d", title) or (num and re.search(r"(19|20)\d\d", num.group(2)))
            year = y.group(0) if y else ""
            path = os.path.join(repo, "acts", (year + "-" if year else "") + slug(title)[:80] + ".md")
            meta = {"title": title, "identifier": "Act No. %s of %s" % (num.group(1), num.group(2)) if num else "",
                    "type": "act", "year": year, "status": "unknown"}
            if it.get("archived"):
                meta["archived_source"] = it["archived"]
        meta.update({"jurisdiction": "ls", "language": "en", "source": it["url"], "retrieved": TODAY})
        write_md(path, meta, title, structure(clean_pages(pages), "en"))
        print("written", path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
