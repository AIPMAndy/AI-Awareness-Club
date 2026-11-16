#!/usr/bin/env python3
"""Fail CI if public PDF loses source coverage, usable text, links or layout."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "pdf/ai-awareness-club-guide.pdf"
EDITION = ROOT / "pdf/edition.json"


def main():
    edition = json.loads(EDITION.read_text(encoding="utf-8"))
    guides = json.loads((ROOT / "data/guides.json").read_text(encoding="utf-8"))
    faqs = json.loads((ROOT / "data/faq.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(PDF.read_bytes()).hexdigest() == edition["pdf_sha256"], "PDF hash mismatch"
    doc = fitz.open(PDF)
    assert 12 <= len(doc) <= 120, f"unexpected page count {len(doc)}"
    texts, links, issues = [], 0, []
    for i, page in enumerate(doc):
        txt = page.get_text()
        texts.append(txt)
        if len(txt.strip()) < 30:
            issues.append(f"page {i+1}: text too sparse")
        links += len(page.get_links())
        for box in page.get_text("blocks"):
            if len(box) < 5 or box[4].strip() == "":
                continue
            if box[0] < -1 or box[1] < -1 or box[2] > page.rect.width + 1 or box[3] > page.rect.height + 1:
                issues.append(f"page {i+1}: text outside page {box[:4]}")
        # Render every page, not just a few sample pages.
        pix = page.get_pixmap(matrix=fitz.Matrix(1.1, 1.1), alpha=False)
        if not pix.samples:
            issues.append(f"page {i+1}: blank render")
    content = "".join("".join(t.split()) for t in texts)
    for guide in guides:
        if "".join(guide["title"].split()) not in content:
            issues.append(f"missing source guide {guide['slug']}")
        if "".join(guide["objective"].split()) not in content:
            issues.append(f"missing objective {guide['slug']}")
    if len(faqs) < 5:
        issues.append("FAQ source unexpectedly small")
    for required in ("AIPMAndy", "metaver.vip", "www.a6no1.cn", "AI醒觉社"):
        if required not in content:
            issues.append(f"missing identity {required}")
    if links < 18:
        issues.append(f"insufficient clickable links: {links}")
    if len(doc.get_toc()) < len(guides):
        issues.append("missing PDF bookmarks")
    qa = {
        "pages": len(doc), "bookmarks": len(doc.get_toc()), "clickable_links": links,
        "characters": len(content), "guides": len(guides), "public_faq": len(faqs),
        "sha256": edition["pdf_sha256"], "issues": issues,
        "scope": "Automated rendering and text checks only; high-resolution human sign-off and real mobile devices remain pending."
    }
    target = ROOT / "pdf/qa-report.json"
    target.write_text(json.dumps(qa, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(qa, ensure_ascii=False, indent=2))
    doc.close()
    if issues:
        raise SystemExit("PDF quality gate failed")


if __name__ == "__main__":
    main()
