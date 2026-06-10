export type UserPayload = {
  id: number;
  username: string;
};

export type SpreadsheetSummary = {
  id: string;
  title: string;
  slug: string;
  row_count: number;
  column_count: number;
  updated_at: string;
};

export type ColumnPayload = {
  position: number;
  label: string;
  data_type: string;
  width: number;
};

export type RowPayload = {
  position: number;
  height: number;
};

export type CellPayload = {
  coordinate: string;
  row_position: number;
  column_position: number;
  raw_input: string;
  value_type: string;
  computed_value: string | number | boolean | null;
  error_message: string;
  version: number;
};

export type GridResponse = {
  spreadsheet: {
    id: string;
    title: string;
    slug: string;
    row_count: number;
    column_count: number;
  };
  rows: RowPayload[];
  columns: ColumnPayload[];
  cells: CellPayload[];
};

async function ensureCsrfToken() {
  const response = await fetch("/api/auth/session/csrf/", {
    credentials: "include",
  });
  const payload = await response.json();
  return payload.csrf_token as string;
}

async function request<T>(url: string, init: RequestInit = {}): Promise<T> {
  const method = init.method?.toUpperCase() ?? "GET";
  const headers = new Headers(init.headers ?? {});
  if (method !== "GET" && method !== "HEAD") {
    const token = (await ensureCsrfToken()) ?? "";
    headers.set("X-CSRFToken", token);
    if (!headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }
  }
  const response = await fetch(url, {
    ...init,
    headers,
    credentials: "include",
  });
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.error ?? "Request failed.");
  }
  return payload as T;
}

export async function fetchSession() {
  return request<{ user: UserPayload | null }>("/api/auth/session/");
}

export async function login(username: string, password: string) {
  return request<{ user: UserPayload }>("/api/auth/session/login/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

export async function logout() {
  return request<{ status: string }>("/api/auth/session/logout/", {
    method: "POST",
  });
}

export async function fetchSpreadsheets() {
  return request<{ results: SpreadsheetSummary[] }>("/api/spreadsheets/");
}

export async function createSpreadsheet(title: string) {
  return request<{ id: string; slug: string }>("/api/spreadsheets/", {
    method: "POST",
    body: JSON.stringify({
      title,
      initial_rows: 30,
      initial_columns: 12,
    }),
  });
}

export async function fetchGrid(
  spreadsheetId: string,
  viewport: { rowStart?: number; rowEnd?: number; columnStart?: number; columnEnd?: number } = {},
) {
  const params = new URLSearchParams();
  if (viewport.rowStart) params.set("row_start", String(viewport.rowStart));
  if (viewport.rowEnd) params.set("row_end", String(viewport.rowEnd));
  if (viewport.columnStart) params.set("column_start", String(viewport.columnStart));
  if (viewport.columnEnd) params.set("column_end", String(viewport.columnEnd));
  return request<GridResponse>(`/api/spreadsheets/${spreadsheetId}/grid/?${params.toString()}`);
}

export async function updateCell(spreadsheetId: string, row: number, column: number, rawInput: string) {
  return request<{ cell: CellPayload }>(`/api/spreadsheets/${spreadsheetId}/cells/`, {
    method: "POST",
    body: JSON.stringify({
      row_position: row,
      column_position: column,
      raw_input: rawInput,
    }),
  });
}
