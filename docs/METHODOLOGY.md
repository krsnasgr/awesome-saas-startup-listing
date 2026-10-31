# Methodology and metadata guide

[← README](../README.md) · [Coverage report](COVERAGE.md)

## What the snapshot contains

The **2026-10-26 UTC** snapshot preserves **1,018 entries across 18 categories**: factual names, exact outgoing URLs, reported pricing, Domain Rating and link-type labels. It includes an **864-entry indexed subset** and 154 additional entries. Subset membership is not a recommendation or a quality score.

The current catalog contains **1,020 entries**, including [AZN8 (2026-10-27)](ADDITIONS.md#azn8) and [BuzzLaunches (2026-10-31)](ADDITIONS.md#buzzlaunches). Additions keep their own record dates and source notes. Historical archive totals and indexed-subset membership remain unchanged.

The catalog contains no copied editorial descriptions, reviews, promotional case studies, complete webpage HTML, screenshots or page replicas.

## Identity: an exact URL, not a domain

There are **1,018 original archive URLs** and **1,020 current catalog URLs**. Entries are not collapsed by hostname. Paths, query strings, fragments and HTTP/HTTPS schemes remain intact; suspected spelling mistakes are not silently corrected. Reddit communities, LinkedIn groups, Discord invitations and platform integration pages therefore remain separate entries.

The `id` field is the first 16 hexadecimal characters of SHA-256 over the exact UTF-8 URL. The full URL remains the identity of record; the short ID is only a convenient reference. No duplicate IDs occur in this snapshot.

Names and category labels retain their captured spelling. Categories may be broad or imperfect, and category guidance is not a claim to have investigated every destination.

## Reading the fields

- **Free / Freemium / Paid:** reported labels at capture, not current quotes. A free account, free submission, free listing and free backlink are not interchangeable. Check what is actually included.
- **DR:** reported Ahrefs Domain Rating on a 0–100 scale. These are not independently queried, real-time scores. A destination's score does not predict the effect of a listing on your own domain.
- **Dofollow / Nofollow:** reported classifications of destination linking behavior, not an independent audit of a resulting listing's HTML or link attributes.
- **Conditional:** a separate classification, never treated as Dofollow. SubmitBear and AppSumo carry this label in the original snapshot; BuzzLaunches was added as Conditional because free dofollow requires a verified badge; verify applicable conditions with each destination.
- **Curated subset:** the historical field name for membership in the 864-entry indexed subset. `true` does not mean verified, recommended or suitable for every SaaS product.
- **Snapshot date:** when these factual records were captured, not the date every destination or metric was independently checked.

## Coverage, not endorsement

**The original archive's destination reachability, eligibility, prices and actual submission flows were not independently tested.** Specific checks for later additions are documented in [addition notes](ADDITIONS.md); they do not imply a fresh audit of the rest of the catalog. Some entries are communities, media outlets, stock-image or local-business destinations, and integration ecosystems. Their inclusion preserves the complete snapshot; it does not make each one a suitable SaaS launch channel.

There is no guarantee of acceptance, indexing, a free backlink, a particular link attribute, a Domain Rating increase or a search-ranking improvement. Choose relevance and useful participation over bulk submissions. Follow each destination's community and commercial rules.

## Consistency checks

All category pages, filtered views and exports are generated from the same saved catalog. Validation checks exact-URL coverage, unique identities, category and filter counts, export agreement and internal links. It also checks that the original 1,018 records remain unchanged. All 864 subset entries are present in the current catalog.

Filter counts depend on their scope. The original archive has 834 entries labeled Free; 695 belong to the indexed subset. The current catalog has 836 Free entries after the additions. These are dated observations, not claims that all prices remain current.
