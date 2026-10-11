"""Generate daily order CSV files with deliberate data problems.

Injected on purpose (they become capstone test cases):
- duplicate rows
- one late-arriving row per file (an order from two days earlier)
"""
from __future__ import annotations

import csv
import logging
import random
from datetime import date, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

FIELDS = ["order_id", "customer_id", "order_date", "amount"]
Row = dict[str, str]


def make_orders(day: date, count: int, first_id: int, rng: random.Random) -> list[Row]:
    """Create `count` clean orders for one day."""
    return [
        {
            "order_id": str(first_id + i),
            "customer_id": f"C{rng.randint(1, 20):02d}",
            "order_date": day.isoformat(),
            "amount": f"{rng.uniform(10, 500):.2f}",
        }
        for i in range(count)
    ]


def add_duplicates(rows: list[Row], count: int, rng: random.Random) -> list[Row]:
    """Return the rows plus `count` exact copies of randomly chosen rows."""
    return rows + [dict(rng.choice(rows)) for _ in range(count)]


def add_late_row(rows: list[Row], day: date, order_id: int, rng: random.Random) -> list[Row]:
    """Add one order dated two days before `day` (it arrives late)."""
    late = {
        "order_id": str(order_id),
        "customer_id": f"C{rng.randint(1, 20):02d}",
        "order_date": (day - timedelta(days=2)).isoformat(),
        "amount": f"{rng.uniform(10, 500):.2f}",
    }
    return rows + [late]


def write_csv(path: Path, rows: list[Row]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    logger.info("Wrote %d rows to %s", len(rows), path)


def generate(output_dir: Path, start: date, days: int = 5,
             orders_per_day: int = 20, seed: int = 42) -> list[Path]:
    """Write one CSV per day and return the file paths."""
    rng = random.Random(seed)
    paths: list[Path] = []
    next_id = 1000
    for offset in range(days):
        day = start + timedelta(days=offset)
        rows = make_orders(day, orders_per_day, next_id, rng)
        next_id += orders_per_day
        rows = add_duplicates(rows, 2, rng)
        rows = add_late_row(rows, day, next_id, rng)
        next_id += 1
        rng.shuffle(rows)
        path = output_dir / f"orders_{day.isoformat()}.csv"
        write_csv(path, rows)
        paths.append(path)
    logger.info("Generated %d files in %s", len(paths), output_dir)
    return paths


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    generate(Path("data/raw"), date(2026, 10, 1))