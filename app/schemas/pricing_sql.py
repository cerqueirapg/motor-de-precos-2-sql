from decimal import Decimal

from pydantic import BaseModel, Field


# --- Schemas SQL (Novas Rotas) ---
class PricingResultDTO(BaseModel):
    sku: str
    old_price: Decimal
    new_price: Decimal
    margin: Decimal
    is_feasible: bool
    outliers_purged: int


class BulkPricingResultDTO(BaseModel):
    total_processed: int
    total_updated: int
    status: str


# --- Schemas Legados (Suporte aos Testes e Rotas Anteriores) ---
class ProductBase(BaseModel):
    sku: str
    name: str | None = "Produto"
    cost_price: Decimal = Field(gt=Decimal("0.0"))


class PricingRequest(BaseModel):
    product: ProductBase
    desired_margin: Decimal
    min_margin: Decimal
    marketplace_tax: Decimal = Decimal("0.00")
    competitor_prices: list[Decimal] = []


class PricingResponse(BaseModel):
    sku: str
    suggested_price: Decimal
    effective_margin: Decimal
    adjusted_competitor_avg: Decimal
    viability_status: str
    alerts: list[str] = []
