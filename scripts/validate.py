#!/usr/bin/env python3
"""Offline catalog, public-field, Markdown, and relative-link integrity checks."""
import csv, hashlib, json, re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
checks=0

def check(ok,message):
    global checks
    checks+=1
    if not ok:raise AssertionError(message)
def read(name):return json.loads((DATA/name).read_text())
def slug(s):return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def table_urls(path):return re.findall(r'^\| \[.*?\]\(<([^>]+)>\) \|',path.read_text(),re.M)
def anchors(path):
    text=path.read_text();result=set(re.findall(r'<a\s+(?:id|name)="([^"]+)"',text));counts=Counter()
    for h in re.findall(r'^#{1,6}\s+(.+)$',text,re.M):
        key=re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-')
        result.add(key+(f'-{counts[key]}' if counts[key] else ''));counts[key]+=1
    return result
rows=read('catalog.json');export=read('directories.json');coverage=read('coverage.json')
by_url={r['url']:r for r in rows}
fields={'id','name','url','category','pricing','domain_rating','link_type','curated_subset','snapshot_date'}
check(rows==export,'Canonical catalog / JSON mismatch')
check(len(rows)==len(by_url)==1018,'Expected 1,018 unique exact URLs')
check(len({r['id'] for r in rows})==1018,'Duplicate short IDs')
check(len({r['category'] for r in rows})==18,'Category count mismatch')
check(rows==sorted(rows,key=lambda r:(r['name'].casefold(),r['url'])),'Catalog not alphabetized')
check(Counter(r['pricing'] for r in rows)=={'Free':834,'Freemium':45,'Paid':139},'Pricing count mismatch')
check(Counter(r['link_type'] for r in rows)=={'Dofollow':595,'Nofollow':421,'Conditional':2},'Link type mismatch')
check(sum(r['curated_subset'] for r in rows)==864,'Indexed subset count mismatch')
check(hashlib.sha256((DATA/'catalog.json').read_bytes()).hexdigest()==coverage['catalog_sha256'],'Catalog hash mismatch')
for r in rows:
    check(set(r)==fields,'Unexpected field: public catalog must contain factual fields only')
    check(r['id']==hashlib.sha256(r['url'].encode()).hexdigest()[:16],'ID mismatch')
    u=urlsplit(r['url']);check(u.scheme in ('http','https') and bool(u.netloc),'Invalid URL syntax')
    check(type(r['domain_rating']) is int and 0<=r['domain_rating']<=100,'Invalid DR')
    check(type(r['curated_subset']) is bool,'Invalid subset flag')
    check(r['snapshot_date']=='2026-10-26','Invalid snapshot date')
for key,field in [('pricing','pricing'),('link_type','link_type'),('category','category')]:
    check(coverage['counts'][key]==dict(Counter(r[field] for r in rows)),f'Manifest {key} mismatch')
check(coverage['captured']=={'entries':1018,'unique_exact_urls':1018,'pages':21,'categories':18,'indexed_views':33,'indexed_subset_entries':864,'view_observations':6265,'additional_archive_entries':154},'Coverage counts mismatch')
with (DATA/'directories.csv').open(newline='',encoding='utf-8') as f:
    reader=csv.DictReader(f);check(set(reader.fieldnames)==fields,'Unexpected CSV fields');csv_rows=list(reader)
check(len(csv_rows)==1018,'CSV row count mismatch')
for c,r in zip(csv_rows,rows):check(all(c[k]==str(r[k]) for k in fields),'CSV/JSON mismatch')
readme=ROOT/'README.md'
check(readme.stat().st_size<500*1024,'README exceeds GitHub 500 KiB limit')
check(Counter(table_urls(readme))==Counter(by_url.keys()),'README must contain every exact URL once')
check(re.search(r'^## (.+)$',readme.read_text(),re.M).group(1)=='Contents','Contents must be first section')
check('https://github.com/krsnasgr/awesome-saas-startup-listing)' in readme.read_text(),'Wrong repository canonical link')
category_files=list((ROOT/'categories').glob('*.md'));check(len(category_files)==18,'Category pages missing')
for category in {r['category'] for r in rows}:
    path=ROOT/'categories'/f'{slug(category)}.md'
    selected=sorted([r for r in rows if r['category']==category],key=lambda r:(-r['domain_rating'],r['name'].casefold(),r['url']))
    check(table_urls(path)==[r['url'] for r in selected],f'Wrong category or DR order: {category}')
expected_readme_urls=[r['url'] for category in sorted({r['category'] for r in rows}) for r in sorted([r for r in rows if r['category']==category],key=lambda r:(-r['domain_rating'],r['name'].casefold(),r['url']))]
check(table_urls(readme)==expected_readme_urls,'README category tables must use descending DR, then name')
for path in [readme]+category_files:
    matches=re.findall(r'^\| \[.*?\]\(<([^>]+)>\) \| ([^|]+) \| (\d+) \| ([^|]+) \|$',path.read_text(),re.M)
    check(len(matches)==len(table_urls(path)),'Malformed metadata row')
    for url,price,rating,kind in matches:
        r=by_url[url];check((price,int(rating),kind)==(r['pricing'],r['domain_rating'],r['link_type']),'Entry metadata mismatch')
views={
 'free-startup-directories':lambda r:r['pricing']=='Free',
 'freemium-startup-directories':lambda r:r['pricing']=='Freemium',
 'paid-startup-directories':lambda r:r['pricing']=='Paid',
 'dofollow-startup-directories':lambda r:r['link_type']=='Dofollow',
 'nofollow-startup-directories':lambda r:r['link_type']=='Nofollow',
 'conditional-links':lambda r:r['link_type']=='Conditional',
 'free-dofollow-startup-directories':lambda r:r['pricing']=='Free' and r['link_type']=='Dofollow',
 'free-dofollow-dr-50-plus':lambda r:r['pricing']=='Free' and r['link_type']=='Dofollow' and r['domain_rating']>=50,
 'dr-30-plus':lambda r:r['domain_rating']>=30,
 'dr-50-plus':lambda r:r['domain_rating']>=50,
 'dr-70-plus':lambda r:r['domain_rating']>=70,
 'dr-90-plus':lambda r:r['domain_rating']>=90,
 'curated-subset':lambda r:r['curated_subset'],
 'archive-only':lambda r:not r['curated_subset'],
}
for key,predicate in views.items():
    selected=sorted([r for r in rows if predicate(r)],key=lambda r:(-r['domain_rating'],r['name'].casefold(),r['url']))
    check(table_urls(ROOT/'views'/f'{key}.md')==[r['url'] for r in selected],f'View URL mismatch: {key}')
    check(len(selected)==coverage['counts']['views'][key],f'View count mismatch: {key}')
relative_links=0;markdown=list(ROOT.rglob('*.md'))
for path in markdown:
    text=path.read_text();check('github.com/krsnasgr/awesome-saas-startup-listings' not in text,'Plural repo self-link')
    text=re.sub(r'^```.*?^```\s*$', '', text, flags=re.M|re.S)
    for target in re.findall(r'\]\((<[^>]+>|[^)\s]+)\)',text):
        target=target.strip('<>');u=urlsplit(target)
        if u.scheme or u.netloc:continue
        relative_links+=1;resolved=(path.parent/unquote(u.path)).resolve() if u.path else path
        check(resolved.is_relative_to(ROOT),f'Link escapes repo: {path}:{target}')
        check(resolved.exists(),f'Broken relative link: {path}:{target}')
        if u.fragment:check(resolved.suffix=='.md' and unquote(u.fragment) in anchors(resolved),f'Broken anchor: {path}:{target}')
for path in ['.github/PULL_REQUEST_TEMPLATE.md','.github/ISSUE_TEMPLATE/correction.md','.github/ISSUE_TEMPLATE/suggestion.md','scripts/validate.py']:
    check((ROOT/path).exists(),f'Missing file: {path}')
check(set(p.name for p in DATA.glob('*.json'))=={'catalog.json','directories.json','coverage.json'},'Non-public audit JSON in data directory')
check(not (ROOT/'docs/DESIGN.md').exists(),'Internal design research should not be published')
print(json.dumps({'status':'PASS','checks':checks,'entries':1018,'categories':18,'filtered_views':14,'markdown_files':len(markdown),'relative_links_checked':relative_links,'readme_bytes':readme.stat().st_size,'github_readme_limit_bytes':512000,'public_fields_only':True,'destination_reachability_tested':False},indent=2))
