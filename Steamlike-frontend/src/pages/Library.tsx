import React, { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import ApiAlert from "../components/ApiAlert";
import ToastMessage from "../components/ToastMessage";
import { apiFetch } from "../lib/api";
import type { CatalogItem, LibraryEntry } from "../lib/types";

type LibraryRow = LibraryEntry & { title?: string; thumb?: string };

export default function Library() {
  const [items, setItems] = useState<LibraryRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState<{ status: number; error: any } | null>(null);
  const [q, setQ] = useState("");

  const navigate = useNavigate();
  const location = useLocation();

  const [success, setSuccess] = useState("");

  const filtered = useMemo(() => {
    const s = q.trim().toLowerCase();
    if (!s) return items;
    return items.filter((x) =>
      (x.title || x.external_game_id).toLowerCase().includes(s)
    );
  }, [items, q]);

  async function load() {
    setLoading(true);
    setErr(null);

    const r = await apiFetch<LibraryEntry[]>("/api/library/entries/");
    if (!r.ok) {
      setErr(r);
      setLoading(false);
      return;
    }

    const entries = r.data;

    // Enriquecer con catálogo (resolve) para mostrar títulos/miniaturas
    const ids = entries.map((e) => e.external_game_id);
    let catalog: CatalogItem[] = [];

    if (ids.length) {
      const cr = await apiFetch<CatalogItem[]>("/api/catalog/resolve/", {
        method: "POST",
        json: { external_game_ids: ids },
      });

      if (cr.ok) catalog = cr.data;
    }

    const byId = new Map(
      catalog.map((c) => [c.external_game_id, c])
    );

    setItems(
      entries.map((e) => {
        const c = byId.get(e.external_game_id);
        return {
          ...e,
          title: c?.title,
          thumb: c?.thumb,
        };
      })
    );

    setLoading(false);
  }

  useEffect(() => {
    load();
  }, []);

  async function deleteEntry(id: number) {
    if (!confirm("¿Seguro que deseas eliminar este juego de tu biblioteca?")) {
      return;
    }

    setErr(null);

    const r = await apiFetch<null>(`/api/library/entries/${id}/`, {
      method: "DELETE",
    });

    if (r.ok) {
      // Elimina la fila de la tabla
      setItems((prev) => prev.filter((item) => item.id !== id));

      // Muestra el toast
      setSuccess("🗑 Juego eliminado correctamente.");

      setTimeout(() => {
        setSuccess("");
      }, 3000);
    } else {
      setErr(r);
    }
  }

  // Mostrar toast recibido desde navigate(...)
  useEffect(() => {
    const toast = (location.state as any)?.toast;

    if (toast) {
      setSuccess(toast);

      // Limpiamos el state para que no vuelva a aparecer
      navigate(location.pathname, {
        replace: true,
        state: {},
      });

      const timer = setTimeout(() => {
        setSuccess("");
      }, 3000);

      return () => clearTimeout(timer);
    }
  }, [location, navigate]);

  function statusBadge(status: LibraryEntry["status"]) {
    const map: Record<string, string> = {
      wishlist: "secondary",
      playing: "primary",
      completed: "success",
      dropped: "danger",
    };

    const cls = map[status] || "secondary";

    return (
      <span className={`badge text-bg-${cls}`}>
        {status}
      </span>
    );
  }

  return (
    <div>
      <ToastMessage
        show={!!success}
        message={success}
        onClose={() => setSuccess("")}
      />

      <div className="d-flex align-items-center justify-content-between gap-2 flex-wrap mb-3">
        <h1 className="h4 m-0">Mi biblioteca</h1>

        <div className="d-flex gap-2">
          <input
            className="form-control"
            style={{ maxWidth: 260 }}
            placeholder="Filtrar por título/ID"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />

          <Link className="btn btn-primary" to="/library/new">
            Añadir
          </Link>

          <button
            className="btn btn-outline-secondary"
            onClick={load}
          >
            Refrescar
          </button>
        </div>
      </div>

      {err && (
        <>
          {err.status === 401 && err.error?.error === "unauthorized" ? (
            <div className="alert alert-info">
              Necesitas{" "}
              <Link to="/auth/login">login</Link> para ver tu biblioteca.
            </div>
          ) : (
            <ApiAlert status={err.status} error={err.error} />
          )}
        </>
      )}

      {loading ? (
        <div className="text-secondary">Cargando…</div>
      ) : (
        <div className="table-responsive">
          <table className="table align-middle">
            <thead>
              <tr>
                <th style={{ width: 72 }}></th>
                <th>Juego</th>
                <th>Estado</th>
                <th className="text-end">Horas</th>
                <th style={{ width: 220 }}></th>
              </tr>
            </thead>

            <tbody>
              {filtered.length === 0 ? (
                <tr>
                  <td colSpan={5}>
                    <div className="empty-state">
                      <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>🎮</div>
                      <div className="fw-semibold mb-1">
                        {items.length === 0
                          ? "Tu biblioteca todavía está vacía."
                          : "No hay resultados para este filtro."}
                      </div>
                      <div>
                        {items.length === 0
                          ? "Añade tu primer juego desde el catálogo o crea una entrada manualmente."
                          : "Prueba con otro nombre o limpia el filtro para ver todos tus juegos."}
                      </div>
                    </div>
                  </td>
                </tr>
              ) : (
                filtered.map((x) => (
                  <tr key={x.id}>
                    <td>
                      {x.thumb ? (
                        <img
                          src={x.thumb}
                          alt=""
                          style={{
                            width: 56,
                            height: 56,
                            objectFit: "cover",
                          }}
                          className="rounded border"
                        />
                      ) : (
                        <div
                          className="rounded border bg-light"
                          style={{ width: 56, height: 56 }}
                        ></div>
                      )}
                    </td>

                    <td>
                      <div className="fw-semibold">
                        {x.title || "(sin título)"}
                      </div>

                      <div className="small text-secondary">
                        external_game_id: {x.external_game_id}
                      </div>
                    </td>

                    <td>{statusBadge(x.status)}</td>

                    <td className="text-end">
                      {x.hours_played}
                    </td>

                    <td className="text-end">
                      <div className="d-flex justify-content-end gap-2">

                        <Link
                          className="btn btn-outline-primary btn-sm"
                          to={`/library/${x.id}`}
                        >
                          Abrir
                        </Link>

                        <button
                          className="btn btn-outline-danger btn-sm"
                          onClick={() => deleteEntry(x.id)}
                        >
                          🗑 Eliminar
                        </button>

                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}