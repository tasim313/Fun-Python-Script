from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Cell
from .services import FormulaService, SpreadsheetService


class FormulaEngineTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="alice", password="password123")
        self.sheet = SpreadsheetService.create_spreadsheet(
            owner=self.user,
            title="Budget",
            initial_rows=12,
            initial_columns=6,
        )

    def test_arithmetic_and_dependency_recalculation(self):
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=1, column_position=1, raw_input="10")
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=1, column_position=2, raw_input="5")
        result = FormulaService.update_cell(
            spreadsheet=self.sheet,
            row_position=1,
            column_position=3,
            raw_input="=A1+B1",
        )
        self.assertEqual(result.computed_value, 15.0)
        updated = FormulaService.update_cell(
            spreadsheet=self.sheet,
            row_position=1,
            column_position=1,
            raw_input="20",
        )
        self.assertEqual(updated.computed_value, 20)
        self.assertEqual(Cell.objects.get(spreadsheet=self.sheet, row_position=1, column_position=3).computed_value, 25.0)

    def test_supported_functions(self):
        for row, value in enumerate([5, 15, 20], start=1):
            FormulaService.update_cell(
                spreadsheet=self.sheet,
                row_position=row,
                column_position=1,
                raw_input=str(value),
            )
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=1, column_position=2, raw_input='=IF(A2>10,"High","Low")')
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=2, column_position=2, raw_input="=SUM(A1:A3)")
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=3, column_position=2, raw_input="=AVERAGE(A1:A3)")
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=4, column_position=2, raw_input="=COUNT(A1:A3)")
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=5, column_position=2, raw_input="=AND(A2>10,A1<10)")
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=6, column_position=2, raw_input='=CONCAT("Q",A1)')
        self.assertEqual(Cell.objects.get(spreadsheet=self.sheet, row_position=1, column_position=2).computed_value, "High")
        self.assertEqual(Cell.objects.get(spreadsheet=self.sheet, row_position=2, column_position=2).computed_value, 40.0)
        self.assertAlmostEqual(Cell.objects.get(spreadsheet=self.sheet, row_position=3, column_position=2).computed_value, 13.333333333333334)
        self.assertEqual(Cell.objects.get(spreadsheet=self.sheet, row_position=4, column_position=2).computed_value, 3)
        self.assertEqual(Cell.objects.get(spreadsheet=self.sheet, row_position=5, column_position=2).computed_value, True)
        self.assertEqual(Cell.objects.get(spreadsheet=self.sheet, row_position=6, column_position=2).computed_value, "Q5")

    def test_circular_reference_detection(self):
        FormulaService.update_cell(spreadsheet=self.sheet, row_position=1, column_position=1, raw_input="=B1")
        with self.assertRaisesMessage(Exception, "Circular reference detected."):
            FormulaService.update_cell(spreadsheet=self.sheet, row_position=1, column_position=2, raw_input="=A1")


class SpreadsheetApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="bob", password="password123")
        self.client = Client()
        self.client.force_login(self.user)

    def test_create_sheet_and_update_cell(self):
        response = self.client.post(
            reverse("spreadsheet-list-create"),
            data='{"title":"Quarterly Plan","initial_rows":10,"initial_columns":5}',
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        spreadsheet_id = response.json()["id"]

        update_response = self.client.post(
            reverse("cell-update", kwargs={"spreadsheet_id": spreadsheet_id}),
            data='{"row_position":1,"column_position":1,"raw_input":"42"}',
            content_type="application/json",
        )
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json()["cell"]["computed_value"], 42)

        grid_response = self.client.get(reverse("spreadsheet-grid", kwargs={"spreadsheet_id": spreadsheet_id}))
        self.assertEqual(grid_response.status_code, 200)
        self.assertEqual(grid_response.json()["spreadsheet"]["title"], "Quarterly Plan")
