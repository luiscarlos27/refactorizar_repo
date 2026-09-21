"""Tests for purchase processing system."""

import pytest
from decimal import Decimal
from pathlib import Path
from src.purchase_processor import (
    Item,
    UserCart,
    UserType,
    PurchaseCalculator,
    FilePurchaseRepository,
    PurchaseProcessor,
)


@pytest.fixture
def calculator():
    return PurchaseCalculator()


@pytest.fixture
def sample_cart():
    return UserCart(
        user_id=101,
        items=[
            Item(name="Laptop", price=Decimal("1000"), category="elec"),
            Item(name="Manzana", price=Decimal("3"), category="food"),
        ],
    )


def test_calculate_total_with_discounts(calculator, sample_cart):
    result = calculator.calculate(sample_cart, UserType.REGULAR)

    assert result.subtotal == Decimal("1003")
    assert result.discount_amount == Decimal("100.15")
    assert result.tax_amount > Decimal("0")
    assert result.total > Decimal("0")


def test_apply_taxes_regular_user(calculator, sample_cart):
    result = calculator.calculate(sample_cart, UserType.REGULAR)
    taxable_amount = result.subtotal - result.discount_amount
    expected_tax = taxable_amount * Decimal("0.18")
    assert result.tax_amount == expected_tax


def test_apply_taxes_vip_user(calculator, sample_cart):
    result = calculator.calculate(sample_cart, UserType.VIP)
    taxable_amount = result.subtotal - result.discount_amount
    base_tax = taxable_amount * Decimal("0.18")
    assert result.tax_amount == max(base_tax - Decimal("10"), Decimal("0"))


def test_apply_taxes_super_vip_user(calculator, sample_cart):
    result = calculator.calculate(sample_cart, UserType.SUPER_VIP)
    taxable_amount = result.subtotal - result.discount_amount
    base_tax = taxable_amount * Decimal("0.18")
    assert result.tax_amount == max(base_tax - Decimal("20"), Decimal("0"))


def test_user_not_found(tmp_path):
    repo = FilePurchaseRepository(tmp_path / "report.txt")
    processor = PurchaseProcessor(PurchaseCalculator(), repo)

    result = processor.process(user_id=999, user_type=UserType.REGULAR)
    assert result is None


def test_empty_cart(calculator):
    cart = UserCart(user_id=102, items=[])
    result = calculator.calculate(cart, UserType.REGULAR)

    assert result.subtotal == Decimal("0")
    assert result.total == Decimal("0")


def test_repository_saves_file(tmp_path, sample_cart):
    report_file = tmp_path / "report.txt"
    repo = FilePurchaseRepository(report_file)
    calculator = PurchaseCalculator()

    result = calculator.calculate(sample_cart, UserType.REGULAR)
    repo.save(result)

    assert report_file.exists()
    content = report_file.read_text()
    assert f"User: {sample_cart.user_id}" in content


def test_processor_registers_and_processes(tmp_path, sample_cart):
    repo = FilePurchaseRepository(tmp_path / "report.txt")
    processor = PurchaseProcessor(PurchaseCalculator(), repo)

    processor.register_cart(sample_cart)
    result = processor.process(sample_cart.user_id, UserType.REGULAR)

    assert result is not None
    assert result.user_id == sample_cart.user_id
    assert result.total > Decimal("0")
