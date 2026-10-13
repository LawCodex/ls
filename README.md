# Lesotho (LS) — legislation as Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

**Minimal corpus.** Only the **Constitution of Lesotho** (1993), in **English**, as published on the Government of
Lesotho portal (https://www.gov.ls, PDF uploaded February 2019; the consolidation date of that text is not stated).
Retrieved 2026-10-13.

| Category | Files |
|---|---|
| Constitution | 1 |

## Structure

```
constitution/constitution-of-lesotho.md     Chapters I–XV, sections (Section N — title), Schedules 1–3
```

Text extracted with poppler `pdftotext`; chapters and schedules become headings, sections `Section N — <title>`.
The table of contents at the top is kept as plain text.

## Not covered / known gaps

* **Acts of Parliament, orders and subsidiary legislation are not covered.** No official open database of Lesotho
  legislation could be found: the Parliament websites (parliament.ls, nationalassembly.parliament.ls,
  senate.parliament.ls) publish Bills, order papers and committee reports but not the enacted Acts; the
  Government portal publishes only a few Acts (Appropriation Acts 2017 and 2019), which are scanned PDFs without a
  text layer (skipped, no OCR); the Ministry of Justice site (justice.gov.ls) has no legislation section.
  The Lesotho Legal Information Institute (LesothoLII) forbids scraping/bulk download and was not used.
* Constitutional amendments after the date of the portal's PDF (e.g. the Tenth Amendment to the Constitution
  process of 2024) are not reflected.

## Sources and licence

| Source | URL |
|---|---|
| Government of Lesotho portal — media library (WordPress REST API, public) | https://www.gov.ls/wp-content/uploads/2019/02/Lesotho_Constitution.pdf |

Official text of the Kingdom of Lesotho. robots.txt allows these paths; requests were made with an identifying
User-Agent.

## Regenerate

```
pip install -r scripts/requirements.txt     # plus poppler (pdftotext, pdfinfo)
python scripts/ls_fetch.py                  # downloads into ../_raw/ls/
python scripts/ls_convert.py .
```
