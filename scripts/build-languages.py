"""Generate static German pages from English pages and reviewed translations.
Run: python3 scripts/build-languages.py. No dependencies required.
"""
from pathlib import Path
from html import escape, unescape
import json, re
from urllib.parse import urlsplit, parse_qs, urlencode
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://www.mujobs.de'
translations = json.loads((ROOT/'locales/de.json').read_text())
pages = sorted(p for p in ROOT.glob('*.html') if p.name != 'concept.html')

def route(name,lang):
    return ('/de/' if lang=='de' else '/') + ('' if name=='index.html' else name)

def strip_generated(s):
    return re.sub(r'<!-- bilingual:start -->.*?<!-- bilingual:end -->', '', s, flags=re.S)

def translate(s):
    parts = re.split(r'(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>|<[^>]+>)',s,flags=re.S)
    for i,part in enumerate(parts):
        if part.startswith(('<script','<style')):
            parts[i]=re.sub(r'src="(?!/|https?:)([^"]+)"', lambda m: 'src="../'+m.group(1)+'"', part)
            continue
        if part.startswith('<'):
            def attr(m):
                key,value=m.group(1),unescape(m.group(2))
                if value not in translations: raise ValueError('Missing attribute translation: '+value)
                return key+'="'+escape(translations[value],quote=True)+'"'
            part=re.sub(r'(alt|aria-label|placeholder)="([^"]+)"',attr,part)
            if part.startswith('<meta') and 'name="description"' in part:
                part=re.sub(r'content="([^"]+)"',lambda m:'content="'+escape(translations[unescape(m.group(1))],quote=True)+'"',part)
            part=part.replace('lang="en"','lang="de"')
            def resource(m):
                a,v=m.groups()
                if a=='src' or (a=='href' and v.endswith('.css')):
                    if not v.startswith(('/','https:','http:','data:')):v='../'+v
                if a=='href' and v.startswith('mailto:') and '?' in v:
                    v=v.split('?')[0]+'?'+urlencode({'subject':'Personalsuche mit mujobs'})
                return a+'="'+v+'"'
            part=re.sub(r'(href|src)="([^"]+)"',resource,part)
        elif part.strip():
            key=unescape(part.strip())
            if key not in translations:raise ValueError('Missing translation: '+key)
            part=part[:len(part)-len(part.lstrip())]+escape(translations[key],quote=False)+part[len(part.rstrip()):]
        parts[i]=part
    return ''.join(parts)

def enhance(s,name,lang):
    en,de=route(name,'en'),route(name,'de')
    meta=f'<link rel="canonical" href="{BASE}{route(name,lang)}"><link rel="alternate" hreflang="en" href="{BASE}{en}"><link rel="alternate" hreflang="de" href="{BASE}{de}"><link rel="alternate" hreflang="x-default" href="{BASE}{en}"><link rel="stylesheet" href="/languages.css"><script src="/languages.js" defer></script>'
    s=s.replace('</head>','<!-- bilingual:start -->'+meta+'<!-- bilingual:end --></head>')
    label='Sprache wählen' if lang=='de' else 'Choose language'
    switch=f'<div class="language-switch" role="group" aria-label="{label}">'
    for code,url,title in [('en',en,'English'),('de',de,'Deutsch')]:
        current=' aria-current="page"' if lang==code else ''
        switch+=f'<a href="{url}" lang="{code}" hreflang="{code}" aria-label="{title}"{current}>{code.upper()}</a>'
    switch+='</div>'
    # Both current homepage and shared inner-page shells are supported.
    marker='<a class="contact-link"' if name=='index.html' else '<a class="mj-contact"'
    assert marker in s,name
    return s.replace(marker,'<!-- bilingual:start -->'+switch+'<!-- bilingual:end -->'+marker,1)

outputs={}
for page in pages:
    source=strip_generated(page.read_text())
    outputs[page]=enhance(source,page.name,'en')
    outputs[ROOT/'de'/page.name]=enhance(translate(source),page.name,'de')
# Write only once all translation coverage has passed.
for path,s in outputs.items():
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(s)
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml')
sitemap=ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
for page in pages:
    for lang in ['en','de']:
        node=ET.SubElement(sitemap,'url')
        ET.SubElement(node,'loc').text=BASE+route(page.name,lang)
        for alt in ['en','de','x-default']:
            ET.SubElement(node,'{http://www.w3.org/1999/xhtml}link',{'rel':'alternate','hreflang':alt,'href':BASE+route(page.name,'en' if alt=='x-default' else alt)})
ET.ElementTree(sitemap).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
print(f'Generated {len(pages)} English/German page pairs and sitemap.xml')
