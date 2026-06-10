# React Grid Integration

Pair the Django API with AG Grid or Handsontable using:

- viewport loading via `/api/spreadsheets/{id}/grid/`
- debounced single-cell writes for standard edits
- `/cells/batch/` for paste, autofill, and multi-cell operations
- optimistic UI with server reconciliation on formula outputs
- WebSocket fanout later for collaborative sessions

The backend payload already returns row metadata, column metadata, and sparse cells, which maps cleanly to virtualized grid components.
