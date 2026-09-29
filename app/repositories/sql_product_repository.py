from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.db_models import PricingHistory, Product
from app.repositories.base_repository import BaseProductRepository


class SQLProductRepository(BaseProductRepository):
    """Implementação concreta de persistência usando SQLAlchemy 2.0 Async."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_sku(self, sku: str) -> Product | None:
        """Busca um produto pelo SKU carregando os preços dos concorrentes."""
        query = (
            select(Product)
            .where(Product.sku == sku)
            .options(selectinload(Product.competitor_prices))
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def save_pricing_history(self, history: PricingHistory) -> None:
        """Registra o log de cálculo no histórico de auditoria."""
        self.session.add(history)
        await self.session.flush()

    async def update_price(self, sku: str, new_price: Decimal) -> Product | None:
        """Atualiza o preço atual de um SKU."""
        product = await self.get_by_sku(sku)
        if product:
            product.current_price = new_price
            await self.session.flush()
        return product

    async def get_active_products(
        self, limit: int = 100, offset: int = 0
    ) -> list[Product]:
        """Retorna uma lista paginada de produtos ativos."""
        query = (
            select(Product)
            .where(Product.is_active == True)
            .options(selectinload(Product.competitor_prices))
            .offset(offset)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())
