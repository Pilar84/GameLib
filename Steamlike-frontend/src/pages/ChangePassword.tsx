import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { apiFetch } from "../lib/api";
import ApiAlert from "../components/ApiAlert";

export default function ChangePassword() {
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [pending, setPending] = useState(false);
  const [err, setErr] = useState<{ status: number; error: any } | null>(null);
  const [ok, setOk] = useState(false);
  const [checkingAuth, setCheckingAuth] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    async function checkAuth() {
      const r = await apiFetch("/api/users/me/");

      setAuthenticated(r.ok);
      setCheckingAuth(false);
    }

    checkAuth();
  }, []);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setPending(true);
    setErr(null);
    setOk(false);

    const r = await apiFetch<{ ok: boolean }>("/api/users/me/password/", {
      method: "POST",
      json: { current_password: current, new_password: next },
    });

    setPending(false);

    if (r.ok) {
      setOk(true);
      setCurrent("");
      setNext("");
      // Redirigir a inicio tras 1.5s
      setTimeout(() => navigate("/"), 1500);
    } else {
      setErr(r);
    }
  }

  if (checkingAuth) {
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-info" role="status"></div>
        <p className="mt-3">Comprobando sesión...</p>
      </div>
    );
  }

  if (!authenticated) {
    return (
      <div className="row justify-content-center">
        <div className="col-md-8 col-lg-6">
          <div className="card shadow border-0">
            <div className="card-body text-center p-5">

              <div style={{ fontSize: "4rem" }}>🔒</div>

              <h2 className="fw-bold mt-3">
                Área privada
              </h2>

              <p className="lead">
                Debes iniciar sesión para acceder a tu perfil.
              </p>

              <p className="text-muted">
                Si ya tienes una cuenta puedes iniciar sesión.
                Si todavía no tienes una cuenta, regístrate gratuitamente y comienza a organizar tu biblioteca de videojuegos.
              </p>

              <div className="d-flex justify-content-center gap-3 mt-4">

                <Link
                  to="/auth/login"
                  className="btn btn-primary"
                >
                  Iniciar sesión
                </Link>

                <Link
                  to="/auth/register"
                  className="btn btn-success"
                >
                  Crear cuenta
                </Link>

              </div>

            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="row justify-content-center">
      <div className="col-md-6 col-lg-5">
        <div className="d-flex align-items-center justify-content-between mb-3">
          <h1 className="h4 m-0">Cambiar contraseña</h1>
          <Link className="btn btn-outline-secondary btn-sm" to="/">Volver</Link>
        </div>

        {ok && (
          <div className="alert alert-success">
            Contraseña actualizada correctamente. Redirigiendo…
          </div>
        )}

        {err && (
          err.status === 401 && err.error?.error === "unauthorized" ? (
            <div className="alert alert-info">
              Necesitas <Link to="/auth/login">iniciar sesión</Link> para cambiar la contraseña.
            </div>
          ) : (
            <ApiAlert status={err.status} error={err.error} />
          )
        )}

        <form className="card card-body" onSubmit={onSubmit}>
          <div className="mb-3">
            <label className="form-label">Contraseña actual</label>
            <input
              className="form-control"
              type="password"
              value={current}
              onChange={e => setCurrent(e.target.value)}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Nueva contraseña</label>
            <input
              className="form-control"
              type="password"
              value={next}
              onChange={e => setNext(e.target.value)}
              required
            />
            <div className="form-text">Mínimo 8 caracteres.</div>
          </div>

          <button className="btn btn-primary" disabled={pending || ok}>
            {pending ? "Guardando..." : "Cambiar contraseña"}
          </button>
        </form>
      </div>
    </div>
  );
}
