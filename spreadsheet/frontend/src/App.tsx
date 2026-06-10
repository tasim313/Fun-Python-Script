import { FormEvent, useEffect, useState, useTransition } from "react";
import {
  createSpreadsheet,
  fetchSession,
  fetchSpreadsheets,
  login,
  logout,
  SpreadsheetSummary,
} from "./api/spreadsheet";
import { SpreadsheetGrid } from "./components/SpreadsheetGrid";

export default function App() {
  const [isPending, startTransition] = useTransition();
  const [user, setUser] = useState<{ id: number; username: string } | null>(null);
  const [spreadsheets, setSpreadsheets] = useState<SpreadsheetSummary[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [newTitle, setNewTitle] = useState("Product Metrics");

  useEffect(() => {
    void (async () => {
      try {
        const session = await fetchSession();
        if (session.user) {
          const nextSheets = await fetchSpreadsheets();
          startTransition(() => {
            setUser(session.user);
            setSpreadsheets(nextSheets.results);
            setSelectedId(nextSheets.results[0]?.id ?? null);
          });
        }
      } catch {
        setUser(null);
      }
    })();
  }, []);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    try {
      const response = await login(credentials.username, credentials.password);
      setUser(response.user);
      const nextSheets = await fetchSpreadsheets();
      setSpreadsheets(nextSheets.results);
      setSelectedId(nextSheets.results[0]?.id ?? null);
    } catch (loginError) {
      setError(loginError instanceof Error ? loginError.message : "Unable to sign in.");
    }
  }

  async function handleCreateSpreadsheet(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    try {
      const spreadsheet = await createSpreadsheet(newTitle);
      const nextSheets = await fetchSpreadsheets();
      setSpreadsheets(nextSheets.results);
      setSelectedId(spreadsheet.id);
      setNewTitle("Untitled Spreadsheet");
    } catch (createError) {
      setError(createError instanceof Error ? createError.message : "Unable to create spreadsheet.");
    }
  }

  async function handleLogout() {
    await logout();
    setUser(null);
    setSpreadsheets([]);
    setSelectedId(null);
  }

  if (!user) {
    return (
      <main className="shell shell-auth">
        <section className="hero-card">
          <p className="eyebrow">Spreadsheet SaaS</p>
          <h1>Excel-style sheets in the browser, backed by Django and PostgreSQL.</h1>
          <p className="hero-copy">
            Sign in to create workbooks, edit cells, and calculate formulas with a safe parser.
          </p>
        </section>

        <section className="auth-card">
          <h2>Sign in</h2>
          <form onSubmit={handleLogin} className="stack">
            <label className="field">
              <span>Username</span>
              <input
                value={credentials.username}
                onChange={(event) => setCredentials((current) => ({ ...current, username: event.target.value }))}
                placeholder="alice"
                autoComplete="username"
              />
            </label>
            <label className="field">
              <span>Password</span>
              <input
                type="password"
                value={credentials.password}
                onChange={(event) => setCredentials((current) => ({ ...current, password: event.target.value }))}
                placeholder="password"
                autoComplete="current-password"
              />
            </label>
            {error ? <p className="error-banner">{error}</p> : null}
            <button type="submit" className="primary-button" disabled={isPending}>
              {isPending ? "Checking..." : "Enter Workspace"}
            </button>
          </form>
        </section>
      </main>
    );
  }

  return (
    <main className="shell shell-app">
      <aside className="sidebar">
        <div className="sidebar-header">
          <p className="eyebrow">Workspace</p>
          <h1>{user.username}</h1>
          <button type="button" className="ghost-button" onClick={handleLogout}>
            Sign out
          </button>
        </div>

        <form onSubmit={handleCreateSpreadsheet} className="stack">
          <label className="field">
            <span>New spreadsheet</span>
            <input value={newTitle} onChange={(event) => setNewTitle(event.target.value)} />
          </label>
          <button type="submit" className="primary-button">
            Create Sheet
          </button>
        </form>

        <div className="sheet-list">
          {spreadsheets.map((sheet) => (
            <button
              key={sheet.id}
              type="button"
              className={`sheet-list-item ${selectedId === sheet.id ? "active" : ""}`}
              onClick={() => setSelectedId(sheet.id)}
            >
              <strong>{sheet.title}</strong>
              <span>
                {sheet.row_count} rows · {sheet.column_count} columns
              </span>
            </button>
          ))}
          {!spreadsheets.length ? <p className="empty-state">No spreadsheets yet. Create your first one.</p> : null}
        </div>
      </aside>

      <section className="workspace">
        {selectedId ? (
          <SpreadsheetGrid
            key={selectedId}
            spreadsheetId={selectedId}
            spreadsheetTitle={spreadsheets.find((sheet) => sheet.id === selectedId)?.title ?? "Spreadsheet"}
          />
        ) : (
          <div className="empty-canvas">Choose a spreadsheet to begin editing.</div>
        )}
      </section>
    </main>
  );
}
