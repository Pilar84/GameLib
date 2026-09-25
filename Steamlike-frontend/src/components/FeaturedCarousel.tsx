import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";
import type { CatalogItem } from "../lib/types";
import ToastMessage from "./ToastMessage";

export default function FeaturedCarousel() {
  const [allGames, setAllGames] = useState<CatalogItem[]>([]);
  const [games, setGames] = useState<CatalogItem[]>([]);

  const [success, setSuccess] = useState("");
  const [pendingId, setPendingId] = useState<string | null>(null);

  const navigate = useNavigate();

  useEffect(() => {
    async function load() {
      const r = await apiFetch<CatalogItem[]>("/api/catalog/search/?q=a");

      if (r.ok) {
        setAllGames(r.data);
      }
    }

    load();
  }, []);

  useEffect(() => {
    if (allGames.length === 0) return;

    function randomGames() {
      const shuffled = [...allGames].sort(() => Math.random() - 0.5);
      setGames(shuffled.slice(0, 4));
    }

    randomGames();

    const interval = setInterval(randomGames, 5000);

    return () => clearInterval(interval);
  }, [allGames]);

  async function addToLibrary(game: CatalogItem) {
    setPendingId(game.external_game_id);

    const r = await apiFetch("/api/library/entries/", {
      method: "POST",
      json: {
        external_game_id: game.external_game_id,
        status: "wishlist",
        hours_played: 0,
      },
    });

    setPendingId(null);

    if (r.ok) {
      setSuccess(`✅ "${game.title}" añadido a tu biblioteca.`);

      setTimeout(() => {
        setSuccess("");
      }, 3000);
    } else if (r.status === 409) {
      setSuccess("ℹ️ Ese juego ya está en tu biblioteca.");

      setTimeout(() => {
        setSuccess("");
      }, 3000);
    } else if (r.status === 401) {
      navigate("/auth/login");
    }
  }

  if (games.length === 0) return null;

  return (
    <section className="mb-1">
      <ToastMessage
        show={!!success}
        message={success}
        onClose={() => setSuccess("")}
      />

      <h2 className="fw-bold mb-1">
        🔥 Juegos destacados
      </h2>

      <p className="text-muted mb-4">
        Descubre nuevos videojuegos que van apareciendo automáticamente.
      </p>

      <div className="row">
        {games.map((game) => (
          <div
            key={game.external_game_id}
            className="col-lg-3 col-md-6 mb-4"
          >
            <div className="card h-100 shadow-lg">
              <img
                src={game.thumb}
                alt={game.title}
                className="card-img-top"
                style={{
                  height: "180px",
                  objectFit: "cover",
                }}
              />

              <div className="card-body">
                <h5 className="fw-bold">
                  {game.title}
                </h5>

                <p className="text-muted small">
                  Descubre este videojuego y añádelo fácilmente a tu biblioteca.
                </p>
              </div>

              <div className="card-footer bg-transparent border-0">
                <button
                  className="btn btn-success w-100"
                  disabled={pendingId === game.external_game_id}
                  onClick={() => addToLibrary(game)}
                >
                  {pendingId === game.external_game_id
                    ? "Añadiendo..."
                    : "➕ Añadir a mi biblioteca"}
                </button>
              </div>

            </div>
          </div>
        ))}
      </div>
    </section>
  );
}