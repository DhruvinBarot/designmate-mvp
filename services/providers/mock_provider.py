from __future__ import annotations

from typing import List

from agents.state import FurnitureItem
from services.catalog import load_catalog, shortlist_candidates
from services.providers.base import ProductProvider


class MockProvider(ProductProvider):
    def search(
        self,
        categories: list[str],
        style: str,
        colors: list[str],
        avoid_colors: list[str] | None = None,
        exclude_retailers: list[str] | None = None,
    ) -> List[FurnitureItem]:
        catalog = load_catalog()

        avoid_colors = [c.lower() for c in (avoid_colors or [])]
        exclude_retailers = [r.lower() for r in (exclude_retailers or [])]

        filtered_catalog = []
        for item in catalog:
            if exclude_retailers and item.retailer.lower() in exclude_retailers:
                continue
            if avoid_colors and any(c.lower() in avoid_colors for c in item.colors):
                continue
            filtered_catalog.append(item)

        return shortlist_candidates(
            items=filtered_catalog,
            categories=categories,
            style=style,
            colors=colors,
        )