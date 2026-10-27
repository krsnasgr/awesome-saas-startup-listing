#!/usr/bin/env python3
"""Build a browsable, factual catalog from saved public-source observations (no network)."""
import csv, hashlib, json, re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
SNAPSHOT = '2026-10-26'

def read(name):
    return json.loads((DATA / name).read_text())
def write(path, value):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(value, encoding='utf-8')
def jwrite(path, value):
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + '\n')
def sha(value):
    return hashlib.sha256(value).hexdigest()
def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')
def esc(s):
    return s.replace('\\', '\\\\').replace('|', '\\|').replace('[', '\\[').replace(']', '\\]')
def link(r):
    return f"[{esc(r['name'])}](<{r['url']}>)"
def table(rows, category=False):
    fields = ['Listing', 'Category'] if category else ['Listing']
    fields += ['Pricing', 'DR¹', 'Link type¹']
    out = ['| ' + ' | '.join(fields) + ' |', '| ' + ' | '.join('---' for _ in fields) + ' |']
    for r in drsort(rows):
        cells = [link(r)] + ([r['category']] if category else [])
        cells += [r['pricing'], str(r['domain_rating']), r['link_type']]
        out.append('| ' + ' | '.join(cells) + ' |')
    return '\n'.join(out)
def az(rows):
    return sorted(rows, key=lambda r:(r['name'].casefold(), r['url']))
def drsort(rows):
    return sorted(rows, key=lambda r:(-r['domain_rating'], r['name'].casefold(), r['url']))

rows = az(read('catalog.json'))
assert len(rows) == len({r['url'] for r in rows}) == 1018
categories = sorted({r['category'] for r in rows})
price_counts = Counter(r['pricing'] for r in rows)
link_counts = Counter(r['link_type'] for r in rows)
category_counts = Counter(r['category'] for r in rows)
assert price_counts == {'Free':834,'Freemium':45,'Paid':139}
assert link_counts == {'Dofollow':595,'Nofollow':421,'Conditional':2}
assert len(categories) == 18
jwrite('data/directories.json', rows)
with (DATA / 'directories.csv').open('w',newline='',encoding='utf-8') as f:
    fields=['id','name','url','category','pricing','domain_rating','link_type','curated_subset','snapshot_date']
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)

category_notes = {
 'AI Tools':'Discovery catalogs and launch surfaces focused on artificial-intelligence products.',
 'Community':'Forums, groups, chat servers and participation-led communities. Read each community’s rules; a presence here is not permission to promote.',
 'Deals / SaaS':'Deal-oriented discovery for software businesses. Check commercial terms and whether your product fits the audience.',
 'Design Tools':'Design discovery, resources and showcases. Some entries require a design asset or portfolio rather than a generic SaaS listing.',
 'Developer Tools':'Places centered on developer-facing products and technical audiences.',
 'General Directory':'Broad directories and mixed-purpose platforms. Several entries are local-business or non-software destinations, so verify eligibility.',
 'Indie Hackers':'Founder- and independent-maker-focused discovery surfaces.',
 'Launchpad':'Launch and product-announcement destinations; check scheduling, eligibility and submission rules.',
 'Marketplace':'App and extension ecosystems. Integration, packaging or platform-specific requirements may apply.',
 'Marketing Tools':'Marketing-focused discovery and platforms; confirm the submission format before investing effort.',
 'No-Code':'No-code product and builder discovery.',
 'Open Source':'Open-source and developer ecosystem destinations. A relevant public project or integration may be required.',
 'Productivity':'Productivity-focused tools and discovery.',
 'SaaS Tools':'Software-as-a-service catalogs and integration ecosystems.',
 'Software Discovery':'Product search and alternative-software discovery destinations.',
 'Software Reviews':'Review-oriented software discovery. Listing a vendor and obtaining customer reviews are different activities.',
 'Startup Directory':'Company and startup-focused listings. Eligibility and verification can vary.',
 'Tech / Startups':'Startup and technology discovery, including news/media entries retained for completeness. Not every entry accepts a self-service product listing.',
}
footer = '\n\n¹ DR, pricing and link type are reported snapshot labels, not independent current verification. See [methodology and caveats](../docs/METHODOLOGY.md). Exact outgoing URLs are preserved; inclusion is not an endorsement.\n'
for category in categories:
    selected = [r for r in rows if r['category']==category]
    write(f'categories/{slug(category)}.md',f'# {category}\n\n[← All categories](../README.md#browse-by-category) · [CSV](../data/directories.csv) · [JSON](../data/directories.json)\n\n{len(selected)} entries · Snapshot: {SNAPSHOT} · Highest reported DR first\n\n{category_notes[category]}\n\n'+table(selected)+footer)

views = [
 ('free-startup-directories','Free startup directories',lambda r:r['pricing']=='Free','Every archive entry labeled Free. This does not mean unrestricted promotion, a guaranteed approval, or a guaranteed free backlink.'),
 ('freemium-startup-directories','Freemium startup directories',lambda r:r['pricing']=='Freemium','Entries labeled Freemium. Check what the free tier includes and whether a listing or link requires payment.'),
 ('paid-startup-directories','Paid startup directories',lambda r:r['pricing']=='Paid','Entries labeled Paid. Compare audience fit and submission terms rather than buying a promised ranking outcome.'),
 ('dofollow-startup-directories','Dofollow startup directories',lambda r:r['link_type']=='Dofollow','Reported Dofollow entries across every pricing tier. This is not a fresh audit of live backlink attributes.'),
 ('nofollow-startup-directories','Nofollow startup directories',lambda r:r['link_type']=='Nofollow','Reported Nofollow entries. Evaluate relevant audience exposure independently of link labels.'),
 ('conditional-links','Conditional link types',lambda r:r['link_type']=='Conditional','Conditional is deliberately preserved as its own type. Confirm the applicable placement, plan and linking terms.'),
 ('free-dofollow-startup-directories','Free dofollow startup directories',lambda r:r['pricing']=='Free' and r['link_type']=='Dofollow','A factual intersection of the Free and Dofollow reported labels. Neither the link nor an increase in Domain Rating is guaranteed.'),
 ('free-dofollow-dr-50-plus','Free dofollow directories with DR 50+',lambda r:r['pricing']=='Free' and r['link_type']=='Dofollow' and r['domain_rating']>=50,'A discovery shortlist, sorted by reported DR. Start with product eligibility and audience relevance, not the score alone.'),
 ('dr-30-plus','Directories with DR 30+',lambda r:r['domain_rating']>=30,'All archive entries whose reported DR is at least 30.'),
 ('dr-50-plus','Directories with DR 50+',lambda r:r['domain_rating']>=50,'All archive entries whose reported DR is at least 50.'),
 ('dr-70-plus','Directories with DR 70+',lambda r:r['domain_rating']>=70,'All archive entries whose reported DR is at least 70.'),
 ('dr-90-plus','Directories with DR 90+',lambda r:r['domain_rating']>=90,'All archive entries whose reported DR is at least 90. Many are communities, media sites or platform ecosystems rather than submission directories.'),
 ('curated-subset','Indexed subset',lambda r:r['curated_subset'],'The 864 exact URLs also present in the 33 indexed views. This is a subset of—not a replacement for—the 1,018-row archive.'),
 ('archive-only','Archive-only entries',lambda r:not r['curated_subset'],'The 154 exact URLs outside the indexed-view union. They remain here so communities, media outlets, separate paths and other excluded entries are not silently lost.'),
]
view_counts={}
for key,title,predicate,note in views:
    selected=drsort([r for r in rows if predicate(r)])
    view_counts[key]=len(selected)
    write(f'views/{key}.md',f'# {title}\n\n[← README](../README.md) · [All views](README.md) · [CSV](../data/directories.csv) · [JSON](../data/directories.json)\n\n{len(selected)} entries · Snapshot: {SNAPSHOT} · Highest reported DR first\n\n{note}\n\n'+table(selected,category=True)+footer)
write('views/README.md','# Browse by pricing, link type and Domain Rating\n\n[← Main catalog](../README.md)\n\nThese views filter the complete 1,018-entry archive; they are not restricted to the smaller indexed subset.\n\n| View | Entries |\n| --- | ---: |\n'+'\n'.join(f'| [{title}]({key}.md) | {view_counts[key]:,} |' for key,title,_,_ in views)+'\n')

manifest={
 'schema_version':1,'snapshot_date':SNAPSHOT,
 'captured':{'entries':len(rows),'unique_exact_urls':len({r['url'] for r in rows}),'pages':21,'categories':len(categories),'indexed_views':33,'indexed_subset_entries':864,'view_observations':6265,'additional_archive_entries':154},
 'counts':{'pricing':dict(sorted(price_counts.items())),'link_type':dict(sorted(link_counts.items())),'category':dict(sorted(category_counts.items())),'views':view_counts},
 'coverage_complete':True,
 'coverage_checks':{'all_1018_exact_urls_preserved':True,'all_18_categories_present':True,'all_33_indexed_views_accounted_for':True,'indexed_subset_is_archive_subset':True,'duplicates_removed_by_domain':False},
 'catalog_sha256':sha((DATA/'catalog.json').read_bytes()),
 'limitations':['Reported metadata was not independently verified at each destination.','Pricing, Domain Rating and link type are snapshot labels, not guarantees or live metrics.','Separate paths on the same domain remain separate entries.','The full archive includes non-SaaS destinations for completeness.'],
}
jwrite('data/coverage.json',manifest)

cat_nav='\n'.join(f'| [{c}](categories/{slug(c)}.md) | {category_counts[c]} | [Browse below](#{slug(c)}) |' for c in categories)
view_nav='\n'.join(f'| [{title}](views/{key}.md) | {view_counts[key]:,} |' for key,title,_,_ in views[:8])
contents_categories='\n'.join(f'  - [{c}](#{slug(c)})' for c in categories)
readme=f'''![SaaS and startup listing sites: 1,018 destinations, 834 free listings, 18 categories](.github/social-preview.png)

# Awesome SaaS & Startup Directories: Free Backlinks & Domain Rating

Find startup directories, SaaS listing sites and free backlink opportunities for your link building research. Compare **1,018 destinations** by pricing, reported Ahrefs Domain Rating (DR), and dofollow or nofollow link type, with the **highest DR first** in every listing table.

**1,018 exact links · 18 categories · 834 free listings · Snapshot: {SNAPSHOT}**

Looking to **increase Domain Rating**, find **free dofollow backlinks**, or submit your SaaS to **high-DR directories**? Start with the filtered shortlists below and the [guide to increasing DR](docs/INCREASE-DOMAIN-RATING.md). This archive includes launch platforms, communities and software review sites as well as directories. [Contributions and corrections are welcome](CONTRIBUTING.md).

## Contents

- [Start here](#start-here)
- [How to increase Domain Rating with directory listings](#how-to-increase-domain-rating-with-directory-listings)
- [Browse by category](#browse-by-category)
- [Reading an entry](#reading-an-entry)
- [Full catalog](#full-catalog)
{contents_categories}
- [Use the list well](#use-the-list-well)
- [Coverage and integrity](#coverage-and-integrity)
- [Downloads and maintenance](#downloads-and-maintenance)

## Start here

| View | Entries |
| --- | ---: |
{view_nav}

**Browse by DR:** [30+](views/dr-30-plus.md) · [50+](views/dr-50-plus.md) · [70+](views/dr-70-plus.md) · [90+](views/dr-90-plus.md). [All 14 filters](views/README.md) · [CSV](data/directories.csv) · [JSON](data/directories.json).

> Pricing, DR and link labels are reported snapshot values—not a current audit or a promise of free backlinks, a DR boost, rankings or acceptance. Communities, media outlets and non-SaaS destinations remain included for completeness. Check eligibility before submitting.

## How to increase Domain Rating with directory listings

Use this catalog to research relevant places to list your startup and earn backlinks. For a focused shortlist, browse [free dofollow directories with DR 50+](views/free-dofollow-dr-50-plus.md), [high-DR sites at 70+](views/dr-70-plus.md), or [all free listing sites](views/free-startup-directories.md).

Ahrefs calculates DR from a domain's backlink profile; the referring site's DR and how many domains it links to both matter. A high-DR directory alone cannot predict your increase. [Ahrefs explains the calculation](https://help.ahrefs.com/en/articles/1409408-what-is-domain-rating-dr).

Check product fit, current submission terms and the actual published link before recording a result. Read the [free backlinks and directory submission guide](docs/INCREASE-DOMAIN-RATING.md) for a workflow and answers about dofollow links, free submissions and DR growth.

## Browse by category

Each archive entry appears once in the full catalog. Open a focused category page below, or jump to its section in this README.

| Category | Entries | On this page |
| --- | ---: | --- |
{cat_nav}

## Reading an entry

Every listing appears in a table with **Listing, Pricing, DR and Link type** columns. The listing name links to the exact destination URL. All listing tables sort by descending DR, then name A–Z for ties. Category sections remain A–Z.

- **Pricing:** `Free`, `Freemium` or `Paid`, as recorded in the snapshot. A free account does not necessarily mean every listing feature is free.
- **DR:** the reported Ahrefs score at capture, not a live lookup or a prediction for your own website.
- **Link type:** `Dofollow`, `Nofollow` or `Conditional`. Conditional is never counted as guaranteed dofollow.
- **Scope:** exact paths and original spellings are retained. Same-domain groups and submission pages are separate entries.

Entries use factual metadata instead of copied reviews or unverified promotional descriptions. See [methodology](docs/METHODOLOGY.md) for details.

## Full catalog

'''
related={
 'AI Tools':['Software Discovery','Developer Tools'],
 'Community':['Indie Hackers','Tech / Startups'],
 'Deals / SaaS':['SaaS Tools','Software Reviews'],
 'Design Tools':['Marketplace','Software Discovery'],
 'Developer Tools':['Open Source','No-Code'],
 'General Directory':['Startup Directory','Community'],
 'Indie Hackers':['Community','Launchpad'],
 'Launchpad':['Tech / Startups','Startup Directory'],
 'Marketing Tools':['SaaS Tools','Productivity'],
 'Marketplace':['SaaS Tools','Developer Tools'],
 'No-Code':['Developer Tools','SaaS Tools'],
 'Open Source':['Developer Tools','Software Discovery'],
 'Productivity':['SaaS Tools','Software Discovery'],
 'SaaS Tools':['Software Reviews','Marketplace'],
 'Software Discovery':['Software Reviews','AI Tools'],
 'Software Reviews':['Software Discovery','SaaS Tools'],
 'Startup Directory':['Launchpad','Tech / Startups'],
 'Tech / Startups':['Launchpad','Indie Hackers'],
}
for c in categories:
    peers=' · '.join(f'[{v}](#{slug(v)})' for v in related[c])
    readme+=f'<a id="{slug(c)}"></a>\n\n### {c}\n\n{category_counts[c]} entries · [Focused page](categories/{slug(c)}.md) · [Back to contents](#contents)\n\n{category_notes[c]}\n\nExplore also: {peers}.\n\n'+table([r for r in rows if r['category']==c])+'\n\n'
readme+=f'''## Use the list well

1. **Check fit first.** Pick a relevant audience and verify that the destination accepts your product type.
2. **Check today’s terms.** Open the exact linked page; confirm requirements, cost, moderation and current link behavior.
3. **Prepare a useful submission.** Share accurate details and follow local rules. Communities are not bulk link-drop lists.
4. **Track outcomes.** Record your submission date, status and live listing URL. A directory’s DR is not a promised result for your domain.

Looking for free startup directories or researching free backlinks and Domain Rating? Start with [Free + Dofollow](views/free-dofollow-startup-directories.md), then check relevance and terms. There are no guaranteed free DR boosts.

## Coverage and integrity

- **Full archive:** 21 rendered pages, **1,018 rows / 1,018 distinct exact URLs**, with 18 rows on the final page.
- **Live list index:** **33 of 33 links**, **6,265 row observations**, **864 unique URLs**. Every per-list count matches the index.
- **Nothing lost to domain deduplication:** separate group, community, integration and submission paths remain distinct. The [154 archive-only entries](views/archive-only.md) are preserved alongside the [864-entry indexed subset](views/curated-subset.md).
- **No copied editorial material:** factual records only; no editorial reviews, descriptions or page replicas.

[Coverage report](docs/COVERAGE.md) · [Machine-readable manifest](data/coverage.json) · [Metadata guide](docs/METHODOLOGY.md).

## Downloads and maintenance

- [CSV](data/directories.csv): one row per exact URL for spreadsheet filtering.
- [JSON](data/directories.json): the same entries with reported metadata.
- [Data dictionary](data/README.md): field meanings and export formats.
- [Maintenance guide](docs/MAINTENANCE.md): reproducible generation and validation.
- [Repository](https://github.com/krsnasgr/awesome-saas-startup-listing): corrections and development history.

## Contributing

[Suggest a destination or report a correction](CONTRIBUTING.md). Provide an exact URL, dated evidence and the relevant field—not a promotional blurb. New suggestions require relevance and submission-path evidence; existing snapshot records remain auditable even if a destination later closes. See the [review checklist](CONTRIBUTING.md#review-checklist).

## Snapshot notes

Captured {SNAPSHOT}. Reported pricing, DR and link types have not been independently verified at every destination. There is no guarantee of acceptance, indexing, backlinks or ranking improvements. The catalog includes broad archive entries for completeness, not as endorsements. [Metadata limitations](docs/METHODOLOGY.md).
'''
write('README.md',readme)
coverage=f'''# Coverage report

[← README](../README.md) · [Machine-readable counts](../data/coverage.json)

Snapshot: **{SNAPSHOT}**. The capture reconciles **1,018 entries**, **18 categories**, and **33 indexed views**.

| Measure | Captured |
| --- | ---: |
| Archive rows / unique exact URLs | 1,018 / 1,018 |
| Archive pages | 21 |
| Categories | 18 |
| Free / Freemium / Paid | 834 / 45 / 139 |
| Dofollow / Nofollow / Conditional | 595 / 421 / 2 |
| Indexed views | 33 |
| Indexed unique entries | 864 |
| View-row observations | 6,265 |
| Additional archive entries | 154 |

Pages 1–20 contained 50 entries each; the final page contained 18. All per-view counts reconciled. The indexed subset is smaller than the full archive, so the 154 additional entries remain visible. There were no conflicting observed names, pricing labels, DR values, link types or known categories across the compared views.

## What completeness means

Every captured archive row is represented once by its exact outgoing URL in the full catalog and exports. Same-domain paths are not collapsed. This does not establish destination availability, eligibility, current pricing, real backlink attributes or suitability for a SaaS product. Reported metadata has not been independently verified at each destination.

## Offline integrity

The validator checks all 1,018 identities, CSV/JSON parity, category and filter membership, metadata tags, relative links and anchors, and the canonical catalog hash. It does not contact every destination or claim those destinations are active. See [methodology](METHODOLOGY.md) and [maintenance](MAINTENANCE.md).
'''
write('docs/COVERAGE.md',coverage)
print(f'Built {len(rows)} entries, {len(categories)} categories, {len(views)} filtered views and full README.')
