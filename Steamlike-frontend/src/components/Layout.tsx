/// <reference types="react" />
import React, { useEffect, useState } from "react";
import { Link, NavLink, Outlet, useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";
import type { User } from "../lib/types";
import { backendUrl } from "../lib/env";

function NavItem({ to, label }: { to: string; label: string }) {
  return (
    <li className="nav-item">
      <NavLink
        to={to}
        className={({ isActive }) => "nav-link" + (isActive ? " active" : "")}
        end
      >
        {label}
      </NavLink>
    </li>
  );
}

export default function Layout() {
  const [me, setMe] = useState<User | null>(null);
  const [meLoading, setMeLoading] = useState(true);
  const [flash, setFlash] = useState<{ type: "success" | "danger"; text: string } | null>(null);
  const navigate = useNavigate();

  async function refreshMe() {
    setMeLoading(true);
    const r = await apiFetch<User>("/api/users/me/");
    if (r.ok) setMe(r.data);
    else setMe(null);
    setMeLoading(false);
  }

  useEffect(() => {
    refreshMe();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function logout() {
    const r = await apiFetch<null>("/api/auth/logout/", { method: "POST" });
    if (r.ok) {
      setFlash({
        type: "success",
        text: "Sesión cerrada correctamente.",
      });

      setTimeout(() => {
        setFlash(null);
      }, 3000);

      setMe(null);
      navigate("/");

    } else {
      setFlash({ type: "danger", text: "error" in r ? r.error.message : "No se pudo cerrar sesión." });
    }
  }

  return (
    <div className="app-shell">
      <nav
        className="navbar navbar-expand-lg navbar-dark shadow"
        style={{
          background: "#171a21",
          borderBottom: "1px solid #2a475e"
        }}
      >
        <div className="container">
          <Link className="navbar-brand" to="/">
            <img
              src="/logo-header.png"
              alt="GameLib"
              className="img-fluid"
              style={{
                height: "45px",
                maxWidth: "180px",
                objectFit: "contain",
              }}
            />
          </Link>

          {!meLoading && !me && (
            <div className="d-flex d-lg-none ms-auto me-2 gap-2">
              <Link className="btn btn-outline-light btn-sm" to="/auth/login">
                Login
              </Link>

              <Link className="btn btn-warning btn-sm" to="/auth/register">
                Registro
              </Link>
            </div>
          )}


          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#nav">
            <span className="navbar-toggler-icon"></span>
          </button>

          <div id="nav" className="collapse navbar-collapse">
            <ul className="navbar-nav me-auto mb-3 mb-lg-0">
              <NavItem to="/" label="Inicio" />
              <NavItem to="/library" label="Biblioteca" />
              <NavItem to="/catalog/search" label="Catálogo" />
            </ul>

            <div className="d-flex flex-column flex-lg-row align-items-stretch align-items-lg-center gap-2 mt-3 mt-lg-0">
              {/*<small className="text-secondary d-none d-lg-inline">API: {backendUrl()}</small>*/}
              {meLoading ? (
                <span className="text-light">…</span>
              ) : me ? (
                <div className="dropdown">
                  <button
                    className="btn btn-outline-light btn-sm dropdown-toggle"
                    data-bs-toggle="dropdown"
                  >
                    {me.username}
                  </button>
                  <ul className="dropdown-menu dropdown-menu-end">
                    <li><Link className="dropdown-item" to="/profile/password">Cambiar contraseña</Link></li>
                    <li><hr className="dropdown-divider" /></li>
                    <li>
                      <button className="dropdown-item" onClick={logout}>Cerrar sesión</button>
                    </li>
                    <li><hr className="dropdown-divider" /></li>
                    <li><Link className="dropdown-item text-danger" to="/profile/delete">Eliminar cuenta</Link></li>
                  </ul>
                </div>
              ) : (
                <>
                  <div className="d-none d-lg-flex gap-2">
                    <Link className="btn btn-outline-light btn-sm" to="/auth/login">
                      Login
                    </Link>

                    <Link className="btn btn-warning btn-sm" to="/auth/register">
                      Registro
                    </Link>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      <main className="app-main container my-4">
        {flash && (
          <div className={`alert alert-${flash.type} alert-dismissible`} role="alert">
            {flash.text}
            <button type="button" className="btn-close" onClick={() => setFlash(null)} aria-label="Close"></button>
          </div>
        )}
        <Outlet context={{ refreshMe, me }} />
      </main>

      <footer className="border-top py-3">
        <div className="container small text-secondary text-center text-lg-start">
          Proyecto GameLib — Diseñado por PilarGiron 2026.
        </div>
      </footer>
    </div>
  );
}
