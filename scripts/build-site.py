"""Build MuJobs' bilingual static website. Run python3 scripts/build-site.py."""
from pathlib import Path
from html import escape as esc
from urllib.parse import quote
import json,sys,math,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'content'))
from editorial import MARKETS,ARTICLE_SECTIONS,CASE_DETAIL,P
cases=json.loads((ROOT/'content/cases.json').read_text()); articles=json.loads((ROOT/'content/articles.json').read_text())
dated_articles=json.loads((ROOT/'content/dated-articles.json').read_text()) if (ROOT/'content/dated-articles.json').exists() else []
BASE='https://www.mujobs.de'; LANG='en'; built=[]
def t(pair):return pair[0 if LANG=='en' else 1]
def e(x):return esc(str(x),quote=True)
def tx(en,de):return e(t(P(en,de)))
def url(file='index.html',lang=None):
    language=lang or LANG
    filename,separator,fragment=file.partition('#')
    if filename=='index.html':
        route='/de/' if language=='de' else '/en/'
    else:
        slug=filename.removesuffix('.html')
        german_slugs={'work':'projekte','insights':'einblicke','real-estate':'immobilien','technology':'technologie','creative-marketing':'marketing-kreation','sales':'vertrieb','finance':'finanzen','executive-support':'operations-personal','pharma-healthcare':'pharma-gesundheit'}
        route=('/de/'+german_slugs.get(slug,slug)) if language=='de' else '/'+slug
    return route+('#'+fragment if separator else '')

def a(file,label,cls=''):return f'<a class="{cls}" href="{url(file)}">{e(label)}</a>'
def p(s):return '<p>'+e(s)+'</p>'
def bullets(items):return '<ul class="check-list">'+''.join('<li>'+e(x)+'</li>' for x in items)+'</ul>'
def brand():return a('index.html','mujobs','wordmark')+'<span class="brand-dot" aria-hidden="true">.</span>'
def nav():return a('work.html',t(P('Our work','Unsere Projekte')))+a('index.html#markets',t(P('Industries & specialisms','Branchen & Fachbereiche')))+a('insights.html',t(P('Insights','Einblicke')))+a('index.html#method',t(P('Our approach','Unser Ansatz')))
def cta():return f'<section class="closing wrap" id="contact"><div><span class="eyebrow">{tx("LET’S DISCUSS YOUR HIRING NEEDS","LASSEN SIE UNS IHREN PERSONALBEDARF BESPRECHEN")}</span><h2>{tx("Specialist recruitment. A clear next step.","Ihre offene Position. Unser gezielter Recruiting-Ansatz.")}</h2><p>{tx("Tell us about the position, the responsibilities and the experience you need. We will agree a recruitment brief and define the next steps with you.","Beschreiben Sie uns die Position, die Aufgaben und die erforderliche Erfahrung. Gemeinsam entwickeln wir ein klares Anforderungsprofil und stimmen die nächsten Schritte ab.")}</p></div><a class="button light" href="mailto:mujtaba@mujobs.de">{tx("Discuss your vacancy","Eine Position besprechen")}</a></section>'
def footer():
    body='<footer class="site-footer"><div class="wrap"><div class="footer-grid"><div class="footer-intro"><div class="brand">'+brand()+'</div><h2>'+tx('Specialist recruitment. Informed decisions.','Spezialisierte Personalberatung. Fundierte Entscheidungen.')+'</h2><p>'+tx('Independent recruitment and active sourcing for specialist and leadership roles in Germany and Switzerland.','Unabhängige Personalberatung und Active Sourcing für Fach- und Führungspositionen in Deutschland und der Schweiz.')+'</p><a class="text-link" href="mailto:mujtaba@mujobs.de">mujtaba@mujobs.de</a></div><nav aria-label="'+tx('Explore MuJobs','MuJobs entdecken')+'"><span class="eyebrow">'+tx('EXPLORE','ENTDECKEN')+'</span>'+nav()+'</nav><nav aria-label="'+tx('Recruitment specialisms','Recruiting-Fachbereiche')+'"><span class="eyebrow">'+tx('INDUSTRIES & ROLES','BRANCHEN & FACHBEREICHE')+'</span>'+''.join(a(m['slug']+'.html',t(m['name'])) for m in MARKETS)+'</nav></div><div class="footer-base"><span>© 2026 MuJobs</span><span>'+tx('Based in Berlin · Recruiting across Germany and Switzerland','Mit Sitz in Berlin · Personalsuche in Deutschland und der Schweiz')+'</span></div></div></footer>'
    return body

def page(file,title,description,body,kind='website',schema=None):
    description=description.strip()
    if len(description)>175:description=description[:172].rsplit(' ',1)[0]+'…'
    canonical=BASE+url(file)
    switch='<div class="language-switch" role="group" aria-label="'+tx('Choose language','Sprache wählen')+'">'+''.join(f'<a href="{url(file,l)}" lang="{l}" hreflang="{l}" aria-label="{label}"'+(' aria-current="page"' if l==LANG else '')+'>'+l.upper()+'</a>' for l,label in [('en','English'),('de','Deutsch')])+'</div>'
    alternates=''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE+url(file,"de" if l=="x-default" else l)}">' for l in ['en','de','x-default'])
    data=schema or {'@context':'https://schema.org','@type':'WebPage','name':title,'description':description,'url':canonical,'inLanguage':LANG}
    is_blog=file=='insights.html' or file.startswith('insight-')
    blog_style='<link rel="stylesheet" href="/insights-design.css"><script src="/insights-design.js" defer></script>' if is_blog else ''
    html=f'''<!doctype html><html lang="{LANG}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" type="image/png" sizes="192x192" href="/favicon.png"><link rel="icon" type="image/x-icon" sizes="16x16 32x32 48x48 64x64" href="/favicon.ico"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"><title>{e(title)}</title><meta name="description" content="{e(description)}"><link rel="canonical" href="{canonical}">{alternates}<meta property="og:type" content="{kind}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="MuJobs"><meta property="og:locale" content="{'de_DE' if LANG=='de' else 'en_GB'}"><meta property="og:image" content="{BASE}/preview-assets/architecture.jpg"><meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/editorial.css"><script src="/site.js" defer></script>{blog_style}<script type="application/ld+json">{json.dumps(data,ensure_ascii=False).replace('<','\\u003c')}</script></head><body class="{'journal-page' if is_blog else ''}"><a class="skip" href="#main">{tx('Skip to content','Zum Inhalt springen')}</a><header class="header"><div class="wrap nav-row"><div class="brand">{brand()}</div><nav class="desktop" aria-label="{tx('Main navigation','Hauptnavigation')}">{nav()}</nav>{switch}<a class="contact-link" href="mailto:mujtaba@mujobs.de">{tx('Let’s talk','Kontakt')}</a><details class="menu"><summary>{tx('Menu','Menü')}</summary><nav aria-label="{tx('Mobile navigation','Mobile Navigation')}">{nav()}<a href="mailto:mujtaba@mujobs.de">{tx('Contact','Kontakt')}</a></nav></details></div></header><main id="main">{body}</main>{footer()}</body></html>'''
    path=ROOT/('de' if LANG=='de' else ('en' if file=='index.html' else ''))/file;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(html+'\n');built.append((file,LANG))
def hero(kicker,title,intro,back=None):return '<section class="wrap page-hero">'+(f'<div class="breadcrumb">{a(back[0],back[1])}<span>/</span><span>{e(kicker)}</span></div>' if back else f'<span class="eyebrow">{e(kicker)}</span>')+f'<h1>{e(title)}</h1><p class="lead">{e(intro)}</p></section>'
def sector_for(c):return CASE_DETAIL[c['file'][11:-5]][0]
def sector(slug):return next(m for m in MARKETS if m['slug']==slug)
def card(c):
    d=c['locales'][LANG]; cat=sector_for(c);slug=c['file'][11:-5]
    status=t(P('Completed hire','Erfolgreiche Besetzung'))
    return f'<article class="work-card" data-sector="{cat}"><div class="card-meta"><span>{e(t(sector(cat)["name"]))}</span><span>{e(status)}</span></div><h3>{a(c["file"],d["title"])}</h3><p>{e(d["intro"])}</p><div class="card-bottom"><span>{e(d["metrics"][0][0])} {e(d["metrics"][0][1])}</span>{a(c["file"],t(P('View the case study','Projekt ansehen')),'text-link')}</div></article>'
def work_cards(tags=None):
    selected=cases if tags is None else [next(c for c in cases if c['file']=='case-study-'+tag+'.html') for tag in tags]
    return '<div class="work-grid">'+''.join(card(c) for c in selected)+'</div>'
def related_article(slug):
    ar=next(x for x in articles if x['slug']==slug);d=ar['locales'][LANG]
    return f'<aside class="related"><span class="eyebrow">{tx("READ NEXT","WEITERLESEN")}</span><h3>{a("insight-"+slug+".html",d["title"])}</h3><p>{e(d["intro"])}</p></aside>'
def insight_card(ar,i):
    d=ar['locales'][LANG]
    return f'<article class="insight-card"><span class="article-number">{i+1:02d}</span><div><span class="eyebrow">{e(t(P(["PASSIVE TALENT","ACTIVE SOURCING","REAL ESTATE","TALENT PIPELINES","CANDIDATE ASSESSMENT","GERMANY & SWITZERLAND"],["PASSIVE KANDIDATEN","ACTIVE SOURCING","IMMOBILIEN","KANDIDATENPIPELINES","EIGNUNGSPRÜFUNG","DEUTSCHLAND & SCHWEIZ"]))[i])}</span><h2>{a("insight-"+ar["slug"]+".html",d["title"])}</h2><p>{e(d["intro"])}</p>{a("insight-"+ar["slug"]+".html",t(P("Read article","Artikel lesen")),"text-link")}</div></article>'
def comparison():
    body='<section class="comparison wrap section" id="search-comparison"><div class="section-heading"><span class="eyebrow">'+tx('INBOUND VS. ACTIVE SOURCING','INBOUND VS. ACTIVE SOURCING')+'</span><h2>'+tx('Less screening. More relevant conversations.','Weniger Sichtungsaufwand. Qualifizierte Gespräche.')+'</h2><p>'+tx('Two recruitment projects. Two different routes to a successful hire.','Zwei Recruiting-Projekte. Zwei unterschiedliche Wege zur erfolgreichen Besetzung.')+'</p></div><div class="comparison-grid recruitment-funnels">'
    examples=[('traditional',P('INBOUND APPLICATIONS','EINGEHENDE BEWERBUNGEN'),P('A large funnel. Months of work.','Viele Bewerbungen. Monatelanger Aufwand.'),P('Frontend recruitment','Frontend-Recruiting'),[('1,071',P('applications received','eingegangene Bewerbungen')),('90',P('first conversations','Erstgespräche')),('13',P('technical interviews','technische Interviews')),('5',P('passed assessment','fachlich geeignet')),('1',P('successful hire','erfolgreiche Besetzung'))],P('Months of recruitment work','Monatelanger Recruiting-Aufwand'),P(['High application volume means extensive CV screening.','Repeated screening and interview rounds take internal team time.','Reach depends on who is actively applying.'],['Viele Bewerbungen erfordern eine umfangreiche Sichtung von Lebensläufen.','Wiederholte Auswahl- und Interviewrunden binden interne Kapazitäten.','Die Reichweite hängt davon ab, wer sich aktiv bewirbt.'])),('focused',P('THE MUJOBS METHOD','DIE MUJOBS-METHODE'),P('A focused search. A faster decision.','Gezielte Suche. Schnellere Entscheidung.'),P('Head of Real Estate Marketing · Switzerland','Leiter Vermarktung · Schweiz'),[('30',P('relevant profiles sourced','passende Profile recherchiert')),('20',P('positive responses','positive Rückmeldungen')),('5',P('first calls','Erstgespräche')),('1',P('successful hire','erfolgreiche Besetzung'))],P('1.5 weeks to hire','1,5 Wochen bis zur Besetzung'),P(['Targeted research around the role and the business.','Personal outreach engages qualified candidates who are not actively applying.','Motivation and experience checked before the shortlist.','A smaller, relevant pool reduces the client’s screening workload.'],['Gezielte Recherche anhand von Stellenprofil und Unternehmensbedarf.','Persönliche Direktansprache erreicht qualifizierte Kandidaten, die nicht aktiv auf Stellensuche sind.','Motivation und Erfahrung werden vor der Vorauswahl geprüft.','Eine gezielte Vorauswahl reduziert den Aufwand für die Prüfung von Bewerbungsunterlagen.']))]
    for cls,kicker,head,context,metrics,timing,points in examples:
        body+='<article class="comparison-card '+cls+'"><span class="eyebrow">'+e(t(kicker))+'</span><h3>'+e(t(head))+'</h3><p class="funnel-context">'+e(t(context))+'</p><ol class="pipeline">'
        for i,(number,label) in enumerate(metrics):
            if LANG=='de':number=number.replace(',','.')
            body+='<li style="--stage:'+str(i)+'"><strong>'+number+'</strong><span>'+e(t(label))+'</span></li>'
        body+='</ol><p class="time-result">'+e(t(timing))+'</p>'+bullets(t(points))+'</article>'
    body+='</div><p class="comparison-note">'+tx('Figures from two separate projects with different roles and requirements. Results illustrate these searches; timing varies by assignment.','Zahlen aus zwei eigenständigen Projekten mit unterschiedlichen Positionen und Anforderungen. Die Ergebnisse beziehen sich auf diese Suchen; die Dauer variiert je Auftrag.')+'</p></section>'
    return body

def home():
    title=t(P('Recruitment & Active Sourcing in Germany and Switzerland | MuJobs','Personalberatung & Active Sourcing in Deutschland und der Schweiz | MuJobs'))
    intro=t(P('Specialist recruitment and active sourcing for real estate, technology, marketing and sales. We assess experience, present qualified candidates and support your hiring decisions.','Spezialisierte Personalberatung und Active Sourcing für Immobilien, IT, Marketing und Vertrieb. Wir prüfen relevante Erfahrung, stellen qualifizierte Kandidaten vor und begleiten Ihre Personalentscheidung.'))
    body=f'<section class="wrap home-hero"><div><span class="eyebrow">{tx("INDEPENDENT SEARCH · GERMANY & SWITZERLAND","UNABHÄNGIGE PERSONALSUCHE · DEUTSCHLAND & SCHWEIZ")}</span><h1>{tx("Specialist recruitment for", "Spezialisierte Personalberatung für")}<br><em>{tx("your next hire.","Ihre nächste Besetzung.")}</em></h1><p class="lead">{e(intro)}</p><div class="actions"><a class="button" href="mailto:mujtaba@mujobs.de">{tx("Discuss your next hire","Ihre nächste Besetzung besprechen")}</a>{a("work.html",t(P("Explore our work","Unsere Projekte entdecken")),"text-link")}</div></div><figure class="hero-image"><img src="/preview-assets/team.jpg" width="1279" height="1919" alt="{tx("People working together around a shared project","Menschen, die gemeinsam an einem Projekt arbeiten")}" fetchpriority="high"><div class="image-inset"><img src="/preview-assets/architecture.jpg" width="1400" height="933" alt="{tx("Commercial buildings representing the real estate sector","Gewerbeimmobilien als Motiv für die Immobilienbranche")}"></div><figcaption>{tx("RECRUITMENT WITH INDUSTRY EXPERTISE.","PERSONALBERATUNG MIT BRANCHENVERSTÄNDNIS.")}</figcaption></figure></section>'
    body+='<section id="why" class="wrap service-intro"><div class="section-heading"><span class="eyebrow">'+tx('WHAT WE DO','WAS WIR FÜR SIE TUN')+'</span><h2>'+tx('We recruit the specialists and leaders your business needs.','Wir rekrutieren Fach- und Führungskräfte für Ihr Unternehmen.')+'</h2><p>'+tx('MuJobs manages candidate research, direct outreach and interview coordination, from the initial brief to a qualified shortlist.','Von der ersten Recherche bis zur qualifizierten Vorauswahl übernimmt MuJobs die Kandidatensuche, die persönliche Ansprache und die Koordination des Auswahlprozesses.')+'</p></div><div class="service-deliverables">'
    for head,copy in [(P('Recruit qualified specialists','Geeignete Fachkräfte gezielt rekrutieren'),P('A targeted market map built around your position, sector and location.','Eine gezielte Marktübersicht für Ihre Position, Branche und Region.')),(P('Start relevant conversations','Relevante Gespräche führen'),P('Personal outreach, follow-ups and initial checks on experience and motivation.','Persönliche Ansprache, gezielte Rückfragen und eine erste Prüfung von Erfahrung und Motivation.')),(P('Bring the shortlist together','Eine fundierte Vorauswahl erstellen'),P('Clear candidate summaries and interview coordination, ready for your decision.','Aussagekräftige Kandidatenprofile und abgestimmte Interviews als Grundlage Ihrer Entscheidung.'))]:
        body+='<article><h3>'+e(t(head))+'</h3><p>'+e(t(copy))+'</p></article>'
    body+='</div></section>'
    body+=f'<section id="markets" class="wrap section"><div class="section-heading"><span class="eyebrow">{tx("INDUSTRIES & SPECIALISMS","BRANCHEN & FACHBEREICHE")}</span><h2>{tx("Recruitment expertise across your industry.","Personalberatung für Ihre Branche.")}</h2><p>{tx("Explore our recruitment expertise in real estate, technology, marketing, sales and other specialist fields, including the positions we fill and our approach to each assignment.","Erfahren Sie mehr über unsere Fachbereiche, die Positionen, die wir besetzen, und unseren jeweiligen Recruiting-Ansatz – von Immobilien und IT bis zu Marketing und Vertrieb.")}</p></div><div class="market-grid">'
    for i,m in enumerate(MARKETS):body+=f'<a class="market-card" href="{url(m["slug"]+".html")}"><span class="eyebrow">0{i+1}</span><h3>{e(t(m["name"]))}</h3><p>{e(t(m["kicker"]))}</p><span class="text-link">{tx("Explore the sector and roles","Branche und Positionen entdecken")}</span></a>'
    body+='</div></section>'
    body+=comparison()
    body+='<section id="method" class="method-section"><div class="wrap section"><div class="section-heading"><span class="eyebrow">'+tx('THE MUJOBS METHOD','DIE MUJOBS-METHODE')+'</span><h2>'+tx('A clear path to your next hire.','Ein klarer Weg zu Ihrer nächsten Besetzung.')+'</h2><p>'+tx('You retain control of the hiring decision. We coordinate each stage of the recruitment process, with clear responsibilities and documented results.','Sie behalten die Entscheidung in der Hand. Wir koordinieren die Suche – mit klaren Schritten und nachvollziehbaren Ergebnissen in jeder Phase.')+'</p></div><ol class="method-cards">'
    stages=[(P('Understand','Verstehen'),P('Define the role, responsibilities and must-have experience together.','Position, Aufgaben und erforderliche Erfahrung gemeinsam definieren.'),P('Your agreed search brief','Ihr abgestimmtes Suchprofil')),(P('Identify & engage','Identifizieren & direkt ansprechen'),P('Research the market and personally approach relevant candidates.','Den Markt recherchieren und passende Kandidaten persönlich ansprechen.'),P('A focused candidate pipeline','Eine gezielte Kandidatenpipeline')),(P('Qualify','Qualifizieren'),P('Explore experience, motivation and availability before introducing candidates.','Erfahrung, Motivation und Verfügbarkeit vor der Vorstellung prüfen.'),P('A shortlist with clear recommendations','Eine fundierte Vorauswahl')),(P('Move to a decision','Zur Entscheidung kommen'),P('Coordinate interviews, collect feedback and support the final steps.','Interviews koordinieren, Feedback einholen und die letzten Schritte begleiten.'),P('A coordinated hiring process','Ein abgestimmter Besetzungsprozess'))]
    for head,copy,result in stages:
        body+='<li><h3>'+e(t(head))+'</h3><p>'+e(t(copy))+'</p><div class="method-result"><span>'+tx('YOU RECEIVE','IHR ERGEBNIS')+'</span><strong>'+e(t(result))+'</strong></div></li>'
    body+='</ol></div></section>'
    body+=f'<section id="work" class="tinted"><div class="wrap section"><div class="section-heading"><span class="eyebrow">{tx("SELECTED WORK","AUSGEWÄHLTE PROJEKTE")}</span><h2>{tx("Selected work. Successful hires.","Ausgewählte Projekte. Erfolgreiche Besetzungen.")}</h2><p>{tx("Explore selected recruitment projects: the hiring requirements, our approach and the results achieved.","Erfahren Sie mehr über die Ausgangslage, unseren Suchansatz und das Ergebnis ausgewählter Projekte für Fach- und Führungspositionen.")}</p></div>'+work_cards(['leiter-vermarktung','project-developer','creative-director'])+f'<div class="section-footer"><p>{tx("Each assignment has specific requirements and circumstances.","Jedes Projekt hat eigene Anforderungen und Rahmenbedingungen.")}</p>{a("work.html",t(P("Browse all work","Alle Projekte ansehen")),"button outline")}</div></div></section>'
    body+=f'<section class="wrap section"><div class="section-heading"><span class="eyebrow">{tx("INSIGHTS","EINBLICKE")}</span><h2>{tx("Practical ideas for hard-to-fill roles.","Impulse für anspruchsvolle Besetzungen.")}</h2></div><div class="insight-list">'+''.join(insight_card(x,i) for i,x in enumerate(articles[:2]))+'</div><div class="section-footer">'+a('insights.html',t(P('Explore all insights','Alle Einblicke ansehen')),'button outline')+'</div></section>'+cta()
    page('index.html',title,intro,body)
def works():
    body=hero(t(P('OUR WORK','UNSERE PROJEKTE')),t(P('Recruitment projects and completed placements.','Recruiting-Projekte und erfolgreiche Besetzungen.')),t(P('Recruitment projects across real estate, technology, marketing, sales and pharmaceuticals. Review the requirements, our approach and the outcome of each assignment.','Erfolgreiche Besetzungen in Immobilien, IT, Marketing, Vertrieb und Pharma. Entdecken Sie Anforderungsprofil, Markt, Direktansprache und Ergebnis jedes Suchprojekts.')))
    body+='<section class="wrap section compact"><div class="filters" hidden aria-label="'+tx('Filter work by sector','Projekte nach Branche filtern')+'"><button type="button" data-filter="all" aria-pressed="true">'+tx('All work','Alle Projekte')+'</button>'
    for m in MARKETS:
        if any(sector_for(c)==m['slug'] for c in cases):body+=f'<button type="button" data-filter="{m["slug"]}" aria-pressed="false">{e(t(m["name"]))}</button>'
    body+='</div><p class="result-count" aria-live="polite"></p>'+work_cards()+'</section>'+cta()
    page('work.html',t(P('Recruitment Case Studies & Search Projects | MuJobs','Recruiting-Fallstudien & Suchprojekte | MuJobs')),t(P('Explore MuJobs recruitment projects in real estate, sales, technology, marketing and pharma. Hiring challenges, search approaches and outcomes.','MuJobs-Suchprojekte für Immobilien, Vertrieb, IT, Marketing und Pharma: Herausforderungen, Suchmethoden und Ergebnisse im Überblick.')),body)
def case_pages():
    for c in cases:
        d=c['locales'][LANG];slug=c['file'][11:-5];cat,heading,context,checks=CASE_DETAIL[slug];m=sector(cat)
        body=hero(d['label'],t(heading),d['intro'],('work.html',t(P('All work','Alle Projekte'))))
        body+='<section class="wrap case-summary"><span class="pill">'+e(d['signal'])+'</span><div class="metrics">'+''.join(f'<div><strong>{e(v)}</strong><span>{e(label)}</span></div>' for v,label in d['metrics'])+'</div><p class="caption">'+tx('Project-specific figures from the existing case record; outcomes for future assignments may differ.','Projektspezifische Angaben aus dem bestehenden Fallbericht; Ergebnisse künftiger Besetzungen können abweichen.')+'</p></section>'
        body+='<div class="wrap reading-layout"><aside class="contents"><span class="eyebrow">'+tx('ABOUT THIS ASSIGNMENT','ZU DIESEM PROJEKT')+'</span>'
        heads=[P('The hiring challenge','Die Herausforderung bei der Besetzung'),P('Our recruitment approach','Unser Recruiting-Ansatz'),P('The outcome','Das Ergebnis'),P('Understanding the position','Die Anforderungen der Position'),P('Planning your next recruitment assignment','Eine vergleichbare Position besetzen')]
        body+=''.join(f'<a href="#section-{i}">{i+1:02d} · {e(t(h))}</a>' for i,h in enumerate(heads))+'</aside><article class="reading">'
        for i,paras in enumerate(d['sections']):body+=f'<section id="section-{i}"><span class="eyebrow">0{i+1}</span><h2>{e(t(heads[i]))}</h2>'+''.join(p(x) for x in paras)+'</section>'
        body+='<section id="section-3"><span class="eyebrow">04</span><h2>'+e(t(heads[3]))+'</h2>'+p(t(context))+'<div class="callout"><h3>'+tx('Questions that make the brief more precise','Fragen für ein genaueres Anforderungsprofil')+'</h3>'+bullets(t(checks))+'</div></section>'
        body+='<section id="section-4"><span class="eyebrow">05</span><h2>'+e(t(heads[4]))+'</h2>'+p(t(P('Start with the work the new person will own, the business context and the constraints that cannot change. Separate essential experience from preferences. That gives the market mapping a clear direction and makes it easier to explain why someone belongs on the shortlist.','Beginnen Sie mit der künftigen Verantwortung, dem Unternehmenskontext und unveränderlichen Rahmenbedingungen. Trennen Sie notwendige Erfahrung von Präferenzen. So erhält die Marktanalyse eine klare Richtung und die Vorauswahl eine nachvollziehbare Begründung.')))+p(t(P('A similar title is only a research starting point. In an initial conversation, we would clarify the project or team, the practical conditions and the evidence you need to make a decision. The scope of sourcing, candidate qualification and interview coordination can then be agreed around the actual requirement.','Eine ähnliche Stellenbezeichnung ist lediglich ein Ausgangspunkt für die Recherche. Im Erstgespräch klären wir Projekt oder Team, praktische Bedingungen und die benötigten Nachweise für Ihre Entscheidung. Darauf aufbauend lässt sich der Umfang von Sourcing, Kandidatenprüfung und Interviewkoordination vereinbaren.')))+a(cat+'.html',t(m['title']),'text-link')+'</section>'+related_article(m['article'])+'</article></div>'
        others=[x for x in m['tags'] if x!=slug][:2]
        if others:body+='<section class="wrap section"><div class="section-heading"><span class="eyebrow">'+tx('RELATED WORK','ÄHNLICHE PROJEKTE')+'</span><h2>'+tx('Related recruitment projects.','Weitere Recruiting-Projekte.')+'</h2></div>'+work_cards(others)+'</section>'
        body+=cta();page(c['file'],t(heading)+' | MuJobs',d['intro'],body)
def market_pages():
    for m in MARKETS:
        body=hero(t(m['kicker']),t(m['title']),t(m['intro']),('index.html#markets',t(P('All industries & specialisms','Alle Branchen & Fachbereiche'))))
        roles_intro='<section id="roles"><span class="eyebrow">'+tx('ROLES AT A GLANCE','POSITIONEN IM ÜBERBLICK')+'</span><h2>'+tx('Positions we recruit for','Positionen, die wir besetzen')+'</h2><div class="role-list">'+''.join('<div>'+e(r)+'</div>' for r in t(m['roles']))+'</div></section>'
        body+='<div class="wrap sector-roles">'+roles_intro+'</div>'
        body+='<div class="wrap reading-layout"><aside class="contents"><span class="eyebrow">'+tx('IN THIS PRACTICE','IN DIESEM FACHBEREICH')+'</span>'+''.join(f'<a href="#{id}">{e(t(label))}</a>' for id,label in [('challenge',P('The hiring challenge','Die Herausforderung bei der Besetzung')),('roles',P('Positions we recruit for','Unsere Fachbereiche')),('assessment',P('What we assess','Was wir prüfen')),('approach',P('How we search','Wie wir suchen'))])+'</aside><article class="reading">'
        body+='<section id="challenge"><span class="eyebrow">01</span><h2>'+tx('Industry-specific recruitment challenges','Branchenspezifische Herausforderungen bei der Besetzung')+'</h2>'+p(t(m['problem']))+'</section>'

        body+='<section id="assessment"><span class="eyebrow">03</span><h2>'+tx('The evidence behind a relevant shortlist','Die Grundlage einer passenden Vorauswahl')+'</h2>'+p(t(P('We assess candidates against the responsibilities of the position. We agree the criteria with you for each assignment so that the shortlist reflects your specific requirements.','Wir bewerten Kandidaten anhand der Aufgaben und Verantwortlichkeiten der Position. Die Auswahlkriterien stimmen wir für jeden Auftrag mit Ihnen ab, damit die Vorauswahl Ihren konkreten Anforderungen entspricht.')))+bullets(t(m['evidence']))+'</section>'
        body+='<section id="approach"><span class="eyebrow">04</span><h2>'+tx('Map the market. Make the connection.','Den Markt verstehen. Die Verbindung herstellen.')+'</h2>'+p(t(m['map']))+'<div class="callout"><h3>'+tx('What the search can include','Was die Suche umfassen kann')+'</h3>'+bullets(t(P(['A focused briefing and role-specific market map.','Relevant profile research and personal candidate outreach.','Initial qualification, follow-ups and interview coordination.','A shortlist with clear reasoning and visible open questions.'],['Ein gezieltes Briefing und eine auf die Position abgestimmte Marktanalyse.','Recherche passender Profile und persönliche Kandidatenansprache.','Eine erste Eignungsprüfung, die weitere Kontaktpflege und die Koordination der Interviews.','Eine fundierte Vorauswahl mit transparenten offenen Fragen.'])))+'</div></section>'
        body+='<section><h2>'+tx('Define the recruitment brief','Das Anforderungsprofil gemeinsam definieren')+'</h2>'+p(t(P('Tell us about the position, location, team structure and the challenges you have faced in filling the vacancy. Together, we can distinguish what is essential from what is flexible and agree a search that fits the business.','Beschreiben Sie uns die Aufgaben der Position, den Standort, die Teamstruktur und die bisherigen Schwierigkeiten bei der Besetzung. Gemeinsam trennen wir unverzichtbare Anforderungen von flexiblen Punkten und vereinbaren eine Suche, die zum Unternehmen passt.')))+'</section>'+related_article(m['article'])+'</article></div>'
        if m['tags']:body+='<section class="wrap section"><div class="section-heading"><span class="eyebrow">'+tx('COMPLETED WORK IN THIS SECTOR','BESETZUNGEN IN DIESEM FACHBEREICH')+'</span><h2>'+tx('From the brief to the right person.','Vom Anforderungsprofil zur Besetzung.')+'</h2></div>'+work_cards(m['tags'])+'</section>'
        body+=cta();page(m['slug']+'.html',t(m['title']).rstrip('.')+' | MuJobs',t(m['intro']),body)
def journal_entries():
    entries=[]
    topics={'passive-candidate-sourcing':'sourcing','active-sourcing-vs-job-advertising':'sourcing','building-candidate-pipelines':'sourcing','evidence-led-candidate-shortlists':'assessment','recruitment-germany-switzerland':'sourcing'}
    for ar in sorted(dated_articles,key=lambda ar:ar['published'],reverse=True):
        d=ar['locales'][LANG]
        entries.append({'ar':ar,'data':d,'slug':ar['slug'],'dated':True,'topic':'real-estate','category':t(P('Real estate recruitment','Immobilien-Recruiting'))})
    for i,ar in enumerate(articles):
        d=ar['locales'][LANG];topic=topics.get(ar['slug'],'real-estate')
        entries.append({'ar':ar,'data':d,'slug':ar['slug'],'dated':False,'index':i,'topic':topic,'category':t(P('Candidate assessment','Kandidatenauswahl')) if topic=='assessment' else t(P('Active sourcing','Active Sourcing')) if topic=='sourcing' else t(P('Real estate recruitment','Immobilien-Recruiting'))})
    for en in entries:
        d=en['data'];paras=d['opening'][:]
        if en['dated']:
            for sec in d['sections']:paras+=sec.get('paragraphs',[])+sec.get('items',[])+sec.get('paragraphs_after',[])
        else:paras += [t(sec[1]) for sec in ARTICLE_SECTIONS[en['index']]]
        en['minutes']=max(3,math.ceil(len(' '.join(paras).split())/180))
        en['date']=en['ar'].get('published','')
    return entries

def journal_date(date):
    if not date:return t(P('Practical guide','Praxiswissen'))
    y,m,d=date.split('-')
    months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'] if LANG=='en' else ['Jan.','Feb.','März','Apr.','Mai','Juni','Juli','Aug.','Sept.','Okt.','Nov.','Dez.']
    return str(int(d))+('. ' if LANG=='de' else ' ')+months[int(m)-1]+' '+y

def journal_card(en,featured=False):
    d=en['data'];link=url('insight-'+en['slug']+'.html');date=journal_date(en['date']);mins=str(en['minutes'])+' '+t(P('min read','Min. Lesezeit'))
    cls='journal-feature' if featured else 'journal-card'
    out=f'<article class="{cls}" data-blog-item data-topic="{en["topic"]}">'
    if featured:
        out+='<div class="journal-feature-copy"><span class="journal-kicker">'+tx('LATEST ARTICLE','AKTUELLER ARTIKEL')+'</span>'
    out+='<div class="journal-meta"><span>'+e(en['category'])+'</span><span>'+e(date)+'</span></div><h2><a href="'+link+'">'+e(d['title'])+'</a></h2><p>'+e(d['intro'])+'</p><div class="journal-card-bottom"><span>'+e(mins)+'</span><a href="'+link+'" class="journal-read">'+tx('Read article','Artikel lesen')+' <span aria-hidden="true">↗</span></a></div>'
    if featured:out+='</div><a href="'+link+'" class="journal-feature-image" tabindex="-1" aria-hidden="true"><img src="/preview-assets/architecture.jpg" alt="" width="1400" height="933" fetchpriority="high"><span>'+tx('UNDERSTAND THE SECTOR. RECRUIT WITH PURPOSE.','DIE BRANCHE VERSTEHEN. GEZIELT REKRUTIEREN.')+'</span></a>'
    return out+'</article>'

def insight_pages():
    entries=journal_entries()
    body='<section class="wrap journal-intro"><div><span class="journal-kicker">'+tx('MUJOBS / INSIGHTS','MUJOBS / EINBLICKE')+'</span><h1>'+tx('Recruitment knowledge.','Recruiting-Wissen.')+'<br><em>'+tx('Better decisions.','Fundierte Entscheidungen.')+'</em></h1></div><p>'+tx('Practical perspectives on specialist recruitment, active sourcing and hiring in the real estate sector. Written for the people making the decisions.','Praxiswissen zu Personalberatung, Active Sourcing und Besetzungen in der Immobilienbranche. Für Unternehmen, die qualifiziertes Personal rekrutieren möchten.')+'</p></section>'
    body+='<section class="wrap journal-library" aria-label="'+tx('Articles and guides','Artikel und Leitfäden')+'"><div class="journal-tools"><div class="journal-filters" hidden aria-label="'+tx('Filter by topic','Nach Thema filtern')+'">'
    for key,label in [('all',P('All articles','Alle Artikel')),('real-estate',P('Real estate','Immobilien')),('sourcing',P('Active sourcing','Active Sourcing')),('assessment',P('Selection','Auswahl'))]:
        body+=f'<button type="button" data-blog-filter="{key}" aria-pressed="'+('true' if key=='all' else 'false')+'">'+e(t(label))+'</button>'
    body+='</div><label class="journal-search" hidden><span class="sr-only">'+tx('Search articles','Artikel durchsuchen')+'</span><span aria-hidden="true">⌕</span><input type="search" data-blog-search placeholder="'+tx('Search articles','Artikel durchsuchen')+'"></label></div>'
    body+=journal_card(entries[0],True)+'<div class="journal-grid-heading"><span class="journal-kicker">'+tx('THE JOURNAL','ALLE BEITRÄGE')+'</span><p data-blog-count aria-live="polite">'+str(len(entries))+' '+tx('articles','Artikel')+'</p></div><div class="journal-grid">'+''.join(journal_card(en) for en in entries[1:])+'</div><p class="journal-empty" hidden>'+tx('No matching articles. Try a different topic or search term.','Keine passenden Artikel. Wählen Sie ein anderes Thema oder einen anderen Suchbegriff.')+'</p></section>'
    body+='<section class="wrap journal-contact"><span class="journal-kicker">'+tx('FROM INSIGHT TO ACTION','VOM WISSEN ZUR BESETZUNG')+'</span><div><h2>'+tx('Let’s discuss your next hire.','Sprechen wir über Ihre nächste Besetzung.')+'</h2><a class="button" href="mailto:mujtaba@mujobs.de">'+tx('Discuss your vacancy','Personalbedarf besprechen')+' <span aria-hidden="true">↗</span></a></div></section>'
    page('insights.html',t(P('Recruitment Insights & Practical Guides | MuJobs','Recruiting-Wissen und Praxisleitfäden | MuJobs')),t(P('Practical recruitment guides on active sourcing, real estate hiring and candidate assessment for employers in Germany and Switzerland.','Praxisleitfäden zu Active Sourcing, Immobilien-Recruiting und Kandidatenauswahl für Arbeitgeber in Deutschland und der Schweiz.')),body)
    for en in entries:journal_article(en,entries)

def journal_article(en,entries):
    d=en['data'];ar=en['ar'];file='insight-'+en['slug']+'.html';mins=str(en['minutes'])+' '+t(P('min read','Min. Lesezeit'))
    if en['dated']:
        sections=[(sec['title'],''.join(p(x) for x in sec.get('paragraphs',[]))+bullets(sec.get('items',[]))+''.join(p(x) for x in sec.get('paragraphs_after',[]))) for sec in d['sections']]
    else:sections=[(t(head),p(t(para))) for head,para in ARTICLE_SECTIONS[en['index']]]
    body='<div class="wrap journal-back">'+a('insights.html',t(P('← All insights','← Alle Einblicke')))+'</div><header class="wrap journal-article-header"><div class="journal-meta"><span>'+e(en['category'])+'</span><span>'+e(journal_date(en['date']))+'</span><span>'+e(mins)+'</span></div><h1>'+e(d['title'])+'</h1><p class="journal-deck">'+e(d['intro'])+'</p><div class="journal-author"><span class="journal-avatar" aria-hidden="true">m.</span><div><strong>MuJobs</strong><span>'+tx('Specialist recruitment · Germany & Switzerland','Personalberatung · Deutschland & Schweiz')+'</span></div></div></header>'
    body+='<div class="wrap journal-article-layout"><aside class="journal-toc"><details open><summary>'+tx('In this article','In diesem Artikel')+'</summary><nav aria-label="'+tx('Article contents','Artikelinhalt')+'">'+''.join('<a href="#part-'+str(i)+'"><span>'+str(i+1).zfill(2)+'</span>'+e(re.sub(r'^\d+\.\s*','',head))+'</a>' for i,(head,content) in enumerate(sections))+'</nav></details><div class="journal-aside-note"><span class="journal-kicker">'+tx('YOUR NEXT HIRE','IHRE NÄCHSTE BESETZUNG')+'</span><p>'+tx('Recruitment starts with a clear brief.','Gutes Recruiting beginnt mit klaren Anforderungen.')+'</p><a href="mailto:mujtaba@mujobs.de">'+tx('Talk to MuJobs ↗','Mit MuJobs sprechen ↗')+'</a></div></aside><article class="journal-reading"><div class="journal-opening">'+''.join(p(x) for x in d['opening'])+'</div>'
    body+=''.join('<section id="part-'+str(i)+'"><h2>'+e(head)+'</h2>'+content+'</section>' for i,(head,content) in enumerate(sections))
    if en['dated']:
        body+='<section class="journal-sources"><h2>'+tx('Sources and context','Quellen und Kontext')+'</h2>'+p(d['source_note'])+''.join('<p><a href="'+e(x['url'])+'">'+e(x['label'])+' ↗</a></p>' for x in ar['sources'])+'</section>'
        title,copy,label=d['cta_title'],d['cta_text'],d['cta_label']
    else:title=t(P('Turn the guidance into a recruitment brief.','Nutzen Sie dieses Wissen für Ihre nächste Besetzung.'));copy=t(P('Tell us about your vacancy and the experience you need. We will help you define a clear brief and a focused recruitment approach.','Beschreiben Sie uns Ihre offene Position und die erforderliche Erfahrung. Gemeinsam entwickeln wir ein klares Anforderungsprofil und einen gezielten Recruiting-Ansatz.'));label=t(P('Discuss your vacancy','Personalbedarf besprechen'))
    body+='<aside class="journal-article-cta"><span class="journal-kicker">'+tx('TAKE THE NEXT STEP','DER NÄCHSTE SCHRITT')+'</span><h2>'+e(title)+'</h2>'+p(copy)+'<a class="button light" href="mailto:mujtaba@mujobs.de">'+e(label)+' ↗</a></aside></article></div>'
    related=[x for x in entries if x['slug']!=en['slug']];related.sort(key=lambda x:x['topic']!=en['topic'])
    body+='<section class="wrap journal-related"><div class="journal-grid-heading"><h2>'+tx('Continue reading','Weitere Einblicke')+'</h2>'+a('insights.html',t(P('All articles ↗','Alle Artikel ↗')),'text-link')+'</div><div class="journal-grid">'+''.join(journal_card(x) for x in related[:3])+'</div></section>'
    schema={'@context':'https://schema.org','@type':'Article','headline':d['title'],'description':d['intro'],'inLanguage':LANG,'author':{'@type':'Organization','name':'MuJobs','url':BASE},'publisher':{'@type':'Organization','name':'MuJobs'},'mainEntityOfPage':BASE+url(file)}
    if en['dated']:schema.update(datePublished=ar['published'],dateModified=ar['modified'])
    page(file,d['title'].rstrip('.')+' | MuJobs',d['intro'],body,'article',schema)

def dated_pages():pass

for LANG in ['en','de']:
    home();works();case_pages();market_pages();insight_pages();dated_pages()
ET.register_namespace('','http://www.sitemaps.org/schemas/sitemap/0.9');ET.register_namespace('xhtml','http://www.w3.org/1999/xhtml')
root=ET.Element('{http://www.sitemaps.org/schemas/sitemap/0.9}urlset')
for file,lang in built:
    node=ET.SubElement(root,'url');ET.SubElement(node,'loc').text=BASE+url(file,lang)
    modification_dates=[ar['modified'] for ar in dated_articles if file == 'insight-'+ar['slug']+'.html' or file == 'insights.html']
    if modification_dates: ET.SubElement(node,'lastmod').text=max(modification_dates)
    for alt in ['en','de','x-default']:ET.SubElement(node,'{http://www.w3.org/1999/xhtml}link',{'rel':'alternate','hreflang':alt,'href':BASE+url(file,'de' if alt=='x-default' else alt)})
ET.ElementTree(root).write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
# Explicit routes preserve static source files while exposing clean public URLs.
redirects=[{'source':'/','destination':'/de/','permanent':False},{'source':'/index.html','destination':'/en/','permanent':True}]
rewrites=[]
for file,lang in built:
    if file=='index.html':
        if lang=='de': redirects.append({'source':'/de/index.html','destination':'/de/','permanent':True})
        continue
    source=('/de/' if lang=='de' else '/')+file
    destination=url(file,lang)
    redirects.append({'source':source,'destination':destination,'permanent':True})
    rewrites.append({'source':destination,'destination':source})
(ROOT/'vercel.json').write_text(json.dumps({'redirects':redirects,'rewrites':rewrites},indent=2)+'\n')
print('Built',len(built),'pages in English and German')
