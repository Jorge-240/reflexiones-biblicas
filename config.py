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
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    DEVELOPER_EMAIL = os.environ.get("DEVELOPER_EMAIL", "andres.herreraote@gmail.com")
