# Contributing

Help founders find relevant submission destinations and make the evidence easier to trust. Corrections are as useful as additions.

[← Catalog](README.md) · [Data dictionary](data/README.md) · [Maintenance](docs/MAINTENANCE.md)

## Scope and inclusion

This repository has two distinct responsibilities:

1. **Preserve the captured catalog.** The 2026-10-26 snapshot retains all 1,018 exact URLs, including communities, media and non-software entries. Presence is not a recommendation. Do not quietly delete an inconvenient record or merge separate paths on the same host.
2. **Review proposed improvements.** A new suggestion should offer a relevant way for a startup or SaaS product to be discovered: a public listing, launch page, integration marketplace, review platform or appropriate community. Provide evidence of how participation or submission actually works.

New suggestions should be reachable when checked and have a clear audience or use case. Parked domains, copied lists with no additional destination, undisclosed referral links, fabricated metrics and guaranteed-ranking pitches are not useful additions. Disclose if you own or work with a suggested service.

A free trial alone is not evidence of a permanently free listing. Free, freemium and paid services can all be relevant; label them honestly. Community membership does not grant permission to advertise.

## Report a correction or retired destination

Use the correction issue template and include:

- Entry name and **exact URL**, preserving its path, query and scheme.
- The field affected: URL, category, pricing, DR, link type, eligibility or reachability.
- What the repository says, what you observed, a public evidence link and your UTC check date.
- Whether the information is a reported claim or something you independently checked at the destination.

One timeout does not establish that a site is permanently gone. Distinguish a redirect, temporary outage, login requirement, eligibility restriction, closed submission flow and confirmed closure. Do not bypass an access control to investigate.

Historical entries must stay recoverable in version history. Propose a dated correction or a new snapshot rather than silently replacing historical facts. A confirmed closure can change future browsing views without erasing the archived identity.

## Suggest a destination

Use the suggestion issue template before making broad data changes. Include the exact public URL, the intended audience, a working submission/participation path, pricing evidence and any eligibility limitations. DR or link-type evidence is optional: unknown is better than an invented score or an assumed dofollow link.

A suggestion is not automatically part of the historical capture or its 864-entry indexed subset. Maintainers should review it separately or include it in a new, clearly documented snapshot with counts and tests updated together. `curated_subset` records historical membership, not approval or quality.

## Entry format and organization

The README and category pages are generated, with one entry per table row:

```markdown
| Listing | Pricing | DR¹ | Link type¹ |
| --- | --- | --- | --- |
| [Name](<exact-url>) | Free | 50 | Dofollow |
```

- Keep names factual and retain captured spelling in preserved records.
- Keep exact URLs; do not replace a path with a homepage or append tracking codes.
- Use the existing category when it fits. Explain proposed category changes before reorganizing many records.
- Keep all listing tables sorted by descending DR, then name A–Z and exact URL for ties. The canonical JSON and CSV exports remain alphabetized by name.
- Use concise, original factual wording for any new explanatory notes—not copied reviews, slogans or unsupported quality claims.

## Review checklist

- [ ] The exact URL and affected record are identified; duplicate URLs were checked.
- [ ] The proposed change has public evidence and a UTC check date.
- [ ] Pricing and link labels are evidenced, or uncertainty is clearly recorded for review; Conditional is not converted to Dofollow.
- [ ] Any commercial relationship is disclosed; no affiliate or tracking parameters were introduced.
- [ ] Historical records remain recoverable, with reported metadata distinguished from independent checks.
- [ ] The canonical `data/catalog.json`, generated README, category pages, views and exports agree.
- [ ] `python scripts/build_catalog.py` and `python scripts/validate.py` pass for the documented snapshot.
- [ ] The pull request explains the change and contains no copied editorial text.

For writing-only fixes, identify which generator or document owns the text. Edit that input rather than only its generated output. Keep pull requests focused; separate unrelated additions and structural changes. Be constructive when discussing evidence or reviewing another contribution.
