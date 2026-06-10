from django.contrib import admin

from .models import Cell, CellDependency, SheetColumn, SheetRow, Spreadsheet


@admin.register(Spreadsheet)
class SpreadsheetAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "row_count", "column_count", "updated_at")
    search_fields = ("title", "owner__username", "slug")


@admin.register(SheetColumn)
class SheetColumnAdmin(admin.ModelAdmin):
    list_display = ("spreadsheet", "position", "label", "data_type", "width")
    list_filter = ("data_type",)


@admin.register(SheetRow)
class SheetRowAdmin(admin.ModelAdmin):
    list_display = ("spreadsheet", "position", "height")


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ("spreadsheet", "coordinate", "raw_input", "value_type", "computed_value", "error_message")
    search_fields = ("spreadsheet__title", "raw_input")
    list_filter = ("value_type",)


@admin.register(CellDependency)
class CellDependencyAdmin(admin.ModelAdmin):
    list_display = ("spreadsheet", "source_cell", "depends_on_row_position", "depends_on_column_position")
