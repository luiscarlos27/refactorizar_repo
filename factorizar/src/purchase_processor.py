"""Purchase processing system with tax calculation and discounts."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from pathlib import Path
from typing import Protocol
import logging

logger = logging.getLogger(__name__)

TAX_RATE: Decimal = Decimal("0.18")
DISCOUNT_RATES: dict[str, Decimal] = {
    "elec": Decimal("0.10"),
    "food": Decimal("0.05"),
}


class UserType(str, Enum):
    REGULAR = "r"
    VIP = "v"
    SUPER_VIP = "sv"


@dataclass(frozen=True)
class Item:
    name: str
    price: Decimal
    category: str


@dataclass(frozen=True)
class UserCart:
    user_id: int
    items: list[Item]


@dataclass
class PurchaseResult:
    user_id: int
    subtotal: Decimal
    tax_amount: Decimal
    discount_amount: Decimal
    total: Decimal
    user_type: UserType


class PurchaseRepository(Protocol):
    def save(self, result: PurchaseResult) -> None:
        ...


class FilePurchaseRepository:
    def __init__(self, filepath: Path = Path("report.txt")):
        self.filepath = filepath

    def save(self, result: PurchaseResult) -> None:
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(f"User: {result.user_id} Total: {result.total:.2f}\n")
        logger.info("Purchase saved", extra={"user_id": result.user_id})


class PurchaseCalculator:
    def __init__(self, tax_rate: Decimal = TAX_RATE):
        self.tax_rate = tax_rate

    def calculate(self, cart: UserCart, user_type: UserType) -> PurchaseResult:
        subtotal = self._calculate_subtotal(cart.items)
        discount = self._calculate_discount(cart.items)
        taxable_amount = subtotal - discount
        tax = self._calculate_tax(taxable_amount, user_type)
        total = taxable_amount + tax

        return PurchaseResult(
            user_id=cart.user_id,
            subtotal=subtotal,
            tax_amount=tax,
            discount_amount=discount,
            total=total,
            user_type=user_type,
        )

    def _calculate_subtotal(self, items: list[Item]) -> Decimal:
        return sum((item.price for item in items), Decimal("0"))

    def _calculate_discount(self, items: list[Item]) -> Decimal:
        return sum(
            (item.price * DISCOUNT_RATES.get(item.category, Decimal("0")) for item in items),
            Decimal("0"),
        )

    def _calculate_tax(self, taxable_amount: Decimal, user_type: UserType) -> Decimal:
        base_tax = taxable_amount * self.tax_rate
        match user_type:
            case UserType.VIP:
                return max(base_tax - Decimal("10"), Decimal("0"))
            case UserType.SUPER_VIP:
                return max(base_tax - Decimal("20"), Decimal("0"))
            case _:
                return base_tax


class PurchaseProcessor:
    def __init__(
        self,
        calculator: PurchaseCalculator,
        repository: PurchaseRepository,
    ):
        self.calculator = calculator
        self.repository = repository
        self._carts: dict[int, UserCart] = {}

    def register_cart(self, cart: UserCart) -> None:
        self._carts[cart.user_id] = cart

    def process(self, user_id: int, user_type: UserType) -> PurchaseResult | None:
        cart = self._carts.get(user_id)
        if cart is None:
            logger.warning("User not found", extra={"user_id": user_id})
            return None

        result = self.calculator.calculate(cart, user_type)
        self.repository.save(result)
        logger.info("Purchase processed", extra={"user_id": user_id, "total": result.total})
        return result
