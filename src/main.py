from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)
from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices
from providers.bloomberg_provider import (
    BLOOMBERG_SYMBOLS,
    fetch_raw_bloomberg_history,
    normalize_bloomberg_history,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "sample"
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"

provider_symbols = {
    "yahoo": YAHOO_SYMBOLS,
    "bloomberg": BLOOMBERG_SYMBOLS,
}


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return [normalize_price_row(row) for row in csv.DictReader(file)]


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def display_market_summary(asset, prices, show_currency=True):
    suffix = f" {asset['currency']}" if show_currency else ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Market       : {asset['market']}")
    print(f"Currency     : {asset['currency']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}{suffix}")
    print(f"Last close   : {get_last_close(prices):.2f}{suffix}")


def validate_bloomberg_sample(data):
    required_fields = {"date", "ticker", "open", "high", "low", "close", "volume"}

    for ticker in ("AAPL", "SP500"):
        rows = data[ticker]
        assert rows, f"{ticker} is empty"

        for row in rows:
            assert set(row) == required_fields
            assert isinstance(row["close"], (int, float))
            assert row["date"]
            assert row["ticker"] == ticker

    with open(DATA_DIR / "bloomberg_reference_expected.json", encoding="utf-8") as file:
        expected = json.load(file)["rows"]

    assert data["AAPL"] + data["SP500"] == expected, "Bloomberg reference mismatch"


def pipeline(provider):
    data = {}
    symbol_mapper = provider_symbols[provider]

    if provider == "bloomberg":
        raw_data = fetch_raw_bloomberg_history()

    for canonical, provider_symbol in symbol_mapper.items():
        if provider == "yahoo":
            data[canonical] = fetch_yahoo_prices(
                provider_symbol,
                canonical,
                period="1mo",
                interval="1d",
            )
        elif provider == "bloomberg":
            data[canonical] = normalize_bloomberg_history(raw_data, canonical)

    if provider == "bloomberg":
        validate_bloomberg_sample(data)

    return data


def build_market_snapshot(provider="bloomberg"):
    data = pipeline(provider)
    instruments = load_instruments()

    instrument, benchmark = align_series(data["AAPL"], data["SP500"])

    assert instrument, "Instrument is empty after alignment"
    assert benchmark, "Benchmark is empty after alignment"
    assert len(instrument) == len(benchmark)
    assert all(a["date"] == b["date"] for a, b in zip(instrument, benchmark))

    instrument_return = calculate_period_return(instrument)
    benchmark_return = calculate_period_return(benchmark)

    return {
        "provider": provider,
        "access_mode": "APPROVED_SAMPLE" if provider == "bloomberg" else "REMOTE",
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instruments["instrument"],
        "benchmark": instruments["benchmark"],
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return, benchmark_return
        ),
        "instrument_base_100": calculate_base_100(instrument),
        "benchmark_base_100": calculate_base_100(benchmark),
    }


def display_snapshot(snapshot):
    provider = snapshot["provider"]
    label = "Bloomberg stage" if provider == "bloomberg" else "Yahoo Finance"
    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]

    print("\n" + "=" * 50)
    print(f"Provider             : {label}")
    print(f"Access mode          : {snapshot['access_mode']}")
    print(f"Instrument           : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark            : {benchmark['name']}")
    print(f"Period               : {snapshot['lookback']}")
    print(f"Interval             : {snapshot['interval']}")
    print(f"Instrument return    : {snapshot['instrument_return']:.2f}%")
    print(f"Benchmark return     : {snapshot['benchmark_return']:.2f}%")
    print(f"Relative performance : {snapshot['relative_performance']:.2f} pp")

    if provider == "bloomberg":
        print("Reference validation : OK (approved sample)")

    print("\nBase 100")
    print(f"{'Date':<12} {'AAPL':>10} {'SP500':>10}")
    for a, b in zip(snapshot["instrument_base_100"], snapshot["benchmark_base_100"]):
        print(f"{a['date']:<12} {a['value']:>10.2f} {b['value']:>10.2f}")


def main():
    snapshots = {}

    for provider in provider_symbols:
        snapshots[provider] = build_market_snapshot(provider)
        display_snapshot(snapshots[provider])

    print(snapshots)


if __name__ == "__main__":
    main()
