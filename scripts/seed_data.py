import asyncio
import sys
from decimal import Decimal
from pathlib import Path

# Adiciona a raiz do projeto ao sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from sqlalchemy.future import select

from app.database import AsyncSessionLocal, Base, engine
from app.models.db_models import Product

# Dados de exemplo ajustados incluindo current_price
INITIAL_PRODUCTS = [
    {
        "tenant_id": 1,
        "sku": "PROD-001",
        "name": "Produto Exemplo A",
        "cost": Decimal("50.00"),
        "min_margin": Decimal("0.15"),
        "target_margin": Decimal("0.25"),
        "current_price": Decimal(
            "66.67"
        ),  # Adicionado para satisfazer a restrição NOT NULL
        "is_active": True,
    },
    {
        "tenant_id": 1,
        "sku": "PROD-002",
        "name": "Produto Exemplo B",
        "cost": Decimal("120.50"),
        "min_margin": Decimal("0.15"),
        "target_margin": Decimal("0.30"),
        "current_price": Decimal("172.14"),
        "is_active": True,
    },
    {
        "tenant_id": 1,
        "sku": "PROD-003",
        "name": "Produto Exemplo C",
        "cost": Decimal("15.00"),
        "min_margin": Decimal("0.10"),
        "target_margin": Decimal("0.20"),
        "current_price": Decimal("18.75"),
        "is_active": True,
    },
]


async def seed_db():
    print("Iniciando o povoamento do banco de dados...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        existing_products = result.scalars().all()

        if existing_products:
            print(
                f"O banco já contém {len(existing_products)} produtos. Povoamento ignorado."
            )
            return

        for prod_data in INITIAL_PRODUCTS:
            product = Product(**prod_data)
            session.add(product)

        await session.commit()
        print(
            f"Sucesso! {len(INITIAL_PRODUCTS)} produtos foram inseridos no banco de dados."
        )


if __name__ == "__main__":
    asyncio.run(seed_db())
