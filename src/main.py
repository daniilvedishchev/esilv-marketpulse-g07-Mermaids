from pathlib import Path
import csv
import json

from analytics import *
from providers.yahoo_provider import *
from providers.bloomberg_provider import (
    BLOOMBERG_IDENTIFIERS,
    fetch_approved_sample_prices,
)


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


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
        return [
            normalize_price_row(row)
            for row in csv.DictReader(file)
        ]


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_close(prices):
    first_row = prices[0]
    return float(first_row["close"])


def get_last_close(prices):
    last_row = prices[-1]
    return float(last_row["close"])


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def display_market_summary(asset, prices, show_currency=True):
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    if show_currency:
        suffix = f" {asset['currency']}"
    else:
        suffix = ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Market       : {asset['market']}")
    print(f"Currency     : {asset['currency']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {first_close:.2f}{suffix}")
    print(f"Last close   : {last_close:.2f}{suffix}")


def build_market_snapshot():
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = fetch_approved_sample_prices(
        BLOOMBERG_IDENTIFIERS["AAPL"]
    )
    benchmark_prices = fetch_approved_sample_prices(
        BLOOMBERG_IDENTIFIERS["SP500"]
    )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices, benchmark_prices
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    return {
        "provider": "Bloomberg stage",
        "access_mode": "APPROVED_SAMPLE",
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return, benchmark_return
        ),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_base = snapshot["instrument_base_100"]
    benchmark_base = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")

    print("\nProvider")
    print(snapshot["provider"])

    print("\nAccess mode")
    print(snapshot["access_mode"])

    print("\nMarket configuration")
    print(f"Instrument : {instrument['ticker']} - {instrument['name']}")
    print(f"Benchmark  : {benchmark['name']}")
    print(f"Period     : {snapshot['lookback']}")
    print(f"Interval   : {snapshot['interval']}")

    print(f"\nInstrument return : {snapshot['instrument_return']:.2f}%")
    print(f"Benchmark return  : {snapshot['benchmark_return']:.2f}%")

    print("\nRelative performance")
    print(f"{instrument['ticker']} vs {benchmark['ticker']} : "
          f"{snapshot['relative_performance']:+.2f} percentage points")

    print("\nBase 100")
    print(f"{instrument['ticker']:<6}: "
          f"{instrument_base[0]['value']:.2f} -> "
          f"{instrument_base[-1]['value']:.2f}")
    print(f"{benchmark['ticker']:<6}: "
          f"{benchmark_base[0]['value']:.2f} -> "
          f"{benchmark_base[-1]['value']:.2f}")


if __name__ == "__main__":
    main()