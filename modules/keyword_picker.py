import csv
import random
from pathlib import Path

KEYWORDS_FILE = Path(__file__).parent.parent / "config" / "keywords.csv"


def pick_keyword() -> dict:
    rows = _load()
    available = [r for r in rows if r["used"].strip().lower() == "false"]

    if not available:
        for r in rows:
            r["used"] = "False"
        available = rows
        _save(rows)

    available.sort(key=lambda x: int(x["search_vol"]), reverse=True)
    chosen = random.choice(available[:5])

    for r in rows:
        if r["keyword"] == chosen["keyword"]:
            r["used"] = "True"
    _save(rows)

    return {"keyword": chosen["keyword"], "category": chosen["category"]}


def _load() -> list[dict]:
    with open(KEYWORDS_FILE, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _save(rows: list[dict]) -> None:
    with open(KEYWORDS_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["keyword", "category", "search_vol", "used"])
        writer.writeheader()
        writer.writerows(rows)
