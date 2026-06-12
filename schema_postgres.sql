-- Fe y Reflexión — esquema PostgreSQL para Supabase.
--
-- Uso en Supabase:
-- 1. Ve a tu proyecto en Supabase (app.supabase.com).
-- 2. Abre el SQL Editor en el menú lateral.
-- 3. Crea un "New query".
-- 4. Copia y pega el contenido de este archivo.
-- 5. Presiona "Run" para crear todas las tablas.

-- ---------------------------------------------------------------------------
-- Tablas (mismo diseño que SQLAlchemy / app/models.py)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL,
  apellido VARCHAR(80) NOT NULL,
  username VARCHAR(64) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(256) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE INDEX ix_users_username ON users (username);
CREATE INDEX ix_users_email ON users (email);

CREATE TABLE IF NOT EXISTS curated_reflections (
  id SERIAL PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  referencia VARCHAR(120) NOT NULL,
  cita TEXT NOT NULL,
  reflexion TEXT NOT NULL,
  orden INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS generated_reflections (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  tema_o_peticion VARCHAR(500) NOT NULL,
  texto_gemini TEXT NOT NULL,
  referencia_sugerida VARCHAR(200) NULL,
  archivo_relativo VARCHAR(512) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_generated_reflections_user
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE INDEX ix_generated_reflections_user_id ON generated_reflections (user_id);

CREATE TABLE IF NOT EXISTS support_reports (
  id SERIAL PRIMARY KEY,
  user_id INT NULL,
  contacto_email VARCHAR(255) NOT NULL,
  asunto VARCHAR(200) NOT NULL,
  descripcion TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_support_reports_user
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
);

CREATE INDEX ix_support_reports_user_id ON support_reports (user_id);
