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


class FurnitureItem(BaseModel):
    id: str
    category: str
    name: str
    style: str
    color: str
    price: float
    width_ft: float
    depth_ft: float
    retailer: str
    url: str = "#"


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
