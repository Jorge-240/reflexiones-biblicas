from datetime import datetime, timezone

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    generated_reflections = db.relationship(
        "GeneratedReflection", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )
    support_reports = db.relationship(
        "SupportReport", backref="user", lazy="dynamic", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}".strip()


class CuratedReflection(db.Model):
    """Reflexiones bíblicas curadas para la comunidad (semilla inicial)."""

    __tablename__ = "curated_reflections"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    referencia = db.Column(db.String(120), nullable=False)
    cita = db.Column(db.Text, nullable=False)
    reflexion = db.Column(db.Text, nullable=False)
    orden = db.Column(db.Integer, default=0, nullable=False)


class GeneratedReflection(db.Model):
    """Tarjetas/imágenes generadas por el usuario con ayuda de Gemini."""

    __tablename__ = "generated_reflections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    tema_o_peticion = db.Column(db.String(500), nullable=False)
    texto_gemini = db.Column(db.Text, nullable=False)
    referencia_sugerida = db.Column(db.String(200), nullable=True)
    libro = db.Column(db.String(100), nullable=True)
    archivo_relativo = db.Column(db.String(512), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class SupportReport(db.Model):
    __tablename__ = "support_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    contacto_email = db.Column(db.String(255), nullable=False)
    asunto = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
