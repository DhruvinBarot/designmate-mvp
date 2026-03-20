from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from agents.state import DesignOption, FurnitureItem


STYLE_WEIGHTS = {
    "exact_style": 2.0,
    "color_match": 1.0,
    "affordability": 1.0,
}


def _item_score(item: FurnitureItem, target_style: str, preferred_colors: List[str], budget: float) -> float:
    score = 0.0
    if item.style == target_style:
        score += STYLE_WEIGHTS["exact_style"]
    if preferred_colors and item.color in preferred_colors:
        score += STYLE_WEIGHTS["color_match"]
    score += max(0.1, 1 - (item.price / max(budget, 1))) * STYLE_WEIGHTS["affordability"]
    return score


def build_initial_options(
    candidates: List[FurnitureItem],
    categories: List[str],
    budget: float,
    target_style: str,
    preferred_colors: List[str],
) -> List[DesignOption]:
    grouped: Dict[str, List[FurnitureItem]] = defaultdict(list)
    for item in candidates:
        grouped[item.category].append(item)

    ranked_groups: Dict[str, List[FurnitureItem]] = {}
    for category, items in grouped.items():
        ranked_groups[category] = sorted(
            items,
            key=lambda item: _item_score(item, target_style, preferred_colors, budget),
            reverse=True,
        )

    options: List[DesignOption] = []
    for index in range(3):
        chosen: List[FurnitureItem] = []
        total_price = 0.0
        running_score = 0.0

        for category in categories:
            pool = ranked_groups.get(category, [])
            if not pool:
                continue
            candidate = pool[min(index, len(pool) - 1)]
            if total_price + candidate.price <= budget:
                chosen.append(candidate)
                total_price += candidate.price
                running_score += _item_score(candidate, target_style, preferred_colors, budget)

        if not chosen:
            continue

        summary = (
            f"A {target_style} {categories[0].replace('_', ' ')}-led concept with "
            f"{len(chosen)} items and a balanced budget profile."
        )
        options.append(
            DesignOption(
                name=f"Concept {index + 1}",
                summary=summary,
                total_price=round(total_price, 2),
                items=chosen,
                score=round(running_score / len(chosen), 2),
            )
        )

    return options
