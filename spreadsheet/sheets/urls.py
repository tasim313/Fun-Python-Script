from django.urls import path

from .views import (
    CellBatchUpdateView,
    CellUpdateView,
    CsrfTokenView,
    ColumnCollectionView,
    ColumnDetailView,
    RowCollectionView,
    RowDetailView,
    SessionStateView,
    SessionLoginView,
    SessionLogoutView,
    SpreadsheetDetailView,
    SpreadsheetGridView,
    SpreadsheetListCreateView,
)

urlpatterns = [
    path("auth/session/csrf/", CsrfTokenView.as_view(), name="session-csrf"),
    path("auth/session/", SessionStateView.as_view(), name="session-state"),
    path("auth/session/login/", SessionLoginView.as_view(), name="session-login"),
    path("auth/session/logout/", SessionLogoutView.as_view(), name="session-logout"),
    path("spreadsheets/", SpreadsheetListCreateView.as_view(), name="spreadsheet-list-create"),
    path("spreadsheets/<uuid:spreadsheet_id>/", SpreadsheetDetailView.as_view(), name="spreadsheet-detail"),
    path("spreadsheets/<uuid:spreadsheet_id>/grid/", SpreadsheetGridView.as_view(), name="spreadsheet-grid"),
    path("spreadsheets/<uuid:spreadsheet_id>/columns/", ColumnCollectionView.as_view(), name="column-create"),
    path(
        "spreadsheets/<uuid:spreadsheet_id>/columns/<int:column_position>/",
        ColumnDetailView.as_view(),
        name="column-delete",
    ),
    path("spreadsheets/<uuid:spreadsheet_id>/rows/", RowCollectionView.as_view(), name="row-create"),
    path(
        "spreadsheets/<uuid:spreadsheet_id>/rows/<int:row_position>/",
        RowDetailView.as_view(),
        name="row-delete",
    ),
    path("spreadsheets/<uuid:spreadsheet_id>/cells/", CellUpdateView.as_view(), name="cell-update"),
    path(
        "spreadsheets/<uuid:spreadsheet_id>/cells/batch/",
        CellBatchUpdateView.as_view(),
        name="cell-batch-update",
    ),
]
