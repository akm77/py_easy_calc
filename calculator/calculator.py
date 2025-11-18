"""Financial calculator that parses expressions with percentages."""
from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import Optional

from lark import Lark, Transformer, UnexpectedInput, v_args

from .exceptions import DivisionByZeroError

getcontext().rounding = ROUND_HALF_UP

GRAMMAR = """
    ?start: expr

    ?expr: term
          | expr "+" term     -> add
          | expr "-" term     -> sub
          | expr "+" term "%" -> add_percent
          | expr "-" term "%" -> sub_percent

    ?term: factor
          | term "*" factor     -> mul
          | term "/" factor     -> div
          | term "*" factor "%" -> mul_percent
          | term "/" factor "%" -> div_percent

    ?factor: atom
          | "-" factor           -> neg
          | "(" expr ")"

    ?atom: NUMBER               -> number

    %import common.NUMBER
    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)
class CalcTransformer(Transformer):
    def __init__(self):
        super().__init__()
        self.context = getcontext()

    def _percent(self, base: Decimal, percent: Decimal) -> Decimal:
        return base * percent / 100

    def _validate_non_zero(self, value: Decimal) -> None:
        if value == 0:
            raise DivisionByZeroError

    def add(self, a: Decimal, b: Decimal) -> Decimal:
        return a + b

    def sub(self, a: Decimal, b: Decimal) -> Decimal:
        return a - b

    def mul(self, a: Decimal, b: Decimal) -> Decimal:
        return a * b

    def div(self, a: Decimal, b: Decimal) -> Decimal:
        self._validate_non_zero(b)
        return a / b

    def mul_percent(self, base: Decimal, percent: Decimal) -> Decimal:
        return self._percent(base, percent)

    def div_percent(self, base: Decimal, percent: Decimal) -> Decimal:
        self._validate_non_zero(percent)
        return base / (percent / 100)

    def add_percent(self, base: Decimal, percent: Decimal) -> Decimal:
        return base + self._percent(base, percent)

    def sub_percent(self, base: Decimal, percent: Decimal) -> Decimal:
        return base - self._percent(base, percent)

    def neg(self, a: Decimal) -> Decimal:
        return -a

    def number(self, value: str) -> Decimal:
        return Decimal(value)


def _round_decimal(value: Decimal, precision: int) -> Decimal:
    if precision < 0:
        raise ValueError("precision must be >= 0")

    quant = Decimal(1).scaleb(-precision)
    quantized = value.quantize(quant)
    trimmed = format(quantized, "f")

    if "." in trimmed:
        trimmed = trimmed.rstrip("0").rstrip(".")

    if trimmed in {"", "-0"}:
        trimmed = "0"

    return Decimal(trimmed)


def _build_parser() -> Lark:
    return Lark(GRAMMAR, parser="lalr", transformer=CalcTransformer())


def safe_parse(parser: Lark, expression: str) -> Optional[Decimal]:
    try:
        result = parser.parse(expression)
        if isinstance(result, Decimal):
            return result
    except (UnexpectedInput, DivisionByZeroError):
        return None
    return None


def calc_expression(expression: str, precision: int = 4) -> Optional[Decimal]:
    """Evaluate an arithmetic expression and return a Decimal trimmed to `precision` digits."""

    raw_value = safe_parse(_build_parser(), expression)
    if raw_value is None:
        return None
    return _round_decimal(raw_value, precision)


def main() -> None:
    """Run a handful of expressions to demonstrate the calculator."""

    expressions = [
        "2 + 2",
        "100 + 2%",
        "100 - 2%",
        "(40+60) + 10%",
        "100 * 5%",
        "100 / 5%",
        "-5 + 15",
        "(2 + 3) * (4 - 1)",
    ]

    for expression in expressions:
        result = calc_expression(expression)
        print(f"{expression} = {result}")


if __name__ == "__main__":
    main()
