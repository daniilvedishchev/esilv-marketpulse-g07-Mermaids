
from pathlib import Path
import csv
import json

from analytics import *
from providers.yahoo_provider import *


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


def main():

    YAHOO_SYMBOLS = {
        "AAPL": "AAPL",
        "SP500": "^GSPC",
    }

    instrument_prices = fetch_yahoo_prices(
    symbol=YAHOO_SYMBOLS["AAPL"],
    canonical_ticker="AAPL",
    period="1mo",
    interval="1d",
    )

    benchmark_prices = fetch_yahoo_prices(
    symbol=YAHOO_SYMBOLS["SP500"],
    canonical_ticker="SP500",
    period="1mo",
    interval="1d",
    )

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices, benchmark_prices
    )

    assert len(aligned_instrument) > 0, "Instrument is empty"

    assert len(aligned_benchmark) > 0, "Benchmark is empty"

    assert len(aligned_instrument) == len(aligned_benchmark), \
    "Different series lengths"

    assert all(
    instrument["date"] == benchmark["date"]
    for instrument, benchmark in zip(
        aligned_instrument, aligned_benchmark
    )
    ), "Dates do not match"

    print("Alignment validation: OK")

if __name__ == "__main__":
    main()


