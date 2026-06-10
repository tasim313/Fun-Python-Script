import { useEffect, useRef, useState, useTransition } from "react";
import { CellPayload, fetchGrid, GridResponse, updateCell } from "../api/spreadsheet";

type EditMap = Record<string, string>;
type SaveState = "idle" | "saving" | "saved" | "error";

function coordinateKey(row: number, column: number) {
  return `${row}:${column}`;
}

function buildCellMap(cells: CellPayload[]) {
  return new Map(cells.map((cell) => [coordinateKey(cell.row_position, cell.column_position), cell]));
}

export function SpreadsheetGrid({
  spreadsheetId,
  spreadsheetTitle,
}: {
  spreadsheetId: string;
  spreadsheetTitle: string;
}) {
  const [isPending, startTransition] = useTransition();
  const [grid, setGrid] = useState<GridResponse | null>(null);
  const [drafts, setDrafts] = useState<EditMap>({});
  const [status, setStatus] = useState<Record<string, SaveState>>({});
  const saveTimers = useRef<Record<string, number>>({});

  useEffect(() => {
    void (async () => {
      const nextGrid = await fetchGrid(spreadsheetId);
      startTransition(() => {
        setGrid(nextGrid);
        setDrafts({});
        setStatus({});
      });
    })();
    return () => {
      Object.values(saveTimers.current).forEach((timer) => window.clearTimeout(timer));
      saveTimers.current = {};
    };
  }, [spreadsheetId]);

  const cellMap = grid ? buildCellMap(grid.cells) : new Map<string, CellPayload>();

  function queueSave(row: number, column: number, rawInput: string) {
    const key = coordinateKey(row, column);
    if (saveTimers.current[key]) {
      window.clearTimeout(saveTimers.current[key]);
    }
    setStatus((current) => ({ ...current, [key]: "saving" }));
    saveTimers.current[key] = window.setTimeout(async () => {
      try {
        const response = await updateCell(spreadsheetId, row, column, rawInput);
        const nextCell = response.cell;
        setGrid((current) => {
          if (!current) return current;
          const nextCells = current.cells.filter(
            (cell) => !(cell.row_position === row && cell.column_position === column),
          );
          return { ...current, cells: [...nextCells, nextCell] };
        });
        setDrafts((current) => {
          const next = { ...current };
          delete next[key];
          return next;
        });
        setStatus((current) => ({ ...current, [key]: "saved" }));
      } catch {
        setStatus((current) => ({ ...current, [key]: "error" }));
      }
    }, 220);
  }

  if (!grid) {
    return <div className="loading-panel">{isPending ? "Loading spreadsheet..." : "Preparing grid..."}</div>;
  }

  return (
    <div className="grid-shell">
      <header className="grid-header">
        <div>
          <p className="eyebrow">Active Spreadsheet</p>
          <h2>{spreadsheetTitle}</h2>
        </div>
        <div className="grid-stats">
          <span>{grid.spreadsheet.row_count} rows</span>
          <span>{grid.spreadsheet.column_count} columns</span>
        </div>
      </header>

      <div className="formula-bar">
        <strong>Formula Engine</strong>
        <span>Supports arithmetic, ranges, IF, logical functions, and text transforms.</span>
      </div>

      <div className="grid-scroll">
        <table className="spreadsheet-table">
          <thead>
            <tr>
              <th className="corner-cell">#</th>
              {grid.columns.map((column) => (
                <th key={column.position}>{column.label}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {grid.rows.map((row) => (
              <tr key={row.position}>
                <th>{row.position}</th>
                {grid.columns.map((column) => {
                  const key = coordinateKey(row.position, column.position);
                  const cell = cellMap.get(key);
                  const value = drafts[key] ?? cell?.raw_input ?? "";
                  const saveState = status[key] ?? "idle";
                  return (
                    <td key={key} data-state={saveState}>
                      <input
                        value={value}
                        onChange={(event) => {
                          const nextValue = event.target.value;
                          setDrafts((current) => ({ ...current, [key]: nextValue }));
                          queueSave(row.position, column.position, nextValue);
                        }}
                        placeholder={cell?.computed_value?.toString() ?? ""}
                      />
                      {cell?.error_message ? <span className="cell-error">{cell.error_message}</span> : null}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
