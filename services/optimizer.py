from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional, Set

from ortools.sat.python import cp_model

from agents.state import DesignOption, FurnitureItem


SCALE = 100


def _base_item_score(
    item: FurnitureItem,
    target_style: str,
    preferred_colors: List[str],
    budget: float,
) -> float:
    score = 0.0

    if target_style in item.style_tags:
        score += 2.0

    if preferred_colors and any(c in item.colors for c in preferred_colors):
        score += 1.5

    affordability = max(0.1, 1 - (item.price / max(budget, 1)))
    score += affordability

    return score


def _concept_item_score(
    item: FurnitureItem,
    concept_type: str,
    target_style: str,
    preferred_colors: List[str],
    budget: float,
    reused_ids: Set[str],
    avoid_colors: Set[str] | None = None,
    exclude_retailers: Set[str] | None = None,
    must_have_categories: Set[str] | None = None,
) -> int:
    base = _base_item_score(item, target_style, preferred_colors, budget)

    style_match = 1 if target_style in item.style_tags else 0
    color_match = 1 if preferred_colors and any(c in item.colors for c in preferred_colors) else 0
    price_ratio = item.price / max(budget, 1)

    score = base

    if concept_type == "style":
        score += 2.0 * style_match
        score += 0.5 * color_match
    elif concept_type == "budget":
        score += 1.0 * style_match
        score += 0.5 * color_match
        score += max(0.0, 1.2 - (2.0 * price_ratio))
    elif concept_type == "color":
        score += 2.0 * color_match
        score += 0.75 * style_match

    if item.id in reused_ids:
        score -= 1.25

    # Refinement penalties and rewards
    if avoid_colors and any(c in avoid_colors for c in item.colors):
        score -= 2.0

    if exclude_retailers and item.retailer in exclude_retailers:
        score -= 2.0

    if must_have_categories and item.category in must_have_categories:
        score += 1.0

    return int(round(score * SCALE))


def _minimum_required_budget(candidates: List[FurnitureItem], categories: List[str]) -> tuple[Optional[float], List[str]]:
    grouped: Dict[str, List[FurnitureItem]] = defaultdict(list)
    for item in candidates:
        grouped[item.category].append(item)

    missing = [category for category in categories if not grouped.get(category)]
    if missing:
        return None, missing

    min_total = 0.0
    for category in categories:
        cheapest = min(grouped[category], key=lambda item: item.price)
        min_total += cheapest.price

    return round(min_total, 2), []


def _solve_concept(
    candidates: List[FurnitureItem],
    categories: List[str],
    budget: float,
    target_style: str,
    preferred_colors: List[str],
    concept_name: str,
    concept_type: str,
    summary: str,
    reused_ids: Optional[Set[str]] = None,
    avoid_colors: Optional[Set[str]] = None,
    exclude_retailers: Optional[Set[str]] = None,
    must_have_categories: Optional[Set[str]] = None,
) -> Optional[DesignOption]:
    reused_ids = reused_ids or set()
    avoid_colors = avoid_colors or set()
    exclude_retailers = exclude_retailers or set()
    must_have_categories = must_have_categories or set()

    filtered = [item for item in candidates if item.category in categories]
    if not filtered:
        return None

    model = cp_model.CpModel()

    x: Dict[int, cp_model.IntVar] = {}
    for i, _ in enumerate(filtered):
        x[i] = model.NewBoolVar(f"x_{concept_type}_{i}")

    budget_cents = int(round(budget * 100))
    model.Add(sum(int(round(item.price * 100)) * x[i] for i, item in enumerate(filtered)) <= budget_cents)

    grouped_indices: Dict[str, List[int]] = defaultdict(list)
    for i, item in enumerate(filtered):
        grouped_indices[item.category].append(i)

    # Require exactly one item for every required category
    for category in categories:
        idxs = grouped_indices.get(category, [])
        if not idxs:
            return None
        model.Add(sum(x[i] for i in idxs) == 1)

    objective_terms = []
    for i, item in enumerate(filtered):
        item_score = _concept_item_score(
            item=item,
            concept_type=concept_type,
            target_style=target_style,
            preferred_colors=preferred_colors,
            budget=budget,
            reused_ids=reused_ids,
            avoid_colors=avoid_colors,
            exclude_retailers=exclude_retailers,
            must_have_categories=must_have_categories,
        )
        objective_terms.append(item_score * x[i])

    model.Maximize(sum(objective_terms))

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 3.0
    solver.parameters.num_search_workers = 8

    status = solver.Solve(model)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None

    chosen: List[FurnitureItem] = []
    total_price = 0.0
    running_score = 0.0

    for i, item in enumerate(filtered):
        if solver.Value(x[i]) == 1:
            chosen.append(item)
            total_price += item.price
            running_score += _base_item_score(item, target_style, preferred_colors, budget)

    if len(chosen) != len(categories):
        return None

    category_order = {category: idx for idx, category in enumerate(categories)}
    chosen.sort(key=lambda item: category_order.get(item.category, 999))

    return DesignOption(
        name=concept_name,
        summary=summary,
        total_price=round(total_price, 2),
        items=chosen,
        score=round(running_score / len(chosen), 2),
    )


def build_initial_options(
    candidates: List[FurnitureItem],
    categories: List[str],
    budget: float,
    target_style: str,
    preferred_colors: List[str],
    avoid_colors: Optional[List[str]] = None,
    exclude_retailers: Optional[List[str]] = None,
    must_have_categories: Optional[List[str]] = None,
) -> List[DesignOption]:
    avoid_colors_set = set(avoid_colors or [])
    exclude_retailers_set = set(exclude_retailers or [])
    must_have_categories_set = set(must_have_categories or [])

    minimum_budget, missing_categories = _minimum_required_budget(candidates, categories)

    if missing_categories:
        missing_text = ", ".join(cat.replace("_", " ") for cat in missing_categories)
        return [
            DesignOption(
                name="No Complete Concept Available",
                summary=f"Missing product coverage for: {missing_text}. Add more products to the catalog for this room type.",
                total_price=0.0,
                items=[],
                score=0.0,
            )
        ]

    if minimum_budget is not None and minimum_budget > budget:
        return [
            DesignOption(
                name="Budget Too Low",
                summary=(
                    f"No complete {target_style} concept fits within ${budget:,.0f}. "
                    f"The minimum feasible budget for all required categories is about ${minimum_budget:,.0f}."
                ),
                total_price=minimum_budget,
                items=[],
                score=0.0,
            )
        ]

    options: List[DesignOption] = []
    reused_ids: Set[str] = set()

    shared = dict(
        candidates=candidates,
        categories=categories,
        budget=budget,
        target_style=target_style,
        preferred_colors=preferred_colors,
        avoid_colors=avoid_colors_set,
        exclude_retailers=exclude_retailers_set,
        must_have_categories=must_have_categories_set,
    )

    style_option = _solve_concept(
        **shared,
        concept_name="Concept 1",
        concept_type="style",
        summary=f"A style-first {target_style} concept focused on strong design consistency.",
        reused_ids=reused_ids,
    )
    if style_option:
        options.append(style_option)
        reused_ids.update(item.id for item in style_option.items)

    budget_option = _solve_concept(
        **shared,
        concept_name="Concept 2",
        concept_type="budget",
        summary=f"A budget-friendly {target_style} concept that lowers spend while covering essentials.",
        reused_ids=reused_ids,
    )
    if budget_option:
        options.append(budget_option)
        reused_ids.update(item.id for item in budget_option.items)

    color_option = _solve_concept(
        **shared,
        concept_name="Concept 3",
        concept_type="color",
        summary=f"A color-coordinated {target_style} concept built around your preferred palette.",
        reused_ids=reused_ids,
    )
    if color_option:
        options.append(color_option)

    return options