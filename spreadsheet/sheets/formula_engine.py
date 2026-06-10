from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from .utils import (
    as_boolean,
    as_number,
    coordinate_to_position,
    flatten,
    iter_range,
)


class FormulaError(Exception):
    pass


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    position: int


@dataclass(frozen=True)
class NumberNode:
    value: float


@dataclass(frozen=True)
class StringNode:
    value: str


@dataclass(frozen=True)
class BooleanNode:
    value: bool


@dataclass(frozen=True)
class UnaryOpNode:
    operator: str
    operand: Any


@dataclass(frozen=True)
class BinaryOpNode:
    left: Any
    operator: str
    right: Any


@dataclass(frozen=True)
class CellNode:
    reference: str


@dataclass(frozen=True)
class RangeNode:
    start: str
    end: str


@dataclass(frozen=True)
class FunctionNode:
    name: str
    args: list[Any]


class FormulaTokenizer:
    def __init__(self, formula: str):
        self.formula = formula[1:] if formula.startswith("=") else formula

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        idx = 0
        while idx < len(self.formula):
            char = self.formula[idx]
            if char.isspace():
                idx += 1
                continue
            if char in "(),:":
                tokens.append(Token(char, char, idx))
                idx += 1
                continue
            if char in "+-*/":
                tokens.append(Token("OP", char, idx))
                idx += 1
                continue
            if char in "<>!=":
                next_char = self.formula[idx + 1] if idx + 1 < len(self.formula) else ""
                if char + next_char in {"<=", ">=", "!=", "=="}:
                    tokens.append(Token("OP", char + next_char, idx))
                    idx += 2
                else:
                    tokens.append(Token("OP", char, idx))
                    idx += 1
                continue
            if char == '"':
                end = idx + 1
                buffer = []
                while end < len(self.formula):
                    if self.formula[end] == '"' and self.formula[end - 1] != "\\":
                        break
                    buffer.append(self.formula[end])
                    end += 1
                if end >= len(self.formula):
                    raise FormulaError("Unterminated string literal.")
                tokens.append(Token("STRING", "".join(buffer), idx))
                idx = end + 1
                continue
            if char.isdigit() or (char == "." and idx + 1 < len(self.formula) and self.formula[idx + 1].isdigit()):
                end = idx + 1
                while end < len(self.formula) and (self.formula[end].isdigit() or self.formula[end] == "."):
                    end += 1
                tokens.append(Token("NUMBER", self.formula[idx:end], idx))
                idx = end
                continue
            if char.isalpha() or char == "_":
                end = idx + 1
                while end < len(self.formula) and (self.formula[end].isalnum() or self.formula[end] == "_"):
                    end += 1
                value = self.formula[idx:end].upper()
                tokens.append(Token("IDENT", value, idx))
                idx = end
                continue
            raise FormulaError(f"Unsupported token at position {idx}.")
        tokens.append(Token("EOF", "", len(self.formula)))
        return tokens


class FormulaParser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def current(self) -> Token:
        return self.tokens[self.position]

    def consume(self, expected_kind: str | None = None, expected_value: str | None = None) -> Token:
        token = self.current()
        if expected_kind and token.kind != expected_kind:
            raise FormulaError(f"Expected token {expected_kind}, found {token.kind}.")
        if expected_value and token.value != expected_value:
            raise FormulaError(f"Expected token {expected_value}, found {token.value}.")
        self.position += 1
        return token

    def parse(self) -> Any:
        node = self.parse_comparison()
        if self.current().kind != "EOF":
            raise FormulaError("Unexpected trailing tokens.")
        return node

    def parse_comparison(self) -> Any:
        node = self.parse_additive()
        while self.current().kind == "OP" and self.current().value in {"==", "!=", ">", "<", ">=", "<="}:
            operator = self.consume("OP").value
            node = BinaryOpNode(node, operator, self.parse_additive())
        return node

    def parse_additive(self) -> Any:
        node = self.parse_multiplicative()
        while self.current().kind == "OP" and self.current().value in {"+", "-"}:
            operator = self.consume("OP").value
            node = BinaryOpNode(node, operator, self.parse_multiplicative())
        return node

    def parse_multiplicative(self) -> Any:
        node = self.parse_unary()
        while self.current().kind == "OP" and self.current().value in {"*", "/"}:
            operator = self.consume("OP").value
            node = BinaryOpNode(node, operator, self.parse_unary())
        return node

    def parse_unary(self) -> Any:
        token = self.current()
        if token.kind == "OP" and token.value in {"+", "-"}:
            operator = self.consume("OP").value
            return UnaryOpNode(operator, self.parse_unary())
        if token.kind == "IDENT" and token.value == "NOT":
            self.consume("IDENT")
            return UnaryOpNode("NOT", self.parse_unary())
        return self.parse_primary()

    def parse_primary(self) -> Any:
        token = self.current()
        if token.kind == "NUMBER":
            self.consume("NUMBER")
            return NumberNode(float(token.value))
        if token.kind == "STRING":
            self.consume("STRING")
            return StringNode(token.value)
        if token.kind == "(":
            self.consume("(")
            node = self.parse_comparison()
            self.consume(")")
            return node
        if token.kind == "IDENT":
            identifier = self.consume("IDENT").value
            if identifier == "TRUE":
                return BooleanNode(True)
            if identifier == "FALSE":
                return BooleanNode(False)
            if self.current().kind == "(":
                self.consume("(")
                args = []
                if self.current().kind != ")":
                    while True:
                        args.append(self.parse_comparison())
                        if self.current().kind != ",":
                            break
                        self.consume(",")
                self.consume(")")
                return FunctionNode(identifier, args)
            if self._looks_like_reference(identifier):
                if self.current().kind == ":":
                    self.consume(":")
                    end = self.consume("IDENT").value
                    if not self._looks_like_reference(end):
                        raise FormulaError("Range end must be a cell reference.")
                    return RangeNode(identifier, end)
                return CellNode(identifier)
            raise FormulaError(f"Unknown identifier '{identifier}'.")
        raise FormulaError(f"Unexpected token {token.kind}.")

    @staticmethod
    def _looks_like_reference(value: str) -> bool:
        try:
            coordinate_to_position(value)
            return True
        except ValueError:
            return False


def parse_formula(formula: str) -> Any:
    tokens = FormulaTokenizer(formula).tokenize()
    return FormulaParser(tokens).parse()


def collect_references(node: Any) -> set[tuple[int, int]]:
    references: set[tuple[int, int]] = set()

    def visit(current: Any) -> None:
        if isinstance(current, CellNode):
            references.add(coordinate_to_position(current.reference))
        elif isinstance(current, RangeNode):
            references.update(iter_range(coordinate_to_position(current.start), coordinate_to_position(current.end)))
        elif isinstance(current, UnaryOpNode):
            visit(current.operand)
        elif isinstance(current, BinaryOpNode):
            visit(current.left)
            visit(current.right)
        elif isinstance(current, FunctionNode):
            for arg in current.args:
                visit(arg)

    visit(node)
    return references


class EvaluationContext:
    def __init__(self, cell_lookup):
        self.cell_lookup = cell_lookup

    def get_cell_value(self, row_position: int, column_position: int) -> Any:
        return self.cell_lookup(row_position, column_position)

    def get_range_values(self, start: str, end: str) -> list[Any]:
        start_pos = coordinate_to_position(start)
        end_pos = coordinate_to_position(end)
        return [self.get_cell_value(row, col) for row, col in iter_range(start_pos, end_pos)]


class FormulaEvaluator:
    def __init__(self, context: EvaluationContext):
        self.context = context
        self.function_map = {
            "SUM": self._sum,
            "AVERAGE": self._average,
            "MIN": self._min,
            "MAX": self._max,
            "COUNT": self._count,
            "IF": self._if,
            "AND": self._and,
            "OR": self._or,
            "NOT": self._not,
            "CONCAT": self._concat,
            "UPPER": self._upper,
            "LOWER": self._lower,
        }

    def evaluate(self, node: Any) -> Any:
        if isinstance(node, NumberNode):
            return node.value
        if isinstance(node, StringNode):
            return node.value
        if isinstance(node, BooleanNode):
            return node.value
        if isinstance(node, CellNode):
            row, column = coordinate_to_position(node.reference)
            return self.context.get_cell_value(row, column)
        if isinstance(node, RangeNode):
            return self.context.get_range_values(node.start, node.end)
        if isinstance(node, UnaryOpNode):
            return self._evaluate_unary(node)
        if isinstance(node, BinaryOpNode):
            return self._evaluate_binary(node)
        if isinstance(node, FunctionNode):
            function = self.function_map.get(node.name)
            if not function:
                raise FormulaError(f"Unsupported function '{node.name}'.")
            return function(*[self.evaluate(arg) for arg in node.args])
        raise FormulaError("Unsupported AST node.")

    def _evaluate_unary(self, node: UnaryOpNode) -> Any:
        value = self.evaluate(node.operand)
        if node.operator == "+":
            return as_number(value)
        if node.operator == "-":
            return -as_number(value)
        if node.operator == "NOT":
            return not as_boolean(value)
        raise FormulaError(f"Unsupported unary operator '{node.operator}'.")

    def _evaluate_binary(self, node: BinaryOpNode) -> Any:
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        if node.operator == "+":
            return as_number(left) + as_number(right)
        if node.operator == "-":
            return as_number(left) - as_number(right)
        if node.operator == "*":
            return as_number(left) * as_number(right)
        if node.operator == "/":
            denominator = as_number(right)
            if denominator == 0:
                raise FormulaError("Division by zero.")
            return as_number(left) / denominator
        if node.operator == "==":
            return left == right
        if node.operator == "!=":
            return left != right
        if node.operator == ">":
            return self._compare(left, right, ">")
        if node.operator == "<":
            return self._compare(left, right, "<")
        if node.operator == ">=":
            return self._compare(left, right, ">=")
        if node.operator == "<=":
            return self._compare(left, right, "<=")
        raise FormulaError(f"Unsupported operator '{node.operator}'.")

    @staticmethod
    def _compare(left: Any, right: Any, operator: str) -> bool:
        try:
            left_value = as_number(left)
            right_value = as_number(right)
        except ValueError:
            left_value = "" if left is None else str(left)
            right_value = "" if right is None else str(right)
        if operator == ">":
            return left_value > right_value
        if operator == "<":
            return left_value < right_value
        if operator == ">=":
            return left_value >= right_value
        return left_value <= right_value

    def _flatten_args(self, *args: Any) -> list[Any]:
        return [value for value in flatten(args)]

    def _sum(self, *args: Any) -> float:
        return sum(as_number(value) for value in self._flatten_args(*args))

    def _average(self, *args: Any) -> float:
        values = [as_number(value) for value in self._flatten_args(*args)]
        if not values:
            return 0.0
        return sum(values) / len(values)

    def _min(self, *args: Any) -> float:
        values = [as_number(value) for value in self._flatten_args(*args)]
        if not values:
            raise FormulaError("MIN requires at least one value.")
        return min(values)

    def _max(self, *args: Any) -> float:
        values = [as_number(value) for value in self._flatten_args(*args)]
        if not values:
            raise FormulaError("MAX requires at least one value.")
        return max(values)

    def _count(self, *args: Any) -> int:
        return sum(1 for value in self._flatten_args(*args) if value not in (None, ""))

    def _if(self, condition: Any, true_value: Any, false_value: Any) -> Any:
        return true_value if as_boolean(condition) else false_value

    def _and(self, *args: Any) -> bool:
        return all(as_boolean(value) for value in self._flatten_args(*args))

    def _or(self, *args: Any) -> bool:
        return any(as_boolean(value) for value in self._flatten_args(*args))

    def _not(self, value: Any) -> bool:
        return not as_boolean(value)

    def _concat(self, *args: Any) -> str:
        return "".join("" if value is None else str(value) for value in self._flatten_args(*args))

    def _upper(self, value: Any) -> str:
        return str("" if value is None else value).upper()

    def _lower(self, value: Any) -> str:
        return str("" if value is None else value).lower()


def build_dependency_map(pairs: list[tuple[tuple[int, int], tuple[int, int]]]) -> dict[tuple[int, int], set[tuple[int, int]]]:
    graph: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for source, dependency in pairs:
        graph[source].add(dependency)
    return graph


def detect_cycle(graph: dict[tuple[int, int], set[tuple[int, int]]]) -> None:
    temporary: set[tuple[int, int]] = set()
    permanent: set[tuple[int, int]] = set()

    def visit(node: tuple[int, int]) -> None:
        if node in permanent:
            return
        if node in temporary:
            raise FormulaError("Circular reference detected.")
        temporary.add(node)
        for dependency in graph.get(node, set()):
            if dependency in graph:
                visit(dependency)
        temporary.remove(node)
        permanent.add(node)

    for node in list(graph):
        visit(node)
