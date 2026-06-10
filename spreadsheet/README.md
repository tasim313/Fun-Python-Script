# Spreadsheet SaaS

Production-oriented Django spreadsheet backend with an Excel-style formula engine, PostgreSQL-ready schema, and React grid integration guidance.

## Architecture

Request flow:

1. React grid issues debounced edits or windowed fetch requests.
2. Django API authenticates the user and validates payloads.
3. Service layer persists structural changes or cell edits inside a transaction.
4. Formula engine tokenizes, parses, evaluates, and recalculates impacted cells only.
5. PostgreSQL stores normalized sheet metadata, sparse cells, and dependency edges.
6. API returns a viewport payload ready for AG Grid or Handsontable.

## Data model

- `Spreadsheet`: workbook-level metadata, ownership, and counts.
- `SheetColumn`: ordered column definitions with type hints and widths.
- `SheetRow`: ordered row records for virtualization and structural changes.
- `Cell`: sparse storage of non-empty cells and formula outputs.
- `CellDependency`: dependency edges for recalculation and circular reference detection.

The schema is PostgreSQL-optimized with compound indexes on hot access paths:

- `(spreadsheet_id, row_position, column_position)` for viewport reads and direct cell updates.
- `(spreadsheet_id, column_position, row_position)` for column-oriented scans and aggregations.
- `(spreadsheet_id, depends_on_row_position, depends_on_column_position)` for reverse dependency traversal.

## Formula engine

Supported features:

- Arithmetic: `+`, `-`, `*`, `/`
- Aggregation: `SUM`, `AVERAGE`, `MIN`, `MAX`, `COUNT`
- Conditional: `IF`
- Logical: `AND`, `OR`, `NOT`
- Text: `CONCAT`, `UPPER`, `LOWER`
- References: `A1`, `B2`, `A1:A10`

Safety:

- No Python `eval()`
- No JavaScript `eval()`
- Custom tokenizer, parser, AST evaluator, and dependency graph

## API surface

- `POST /api/auth/session/login/`
- `POST /api/auth/session/logout/`
- `GET /api/spreadsheets/`
- `POST /api/spreadsheets/`
- `DELETE /api/spreadsheets/{id}/`
- `GET /api/spreadsheets/{id}/grid/?row_start=1&row_end=200&column_start=1&column_end=50`
- `POST /api/spreadsheets/{id}/rows/`
- `DELETE /api/spreadsheets/{id}/rows/{position}/`
- `POST /api/spreadsheets/{id}/columns/`
- `DELETE /api/spreadsheets/{id}/columns/{position}/`
- `POST /api/spreadsheets/{id}/cells/`
- `POST /api/spreadsheets/{id}/cells/batch/`

## Frontend integration

Recommended stack:

- React 18+
- AG Grid Community or Handsontable
- Windowed grid rendering with server-side viewport fetches
- Debounced cell writes every 150-250ms
- Batch API flush on paste/fill operations

Editing lifecycle:

1. Grid opens an editor and keeps optimistic local state.
2. On commit, send `{row_position, column_position, raw_input}` or batch updates.
3. Refresh impacted viewport or merge returned cells locally.
4. Use WebSocket invalidation for multi-user collaboration.

## Performance strategy

- Sparse cell storage keeps empty cells out of the database.
- `bulk_create` seeds rows and columns.
- `bulk_update` recalculates impacted formulas in batches.
- Viewport API fetches only visible windows instead of entire sheets.
- Dependency edges enable partial recalculation instead of full-sheet recompute.
- Redis can cache hot viewports and dependency snapshots in production.
- PostgreSQL partitioning by tenant or workbook family can be added when workbook counts grow.

## Real-time collaboration design

Optional next layer:

- Django Channels with a sheet room per spreadsheet id
- Last-write-wins with per-cell version checks
- Broadcast changed coordinates only, not whole sheets
- Presence and selection overlays stored in Redis

## Security

- Session-based authentication is implemented.
- Workbook ownership is enforced on all API reads and writes.
- Formula execution is sandboxed by a custom parser.
- Inputs are parsed as data, never executed.
- Add rate limiting and audit logging at the reverse proxy for SaaS deployment.

## Running locally

```bash
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Tests

```bash
python3 manage.py test
```
