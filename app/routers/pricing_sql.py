from decimal import Decimal
from types import SimpleNamespace

from app.repositories.sql_product_repository import SQLProductRepository
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.models.db_models import PricingHistory
from app.schemas.pricing_sql import BulkPricingResultDTO, PricingResultDTO
from app.services.calculator import PriceCalculatorService

router = APIRouter(prefix="/api/v1/sql/pricing", tags=["SQL Pricing Engine"])
DB_SESSION_DEPENDENCY = Depends(get_db_session)


def _build_calc_request(product, competitor_prices: list[Decimal]):
    """Constrói o objeto de entrada mockado/namespace para o PriceCalculatorService."""
    return SimpleNamespace(
        product=SimpleNamespace(
            sku=product.sku,
            cost_price=product.cost,
        ),
        desired_margin=product.target_margin,
        min_margin=product.min_margin,
        marketplace_tax=Decimal("0.00"),
        competitor_prices=competitor_prices,
    )


@router.post("/calculate/{tenant_id}/{sku}", response_model=PricingResultDTO)
async def calculate_sku_price(
    tenant_id: int, sku: str, db: AsyncSession = DB_SESSION_DEPENDENCY
):
    repo = SQLProductRepository(db)
    data = await repo.get_product_with_competitors(tenant_id, sku)

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"SKU '{sku}' não encontrado para este tenant.",
        )

    product, competitors = data
    competitor_prices = [c.captured_price for c in competitors]

    # Prepara payload e executa o motor de cálculo
    calc_req = _build_calc_request(product, competitor_prices)
    calc_result = PriceCalculatorService.calculate_price(calc_req)

    is_feasible = getattr(calc_result, "viability_status", "") != "incompetitivo"

    # Salva o histórico de auditoria
    history = PricingHistory(
        product_id=product.id,
        suggested_price=calc_result.suggested_price,
        calculated_margin=calc_result.effective_margin,
        outliers_purged_count=0,
        is_feasible=is_feasible,
        reason_unfeasible=", ".join(calc_result.alerts) if calc_result.alerts else None,
    )
    await repo.save_pricing_log(history)

    if is_feasible:
        await repo.update_product_price(product.id, calc_result.suggested_price)

    return PricingResultDTO(
        sku=product.sku,
        old_price=product.current_price,
        new_price=calc_result.suggested_price if is_feasible else product.current_price,
        margin=calc_result.effective_margin,
        is_feasible=is_feasible,
        outliers_purged=0,
    )


@router.post("/bulk-reprice/{tenant_id}", response_model=BulkPricingResultDTO)
async def bulk_reprice(
    tenant_id: int,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = DB_SESSION_DEPENDENCY,
):
    repo = SQLProductRepository(db)
    products = await repo.bulk_fetch_products_for_repricing(tenant_id, limit, offset)

    processed_count = 0
    updated_count = 0

    try:
        for product in products:
            comp_prices = [c.captured_price for c in product.competitor_prices]
            calc_req = _build_calc_request(product, comp_prices)
            calc_result = PriceCalculatorService.calculate_price(calc_req)

            is_feasible = (
                getattr(calc_result, "viability_status", "") != "incompetitivo"
            )

            history = PricingHistory(
                product_id=product.id,
                suggested_price=calc_result.suggested_price,
                calculated_margin=calc_result.effective_margin,
                outliers_purged_count=0,
                is_feasible=is_feasible,
                reason_unfeasible=", ".join(calc_result.alerts)
                if calc_result.alerts
                else None,
            )
            await repo.save_pricing_log(history)

            if is_feasible:
                await repo.update_product_price(product.id, calc_result.suggested_price)
                updated_count += 1

            processed_count += 1

        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao executar precificação em lote: {str(e)}",
        )

    return BulkPricingResultDTO(
        total_processed=processed_count,
        total_updated=updated_count,
        status="Success",
    )
