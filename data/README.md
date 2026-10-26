# Data dictionary

[← README](../README.md)

| File | Purpose |
| --- | --- |
| `catalog.json` | Canonical factual input for the 1,018-entry snapshot. |
| `directories.json` | Generated JSON export of the same entries and fields. |
| `directories.csv` | Generated spreadsheet-friendly export of the same entries and fields. |
| `coverage.json` | Aggregate snapshot, category, pricing, link-type, subset and view counts. |

## Catalog fields

| Field | Meaning |
| --- | --- |
| `id` | First 16 hex characters of SHA-256 of the exact UTF-8 outgoing URL. |
| `name` | Captured directory or destination name, retaining capitalization and spelling. |
| `url` | Exact outgoing URL, including its scheme, path, query and fragment when present. |
| `category` | One of 18 captured category labels; not an independent suitability assessment. |
| `pricing` | `Free`, `Freemium`, or `Paid`; reported at capture, not a current quote. |
| `domain_rating` | Integer 0–100; reported Ahrefs Domain Rating, not an independent live query. |
| `link_type` | `Dofollow`, `Nofollow`, or `Conditional`; reported classification, not a fresh link audit. |
| `curated_subset` | Membership in the 864-entry indexed subset; not a recommendation or verification flag. |
| `snapshot_date` | UTC capture date, `2026-10-26`; not the date every destination was checked. |

CSV represents `curated_subset` as `True`/`False`; JSON uses booleans. All public exports use the same factual fields. The catalog keeps distinct exact URLs even when they share a hostname.

Read [methodology](../docs/METHODOLOGY.md) before interpreting the labels. Destination availability, current prices, eligibility, submission flows and backlink behavior were not independently verified. A consistent export is not proof that its destinations remain active or suitable.
