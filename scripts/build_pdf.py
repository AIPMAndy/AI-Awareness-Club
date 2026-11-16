#!/usr/bin/env python3
"""Build a public, source-driven PDF from the nine free AI Awareness Club guides.

Source of truth is data/guides.json and data/faq.json. No paid, member-only,
private, or customer materials are included. Run scripts/check_pdf.py after build.
"""
from __future__ import annotations

import hashlib
import html
import json
import sys
from pathlib import Path
from weasyprint import HTML

ROOT = Path(__file__).resolve().parents[1]
GUIDES_FILE = ROOT / "data/guides.json"
FAQ_FILE = ROOT / "data/faq.json"
PDF = ROOT / "pdf/ai-awareness-club-guide.pdf"
EDITION = ROOT / "pdf/edition.json"
BASE = "https://aipmandy.github.io/AI-Awareness-Club/"
REPO = "https://github.com/AIPMAndy/AI-Awareness-Club"
DRAFT_DATE = "2026-10-29"


def safe(value: object) -> str:
    return html.escape(str(value), quote=True)


def para(value: object) -> str:
    return safe(value).replace("\n", "<br>")


def load_source():
    guides = json.loads(GUIDES_FILE.read_text(encoding="utf-8"))
    faqs = json.loads(FAQ_FILE.read_text(encoding="utf-8"))
    assert len(guides) == 9 and len({g["slug"] for g in guides}) == 9
    for guide in guides:
        assert guide["title"] and guide["steps"] and guide["pitfalls"]
    return guides, faqs


def source_fingerprint() -> str:
    digest = hashlib.sha256()
    for path in (GUIDES_FILE, FAQ_FILE, Path(__file__), ROOT / "scripts/pdf-requirements.txt"):
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def make_html(guides, faqs):
    css = r"""
    @page {
      size: A4; margin: 21mm 20mm 20mm 20mm;
      @top-left { content: "AI 醒觉社 / PUBLIC KNOWLEDGE"; color: #686d76; font: 8pt "Noto Sans CJK SC", sans-serif; }
      @top-right { content: "AIPMAndy"; color: #686d76; font: 8pt "Noto Sans CJK SC", sans-serif; }
      @bottom-left { content: "公开教程 · 免费阅读 · 不承诺收入或录用结果"; color: #7b7f87; font: 7pt "Noto Sans CJK SC", sans-serif; }
      @bottom-right { content: counter(page); color: #555b65; font: 8pt "Noto Sans CJK SC", sans-serif; }
    }
    @page cover {
      @top-left { content: none; } @top-right { content: none; }
      @bottom-left { content: none; } @bottom-right { content: none; }
    }
    html { font-family: "Noto Sans CJK SC", "Noto Sans CJK JP", sans-serif; color: #252a31; }
    body { font-size: 10.25pt; line-height: 1.74; }
    a { color: #224b84; text-decoration: none; overflow-wrap: anywhere; }
    h1,h2,h3 { font-weight: 700; line-height: 1.42; color: #14191f; }
    h1 { font-size: 30pt; margin: 12mm 0 6mm; }
    h2 { font-size: 19pt; margin: 0 0 5mm; }
    h3 { font-size: 12pt; margin: 5mm 0 2mm; }
    p { margin: 2mm 0 3mm; }
    .cover { page: cover; break-after: page; height: 240mm; position: relative; padding-top: 27mm; }
    .eyebrow { color: #505e6f; text-transform: uppercase; letter-spacing: .1em; font-size: 9pt; font-weight: 700; }
    .cover .ink { width: 21mm; height: 2mm; background: #1e3759; margin: 14mm 0 18mm; }
    .cover h1 { font-size: 33pt; line-height: 1.38; max-width: 145mm; }
    .cover .subtitle { color: #56616d; font-size: 14pt; max-width: 143mm; }
    .cover-bottom { position: absolute; bottom: 7mm; border-top: 1px solid #ccd2d9; width: 100%; padding-top: 6mm; font-size: 9pt; color: #56616d; }
    .toc { break-after: page; }
    .toc-list { padding: 0; list-style: none; }
    .toc-list li { border-bottom: 1px solid #e3e6ea; padding: 2.8mm 0; }
    .toc-list b { display: inline-block; width: 12mm; color: #516175; }
    .guide { break-before: page; }
    .guide-header { border-bottom: 2px solid #243b5a; padding-bottom: 6mm; margin-bottom: 8mm; }
    .guide-header .tag { font-size: 8.5pt; letter-spacing: .06em; color: #596679; }
    .guide-header h2 { margin: 3mm 0; }
    .lead { font-size: 11.4pt; color: #3b4550; }
    .outcome { padding: 4mm 5mm; background: #f1f4f7; border-left: 3px solid #304f79; margin: 6mm 0; }
    .outcome strong { display: block; font-size: 8.5pt; letter-spacing: .02em; }
    .step { break-inside: avoid; margin: 7mm 0 5mm; }
    .step-head { font-weight: 700; color: #202a35; font-size: 11.3pt; margin-bottom: 1mm; }
    .step .result { font-size: 9.3pt; color: #53616f; margin-top: 2mm; border-bottom: 1px solid #e4e8ec; padding-bottom: 3mm; }
    .callout { border: 1px solid #d6dde4; padding: 4mm 5mm; margin: 7mm 0; }
    .callout h3 { margin-top: 0; }
    .callout li { margin-bottom: 2mm; }
    .qa { break-inside: avoid; margin: 5mm 0; }
    .qa strong { display: block; }
    .source { font-size: 8.8pt; color: #59636e; margin-top: 7mm; border-top: 1px solid #e0e5ea; padding-top: 4mm; }
    .appendix { break-before: page; }
    .disclaimer { background: #f3f5f7; padding: 4mm 6mm; color: #4d5763; }
    .meta-grid { display: table; width: 100%; border-collapse: collapse; }
    .meta-grid div { padding: 2.5mm 0; border-bottom: 1px solid #dce1e6; }
    .small { font-size: 9pt; color: #59646e; }
    """
    output = [
        "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><title>AI 醒觉社 · 九条免费实战指南</title>",
        "<style>", css, "</style></head><body>",
        "<section class='cover'><div class='eyebrow'>AI AWARENESS CLUB / OPEN EDITION</div>",
        "<div class='ink'></div><h1>把 AI 变成<br>真实、可检验的行动。</h1>",
        "<p class='subtitle'>AI 醒觉社 · 九条免费实战指南</p>",
        "<p>从 AI 入门、职业转型、个人 IP 到管理者 AI 实战。<br>不是结果保证，而是一份可以拿去做的行动手册。</p>",
        "<div class='cover-bottom'>作者 / 维护者：AI 酋长 Andy（AIPMAndy）<br>",
        "公开内容初稿：", DRAFT_DATE, " · 版本：源文件同步版<br>",
        "微信：AIPMAndy · ", '<a href="https://metaver.vip/">个人官网</a>', " · ",
        '<a href="https://www.a6no1.cn/">星觉科技官网</a>', "</div></section>",
        "<section class='toc'><div class='eyebrow'>READING MAP</div><h1>阅读导航</h1>",
        "<p class='lead'>先选一个当下的问题，再按步骤完成交付物。每条路线含目标、具体动作、常见错误和可查来源。</p>",
        "<ol class='toc-list'>",
    ]
    for i, g in enumerate(guides, 1):
        output += ["<li><b>", f"{i:02d}", "</b><a href='#guide-", safe(g["slug"]), "'>", safe(g["title"]), "</a></li>"]
    output += [
        "</ol><p class='small'>本 PDF 仅包含仓库中的九条公开、免费指南和公开 FAQ；不包含会员专属知识、客户材料或第三方受限内容。</p>",
        '<p class="small">在线更新与勘误：<a href="', REPO, '">', REPO, "</a></p></section>"
    ]
    for i, g in enumerate(guides, 1):
        output += [
            "<section class='guide' id='guide-", safe(g["slug"]), "'>",
            "<div class='guide-header'><div class='tag'>", f"GUIDE {i:02d} / ", safe(g["category"]), " · ", safe(g["level"]), "</div>",
            "<h2>", safe(g["title"]), "</h2><p class='lead'>", safe(g["subtitle"]), "</p><p>", para(g["description"]), "</p></div>",
            "<div class='outcome'><strong>可验收交付物</strong>", para(g["objective"]), "</div>",
            "<p>", para(g["intro"]), "</p>",
            "<h3>按步骤完成</h3>",
        ]
        for j, step in enumerate(g["steps"], 1):
            output += [
                "<div class='step'><div class='step-head'>", f"{j:02d}. ", safe(step["title"]), "</div>",
                "<p>", para(step["body"]), "</p>",
                "<div class='result'><b>交付物：</b>", para(step["output"]), "</div></div>",
            ]
        output += ["<div class='callout'><h3>常见错误 / 风险边界</h3><ul>"]
        for pitfall in g["pitfalls"]:
            output += ["<li>", para(pitfall), "</li>"]
        output += ["</ul></div><h3>常见问题</h3>"]
        for item in g["faqs"]:
            output += ["<div class='qa'><strong>", safe(item["q"]), "</strong><p>", para(item["a"]), "</p></div>"]
        output += [
            "<p class='source'>公开在线原文：<a href='", BASE, "guides/", safe(g["slug"]), "/'>",
            BASE, "guides/", safe(g["slug"]), "/</a><br>",
            "原始结构化数据：<a href='", REPO, "/blob/main/data/guides.json'>data/guides.json</a> · ",
            "公开内容初稿 ", DRAFT_DATE, "；不代表外部政策或链接今天已重新核验。</p></section>"
        ]
    output += [
        "<section class='appendix'><div class='eyebrow'>REFERENCE / FAQ</div><h2>公开常见问题</h2>",
        "<p>社区申请、价格和会员权益是动态信息，请以官网当前页面为准。</p>",
    ]
    for item in faqs:
        output += ["<div class='qa'><strong>", safe(item["q"]), "</strong><p>", para(item["a"]), "</p></div>"]
    output += [
        "<div class='disclaimer'><b>边界说明</b><p>所有路径仅提供公开学习方法，不保证就业、获客、收入、AI 引用或流量排名。",
        "公开示例和练习不能冒充实际客户案例。职业与合规决策应以所在地区最新官方规则为准。</p></div>",
        "<h3>联系与核验</h3><div class='meta-grid'>",
        '<div>微信：<b>AIPMAndy</b></div>',
        '<div>个人官网：<a href="https://metaver.vip/">https://metaver.vip/</a></div>',
        '<div>个人服务：<a href="https://metaver.vip/services">https://metaver.vip/services</a></div>',
        '<div>公司官网：<a href="https://www.a6no1.cn/">https://www.a6no1.cn/</a></div>',
        '<div>醒觉社：<a href="https://metaver.vip/community">https://metaver.vip/community</a></div>',
        '<div>开源与勘误：<a href="', REPO, '">', REPO, '</a></div>',
        "</div><p class='small'>原始来源：仓库 data/guides.json、data/faq.json。内容初稿：", DRAFT_DATE,
        "。构建本文件并不表示已重新验证外部资料时效。</p></section></body></html>"
    ]
    return "".join(output)


def main():
    guides, faqs = load_source()
    fingerprint = source_fingerprint()
    if PDF.exists() and EDITION.exists():
        edition = json.loads(EDITION.read_text(encoding="utf-8"))
        if edition.get("source_sha256") == fingerprint:
            existing_hash = hashlib.sha256(PDF.read_bytes()).hexdigest()
            if existing_hash == edition.get("pdf_sha256"):
                print("Reusing verified PDF edition:", existing_hash)
                return
    PDF.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=make_html(guides, faqs), base_url=str(ROOT)).write_pdf(str(PDF))
    pdf_hash = hashlib.sha256(PDF.read_bytes()).hexdigest()
    EDITION.write_text(json.dumps({
        "title": "AI 醒觉社 · 九条免费实战指南",
        "source_sha256": fingerprint,
        "pdf_sha256": pdf_hash,
        "source_initial_date": DRAFT_DATE,
        "source_files": ["data/guides.json", "data/faq.json"],
        "note": "Source-driven public edition; source date is not a new verification date."
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Built public PDF", PDF, PDF.stat().st_size, pdf_hash)


if __name__ == "__main__":
    main()
