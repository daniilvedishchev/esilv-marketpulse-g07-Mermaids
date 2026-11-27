import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "sample"

BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

BLOOMBERG_SYMBOLS = BLOOMBERG_IDENTIFIERS


def fetch_raw_bloomberg_history():
    with open(DATA_DIR / "bloomberg_reference_sample.json", encoding="utf-8") as f:
        return json.load(f)


def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []

    for series in raw_data["series"]:
        if series["canonical_ticker"] == canonical_ticker:
            for obs in series["observations"]:
                rows.append({
                    "date": obs["observation_date"],
                    "ticker": canonical_ticker,
                    "open": float(obs["open_value"]),
                    "high": float(obs["high_value"]),
                    "low": float(obs["low_value"]),
                    "close": float(obs["close_value"]),
                    "volume": int(obs["volume_value"]),
                })

    return rows


def validate():
    raw_data = fetch_raw_bloomberg_history()
    aapl = normalize_bloomberg_history(raw_data, "AAPL")
    sp500 = normalize_bloomberg_history(raw_data, "SP500")

    required_fields = {
        "date", "ticker", "open", "high", "low", "close", "volume"
    }

    assert aapl, "AAPL is empty"
    assert sp500, "SP500 is empty"

    for row in aapl + sp500:
        assert set(row.keys()) == required_fields
        assert isinstance(row["close"], (int, float))
        assert row["date"]

    assert all(row["ticker"] == "AAPL" for row in aapl)
    assert all(row["ticker"] == "SP500" for row in sp500)

    print("Canonical structure validation passed")

    with open(DATA_DIR / "bloomberg_reference_expected.json", encoding="utf-8") as f:
        expected = json.load(f)["rows"]

    normalized = aapl + sp500
    assert normalized == expected

    print("Reference validation passed")
    print(f"Total validated rows: {len(normalized)}")


if __name__ == "__main__":
    validate()
