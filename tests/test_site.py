import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
BASE = 'https://aipmandy.github.io/AI-Awareness-Club/'

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]; self.titles=[]; self.meta={}; self.h1=0; self.html_lang=''; self.scripts=[]; self.in_json=False; self.in_title=False
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='html': self.html_lang=attrs.get('lang','')
        if tag=='h1': self.h1+=1
        if tag=='link' and attrs.get('rel')=='canonical': self.meta['canonical']=attrs.get('href')
        if tag=='meta' and (attrs.get('name') or attrs.get('property')): self.meta[attrs.get('name') or attrs.get('property')]=attrs.get('content','')
        if tag=='a': self.links.append(attrs.get('href',''))
        if tag=='script' and attrs.get('type')=='application/ld+json': self.in_json=True; self.scripts.append('')
        if tag=='title': self.in_title=True; self.titles.append('')
    def handle_endtag(self,tag):
        if tag=='script': self.in_json=False
        if tag=='title': self.in_title=False
    def handle_data(self,data):
        if self.in_json: self.scripts[-1]+=data
        if self.in_title: self.titles[-1]+=data

class ContentChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guides=json.loads((ROOT/'data/guides.json').read_text(encoding='utf-8'))
        cls.faq=json.loads((ROOT/'data/faq.json').read_text(encoding='utf-8'))
        cls.pages=sorted(DOCS.rglob('index.html'))
        cls.parsed={}
        for p in cls.pages:
            parser=PageParser(); parser.feed(p.read_text(encoding='utf-8')); cls.parsed[p]=parser
    def test_guides_are_nine_and_unique(self):
        self.assertEqual(len(self.guides),9)
        slugs=[g['slug'] for g in self.guides]
        self.assertEqual(len(set(slugs)),len(slugs))
        for g in self.guides:
            self.assertRegex(g['slug'],r'^[a-z0-9-]+$')
            self.assertGreaterEqual(len(g['steps']),3)
            self.assertGreaterEqual(len(g['pitfalls']),2)
            self.assertGreaterEqual(len(g['faqs']),2)
            for step in g['steps']:
                self.assertTrue(all(step.get(k) for k in ('title','body','output')))
            for related in g['related']:
                self.assertIn(related,slugs)
    def test_total_pages_and_basic_seo(self):
        self.assertEqual(len(self.pages),14)
        titles=[]; canonicals=[]
        for page, p in self.parsed.items():
            self.assertEqual(p.html_lang,'zh-CN',str(page))
            self.assertEqual(p.h1,1,str(page))
            self.assertEqual(len(p.titles),1,str(page))
            self.assertGreater(len(p.titles[0]),12,str(page))
            self.assertGreater(len(p.meta.get('description','')),30,str(page))
            self.assertIn('og:image',p.meta)
            self.assertEqual(p.meta.get('robots',''), 'index,follow,max-image-preview:large')
            route=page.parent.relative_to(DOCS).as_posix()
            expected=BASE+(route+'/' if route!='.' else '')
            self.assertEqual(p.meta.get('canonical'),expected)
            titles+=p.titles; canonicals.append(expected)
            for source in p.scripts: json.loads(source)
        self.assertEqual(len(titles),len(set(titles)))
        self.assertEqual(len(canonicals),len(set(canonicals)))
    def test_all_internal_links_resolve(self):
        failures=[]
        for page, p in self.parsed.items():
            for href in p.links:
                self.assertNotIn('javascript:',href.lower())
                if href.startswith('https://') or href.startswith('http://') or href.startswith('#'): continue
                decoded=unquote(href.split('#')[0].split('?')[0])
                target=(page.parent/decoded).resolve()
                if not target.is_file(): failures.append((str(page),href))
        self.assertEqual(failures,[])
    def test_sitemap_matches_all_pages(self):
        root=ET.fromstring((DOCS/'sitemap.xml').read_bytes())
        found={e.text for e in root.findall('.//{*}loc')}
        expected={p.meta['canonical'] for p in self.parsed.values()}
        self.assertEqual(found,expected)
    def test_structured_data_represents_visible_content(self):
        faqpage=DOCS/'faq/index.html'
        jsonlds=[json.loads(s) for s in self.parsed[faqpage].scripts]
        faq_schema=next(x for x in jsonlds if x['@type']=='FAQPage')
        self.assertEqual(len(faq_schema['mainEntity']),len(self.faq))
        for x in faq_schema['mainEntity']:
            self.assertIn(x['name'],[y['q'] for y in self.faq])
            self.assertIn(x['acceptedAnswer']['text'],[y['a'] for y in self.faq])
    def test_docs_have_no_runtime_external_scripts_or_fonts(self):
        css=(DOCS/'assets/style.css').read_text(encoding='utf-8')
        js=(DOCS/'assets/app.js').read_text(encoding='utf-8')
        self.assertNotIn('@import',css)
        self.assertNotIn('fetch(',js)
        self.assertNotIn('XMLHttpRequest',js)
        for page in self.pages:
            source=page.read_text(encoding='utf-8')
            self.assertNotIn('<script src="https://www.',source)
            self.assertNotIn('google-analytics',source.lower())
            self.assertNotIn('href="#"',source)
    def test_brand_consistency(self):
        texts=[(ROOT/'README.md').read_text(encoding='utf-8'),(DOCS/'index.html').read_text(encoding='utf-8'),(DOCS/'about/index.html').read_text(encoding='utf-8'),(DOCS/'llms.txt').read_text(encoding='utf-8')]
        for text in texts:
            self.assertIn('AI Awareness Club',text)
            self.assertIn('AI醒觉社',text)
        self.assertNotIn('AI Awake Group','\n'.join(texts))
    def test_apple_inspired_design_is_original_and_present(self):
        source=(ROOT/'site/assets/apple.css').read_text(encoding='utf-8')
        built=(DOCS/'assets/apple.css').read_text(encoding='utf-8')
        self.assertEqual(source,built)
        self.assertIn('#0071e3',source.lower())
        self.assertIn('prefers-reduced-motion',source)
        self.assertEqual((ROOT/'site/assets/awareness-object.svg').read_bytes(),
                         (DOCS/'assets/awareness-object.svg').read_bytes())
        homepage=(DOCS/'index.html').read_text(encoding='utf-8')
        self.assertIn('apple.css',homepage)
        self.assertIn('awareness-object.svg',homepage)
        self.assertIn('让 AI 成为',homepage)
        self.assertIn('开始探索',homepage)
        self.assertIn('了解醒觉社',homepage)
        self.assertNotIn('apple.com',homepage.lower())

    def test_all_guides_accessible_from_library(self):
        library=(DOCS/'library/index.html').read_text(encoding='utf-8')
        for g in self.guides:
            self.assertIn('guides/'+g['slug']+'/',library)
            self.assertTrue((DOCS/'guides'/g['slug']/'index.html').is_file())

    def test_andy_contact_visible_and_functional(self):
        homepage=(DOCS/'index.html').read_text(encoding='utf-8')
        about=(DOCS/'about/index.html').read_text(encoding='utf-8')
        readme=(ROOT/'README.md').read_text(encoding='utf-8')
        js=(DOCS/'assets/app.js').read_text(encoding='utf-8')
        for page in self.pages:
            text=page.read_text(encoding='utf-8')
            self.assertIn('个人微信',text,str(page))
            self.assertIn('AIPMAndy',text,str(page))
            self.assertIn('https://metaver.vip/',text,str(page))
            self.assertIn('data-copy-wechat=',text,str(page))
        self.assertIn('id="contact"',homepage)
        self.assertIn('主理人个人微信',about)
        self.assertIn('个人微信',readme)
        self.assertIn('navigator.clipboard',js)

if __name__=='__main__': unittest.main()
