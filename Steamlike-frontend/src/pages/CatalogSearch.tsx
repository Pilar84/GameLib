import React, { useState } from "react";
import { Link } from "react-router-dom";
import ApiAlert from "../components/ApiAlert";
import { apiFetch } from "../lib/api";
import type { CatalogItem } from "../lib/types";
import ToastMessage from "../components/ToastMessage";

export default function CatalogSearch() {
  const [q, setQ] = useState("");
  const [pending, setPending] = useState(false);
  const [err, setErr] = useState<{ status: number; error: any } | null>(null);
  const [results, setResults] = useState<CatalogItem[]>([]);
  const [success, setSuccess] = useState("");

  async function search(e: React.FormEvent) {
    e.preventDefault();

    try {
      setPending(true);
      setErr(null);

      const r = await apiFetch<CatalogItem[]>(
        `/api/catalog/search/?q=${encodeURIComponent(q.trim())}`
      );

      console.log("Respuesta completa:", r);

      if (r.ok) {
        console.log("Datos:", r.data);
        console.log("Número de resultados:", r.data.length);
        setResults(r.data);
      } else {
        console.log("Error:", r);
        setErr(r);
      }
    } catch (error) {
      console.error("Excepción:", error);
    } finally {
      setPending(false);
    }
  }

  /*Funcion para añadir un juego a la biblioteca usando su external_game_id*/
  async function addToLibrary(game: CatalogItem) {

    setPending(true);
    setErr(null);

    const r = await apiFetch("/api/library/entries/", {
      method: "POST",
      json: {
        external_game_id: game.external_game_id,
        status: "wishlist",
        hours_played: 0,
      },
    });

    setPending(false);

    if (r.ok) {

      setSuccess("✅ Juego añadido correctamente a tu biblioteca.");

      setTimeout(() => {
        setSuccess("");
      }, 3000);

    } else {

      setErr(r);

    }

  }

  return (
    <div>
      <div className="d-flex align-items-center justify-content-between gap-2 flex-wrap mb-3">
        <h1 className="h4 m-0">Catálogo</h1>
        <Link className="btn btn-outline-secondary btn-sm" to="/library/new">Añadir (manual)</Link>
      </div>

      {err && <ApiAlert status={err.status} error={err.error} />}
      <ToastMessage
        show={!!success}
        message={success}
        onClose={() => setSuccess("")}
      />

      <form className="card card-body mb-3" onSubmit={search}>
        <label className="form-label">Buscar por título</label>
        <div className="d-flex gap-2">
          <input className="form-control" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ej: portal" />
          <button className="btn btn-primary" disabled={pending || !q.trim()}>
            {pending ? "Buscando..." : "Buscar"}
          </button>
        </div>
      </form>

      <div className="row g-3">
        {results.length === 0 ? (
          <div className="col-12">
            <div className="empty-state">
              <div style={{ fontSize: "2rem", marginBottom: "0.5rem" }}>🔎</div>
              <div className="fw-semibold mb-1">
                {q.trim() ? "No encontramos resultados para esa búsqueda." : "Busca tu próximo juego."}
              </div>
              <div>
                {q.trim()
                  ? "Prueba con otro título o vuelve a escribir el nombre del juego."
                  : "Escribe el nombre de un juego para empezar a explorar el catálogo."}
              </div>
            </div>
          </div>
        ) : (
          results.map((x) => (
            <div className="col-md-6 col-lg-4" key={x.external_game_id}>
              <div className="card h-100">
                {x.thumb ? (
                  <img src={x.thumb} className="card-img-top" alt="" style={{ height: 160, objectFit: "cover" }} />
                ) : null}
                <div className="card-body">
                  <div className="fw-semibold">{x.title}</div>
                  <div className="small text-secondary">ID: {x.external_game_id}</div>
                </div>
                <div className="card-footer bg-white border-top-0">
                  <button
                    className="btn btn-primary btn-sm"
                    onClick={() => addToLibrary(x)}
                    disabled={pending}
                  >
                    ➕ Añadir a mi biblioteca
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
