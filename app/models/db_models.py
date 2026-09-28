from datetime import datetime
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import (
    Base,  # Certifique-se de não haver outros imports circulares aqui
)


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    document_number: Mapped[str] = mapped_column(
        String(20), unique=True, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    products: Mapped[list["Product"]] = relationship(
        back_populates="tenant", cascade="all, delete-orphan"
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tenant_id: Mapped[int] = mapped_column(
        ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False
    )
    sku: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Precisão Monetária e Margens
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    min_margin: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )  # Ex: 0.15 (15%)
    target_margin: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )  # Ex: 0.25 (25%)
    current_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    tenant: Mapped["Tenant"] = relationship(back_populates="products")
    competitor_prices: Mapped[list["CompetitorPrice"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )
    history: Mapped[list["PricingHistory"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_tenant_sku", "tenant_id", "sku", unique=True),)


class CompetitorPrice(Base):
    __tablename__ = "competitor_prices"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    competitor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    captured_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    url: Mapped[str | None] = mapped_column(Text, nullable=True)

    product: Mapped["Product"] = relationship(back_populates="competitor_prices")


class PricingHistory(Base):
    __tablename__ = "pricing_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), nullable=False
    )
    suggested_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    calculated_margin: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    outliers_purged_count: Mapped[int] = mapped_column(default=0)
    is_feasible: Mapped[bool] = mapped_column(Boolean, default=True)
    reason_unfeasible: Mapped[str | None] = mapped_column(String(255), nullable=True)
    calculated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product: Mapped["Product"] = relationship(back_populates="history")
