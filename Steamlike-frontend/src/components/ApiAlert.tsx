import React from "react";
import type { ApiError } from "../lib/api";

export default function ApiAlert({
  status,
  error,
}: {
  status: number;
  error: ApiError;
}) {

  function traducirCampo(campo: string) {
    switch (campo) {
      case "username":
        return "Usuario";
      case "password":
        return "Contraseña";
      case "email":
        return "Correo electrónico";
      default:
        return campo;
    }
  }

  function renderContenido() {

    const isUnauthorized =
      status === 401 &&
      (error?.error === "unauthorized" ||
        /no autenticado|not authenticated/i.test(String(error?.message ?? "")));

    if (isUnauthorized) {
      return (
        <>
          <strong>Necesitas iniciar sesión.</strong>
          <div className="mt-1">
            Inicia sesión para ver tu biblioteca.
          </div>
        </>
      );
    }

    // Login incorrecto
    if (status === 401) {
      return (
        <>
          <strong>Usuario o contraseña incorrectos.</strong>
          <div className="mt-1">
            Comprueba tus credenciales e inténtalo de nuevo.
          </div>
        </>
      );
    }

    // API externa caída
    if (status === 503) {
      return (
        <>
          <strong>No se ha podido conectar con el catálogo de juegos.</strong>
          <div className="mt-1">
            Inténtalo de nuevo dentro de unos minutos.
          </div>
        </>
      );
    }

    // Errores de validación
    if (status === 400 && "details" in error && error.details) {

      return (
        <>
          <strong>Revisa los datos introducidos.</strong>

          <ul className="mt-2 mb-0">
            {Object.entries(error.details).map(([campo, mensaje]) => (
              <li key={campo}>
                <strong>{traducirCampo(campo)}:</strong> {String(mensaje)}
              </li>
            ))}
          </ul>
        </>
      );
    }

    // Error genérico
    return (
      <>
        <strong>Ha ocurrido un error.</strong>
        <div>{error.message}</div>
      </>
    );
  }

  return (
    <div className="alert alert-danger">
      {renderContenido()}
    </div>
  );
}