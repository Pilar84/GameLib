import React from "react";
import { Link } from "react-router-dom";
import FeaturedCarousel from "../components/FeaturedCarousel";

export default function Home() {
  return (
    <>
      <section className="home-hero text-white rounded-4 px-4 py-3 mb-4 overflow-hidden">
        <div className="row align-items-center py-1">
          <div className="col-lg-6 d-flex flex-column align-items-center align-items-lg-start text-center text-lg-start" style={{ marginTop: "-50px" }}>
            <img
              src="/logo-hero.png"
              alt="GameLib"
              className="img-fluid mb-3 home-logo"
            />
            <p className="lead mb-4 home-copy">
              Gestiona tu biblioteca, descubre ofertas y lleva tu colección siempre organizada en un solo lugar.
            </p>

            <div className="d-flex justify-content-center justify-content-lg-start gap-2 flex-wrap home-actions">
              <Link to="/catalog/search" className="btn btn-primary home-primary-btn">
                Explorar catálogo
              </Link>

              <Link to="/library" className="btn btn-outline-light home-secondary-btn">
                Mi biblioteca
              </Link>
            </div>
          </div>

          <div className="col-lg-6 d-flex justify-content-center mt-4 mt-lg-0">
            <img
              src="/hero-collage.png"
              alt="Colección de videojuegos"
              className="img-fluid home-hero-image"
            />
          </div>
        </div>
      </section>

      <FeaturedCarousel />

      <section className="mt-4 mb-3">
        <div className="text-center mb-3">
          <h2 className="fw-bold mb-2">Todo lo que necesitas para tu colección</h2>
          <p className="text-muted mb-0">Una experiencia más clara, ordenada y centrada en tus juegos.</p>
        </div>

        <div className="row g-3 mt-1">
          <div className="col-md-4">
            <div className="card h-100 border-0 shadow-lg home-feature-card home-feature-library">
              <div className="card-body text-center p-3">
                <div className="feature-icon">🎮</div>
                <h3 className="h4 mt-2 fw-bold">Mi biblioteca</h3>
                <p className="text-muted mb-3">
                  Guarda tus títulos y controla lo que tienes jugado, pendiente o favorito.
                </p>
                <Link to="/library" className="btn btn-info btn-sm">
                  Ver biblioteca
                </Link>
              </div>
            </div>
          </div>

          <div className="col-md-4">
            <div className="card h-100 border-0 shadow-lg home-feature-card home-feature-catalog">
              <div className="card-body text-center p-3">
                <div className="feature-icon">🔍</div>
                <h3 className="h4 mt-2 fw-bold">Descubre ofertas</h3>
                <p className="text-muted mb-3">
                  Explora nuevos juegos y encuentra precios que te interesen de forma rápida.
                </p>
                <Link to="/catalog/search" className="btn btn-info btn-sm">
                  Explorar juegos
                </Link>
              </div>
            </div>
          </div>

          <div className="col-md-4">
            <div className="card h-100 border-0 shadow-lg home-feature-card home-feature-profile">
              <div className="card-body text-center p-3">
                <div className="feature-icon">👤</div>
                <h3 className="h4 mt-2 fw-bold">Tu perfil</h3>
                <p className="text-muted mb-3">
                  Administra tu cuenta y configura tu acceso con total tranquilidad.
                </p>
                <Link to="/profile/password" className="btn btn-info btn-sm">
                  Mi perfil
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}