# Rebuild and validate

[← README](../README.md) · [Data dictionary](../data/README.md)

## Offline rebuild

Requires Python 3.10 or newer. The build and validation scripts use only the standard library.

```bash
python scripts/build_catalog.py
python scripts/validate.py
```

`data/catalog.json` is the canonical factual input. Generated outputs include the README catalog, category pages, 14 filtered views, CSV/JSON exports and aggregate coverage information. Edit the input or the generator rather than only its generated output.

A rebuild is offline: it does not fetch live Domain Rating values, check prices, visit destinations or verify submission flows.

## Maintain historical snapshots

Keep the captured exact URLs recoverable in version history. Do not silently replace a path with a homepage, normalize schemes, merge distinct communities on the same host or erase a record because its current destination is unavailable.

For corrections or additions, record the observation date, explain the proposed change and supply public evidence from the destination when available. Distinguish reported snapshot metadata from independently checked current facts. Preserve an earlier snapshot in version history before making a dated update.

Do not assume that an old pricing label, DR value, link classification or submission flow still applies. One timeout does not prove permanent closure. Do not bypass access controls or site restrictions while checking a destination.

## Review before publishing

- Check the exact URL and identity of every changed record.
- Preserve `Conditional` as a third link type; never turn uncertainty into an invented score or label.
- Keep historical subset membership separate from recommendations or verification status.
- Update snapshot dates and expected counts only for a documented, reviewed change.
- Rebuild category pages, views and exports together.
- Run validation and review the README, affected categories and special-case views.
- Ensure no copied reviews, descriptions, full webpage HTML or credentials enter the repository.

The validator checks local catalog consistency and links. A passing result does **not** establish destination availability, acceptance, backlink treatment or SEO outcomes.
