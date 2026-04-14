-- Base de datos sugerida para Fe y Reflexión (utf8mb4 para emojis y acentos).
-- Crear antes de arrancar la app: mysql -u root -p < schema_mysql.sql

CREATE DATABASE IF NOT EXISTS fe_reflexiones
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE fe_reflexiones;

-- Las tablas siguientes también las crea SQLAlchemy al iniciar la app;
-- este script documenta el diseño relacional esperado.

/*
users
  id PK, nombre, apellido, username UNIQUE, email UNIQUE, password_hash,
  created_at, is_active

curated_reflexiones
  id PK, titulo, referencia, cita, reflexion, orden

generated_reflections
  id PK, user_id FK -> users.id ON DELETE CASCADE,
  tema_o_peticion, texto_gemini, referencia_sugerida, archivo_relativo, created_at

support_reports
  id PK, user_id FK -> users.id ON DELETE SET NULL,
  contacto_email, asunto, descripcion, created_at
*/
