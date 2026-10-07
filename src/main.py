from pathlib import Path
import csv
import json


DATA_DIR = Path("data/sample")

LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def display_market_summary(asset, prices):
    print(f"Current asset: {asset}")
    print(f"Observations: {len(prices)}")
    print(f"First close: {get_first_close(prices)}")
    print(f"Last close: {get_last_close(prices)}")
    print()


def main():
    # 1. Load metadata
    instruments = load_instruments()

    # 2. Load prices
    prices = load_prices()

    # 3. Select instrument + benchmark
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    # 4. Filter both series
    instrument_prices = filter_prices(
        prices,
        instrument["ticker"]
    )

    benchmark_prices = filter_prices(
        prices,
        benchmark["ticker"]
    )

    # 5. Display configuration
    print("=== MarketPulse ===")
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")
    print()

    # 6. Display both summaries
    display_market_summary(
        instrument["ticker"],
        instrument_prices
    )

    display_market_summary(
        benchmark["ticker"],
        benchmark_prices
    )


if __name__ == "__main__":
    main()
