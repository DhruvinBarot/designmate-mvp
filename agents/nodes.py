from __future__ import annotations

from typing import Dict, List

from agents.state import DesignOption, DesignState, FurnitureItem
from services.catalog import load_catalog, shortlist_candidates
from services.optimizer import build_initial_options


def analyze_room(state: DesignState) -> DesignState:
    request = state["request"]
    area = request.width_ft * request.length_ft

    category_map = {
        "living_room": ["sofa", "coffee_table", "rug", "lamp"],
        "bedroom": ["bed", "nightstand", "rug", "lamp"],
        "office": ["desk", "chair", "shelf", "lamp"],
    }

    room_analysis = {
        "area_sqft": area,
        "room_type": request.room_type,
        "style": request.style,
        "budget": request.budget,
        "colors": request.colors,
        "notes": request.notes,
        "image_received": bool(request.image_path),
        "fit_profile": "small" if area < 140 else "medium" if area < 220 else "large",
    }

    return {
        **state,
        "room_analysis": room_analysis,
        "required_categories": category_map.get(request.room_type, ["lamp", "rug"]),
        "debug": [f"Analyzed {request.room_type} with {area:.1f} sqft."],
    }


def retrieve_candidates(state: DesignState) -> DesignState:
    request = state["request"]
    required_categories = state["required_categories"]
    catalog = load_catalog()
    candidates = shortlist_candidates(
        items=catalog,
        categories=required_categories,
        style=request.style,
        colors=request.colors,
    )

    debug = state.get("debug", []) + [f"Retrieved {len(candidates)} candidate products."]
    return {**state, "candidates": candidates, "debug": debug}


def generate_options(state: DesignState) -> DesignState:
    request = state["request"]
    options = build_initial_options(
        candidates=state["candidates"],
        categories=state["required_categories"],
        budget=request.budget,
        target_style=request.style,
        preferred_colors=request.colors,
    )
    debug = state.get("debug", []) + [f"Built {len(options)} design options."]
    return {**state, "options": options, "debug": debug}
