from __future__ import annotations

from services.providers.base import ProductProvider
from services.providers.mock_provider import MockProvider


def get_product_provider() -> ProductProvider:
    return MockProvider()