# Contributing evidence

Corrections and independently reproducible findings are the most useful contributions. Start with a source and a specific claim, not a conclusion about an entire service.

## Add a record

Edit `dprk_fightback/data.json`. Use an existing record as a template. Each numerical record needs:

- A unique stable `id` and an existing `service` id.
- A metric: `flow`, `fee`, `processing_cost` or `context_revenue`.
- An evidence type: `reported` or `calculated`.
- An ISO `as_of` date. State in the scope or limitations if this is an access date rather than the date of the underlying observation.
- An amount with decimal strings, currency and a qualifier: `approximate`, `more_than`, `at_least`, `reported` or `scenario`.
- A scope identifying the incident, reporting window and actor attribution where known.
- Explicit limitations, including overlap with other records and any attribution uncertainty.
- HTTPS source URLs and descriptive titles. Prefer original statements, court records, research and protocol documentation.

Do not copy complete articles, paid datasets or screenshots into the repository. Summarize the claim in your own words and link to the relevant page. Do not add personal information or unsupported ownership labels.

## Add a fee scenario

Reference a reported `flow` record for the same service in `calculation.flow_claim`. Set `calculation.rates` to decimal strings and explain `calculation.assumptions`. Store the corresponding computed amounts in `amount.values` and use the `scenario` qualifier.

A scenario can use a baseline from a lower-bound flow, but must not describe its result as a verified lower bound when the actual fee rate is unknown. Later fee schedules are allowed only when the date mismatch is explicit. Entry-only and round-trip scenarios are alternatives, not additive revenue.

## Review a contribution

```sh
python3 -m dprk_fightback validate
python3 -m unittest discover -s tests -v
python3 -m dprk_fightback show SERVICE
```

Read the original source. Check the asset, date, scope, units, attribution and recipient of fees. Record a disagreement or correction explicitly instead of silently replacing an allegation with a certainty. A passing validator checks structure and arithmetic; it does not verify the source's claim.
