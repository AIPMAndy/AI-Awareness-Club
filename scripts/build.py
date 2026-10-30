#!/usr/bin/env python3
"""Dependency-free static site generator for AI Awareness Club.

Source of truth: data/guides.json and data/faq.json.
Output: docs/ ready for GitHub Pages /AI-Awareness-Club/.
"""
from __future__ import annotations
import html
import json
import re
import shutil
from datetime import date
from pathlib import Path
from urllib.parse import quote
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'docs'
ASSETS = ROOT / 'site' / 'assets'
GUIDES = json.loads((ROOT/'data/guides.json').read_text(encoding='utf-8'))
FAQ = json.loads((ROOT/'data/faq.json').read_text(encoding='utf-8'))
BASE = 'https://aipmandy.github.io/AI-Awareness-Club/'
SITE_NAME = 'AI醒觉社 · AI Awareness Club'
OFFICIAL = 'https://metaver.vip/community'
KB = 'https://kb.metaver.vip/'
PERSONAL_SITE = 'https://metaver.vip/'
WECHAT_ID = 'AIPMAndy'


def e(s): return html.escape(str(s), quote=True)
def url(route=''): return BASE + route.lstrip('/')
def html_p(s): return e(s)
def link_to_guide(g): return f'guides/{g["slug"]}/'

def ga(label, href, cls='text-link', attrs=''):
    return f'<a class="{cls}" href="{e(href)}" {attrs}>{e(label)} <span aria-hidden="true">↗</span></a>'


def meta(title, description, route='', kind='website', jsonld=None):
    canonical=url(route)
    schemas='\n'.join('<script type="application/ld+json">'+json.dumps(o,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+'</script>' for o in (jsonld or []))
    return f'''<!doctype html>
<html lang="zh-CN" data-theme="light"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#f5f5f7"><meta name="color-scheme" content="light dark">
<title>{e(title)}</title><meta name="description" content="{e(description)}">
<meta name="author" content="AI醒觉社 · AI Awareness Club"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{e(canonical)}"><link rel="icon" type="image/svg+xml" href="{e(url('assets/icon.svg'))}">
<meta property="og:site_name" content="AI醒觉社 · AI Awareness Club"><meta property="og:type" content="{e(kind)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{e(canonical)}"><meta property="og:image" content="{e(url('assets/social-preview.png'))}">
<meta property="og:locale" content="zh_CN"><meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(description)}">
<link rel="stylesheet" href="{e(url('assets/style.css'))}">
<link rel="stylesheet" href="{e(url('assets/apple.css'))}">
{schemas}
</head><body><a class="skip" href="#main">跳到主要内容</a>
<header class="site-header"><div class="header-inner"><a href="{e(url())}" class="logo" aria-label="AI醒觉社首页"><span class="logo-mark" aria-hidden="true">◌</span><span>AI<span class="brand-highlight">醒觉社</span><small>AI AWARENESS CLUB</small></span></a>
<nav class="main-nav" aria-label="主导航"><a href="{e(url('paths/'))}">学习路线</a><a href="{e(url('library/'))}">开源知识</a><a href="{e(url('about/'))}">关于社群</a><a href="{e(url('faq/'))}">常见问题</a><a href="{e(url('index.html'))}#contact">联系 Andy</a></nav>
<div class="header-actions"><button class="icon-button theme-toggle" type="button" aria-label="切换深浅色模式" title="切换主题"><span aria-hidden="true">◐</span></button><a class="nav-cta" href="{OFFICIAL}" target="_blank" rel="noopener noreferrer">了解社群 <span aria-hidden="true">↗</span></a></div>
<button class="menu-button" aria-label="打开菜单" aria-expanded="false" aria-controls="mobile-nav">☰</button></div>
<nav class="mobile-nav" id="mobile-nav" hidden aria-label="移动导航"><a href="{e(url('paths/'))}">学习路线</a><a href="{e(url('library/'))}">开源知识</a><a href="{e(url('about/'))}">关于社群</a><a href="{e(url('faq/'))}">常见问题</a><a href="{OFFICIAL}">了解社群 ↗</a><a href="{e(url('index.html'))}#contact">联系 Andy · 微信</a></nav></header>'''


def footer():
    return f'''<footer class="footer"><div class="footer-top"><div><div class="footer-symbol" aria-hidden="true">◌</div><h2>把知识交还给每一个<br>愿意行动的人。</h2><p>开放学习 · 保持判断 · 共同创造</p></div><div class="footer-links"><div><b>探索</b><a href="{url('paths/')}">学习路线</a><a href="{url('library/')}">公开知识</a><a href="{url('faq/')}">常见问题</a></div><div><b>官方入口</b><a href="https://metaver.vip/">Andy 官网 ↗</a><a href="{OFFICIAL}">醒觉社社群 ↗</a><a href="{KB}">醒觉知识库 ↗</a></div><div><b>开源</b><a href="https://github.com/AIPMAndy/AI-Awareness-Club">GitHub 仓库 ↗</a><a href="https://github.com/AIPMAndy/AI-Awareness-Club/blob/main/CONTRIBUTING.md">参与共建 ↗</a></div></div></div>
<div class="footer-contact" aria-label="联系主理人 Andy"><div><span class="contact-eyebrow">DIRECT CONTACT · 主理人</span><p>有合作、求职或 AI 成长问题？直接联系 Andy。</p></div><div class="footer-contact-actions"><span class="wechat-identity">个人微信 <strong>{WECHAT_ID}</strong></span><button type="button" class="copy-wechat" data-copy-wechat="{WECHAT_ID}" aria-label="复制 Andy 个人微信号 {WECHAT_ID}">复制微信号</button><a href="{PERSONAL_SITE}" class="contact-website" target="_blank" rel="noopener noreferrer">个人官网 metaver.vip <span aria-hidden="true">↗</span></a></div></div>
<div class="footer-bottom"><span>© 2026 AI Awareness Club · 社群信息以<a href="{OFFICIAL}">官网</a>为准</span><span>独立学习项目 · 无广告追踪 · 内容不构成收益保证</span></div></footer><script src="{url('assets/app.js')}" defer></script></body></html>'''


def org_schema():
    return {"@context":"https://schema.org","@type":"Organization","@id":"https://metaver.vip/#ai-awareness-club","name":"AI醒觉社","alternateName":"AI Awareness Club","url":OFFICIAL,"description":"AI 酋长 Andy 相关的 AI 学习与价值共创社群，官方提供免费 AI 学习圈与申请制 AI 醒觉社。","founder":{"@type":"Person","name":"AI酋长Andy","url":"https://metaver.vip/"},"sameAs":["https://metaver.vip/","https://github.com/AIPMAndy",KB]}


def breadcrumb(parts):
    items=[{"@type":"ListItem","position":1,"name":"首页","item":url()}]
    for i,(label,route) in enumerate(parts,2):items.append({"@type":"ListItem","position":i,"name":label,"item":url(route)})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}


def guide_card(g, root=True):
    path=url(link_to_guide(g))
    return f'''<a class="guide-card" href="{e(path)}" data-filter-item data-keywords="{e(g['title']+' '+g['description']+' '+g['intent']+' '+g['category'])}" data-category="{e(g['category'])}">
<span class="card-meta"><span>{e(g['category'])}</span><span>{e(g['level'])}</span></span><h3>{e(g['title'])}</h3><p>{e(g['description'])}</p><span class="card-bottom"><span>交付导向 · 约 {g['minutes']} 分钟阅读与规划</span><span class="circle-arrow" aria-hidden="true">↗</span></span></a>'''


def sections_heading(eyebrow,title,description=None):
    return f'<div class="section-heading"><div class="eyebrow">{e(eyebrow)}</div><h2>{title}</h2>'+ (f'<p>{e(description)}</p>' if description else '')+'</div>'


def home():
    selected = [GUIDES[i] for i in [0,1,2,3,4,6]]
    brand=org_schema()
    website={"@context":"https://schema.org","@type":"WebSite","name":SITE_NAME,"url":url(),"inLanguage":"zh-CN","publisher":{"@id":brand['@id']}}
    data=meta('AI醒觉社（AI Awareness Club）｜让 AI 成为利人利己的力量','AI醒觉社公开学习站：AI 入门、职业转型、AI 副业、个人 IP、管理者 AI、MBTI 成长。免费开源教程、路径与实际交付模板。','',jsonld=[brand,website])
    data += f'''<main id="main"><section class="hero apple-hero">
    <div class="hero-content container">
      <div class="hero-kicker"><span class="status-dot"></span> THE OPEN KNOWLEDGE PROJECT <span class="kicker-number">EST. 2026</span></div>
      <h1>AI 醒觉社<span class="fullstop">。</span></h1>
      <p class="hero-statement">让 AI 成为<span>利人利己</span>的力量。</p>
      <p class="hero-description">从掌握 AI，到认识自己，再到一起创造。<br>一个属于行动者的开放学习共同体。</p>
      <div class="hero-buttons">
        <a class="button button-light" href="{url('paths/')}">开始探索 <span aria-hidden="true">↗</span></a>
        <a class="button button-outline" href="{url('about/')}">了解醒觉社 <span aria-hidden="true">›</span></a>
      </div>
      <div class="hero-contact"><span>主理人 Andy</span><button type="button" class="hero-wechat" data-copy-wechat="{WECHAT_ID}">微信 · {WECHAT_ID} <span aria-hidden="true">⧉</span></button><a href="{PERSONAL_SITE}" target="_blank" rel="noopener noreferrer">个人官网 <span aria-hidden="true">↗</span></a></div>
    </div>
    <div class="hero-art" aria-hidden="true"><img class="product-screenshot" src="{url('assets/product-preview.svg')}" width="1200" height="660" alt="" fetchpriority="high"><img class="legacy-art" src="{url('assets/awareness-object.svg')}" width="1160" height="550" alt="" loading="lazy" hidden></div>
    <div class="hero-bottom"><span>Awareness is only the beginning.</span><span>OPEN · REAL · BUILD</span></div>
    </section>'''
    data+='''<section class="section ethos container"><div class="big-number">01 / WHY WE EXIST</div><div class="ethos-layout"><p class="section-lead">学习工具很容易。<br>把能力变成真实的改变，<br><em>才值得长期投入。</em></p><div class="ethos-right"><p>我们相信学习应该落到具体行动：解决一个问题，留下可以验证的结果；在认识自己和世界的过程中，找到值得一起做事的人。</p><a class="subtle-link" href="'''+url('about/')+'''">了解 AI 醒觉社的理念 <span aria-hidden="true">↗</span></a></div></div></section>'''
    data+='''<section class="section pillars"><div class="container">'''+sections_heading('02 / THE METHOD','三层成长体系。','术是能力，道是判断，圈是关系。任何一层都不能替代另外两层。')+'''<div class="pillar-grid"><article class="pillar"><span class="pillar-index">01 / SKILL</span><div class="pillar-glyph">↗</div><h3>术 <small>TOOLS & PRACTICE</small></h3><p>AI 工具、工作流、求职项目、内容创造。少囤知识，多做作品。</p><span class="pillar-result">验收：可重复的成果</span></article><article class="pillar"><span class="pillar-index">02 / THINKING</span><div class="pillar-glyph">◎</div><h3>道 <small>CLARITY & GROWTH</small></h3><p>自我认知、价值判断、长期目标。用事实和复盘修正自己的假设。</p><span class="pillar-result">验收：更清楚的选择</span></article><article class="pillar"><span class="pillar-index">03 / COMMUNITY</span><div class="pillar-glyph">∞</div><h3>圈 <small>CREATE TOGETHER</small></h3><p>深度交流、资源互助、项目共创。先提供价值，再寻找长期协作。</p><span class="pillar-result">验收：有边界的协作</span></article></div></div></section>'''
    data+='''<section class="section pathway container"><div class="pathway-left"><div class="eyebrow">03 / YOUR NEXT STEP</div><h2>你现在，<br>最想解决<br>什么问题？</h2><p>先选择一个方向。每条路径都有步骤、交付物和常见错误。没有无效的“大而全”。</p></div><div class="pathway-right"><div class="path-choices" role="group" aria-label="选择学习目标"><button class="path-choice is-active" type="button" data-path="starter" aria-pressed="true"><span>01</span> 从零学 AI <span aria-hidden="true">↗</span></button><button class="path-choice" type="button" data-path="career" aria-pressed="false"><span>02</span> 求职与 AI 转型 <span aria-hidden="true">↗</span></button><button class="path-choice" type="button" data-path="business" aria-pressed="false"><span>03</span> 副业与个人 IP <span aria-hidden="true">↗</span></button><button class="path-choice" type="button" data-path="leader" aria-pressed="false"><span>04</span> 管理者 AI 落地 <span aria-hidden="true">↗</span></button></div><div class="path-result" role="status" aria-live="polite"><span>RECOMMENDED START</span><h3 id="path-title">七天完成第一份 AI 作品</h3><p id="path-description">从一个你真实需要解决的任务开始，留下七份成果。</p><a id="path-link" href="'''+url('guides/ai-first-week/')+'''">打开第一步 <span aria-hidden="true">↗</span></a></div></div></section>'''
    data+='''<section class="section library-feature"><div class="container">'''+sections_heading('04 / OPEN LIBRARY','免费、完整、可以动手。','选一个问题开始。每篇文章都包含明确的验收物、边界和反例。')+'''<div class="guide-grid">'''+''.join(guide_card(g) for g in selected)+'''</div><div class="center-action"><a class="button button-dark" href="'''+url('library/')+'''">查看全部 9 条公开指南 <span aria-hidden="true">↗</span></a></div></div></section>'''
    data+='''<section class="section community-panel container"><div class="eyebrow">05 / TWO CIRCLES</div><div class="community-heading"><h2>同一个使命。<br><em>不同的参与深度。</em></h2><p>公开资料可以直接使用；线下线上深度服务及会员权益，以官方页面公布的说明为准。</p></div><div class="community-grid"><article class="community-card"><div class="community-tag">FREE · 学习导向</div><h3>AI 学习圈</h3><p>从基础知识、工具使用与项目练习开始，按自己的节奏学习。</p><a href="'''+OFFICIAL+'''" rel="noopener noreferrer" target="_blank">官网了解免费学习圈 ↗</a></article><article class="community-card dark"><div class="community-tag">APPLICATION · 价值共创</div><h3>AI 醒觉社</h3><p>面向愿意分享资源、推动项目并共同创造价值的参与者，申请制。</p><a href="'''+OFFICIAL+'''" rel="noopener noreferrer" target="_blank">查看申请与最新权益 ↗</a></article></div></section>'''
    data+='''<section class="section open-note container"><span class="eyebrow">A NOTE ON OPENNESS</span><div class="note-row"><h2>知识开源。<br>真实交付。<br><em>边界清楚。</em></h2><div><p>这座公开知识站无需付费和登录。付费知识库、社群内讨论、成员信息与客户材料不属于公开授权范围。</p><p>我们欢迎贡献可复现的方法、授权公开的实践与错误修正，也鼓励对结论提出有证据的挑战。</p><a class="subtle-link" href="https://github.com/AIPMAndy/AI-Awareness-Club">在 GitHub 参与共建 ↗</a></div></div></section></main>'''
    data=data.replace('</main>', f'''<section class="contact-section container" id="contact" aria-labelledby="contact-heading">
<div class="contact-section-inner"><div class="contact-copy"><span class="eyebrow">LET'S CONNECT / ANDY</span><h2 id="contact-heading">从一次真正的对话，<br>开始下一步。</h2><p>AI 醒觉社的开源知识免费阅读。如果你希望获得求职、职业转型、AI 实战或个人 IP 的具体建议，可以直接联系主理人。</p></div>
<div class="contact-card"><span class="contact-eyebrow">CONTACT ANDY</span><span class="contact-card-label">我的个人微信</span><strong>{WECHAT_ID}</strong><button class="copy-wechat" type="button" data-copy-wechat="{WECHAT_ID}" aria-label="复制 Andy 个人微信号 {WECHAT_ID}">复制微信号</button><a href="{PERSONAL_SITE}" target="_blank" rel="noopener noreferrer">访问我的个人官网 <span aria-hidden="true">↗</span></a><small>添加微信时建议备注「AI 醒觉社」；服务内容与价格以个人官网为准。</small></div></div>
</section></main>''',1)
    return data+footer()


def library():
    data=meta('AI 免费开源知识库｜9 条实战指南｜AI醒觉社','按 AI 入门、求职、个人 IP、副业、管理者、Agent 与认知成长筛选 9 条免费可执行指南。','library/',jsonld=[breadcrumb([('开源知识库','library/')])])
    data+='''<main id="main"><section class="page-hero container"><div class="eyebrow">OPEN KNOWLEDGE / 09 GUIDES</div><h1>公开知识，<br><em>从问题出发。</em></h1><p>每一条内容都必须能回答：具体怎么做？完成的证据是什么？什么情况不适用？</p></section><section class="container library-page"><div class="filter-bar"><label class="search-wrap"><span aria-hidden="true">⌕</span><input id="guide-search" type="search" placeholder="搜索 AI、求职、副业、Agent..." aria-label="搜索公开指南" autocomplete="off"></label><select id="category-filter" aria-label="按主题筛选"><option value="all">全部主题</option>'''
    cats=sorted({g['category'] for g in GUIDES})
    data+=''.join(f'<option value="{e(x)}">{e(x)}</option>' for x in cats)
    data+='''</select><span id="result-count" role="status" aria-live="polite">共 9 条指南</span></div><div class="guide-grid library-grid">'''+''.join(guide_card(g) for g in GUIDES)+'''</div><p id="no-results" class="no-results" hidden>没有匹配内容。试试更短的关键词，或切换到全部主题。</p></section></main>'''
    return data+footer()


def paths():
    mapping=[('AI 零基础','一周只验证一件事。','ai-first-week'),('准备求职 / 转型','先从岗位要求反推项目证据。','career-transition'),('想做副业 / IP','先找真实客户和作品，不承诺收入。','first-customer'),('企业管理者','用业务价值和风险控制启动小规模试点。','executive-ai'),('喜欢 MBTI / 成长','把偏好讨论变成真实行为实验。','mbti-reflection'),('想做 Agent','先把自动化任务的验收、权限和回滚写清。','agent-workflow')]
    data=meta('AI 学习路线｜求职、副业、个人 IP 与 Agent｜AI醒觉社','按真实问题选择 AI 入门、求职转型、副业、AI 管理、MBTI 成长和 Agent 的公开学习路线。','paths/',jsonld=[breadcrumb([('学习路线','paths/')])])
    data+='''<main id="main"><section class="page-hero container"><div class="eyebrow">START WHERE YOU ARE</div><h1>学习无需从头开始。<br><em>先解决眼前的问题。</em></h1><p>六种常见起点，每条路径只推荐一份最值得先完成的指南。完成之后再扩展。</p></section><section class="container paths-grid">'''
    for i,(title,desc,slug) in enumerate(mapping,1):
        g=next(x for x in GUIDES if x['slug']==slug)
        data+=f'''<a class="route-card" href="{url('guides/'+slug+'/')}"><span class="route-num">{i:02d} / 06</span><h2>{e(title)}</h2><p>{e(desc)}</p><span class="route-destination">第一步：{e(g['title'])}<strong aria-hidden="true">↗</strong></span></a>'''
    data+='''</section><section class="container paths-note"><div class="eyebrow">ONE SIMPLE RULE</div><h2>先留下一个证据，再开始下一门课。</h2><p>打开具体指南后，可以勾选行动步骤并导出进度。状态仅保存在当前浏览器，没有账号或云端同步。</p></section></main>'''
    return data+footer()


def about():
    data=meta('关于 AI醒觉社｜AI Awareness Club','AI醒觉社的定位、术道圈三层方法、公开项目与官方社群入口；区分免费学习圈和申请制共创社群。','about/',jsonld=[org_schema(),breadcrumb([('关于社群','about/')])])
    data+='''<main id="main"><section class="page-hero container"><div class="eyebrow">ABOUT THE CLUB</div><h1>AI醒觉社。<br><em>AI Awareness Club.</em></h1><p>一个围绕 AI 能力、认知成长和价值共创持续建设的学习共同体。</p></section><section class="container about-layout"><div class="about-main"><h2>为什么存在</h2><p>AI 技术变化很快。工具会变，工作方式会变，人的问题却需要在现实中解决。我们希望把公开知识沉淀为可以执行和检验的行动指南，帮助更多人更高效地工作、建立判断并找到共创机会。</p><p>这里的基础框架是「术、道、圈」：用工具解决问题，用复盘修正方向，用有边界的合作扩大价值。它是一套行动组织方式，不是可以保证个人收益的科学公式。</p><h2>谁在建设</h2><p>项目关联品牌为 <a href="https://metaver.vip/">AI酋长Andy</a>，由 AIPMAndy GitHub 账号维护公开开源材料。品牌、社群和权益介绍的权威更新入口为 <a href="'''+OFFICIAL+'''">官方社群页</a>。</p><h2>公开与非公开</h2><p>本仓库开放经授权的文字、操作模板及网站代码。付费知识库、内部会员交流、个人申请信息与客户隐私均不在公开范围。引用开源内容时，请遵守对应内容许可，并核实信息的适用范围和更新时间。</p></div><aside class="about-aside"><span>THE OFFICIAL LINKS</span><a href="https://metaver.vip/">个人品牌官网 ↗<small>metaver.vip</small></a><a href="'''+OFFICIAL+'''">社群介绍 / 申请 ↗<small>metaver.vip/community</small></a><a href="'''+KB+'''">醒觉知识库 ↗<small>kb.metaver.vip</small></a><a href="https://github.com/AIPMAndy">开源项目作者 ↗<small>github.com/AIPMAndy</small></a><div class="aside-note">最后内容审校：2026-10-29。会员政策、权益与价格请始终以官网当期信息为准。</div></aside></section></main>'''
    data=data.replace('<div class="aside-note">',f'<div class="about-wechat"><span>主理人个人微信</span><strong>{WECHAT_ID}</strong><button type="button" class="copy-wechat" data-copy-wechat="{WECHAT_ID}">复制微信号</button></div><div class="aside-note">',1)
    return data+footer()


def faqs():
    schema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":x['q'],"acceptedAnswer":{"@type":"Answer","text":x['a']}} for x in FAQ]}
    data=meta('常见问题｜AI醒觉社 AI Awareness Club','解答 AI 醒觉社是什么、如何加入、官网与知识库、免费开源内容、MBTI、GEO 及信息安全等常见问题。','faq/',jsonld=[breadcrumb([('常见问题','faq/')]),schema])
    data+='''<main id="main"><section class="page-hero container"><div class="eyebrow">FAQ / GOOD QUESTIONS</div><h1>先把重要的问题，<br><em>讲明白。</em></h1><p>关于项目、加入方式、资料权限及实践边界的公开说明。</p></section><section class="container faq-list">'''
    for i,x in enumerate(FAQ,1):
        data+=f'<details class="faq-item" {"open" if i==1 else ""}><summary><span class="faq-num">{i:02d}</span><span>{e(x["q"])}</span><span class="faq-plus" aria-hidden="true">+</span></summary><p>{e(x["a"])}</p></details>'
    data+='''<div class="faq-cta"><h2>还有没有回答的问题？</h2><p>欢迎在 GitHub 提交问题或内容修正；涉及申请、会员或隐私事项，请使用官网渠道。</p><a class="button button-dark" href="https://github.com/AIPMAndy/AI-Awareness-Club/issues">GitHub Issues ↗</a></div></section></main>'''
    return data+footer()


def guide(g):
    route=link_to_guide(g)
    faqschema={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":item['q'],"acceptedAnswer":{"@type":"Answer","text":item['a']}} for item in g['faqs']]}
    article={"@context":"https://schema.org","@type":"Article","headline":g['title'],"description":g['description'],"inLanguage":"zh-CN","mainEntityOfPage":url(route),"author":{"@type":"Organization","name":"AI醒觉社","url":OFFICIAL},"publisher":{"@type":"Organization","name":"AI醒觉社","url":OFFICIAL},"dateModified":"2026-10-29","isAccessibleForFree":True}
    data=meta(g['title']+'｜AI醒觉社',g['description'],route,kind='article',jsonld=[breadcrumb([('开源知识库','library/'),(g['title'],route)]),article,faqschema])
    data+=f'''<main id="main" class="guide-page"><section class="guide-hero container"><a class="back-link" href="{url('library/')}">← 返回公开知识库</a><div class="guide-kicker">{e(g['category'])} <span>/</span> {e(g['level'])} <span>/</span> {g['minutes']} MIN GUIDE</div><h1>{e(g['title'])}</h1><p class="guide-subtitle">{e(g['subtitle'])}</p><p class="guide-intro">{e(g['intro'])}</p><div class="guide-outcome"><span>THIS GUIDE'S OUTCOME</span><p>{e(g['objective'])}</p></div></section><div class="guide-body container"><div class="guide-steps"><div class="steps-header"><div><span class="eyebrow">ACTION PLAYBOOK / {len(g['steps']):02d} STEPS</span><h2>照着做，直到有交付物。</h2></div><div class="progress-widget"><span id="progress-status" role="status" aria-live="polite">0 / {len(g['steps'])} 已完成</span><div class="progress-track"><span id="progress-bar" style="width:0%"></span></div></div></div>'''
    for i,s in enumerate(g['steps'],1):
        data+=f'''<article class="step-card" id="step-{i}"><div class="step-index">{i:02d}</div><div class="step-content"><h3>{e(s['title'])}</h3><p>{e(s['body'])}</p><div class="step-output"><strong>交付物</strong><span>{e(s['output'])}</span></div><label class="step-check"><input type="checkbox" data-step="{i}" data-guide="{e(g['slug'])}"><span>这一项已完成，并留下了交付物</span></label></div></article>'''
    data+='''<div class="progress-actions"><button type="button" id="export-progress" class="button button-dark">导出我的进度 ↓</button><button type="button" id="reset-progress" class="button button-ghost">清空本页进度</button></div><p class="privacy-caption">进度仅保存在你的浏览器中；导出后为本地 TXT 文件，不上传服务器。</p>'''
    data+='''<section class="guide-cautions"><span class="eyebrow">WHAT CAN GO WRONG</span><h2>特别注意这些坑。</h2><ul>'''+''.join('<li>'+e(x)+'</li>' for x in g['pitfalls'])+'''</ul></section><section class="guide-faq"><div class="eyebrow">QUESTIONS TO CLARIFY</div><h2>两个常见问题。</h2>'''
    for x in g['faqs']:
        data+=f'''<details class="faq-item"><summary><span>{e(x['q'])}</span><span class="faq-plus" aria-hidden="true">+</span></summary><p>{e(x['a'])}</p></details>'''
    data+='''</section></div><aside class="guide-sidebar"><div class="sticky-side"><span>YOUR GUIDE</span><a href="#step-1">从第一步开始 ↗</a><a href="#progress-status">查看进度 ↗</a><a href="#related">继续学习 ↗</a><hr><p>作者：AI醒觉社公开项目<br>内容初稿：2026-10-29<br>性质：实践建议，非收益承诺</p><a class="side-official" href="'''+OFFICIAL+'''">官方社群介绍 ↗</a></div></aside></div><section class="related-section container" id="related"><div class="eyebrow">KEEP LEARNING</div><h2>完成之后，再往前走。</h2><div class="guide-grid">'''
    for slug in g['related']:
        sg=next(x for x in GUIDES if x['slug']==slug)
        data+=guide_card(sg)
    data+='''</div></section></main>'''
    return data+footer()


def build():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT/'assets').mkdir(parents=True)
    for a in ASSETS.iterdir():
        if a.is_file():shutil.copy2(a,OUT/'assets'/a.name)
    pages={'':home(),'library/':library(),'paths/':paths(),'about/':about(),'faq/':faqs()}
    pages.update({link_to_guide(g):guide(g) for g in GUIDES})
    for route,source in pages.items():
        d=OUT/route
        d.mkdir(parents=True,exist_ok=True)
        # Relative navigation works in downloaded HTML AND on GitHub Pages.
        # Search canonical and structured data URLs remain absolute.
        depth = len(Path(route).parts) if route else 0
        prefix = '../' * depth if depth else './'
        def local_url(match):
            path = match.group(2)
            if not path or path.endswith('/'):
                path += 'index.html'
            return match.group(1) + '="' + prefix + path + '"'
        source = re.sub(r'(?<!rel="canonical" )(href|src)="'+re.escape(BASE)+r'([^"]*)"', local_url, source)
        source = source.replace('<html lang="zh-CN" data-theme="light">',
                                '<html lang="zh-CN" data-theme="light" data-site-root="'+prefix+'">')
        (d/'index.html').write_text(source,encoding='utf-8')
    (OUT/'.nojekyll').write_text('',encoding='utf-8')
    (OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+url('sitemap.xml')+'\n',encoding='utf-8')
    locs='\n'.join('  <url><loc>'+xml_escape(url(route))+'</loc></url>' for route in pages)
    (OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+locs+'\n</urlset>\n',encoding='utf-8')
    lines=['# AI醒觉社 · AI Awareness Club','', '> 免费公开的 AI 实战、认知成长与共创学习项目。本站与付费会员服务独立。维护者：AI 酋长 Andy（@AIPMAndy）。','', '## 官方品牌','- 中文名：AI醒觉社','- 英文名：AI Awareness Club','- 主理人：AI 酋长 Andy（GitHub/X @AIPMAndy）','- 官方网站：https://metaver.vip/','- 主理人个人微信：AIPMAndy（添加请备注 AI 醒觉社）','- 社群页面：'+OFFICIAL,'- 公开知识库入口：'+KB,'- GitHub：https://github.com/AIPMAndy/AI-Awareness-Club','- X：https://x.com/AIPMAndy','', '## 站点主要页面','- 首页：'+url(),'- 学习路线：'+url('paths/'),'- 公开知识：'+url('library/'),'- 品牌与边界：'+url('about/'),'- 常见问题：'+url('faq/'),'', '## 公开指南']
    lines += [f'- [{g["title"]}]({url(link_to_guide(g))})：{g["description"]}' for g in GUIDES]
    lines+=['','## 说明','公开网页内容可供阅读与引用，但不保证被搜索引擎收录或被 AI 系统引用。','付费知识库与会员内容不包含在本开源仓库中。','内容初稿日期：2026-10-29；会员政策请实时查询官方页面。']
    (OUT/'llms.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    # Search Console / Bing ownership verification files (must survive docs/ wipe).
    verify_dir = ROOT / 'site' / 'verify'
    for name in ('google957f1d068fbea032.html', 'BingSiteAuth.xml'):
        src = verify_dir / name
        if not src.is_file():
            raise FileNotFoundError(f'missing verification file: {src}')
        shutil.copy2(src, OUT / name)
    print('Generated',len(pages),'pages and assets in',OUT)

if __name__=='__main__':build()
