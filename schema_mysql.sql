-- Fe y Reflexión — esquema MySQL (utf8mb4).
--
-- ¿Quién crea qué?
-- • En Railway: el servicio MySQL ya incluye una base (suele llamarse `railway`).
--   Al desplegar la app Flask, SQLAlchemy ejecuta db.create_all() y crea las TABLAS
--   automáticamente la primera vez que arranca bien la conexión.
-- • En local: puedes crear la base con este archivo y las tablas, o solo la base
--   y dejar que la app cree las tablas al iniciar.
--
-- Uso local típico:
--   mysql -u root -p < schema_mysql.sql
--
-- Uso Railway: conéctate al MySQL (CLI o cliente) y ejecuta solo el bloque
-- "TABLAS" más abajo, eligiendo la base:  USE railway;

-- ---------------------------------------------------------------------------
-- Base local (opcional; en Railway omite y usa USE railway;)
-- ---------------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS fe_reflexiones
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE fe_reflexiones;

-- ---------------------------------------------------------------------------
-- Tablas (mismo diseño que SQLAlchemy / app/models.py)
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(80) NOT NULL,
  apellido VARCHAR(80) NOT NULL,
  username VARCHAR(64) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password_hash VARCHAR(256) NOT NULL,
  created_at DATETIME(6) NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uq_users_username (username),
  UNIQUE KEY uq_users_email (email),
  KEY ix_users_username (username),
  KEY ix_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS curated_reflections (
  id INT AUTO_INCREMENT PRIMARY KEY,
  titulo VARCHAR(200) NOT NULL,
  referencia VARCHAR(120) NOT NULL,
  cita TEXT NOT NULL,
  reflexion TEXT NOT NULL,
  orden INT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS generated_reflections (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  tema_o_peticion VARCHAR(500) NOT NULL,
  texto_gemini TEXT NOT NULL,
  referencia_sugerida VARCHAR(200) NULL,
  archivo_relativo VARCHAR(512) NOT NULL,
  created_at DATETIME(6) NULL,
  KEY ix_generated_reflections_user_id (user_id),
  CONSTRAINT fk_generated_reflections_user
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS support_reports (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NULL,
  contacto_email VARCHAR(255) NOT NULL,
  asunto VARCHAR(200) NOT NULL,
  descripcion TEXT NOT NULL,
  created_at DATETIME(6) NULL,
  KEY ix_support_reports_user_id (user_id),
  CONSTRAINT fk_support_reports_user
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
