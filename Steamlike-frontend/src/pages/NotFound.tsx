import React from "react";
import { Link } from "react-router-dom";

export default function NotFound() {
    return (
        <div
            className="d-flex flex-column justify-content-center align-items-center text-center"
            style={{ minHeight: "70vh" }}
        >
            <h1
                className="display-1 fw-bold text-info"
                style={{ fontSize: "6rem" }}
            >
                404
            </h1>

            <h2 className="mb-3">
                Página no encontrada
            </h2>

            <p className="text-secondary mb-4" style={{ maxWidth: 500 }}>
                La página que intentas visitar no existe o ha sido movida.
            </p>

            <div className="d-flex gap-3">
                <Link className="btn btn-primary" to="/">
                    🏠 Ir al inicio
                </Link>

                <Link className="btn btn-outline-light" to="/library">
                    🎮 Mi biblioteca
                </Link>
            </div>
        </div>
    );
}