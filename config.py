import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def _normalize_mysql_sqlalchemy_url(url: str) -> str:
    """Railway expone MYSQL_URL como mysql://...; SQLAlchemy con PyMySQL necesita mysql+pymysql://."""
    url = url.strip().strip('"').strip("'")
    if url.startswith("mysql://"):
        url = "mysql+pymysql://" + url[len("mysql://") :]
    elif not url.startswith("mysql+pymysql://"):
        return url
    if "charset=" not in url:
        url = url + ("&" if "?" in url else "?") + "charset=utf8mb4"
    return url


def _resolve_database_url() -> str:
    """
    Orden: DATABASE_URL → MYSQL_URL (Railway) → piezas MYSQL* (Railway).
    Así puedes usar «Variable Reference» al servicio MySQL sin armar la URI a mano.
    """
    direct = os.environ.get("DATABASE_URL", "").strip()
    if direct:
        if direct.startswith("mysql://") or direct.startswith("mysql+pymysql://"):
            return _normalize_mysql_sqlalchemy_url(direct)
        return direct

    mysql_url = os.environ.get("MYSQL_URL", "").strip()
    if mysql_url:
        return _normalize_mysql_sqlalchemy_url(mysql_url)

    host = os.environ.get("MYSQLHOST") or os.environ.get("MYSQL_HOST")
    user = os.environ.get("MYSQLUSER") or os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQLPASSWORD")
    if password is None:
        password = os.environ.get("MYSQL_PASSWORD", "")
    database = os.environ.get("MYSQLDATABASE") or os.environ.get("MYSQL_DATABASE")
    port = os.environ.get("MYSQLPORT") or os.environ.get("MYSQL_PORT") or "3306"

    if host and user and database is not None:
        return (
            f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password or '')}"
            f"@{host}:{port}/{database}?charset=utf8mb4"
        )

    return "mysql+pymysql://root:@127.0.0.1:3306/fe_reflexiones?charset=utf8mb4"


def mysql_uri_uses_loopback(uri: str) -> bool:
    if not uri or "mysql" not in uri.lower():
        return False
    u = uri.lower()
    return "127.0.0.1" in u or "@localhost:" in u or "://localhost:" in u or "@localhost/" in u


def running_on_managed_hosting() -> bool:
    """Render, Railway, Fly.io, Cloud Run, etc. suelen definir alguna de estas variables."""
    return bool(
        os.environ.get("RENDER")
        or os.environ.get("RENDER_EXTERNAL_URL")
        or os.environ.get("IS_RENDER")
        or os.environ.get("RAILWAY_ENVIRONMENT")
        or os.environ.get("RAILWAY_PROJECT_ID")
        or os.environ.get("FLY_APP_NAME")
        or os.environ.get("K_SERVICE")
    )


def assert_db_not_localhost_in_cloud(uri: str) -> None:
    if running_on_managed_hosting() and mysql_uri_uses_loopback(uri):
        raise RuntimeError(
            "MySQL está configurado en 127.0.0.1/localhost, pero en la nube la base "
            "va en otro servicio. En el panel del hosting: borra DATABASE_URL de ejemplo, "
            "o pon la URI real (host del proveedor, no localhost). En Railway referencia "
            "MYSQL_URL o MYSQLHOST/MYSQLUSER/MYSQLPASSWORD/MYSQLDATABASE desde el plugin MySQL."
        )


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-cambiar-en-produccion"
    SQLALCHEMY_DATABASE_URI = _resolve_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ("1", "true", "yes")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    APP_BASE_URL = os.environ.get("APP_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    DEVELOPER_EMAIL = os.environ.get("DEVELOPER_EMAIL", "andres.herreraote@gmail.com")
