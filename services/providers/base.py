from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from agents.state import FurnitureItem


class ProductProvider(ABC):
    @abstractmethod
    def search(
        self,
        categories: list[str],
        style: str,
        colors: list[str],
        avoid_colors: list[str] | None = None,
        exclude_retailers: list[str] | None = None,
    ) -> List[FurnitureItem]:
        raise NotImplementedError