from decimal import Decimal

import pytest

from calculator import calc_expression


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("2 + 2", Decimal("4")),
        ("100 + 2%", Decimal("102")),
        ("100 - 2%", Decimal("98")),
        ("(40+60) + 10%", Decimal("110")),
        ("100 * 5%", Decimal("5")),
    ],
)
def test_basic_expressions(expression, expected):
    assert calc_expression(expression) == expected


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("100 / 5%", Decimal("2000")),
        ("100 * 5% + 2", Decimal("7")),
        ("100 + 5 * 2%", Decimal("100.1")),
        ("(50 + 50) * 5%", Decimal("5")),
        ("(2 + 3) * (4 - 1)", Decimal("15")),
        ("(2 + 3) * (4 - 1) + 10%", Decimal("16.5")),
    ],
)
def test_complex_percentage_expressions(expression, expected):
    assert calc_expression(expression) == expected


def test_default_precision_items():
    assert calc_expression("1 / 3") == Decimal("0.3333")
    assert calc_expression("1 / 6") == Decimal("0.1667")
    assert calc_expression("2.50000") == Decimal("2.5")


def test_precision_and_trim():
    assert calc_expression("10 / 3", precision=2) == Decimal("3.33")
    assert calc_expression("2.5000 + 0", precision=4) == Decimal("2.5")
    assert calc_expression("0.0000", precision=4) == Decimal("0")


def test_invalid_expression_returns_none():
    assert calc_expression("2 ++ 2") is None
    assert calc_expression("1 / 0") is None


def test_negative_precision_raises():
    with pytest.raises(ValueError):
        calc_expression("1 + 1", precision=-1)
