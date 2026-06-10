from __future__ import annotations

import json

from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from .formula_engine import FormulaError
from .services import FormulaService, SpreadsheetService, serialize_cell, serialize_grid


class JsonView(View):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except (FormulaError, ValueError, KeyError) as exc:
            return self.render_json({"error": str(exc)}, status=400)

    def parse_body(self, request: HttpRequest) -> dict:
        if not request.body:
            return {}
        return json.loads(request.body.decode("utf-8"))

    def render_json(self, payload: dict, status: int = 200) -> JsonResponse:
        return JsonResponse(payload, status=status)


class AuthenticatedJsonView(JsonView):
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.render_json({"error": "Authentication required."}, status=401)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfTokenView(JsonView):
    def get(self, request: HttpRequest) -> JsonResponse:
        return self.render_json({"status": "ok", "csrf_token": get_token(request)})


class SessionStateView(JsonView):
    def get(self, request: HttpRequest) -> JsonResponse:
        if not request.user.is_authenticated:
            return self.render_json({"user": None})
        return self.render_json({"user": {"id": request.user.id, "username": request.user.username}})


class SessionLoginView(JsonView):
    def post(self, request: HttpRequest) -> JsonResponse:
        payload = self.parse_body(request)
        user = authenticate(
            request,
            username=payload.get("username", ""),
            password=payload.get("password", ""),
        )
        if not user:
            return self.render_json({"error": "Invalid credentials."}, status=401)
        login(request, user)
        return self.render_json({"user": {"id": user.id, "username": user.username}})


class SessionLogoutView(AuthenticatedJsonView):
    def post(self, request: HttpRequest) -> JsonResponse:
        logout(request)
        return self.render_json({"status": "logged_out"})


class SpreadsheetListCreateView(AuthenticatedJsonView):
    def get(self, request: HttpRequest) -> JsonResponse:
        spreadsheets = request.user.spreadsheets.all()
        return self.render_json(
            {
                "results": [
                    {
                        "id": str(sheet.id),
                        "title": sheet.title,
                        "slug": sheet.slug,
                        "row_count": sheet.row_count,
                        "column_count": sheet.column_count,
                        "updated_at": sheet.updated_at.isoformat(),
                    }
                    for sheet in spreadsheets
                ]
            }
        )

    def post(self, request: HttpRequest) -> JsonResponse:
        payload = self.parse_body(request)
        spreadsheet = SpreadsheetService.create_spreadsheet(
            owner=request.user,
            title=payload.get("title", "Untitled Spreadsheet"),
            initial_rows=int(payload.get("initial_rows", 100)),
            initial_columns=int(payload.get("initial_columns", 26)),
        )
        return self.render_json({"id": str(spreadsheet.id), "slug": spreadsheet.slug}, status=201)


class SpreadsheetDetailView(AuthenticatedJsonView):
    def delete(self, request: HttpRequest, spreadsheet_id: str) -> JsonResponse:
        spreadsheet = get_object_or_404(request.user.spreadsheets, id=spreadsheet_id)
        SpreadsheetService.delete_spreadsheet(spreadsheet=spreadsheet)
        return self.render_json({"status": "deleted"})


class SpreadsheetGridView(AuthenticatedJsonView):
    def get(self, request: HttpRequest, spreadsheet_id: str) -> JsonResponse:
        spreadsheet = get_object_or_404(request.user.spreadsheets, id=spreadsheet_id)
        window = SpreadsheetService.fetch_grid(
            spreadsheet=spreadsheet,
            row_start=int(request.GET.get("row_start", 1)),
            row_end=int(request.GET["row_end"]) if request.GET.get("row_end") else None,
            column_start=int(request.GET.get("column_start", 1)),
            column_end=int(request.GET["column_end"]) if request.GET.get("column_end") else None,
        )
        return self.render_json(serialize_grid(window))


class ColumnCollectionView(AuthenticatedJsonView):
    def post(self, request: HttpRequest, spreadsheet_id: str) -> JsonResponse:
        spreadsheet = get_object_or_404(request.user.spreadsheets, id=spreadsheet_id)
        payload = self.parse_body(request)
        column = SpreadsheetService.add_column(
            spreadsheet=spreadsheet,
            label=payload.get("label"),
            data_type=payload.get("data_type", "text"),
        )
        return self.render_json(
            {
                "position": column.position,
                "label": column.label,
                "data_type": column.data_type,
                "width": column.width,
            },
            status=201,
        )


class ColumnDetailView(AuthenticatedJsonView):
    def delete(self, request: HttpRequest, spreadsheet_id: str, column_position: int) -> JsonResponse:
        spreadsheet = get_object_or_404(request.user.spreadsheets, id=spreadsheet_id)
        SpreadsheetService.delete_column(spreadsheet=spreadsheet, column_position=column_position)
        return self.render_json({"status": "deleted"})


class RowCollectionView(AuthenticatedJsonView):
    def post(self, request: HttpRequest, spreadsheet_id: str) -> JsonResponse:
        spreadsheet = get_object_or_404(request.user.spreadsheets, id=spreadsheet_id)
        row = SpreadsheetService.add_row(spreadsheet=spreadsheet)
        return self.render_json({"position": row.position, "height": row.height}, status=201)


class RowDetailView(AuthenticatedJsonView):
    def delete(self, request: HttpRequest, spreadsheet_id: str, row_position: int) -> JsonResponse:
        spreadsheet = get_object_or_404(request.user.spreadsheets, id=spreadsheet_id)
        SpreadsheetService.delete_row(spreadsheet=spreadsheet, row_position=row_position)
        return self.render_json({"status": "deleted"})


class CellUpdateView(AuthenticatedJsonView):
    def post(self, request: HttpRequest, spreadsheet_id: str) -> JsonResponse:
        spreadsheet = get_object_or_404(request.user.spreadsheets, id=spreadsheet_id)
        payload = self.parse_body(request)
        cell = FormulaService.update_cell(
            spreadsheet=spreadsheet,
            row_position=int(payload["row_position"]),
            column_position=int(payload["column_position"]),
            raw_input=payload.get("raw_input", ""),
        )
        return self.render_json({"cell": serialize_cell(cell)})


class CellBatchUpdateView(AuthenticatedJsonView):
    def post(self, request: HttpRequest, spreadsheet_id: str) -> JsonResponse:
        spreadsheet = get_object_or_404(request.user.spreadsheets, id=spreadsheet_id)
        payload = self.parse_body(request)
        cells = FormulaService.batch_update(
            spreadsheet=spreadsheet,
            updates=payload.get("updates", []),
        )
        return self.render_json({"updated_count": len(cells), "cells": [serialize_cell(cell) for cell in cells]})
