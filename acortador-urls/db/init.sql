-- Tabla de enlaces (Cloud SQL / PostgreSQL). El servicio "links" también la crea al arrancar si no existe.
CREATE TABLE IF NOT EXISTS links (
    code        VARCHAR(32)  PRIMARY KEY,
    url         TEXT         NOT NULL,
    permanent   BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT now()
);
