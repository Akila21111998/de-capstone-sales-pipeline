import csv
from datetime import date
from pathlib import Path

from generate_orders import generate


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_generates_one_file_per_day(tmp_path: Path) -> None:
    paths = generate(tmp_path, date(2026, 10, 1), days=3, orders_per_day=10)
    assert len(paths) == 3
    assert all(p.exists() for p in paths)


def test_each_file_has_duplicates_and_one_late_row(tmp_path: Path) -> None:
    paths = generate(tmp_path, date(2026, 10, 1), days=2, orders_per_day=10)
    for path in paths:
        rows = read_rows(path)
        file_day = path.stem.replace("orders_", "")
        ids = [r["order_id"] for r in rows]
        late = [r for r in rows if r["order_date"] < file_day]
        assert len(ids) - len(set(ids)) == 2
        assert len(late) == 1


def test_same_seed_gives_same_output(tmp_path: Path) -> None:
    a = generate(tmp_path / "a", date(2026, 10, 1), days=1, orders_per_day=5, seed=7)
    b = generate(tmp_path / "b", date(2026, 10, 1), days=1, orders_per_day=5, seed=7)
    assert a[0].read_text() == b[0].read_text()