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
    avoid_colors: List[str] | None = None,
    exclude_retailers: List[str] | None = None,
    must_have_categories: List[str] | None = None,
) -> List[FurnitureItem]:
    categories = set(categories)
    avoid_colors = set(avoid_colors or [])
    exclude_retailers = set(exclude_retailers or [])
    must_have_categories = set(must_have_categories or [])

    shortlisted = [
        item for item in items
        if item.category in categories
        and not any(c in avoid_colors for c in item.colors)
        and item.retailer not in exclude_retailers
    ]

    def score(item: FurnitureItem) -> tuple:
        style_match = 1 if style in item.style_tags else 0
        color_match = 1 if (not colors or any(c in item.colors for c in colors)) else 0
        must_have_boost = 1 if item.category in must_have_categories else 0
        return (must_have_boost, style_match, color_match, -item.price)

    shortlisted.sort(key=score, reverse=True)
    return shortlisted