from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Any

from django.db import transaction
from django.db.models import F
from django.utils.text import slugify

from .formula_engine import (
    EvaluationContext,
    FormulaError,
    FormulaEvaluator,
    build_dependency_map,
    collect_references,
    detect_cycle,
    parse_formula,
)
from .models import Cell, CellDependency, SheetColumn, SheetRow, Spreadsheet
from .utils import column_index_to_label, normalize_result, parse_literal, position_to_coordinate


@dataclass
class GridWindow:
    spreadsheet: Spreadsheet
    rows: list[SheetRow]
    columns: list[SheetColumn]
    cells: list[Cell]


class SpreadsheetService:
    @staticmethod
    @transaction.atomic
    def create_spreadsheet(*, owner, title: str, initial_rows: int = 100, initial_columns: int = 26) -> Spreadsheet:
        base_slug = slugify(title) or "sheet"
        slug = base_slug
        suffix = 1
        while Spreadsheet.objects.filter(owner=owner, slug=slug).exists():
            suffix += 1
            slug = f"{base_slug}-{suffix}"
        spreadsheet = Spreadsheet.objects.create(
            owner=owner,
            title=title,
            slug=slug,
            row_count=initial_rows,
            column_count=initial_columns,
        )
        SheetColumn.objects.bulk_create(
            [
                SheetColumn(spreadsheet=spreadsheet, position=index, label="")
                for index in range(1, initial_columns + 1)
            ]
        )
        SheetRow.objects.bulk_create(
            [SheetRow(spreadsheet=spreadsheet, position=index) for index in range(1, initial_rows + 1)]
        )
        return spreadsheet

    @staticmethod
    @transaction.atomic
    def delete_spreadsheet(*, spreadsheet: Spreadsheet) -> None:
        spreadsheet.delete()

    @staticmethod
    @transaction.atomic
    def add_column(*, spreadsheet: Spreadsheet, label: str | None = None, data_type: str = "text") -> SheetColumn:
        position = spreadsheet.column_count + 1
        column = SheetColumn.objects.create(
            spreadsheet=spreadsheet,
            position=position,
            label=label or "",
            data_type=data_type,
        )
        spreadsheet.column_count = position
        spreadsheet.save(update_fields=["column_count", "updated_at"])
        return column

    @staticmethod
    @transaction.atomic
    def add_row(*, spreadsheet: Spreadsheet) -> SheetRow:
        position = spreadsheet.row_count + 1
        row = SheetRow.objects.create(spreadsheet=spreadsheet, position=position)
        spreadsheet.row_count = position
        spreadsheet.save(update_fields=["row_count", "updated_at"])
        return row

    @staticmethod
    @transaction.atomic
    def delete_row(*, spreadsheet: Spreadsheet, row_position: int) -> None:
        SheetRow.objects.filter(spreadsheet=spreadsheet, position=row_position).delete()
        SheetRow.objects.filter(spreadsheet=spreadsheet, position__gt=row_position).update(position=F("position") - 1)
        Cell.objects.filter(spreadsheet=spreadsheet, row_position__gt=row_position).update(
            row_position=F("row_position") - 1
        )
        CellDependency.objects.filter(spreadsheet=spreadsheet, depends_on_row_position__gt=row_position).update(
            depends_on_row_position=F("depends_on_row_position") - 1
        )
        spreadsheet.row_count = max(spreadsheet.row_count - 1, 0)
        spreadsheet.save(update_fields=["row_count", "updated_at"])
        FormulaService.recalculate_sheet(spreadsheet=spreadsheet)

    @staticmethod
    @transaction.atomic
    def delete_column(*, spreadsheet: Spreadsheet, column_position: int) -> None:
        SheetColumn.objects.filter(spreadsheet=spreadsheet, position=column_position).delete()
        SheetColumn.objects.filter(spreadsheet=spreadsheet, position__gt=column_position).update(
            position=F("position") - 1
        )
        Cell.objects.filter(spreadsheet=spreadsheet, column_position__gt=column_position).update(
            column_position=F("column_position") - 1
        )
        CellDependency.objects.filter(spreadsheet=spreadsheet, depends_on_column_position__gt=column_position).update(
            depends_on_column_position=F("depends_on_column_position") - 1
        )
        shifted_columns = list(spreadsheet.columns.filter(position__gte=column_position).order_by("position"))
        for column in shifted_columns:
            column.label = column_index_to_label(column.position)
        if shifted_columns:
            SheetColumn.objects.bulk_update(shifted_columns, ["label"])
        spreadsheet.column_count = max(spreadsheet.column_count - 1, 0)
        spreadsheet.save(update_fields=["column_count", "updated_at"])
        FormulaService.recalculate_sheet(spreadsheet=spreadsheet)

    @staticmethod
    def fetch_grid(
        *,
        spreadsheet: Spreadsheet,
        row_start: int = 1,
        row_end: int | None = None,
        column_start: int = 1,
        column_end: int | None = None,
    ) -> GridWindow:
        row_end = row_end or min(spreadsheet.row_count, row_start + 199)
        column_end = column_end or min(spreadsheet.column_count, column_start + 49)
        rows = list(
            spreadsheet.rows.filter(position__gte=row_start, position__lte=row_end).order_by("position")
        )
        columns = list(
            spreadsheet.columns.filter(position__gte=column_start, position__lte=column_end).order_by("position")
        )
        cells = list(
            spreadsheet.cells.filter(
                row_position__gte=row_start,
                row_position__lte=row_end,
                column_position__gte=column_start,
                column_position__lte=column_end,
            ).order_by("row_position", "column_position")
        )
        return GridWindow(spreadsheet=spreadsheet, rows=rows, columns=columns, cells=cells)


class FormulaService:
    @staticmethod
    @transaction.atomic
    def update_cell(*, spreadsheet: Spreadsheet, row_position: int, column_position: int, raw_input: str) -> Cell:
        row = SheetRow.objects.get(spreadsheet=spreadsheet, position=row_position)
        column = SheetColumn.objects.get(spreadsheet=spreadsheet, position=column_position)
        cell, _ = Cell.objects.get_or_create(
            spreadsheet=spreadsheet,
            row=row,
            column=column,
            defaults={
                "row_position": row_position,
                "column_position": column_position,
            },
        )
        cell.row_position = row_position
        cell.column_position = column_position
        cell.raw_input = raw_input
        cell.version += 1
        if not raw_input.startswith("="):
            value_type, computed_value = parse_literal(raw_input)
            cell.value_type = value_type
            cell.computed_value = computed_value
            cell.error_message = ""
        cell.save()

        FormulaService._sync_dependencies(spreadsheet=spreadsheet, cell=cell)
        FormulaService.recalculate_impacted(spreadsheet=spreadsheet, changed_coordinates={(row_position, column_position)})
        return Cell.objects.get(pk=cell.pk)

    @staticmethod
    @transaction.atomic
    def batch_update(*, spreadsheet: Spreadsheet, updates: list[dict[str, Any]]) -> list[Cell]:
        changed = set()
        updated_coordinates = []
        for payload in updates:
            row_position = int(payload["row_position"])
            column_position = int(payload["column_position"])
            row = SheetRow.objects.get(spreadsheet=spreadsheet, position=row_position)
            column = SheetColumn.objects.get(spreadsheet=spreadsheet, position=column_position)
            cell, _ = Cell.objects.get_or_create(
                spreadsheet=spreadsheet,
                row=row,
                column=column,
                defaults={
                    "row_position": row_position,
                    "column_position": column_position,
                },
            )
            cell.raw_input = payload.get("raw_input", "")
            cell.row_position = row_position
            cell.column_position = column_position
            cell.version += 1
            if not cell.raw_input.startswith("="):
                value_type, computed_value = parse_literal(cell.raw_input)
                cell.value_type = value_type
                cell.computed_value = computed_value
                cell.error_message = ""
            cell.save()
            FormulaService._sync_dependencies(spreadsheet=spreadsheet, cell=cell)
            changed.add((row_position, column_position))
            updated_coordinates.append((row_position, column_position))
        FormulaService.recalculate_impacted(spreadsheet=spreadsheet, changed_coordinates=changed)
        cell_map = {
            (cell.row_position, cell.column_position): cell
            for cell in Cell.objects.filter(spreadsheet=spreadsheet)
        }
        return [cell_map[coordinate] for coordinate in updated_coordinates if coordinate in cell_map]

    @staticmethod
    def _sync_dependencies(*, spreadsheet: Spreadsheet, cell: Cell) -> None:
        CellDependency.objects.filter(source_cell=cell).delete()
        if not cell.raw_input.startswith("="):
            return
        ast = parse_formula(cell.raw_input)
        dependencies = collect_references(ast)
        CellDependency.objects.bulk_create(
            [
                CellDependency(
                    spreadsheet=spreadsheet,
                    source_cell=cell,
                    depends_on_row_position=row_position,
                    depends_on_column_position=column_position,
                )
                for row_position, column_position in sorted(dependencies)
            ]
        )

    @staticmethod
    def _build_graph(spreadsheet: Spreadsheet) -> dict[tuple[int, int], set[tuple[int, int]]]:
        pairs = [
            (
                (dependency.source_cell.row_position, dependency.source_cell.column_position),
                (dependency.depends_on_row_position, dependency.depends_on_column_position),
            )
            for dependency in CellDependency.objects.filter(spreadsheet=spreadsheet).select_related("source_cell")
        ]
        graph = build_dependency_map(pairs)
        detect_cycle(graph)
        return graph

    @staticmethod
    def _collect_impacted(
        *,
        spreadsheet: Spreadsheet,
        changed_coordinates: set[tuple[int, int]],
    ) -> set[tuple[int, int]]:
        reverse_graph: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
        for dependency in CellDependency.objects.filter(spreadsheet=spreadsheet).select_related("source_cell"):
            source = (dependency.source_cell.row_position, dependency.source_cell.column_position)
            target = (dependency.depends_on_row_position, dependency.depends_on_column_position)
            reverse_graph[target].add(source)
        queue = deque(changed_coordinates)
        impacted = set(changed_coordinates)
        while queue:
            current = queue.popleft()
            for source in reverse_graph.get(current, set()):
                if source not in impacted:
                    impacted.add(source)
                    queue.append(source)
        return impacted

    @staticmethod
    def _topological_order(
        *,
        spreadsheet: Spreadsheet,
        impacted: set[tuple[int, int]],
        graph: dict[tuple[int, int], set[tuple[int, int]]],
    ) -> list[tuple[int, int]]:
        order: list[tuple[int, int]] = []
        visited: set[tuple[int, int]] = set()

        def dfs(node: tuple[int, int]) -> None:
            if node in visited:
                return
            visited.add(node)
            for dependency in graph.get(node, set()):
                if dependency in impacted:
                    dfs(dependency)
            order.append(node)

        formula_coordinates = set(
            Cell.objects.filter(spreadsheet=spreadsheet, raw_input__startswith="=").values_list(
                "row_position", "column_position"
            )
        )
        for node in impacted:
            if node in formula_coordinates:
                dfs(node)
        return order

    @staticmethod
    def recalculate_impacted(
        *,
        spreadsheet: Spreadsheet,
        changed_coordinates: set[tuple[int, int]],
    ) -> None:
        graph = FormulaService._build_graph(spreadsheet)
        impacted = FormulaService._collect_impacted(spreadsheet=spreadsheet, changed_coordinates=changed_coordinates)
        order = FormulaService._topological_order(spreadsheet=spreadsheet, impacted=impacted, graph=graph)
        cell_map = {
            (cell.row_position, cell.column_position): cell
            for cell in Cell.objects.filter(spreadsheet=spreadsheet).select_related("row", "column")
        }

        def lookup(row_position: int, column_position: int) -> Any:
            target = cell_map.get((row_position, column_position))
            if not target:
                return None
            if target.value_type == "error":
                raise FormulaError(target.error_message or "Referenced cell contains an error.")
            return target.computed_value

        evaluator = FormulaEvaluator(EvaluationContext(lookup))
        changed_cells = []
        for coordinate in order:
            cell = cell_map.get(coordinate)
            if not cell or not cell.raw_input.startswith("="):
                continue
            try:
                ast = parse_formula(cell.raw_input)
                result = evaluator.evaluate(ast)
                value_type, computed_value = normalize_result(result)
                cell.value_type = value_type
                cell.computed_value = computed_value
                cell.error_message = ""
            except FormulaError as exc:
                cell.value_type = "error"
                cell.computed_value = None
                cell.error_message = str(exc)
            changed_cells.append(cell)
        if changed_cells:
            Cell.objects.bulk_update(changed_cells, ["value_type", "computed_value", "error_message"])

    @staticmethod
    def recalculate_sheet(*, spreadsheet: Spreadsheet) -> None:
        formula_cells = set(
            Cell.objects.filter(spreadsheet=spreadsheet, raw_input__startswith="=").values_list(
                "row_position", "column_position"
            )
        )
        if formula_cells:
            FormulaService.recalculate_impacted(spreadsheet=spreadsheet, changed_coordinates=formula_cells)


def serialize_cell(cell: Cell) -> dict[str, Any]:
    return {
        "coordinate": cell.coordinate,
        "row_position": cell.row_position,
        "column_position": cell.column_position,
        "raw_input": cell.raw_input,
        "value_type": cell.value_type,
        "computed_value": cell.computed_value,
        "error_message": cell.error_message,
        "version": cell.version,
    }


def serialize_grid(window: GridWindow) -> dict[str, Any]:
    return {
        "spreadsheet": {
            "id": str(window.spreadsheet.id),
            "title": window.spreadsheet.title,
            "slug": window.spreadsheet.slug,
            "row_count": window.spreadsheet.row_count,
            "column_count": window.spreadsheet.column_count,
        },
        "rows": [{"position": row.position, "height": row.height} for row in window.rows],
        "columns": [
            {
                "position": column.position,
                "label": column.label,
                "data_type": column.data_type,
                "width": column.width,
            }
            for column in window.columns
        ],
        "cells": [serialize_cell(cell) for cell in window.cells],
    }
