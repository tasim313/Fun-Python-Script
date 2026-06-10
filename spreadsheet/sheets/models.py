from __future__ import annotations

import uuid

from django.conf import settings
from django.db import models

from .utils import column_index_to_label, position_to_coordinate


class Spreadsheet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="spreadsheets",
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    row_count = models.PositiveIntegerField(default=0)
    column_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(fields=["owner", "slug"], name="uniq_sheet_slug_per_owner")
        ]

    def __str__(self) -> str:
        return self.title


class SheetColumn(models.Model):
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, related_name="columns")
    position = models.PositiveIntegerField()
    label = models.CharField(max_length=16)
    data_type = models.CharField(max_length=16, default="text")
    width = models.PositiveIntegerField(default=140)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(fields=["spreadsheet", "position"], name="uniq_sheet_column_position")
        ]
        indexes = [
            models.Index(fields=["spreadsheet", "position"]),
        ]

    def save(self, *args, **kwargs):
        if not self.label:
            self.label = column_index_to_label(self.position)
        super().save(*args, **kwargs)


class SheetRow(models.Model):
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, related_name="rows")
    position = models.PositiveIntegerField()
    height = models.PositiveIntegerField(default=34)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(fields=["spreadsheet", "position"], name="uniq_sheet_row_position")
        ]
        indexes = [
            models.Index(fields=["spreadsheet", "position"]),
        ]


class Cell(models.Model):
    VALUE_TYPES = [
        ("blank", "Blank"),
        ("text", "Text"),
        ("number", "Number"),
        ("boolean", "Boolean"),
        ("date", "Date"),
        ("error", "Error"),
    ]

    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, related_name="cells")
    row = models.ForeignKey(SheetRow, on_delete=models.CASCADE, related_name="cells")
    column = models.ForeignKey(SheetColumn, on_delete=models.CASCADE, related_name="cells")
    row_position = models.PositiveIntegerField()
    column_position = models.PositiveIntegerField()
    raw_input = models.TextField(blank=True, default="")
    value_type = models.CharField(max_length=16, choices=VALUE_TYPES, default="blank")
    computed_value = models.JSONField(null=True, blank=True)
    error_message = models.CharField(max_length=255, blank=True, default="")
    version = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["spreadsheet", "row", "column"], name="uniq_cell_row_column"),
            models.UniqueConstraint(
                fields=["spreadsheet", "row_position", "column_position"],
                name="uniq_cell_position_in_sheet",
            ),
        ]
        indexes = [
            models.Index(fields=["spreadsheet", "row_position", "column_position"]),
            models.Index(fields=["spreadsheet", "column_position", "row_position"]),
            models.Index(fields=["spreadsheet", "updated_at"]),
        ]

    @property
    def coordinate(self) -> str:
        return position_to_coordinate(self.row_position, self.column_position)

    def sync_positions(self) -> None:
        self.row_position = self.row.position
        self.column_position = self.column.position


class CellDependency(models.Model):
    spreadsheet = models.ForeignKey(Spreadsheet, on_delete=models.CASCADE, related_name="dependencies")
    source_cell = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name="dependencies")
    depends_on_row_position = models.PositiveIntegerField()
    depends_on_column_position = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source_cell", "depends_on_row_position", "depends_on_column_position"],
                name="uniq_cell_dependency",
            )
        ]
        indexes = [
            models.Index(fields=["spreadsheet", "depends_on_row_position", "depends_on_column_position"]),
            models.Index(fields=["spreadsheet", "source_cell"]),
        ]
