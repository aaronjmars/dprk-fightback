# DPRK Fightback

Make stolen crypto harder to hide.

An open-source research toolkit for understanding publicly reported DPRK crypto theft, the services funds passed through, and the fees those flows may have generated. Built for investigators, journalists, developers and people trying to understand where stolen assets go.

The first version is an **offline evidence library and CLI**. It searches a curated dataset and reproduces fee scenarios. Its validation checks data consistency, not source truth, current balances or ownership.

## Start here

Requires Python 3.11 or newer. No API keys, accounts or runtime dependencies.

```sh
python3 -m dprk_fightback services
python3 -m dprk_fightback show thorchain
python3 -m dprk_fightback search Harmony
python3 -m dprk_fightback fees --service exch
python3 -m dprk_fightback fees --evidence reported --json
python3 -m dprk_fightback export --format csv > claims.csv
python3 -m dprk_fightback validate
```

Run these from the repository root. To install a local command:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install .
dprk-fightback show vultisig
```

## What you can investigate

- **Service roles:** distinguish wallets, swap interfaces, exchanges, mixers and privacy protocols.
- **Historical flows:** find reported amounts, incidents, reporting dates and original sources.
- **Fee economics:** reproduce calculations and inspect their assumptions instead of treating estimates as receipts.
- **Methods and response:** understand the broad laundering stages and where evidence can help defenders. Read [the guide](docs/METHODS.md).
- **Evidence gaps:** see where an amount is unknown or a source describes a wider scope than DPRK activity alone.

The seed catalog contains 34 services and 21 numerical records. Some catalog entries have no numerical records. Listing a service does not establish criminal use, knowing assistance or a fiat payout.

## How to read a result

Every numerical record includes a source, reporting or access date, scope, amount qualifier and limitations. `reported` means a named source reported the figure; it does not mean this project independently verified it. `calculated` means a reproducible scenario, not observed receipts.

| Metric | Meaning |
| --- | --- |
| `flow` | Historical amount reportedly processed or exposed. Not a current balance. |
| `fee` | Reported fees or an explicitly conditional fee calculation. Not net profit. |
| `processing_cost` | Cost paid by the sender. Recipient revenue is not necessarily equal to this amount. |
| `context_revenue` | Wider service revenue for context. Not an attributed DPRK fee total. |

For example, the Vultisig record describes **$200,000 in total swap revenue**, while the DPRK portion remains unquantified. The Wasabi record describes a **193 BTC batch going mainly through it**, not an exclusive 193 BTC allocation. These limits appear in normal CLI output and exports.

Do not sum the records. The same funds may pass through multiple services, alternative estimates may describe the same activity, and reporting windows differ. Fee calculations may use schedules documented later than the underlying incident. A calculated range is not a confidence interval or a verified minimum/maximum.

The seed collection covers selected historical findings from 2022-2025 and research accessed on October 30, 2026. It is not exhaustive. It excludes unreviewed live holdings snapshots and raw commercial API responses.

## Data and contributions

The reusable dataset is [dprk_fightback/data.json](dprk_fightback/data.json). JSON and CSV exports preserve attribution and limitations. See [CONTRIBUTING.md](CONTRIBUTING.md) for the evidence format and correction process.

```sh
python3 -m unittest discover -s tests -v
python3 -m dprk_fightback validate
```

Original code and original research summaries are MIT licensed. Linked articles, reports, images, source code and provider data retain their own licenses. This repository links to sources rather than redistributing their full contents.
