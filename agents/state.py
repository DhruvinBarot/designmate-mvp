from __future__ import annotations

from typing import Dict, List, Optional, TypedDict

from pydantic import BaseModel, Field


class RoomInput(BaseModel):
    room_type: str
    width_ft: float
    length_ft: float
    style: str
    budget: float
    colors: List[str] = Field(default_factory=list)
    notes: str = ""
    image_path: Optional[str] = None
    # Refinement fields
    avoid_colors: List[str] = Field(default_factory=list)
    exclude_retailers: List[str] = Field(default_factory=list)
    must_have_categories: List[str] = Field(default_factory=list)
    refinement_notes: str = ""


class FurnitureItem(BaseModel):
    id: str
    category: str
    name: str
    price: float
    retailer: str
    product_url: Optional[str] = None
    image_url: Optional[str] = None
    style_tags: List[str] = Field(default_factory=list)
    colors: List[str] = Field(default_factory=list)
    width_in: float
    depth_in: float
    height_in: Optional[float] = None


class DesignOption(BaseModel):
    name: str
    summary: str
    total_price: float
    items: List[FurnitureItem]
    score: float


class DesignState(TypedDict, total=False):
    request: RoomInput
    room_analysis: Dict
    required_categories: List[str]
    candidates: List[FurnitureItem]
    options: List[DesignOption]
    debug: List[str]