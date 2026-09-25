import React, { useState } from "react";
import { Link, useNavigate, useOutletContext } from "react-router-dom";
import { apiFetch } from "../lib/api";
import ApiAlert from "../components/ApiAlert";

export default function DeleteAccount() {
  const [confirm, setConfirm] = useState("");
  const [pending, setPending] = useState(false);
  const [err, setErr] = useState<{ status: number; error: any } | null>(null);
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();
  const { refreshMe } = useOutletContext<{
    refreshMe: () => Promise<void>;
  }>();

  const CONFIRM_WORD = "ELIMINAR";

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (confirm !== CONFIRM_WORD) return;

    setPending(true);
    setErr(null);

    const r = await apiFetch<null>("/api/users/me/", { method: "DELETE" });
    setPending(false);

    if (r.ok) {
      await refreshMe();
      setSuccess(true);

      setTimeout(() => {
        navigate("/");
      }, 1200);
    } else {
      setErr(r);
    }
  }

  return (
    <div className="row justify-content-center">
      <div className="col-md-6 col-lg-5">
        <div className="d-flex align-items-center justify-content-between mb-3">
          <h1 className="h4 m-0 text-danger">Eliminar cuenta</h1>
          <Link className="btn btn-outline-secondary btn-sm" to="/">Cancelar</Link>
        </div>

        <div className="alert alert-warning">
          <strong>Esta acción es irreversible.</strong> Se eliminarán tu cuenta y todas
          tus entradas de biblioteca.
        </div>

        {err && (
          err.status === 401 && err.error?.error === "unauthorized" ? (
            <div className="alert alert-info">
              Necesitas <Link to="/auth/login">iniciar sesión</Link> para eliminar tu cuenta.
            </div>
          ) : (
            <ApiAlert status={err.status} error={err.error} />
          )
        )}

        {success && (
          <div className="alert alert-success" role="alert">
            Tu cuenta se ha eliminado correctamente. Volviendo a la página principal...
          </div>
        )}

        <form className="card card-body border-danger" onSubmit={onSubmit}>
          <div className="mb-3">
            <label className="form-label">
              Escribe <strong>{CONFIRM_WORD}</strong> para confirmar
            </label>
            <input
              className="form-control"
              value={confirm}
              onChange={e => setConfirm(e.target.value)}
              placeholder={CONFIRM_WORD}
              required
            />
          </div>

          <button
            className="btn btn-danger"
            disabled={pending || confirm !== CONFIRM_WORD}
          >
            {pending ? "Eliminando..." : "Eliminar cuenta definitivamente"}
          </button>
        </form>
      </div>
    </div>
  );
}