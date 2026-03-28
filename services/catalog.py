from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from agents.state import FurnitureItem


DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "catalog.json"


def load_catalog() -> List[FurnitureItem]:
    raw = json.loads(DATA_PATH.read_text())
    return [FurnitureItem(**item) for item in raw]


def shortlist_candidates(
    items: List[FurnitureItem],
    categories: Iterable[str],
    style: str,
    colors: List[str],
) -> List[FurnitureItem]:
    categories = set(categories)
    shortlisted = [item for item in items if item.category in categories]

    def score(item: FurnitureItem) -> tuple:
        style_match = 1 if style in item.style_tags else 0
        color_match = 1 if (not colors or any(c in item.colors for c in colors)) else 0
        return (style_match, color_match, -item.price)

    shortlisted.sort(key=score, reverse=True)
    return shortlisted