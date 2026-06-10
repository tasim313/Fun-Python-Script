from __future__ import annotations

import math
import re
from datetime import date, datetime
from typing import Any, Iterable, Iterator

CELL_REF_RE = re.compile(r"^(?P<col>[A-Z]+)(?P<row>[1-9][0-9]*)$")


def column_index_to_label(index: int) -> str:
    if index < 1:
        raise ValueError("Column index must be 1 or greater.")
    label = []
    while index:
        index, remainder = divmod(index - 1, 26)
        label.append(chr(65 + remainder))
    return "".join(reversed(label))


def column_label_to_index(label: str) -> int:
    total = 0
    for char in label.upper():
        if not ("A" <= char <= "Z"):
            raise ValueError(f"Invalid column label: {label}")
        total = total * 26 + (ord(char) - 64)
    return total


def coordinate_to_position(reference: str) -> tuple[int, int]:
    match = CELL_REF_RE.match(reference.upper())
    if not match:
        raise ValueError(f"Invalid cell reference: {reference}")
    return int(match.group("row")), column_label_to_index(match.group("col"))


def position_to_coordinate(row_position: int, column_position: int) -> str:
    return f"{column_index_to_label(column_position)}{row_position}"


def iter_range(start: tuple[int, int], end: tuple[int, int]) -> Iterator[tuple[int, int]]:
    start_row, start_col = start
    end_row, end_col = end
    row_min, row_max = sorted((start_row, end_row))
    col_min, col_max = sorted((start_col, end_col))
    for row in range(row_min, row_max + 1):
        for col in range(col_min, col_max + 1):
            yield row, col


def flatten(values: Iterable[Any]) -> Iterator[Any]:
    for value in values:
        if isinstance(value, list):
            yield from flatten(value)
        else:
            yield value


def parse_literal(raw_input: str) -> tuple[str, Any]:
    value = raw_input.strip()
    if raw_input == "":
        return "blank", None
    if value.upper() == "TRUE":
        return "boolean", True
    if value.upper() == "FALSE":
        return "boolean", False
    try:
        if "." in value:
            return "number", float(value)
        return "number", int(value)
    except ValueError:
        pass
    for parser in (date.fromisoformat, datetime.fromisoformat):
        try:
            parsed = parser(value)
            return "date", parsed.isoformat()
        except ValueError:
            continue
    return "text", raw_input


def as_number(value: Any) -> float:
    if value is None or value == "":
        return 0.0
    if isinstance(value, bool):
        return float(value)
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("Numeric value is not finite.")
        return float(value)
    if isinstance(value, str):
        try:
            return float(value)
        except ValueError as exc:
            raise ValueError(f"Cannot convert '{value}' to number.") from exc
    raise ValueError(f"Unsupported numeric value: {value!r}")


def as_boolean(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None or value == "":
        return False
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1"}:
            return True
        if normalized in {"false", "no", "0", ""}:
            return False
    return bool(value)


def normalize_result(value: Any) -> tuple[str, Any]:
    if value is None:
        return "blank", None
    if isinstance(value, bool):
        return "boolean", value
    if isinstance(value, (int, float)):
        return "number", value
    return "text", str(value)
