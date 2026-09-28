from abc import ABC, abstractmethod
from decimal import Decimal

from app.models.db_models import CompetitorPrice, PricingHistory, Product


class BaseProductRepository(ABC):
    @abstractmethod
    async def get_product_with_competitors(
        self, tenant_id: int, sku: str
    ) -> tuple[Product, list[CompetitorPrice]]:
        pass

    @abstractmethod
    async def save_pricing_log(self, history: PricingHistory) -> None:
        pass

    @abstractmethod
    async def update_product_price(
        self, product_id: int, new_price: Decimal
    ) -> Product:
        pass

    @abstractmethod
    async def bulk_fetch_products_for_repricing(
        self, tenant_id: int, limit: int, offset: int
    ) -> list[Product]:
        pass


# Alias/Classe legado para manter compatibilidade com os testes legados
class ProductRepository(BaseProductRepository):
    pass
