# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

Source:
data/sample/bloomberg_reference_sample.json

Reference:
docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md

Live connectivity:
not demonstrated

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

## Field mapping

| MarketPulse field | Source field | Status / notes |
|---|---|---|
| date | observation_date | YYYY-MM-DD |
| ticker | canonical_ticker | AAPL or SP500 |
| open | open_value | Numeric |
| high | high_value | Numeric |
| low | low_value | Numeric |
| close | close_value | Numeric |
| volume | volume_value | Numeric |

The source fields are teaching wrapper keys,
not Bloomberg LIVE field mnemonics.

## Input observations

- AAPL: 21 daily observations.
- SP500: 21 daily observations.
- Period: September 2026.
- No missing required fields observed.
- SP500 volume is consistently zero.
- Values are illustrative teaching data.

## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity
- Benchmark identifier: SPX Index
- Date representation: YYYY-MM-DD
- Input structure: JSON with series and observations
- Missing fields: none observed in the sample
- Special normalization notes:
  - Preserve canonical tickers AAPL and SP500.
  - Flatten observations into canonical rows.
  - Preserve benchmark volume values.

Expected canonical reference:
data/sample/bloomberg_reference_expected.json
