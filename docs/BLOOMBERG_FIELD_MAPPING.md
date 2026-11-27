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

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | observation_date | teaching wrapper key, text YYYY-MM-DD |
| ticker | application mapping | AAPL or SP500, taken from canonical_ticker |
| open | open_value | teaching wrapper key |
| high | high_value | teaching wrapper key |
| low | low_value | teaching wrapper key |
| close | close_value | teaching wrapper key |
| volume | volume_value | teaching wrapper key, always 0 for SP500 (index) |

Teaching wrapper key != Bloomberg LIVE field mnemonic.


## TD10 handoff

- Access mode: APPROVED_SAMPLE
- Instrument identifier: AAPL US Equity (canonical ticker AAPL)
- Benchmark identifier: SPX Index (canonical ticker SP500)
- Date representation: text YYYY-MM-DD in observation_date
- Input structure: JSON object with a "series" list; each series has role, canonical_ticker, provider_identifier and an "observations" list; each observation has observation_date, open_value, high_value, low_value, close_value, volume_value
- Missing fields: none; volume_value is always 0 for SP500 because an index has no traded volume
- Special normalization notes: take ticker from canonical_ticker, never from provider_identifier; convert open, high, low, close to float and volume to int; the wrapper keys are teaching keys, not Bloomberg field mnemonics
- Expected canonical reference: data/sample/bloomberg_reference_expected.json