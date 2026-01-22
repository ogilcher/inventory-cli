from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

import psycopg
from psycopg import Connection
from inv.core.config import Settings

def _normalize_database_url(database_url: str) -> str:
    """
    Normalize DATABASE_URL to a psycopg-compatible URL.

    - SQLAlchemy commonly uses: postgresql+psycopg://...
    - psycopg expects:          postgresql://...
    """
    if database_url.startswith("postgresql+psycopg://"):
        return database_url.replace("postgresql+psycopg://", "postgresql://", 1)
    if database_url.startswith("postgres_psycopg://"):
        return database_url.replace("postgres+psycopg://", "postgresql://", 1)
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql://", 1)
    return database_url

def _apply_ssl_defaults_if_needed(database_url: str, require_ssl: bool) -> str:
    """
    For many Postgres providers, TLS is required.
    psycopg can receive sslmode via query string.
    """
    if not require_ssl:
        return database_url

    parsed = urlparse(database_url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))

    # Only set if not already provided
    query.setDefault("sslmode", "require")

    new_query = urlencode(query)
    return str(urlunparse(parsed._replace(query=new_query)))

@dataclass(frozen=True)
class DbConfig:
    dsn: str

def build_db_config(settings: Settings) -> DbConfig:
    dsn = _normalize_database_url(settings.database_url)

    dsn = _apply_ssl_defaults_if_needed(dsn, require_ssl=settings.require_ssl)
    return DbConfig(dsn=dsn)

def connect(settings: Optional[Settings] = None) -> Connection:
    """
    Open a new psycopg connection to Postgres.

    No transactions here. No global singleton. Caller owns lifecycle
    """
    settings = settings or Settings()
    cfg = build_db_config(settings)

    return psycopg.connect(cfg.dsn)

def ping(settings: Optional[Settings] = None) -> bool:
    settings = settings or Settings()
    with connect(settings) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1;")
            return cur.fetchone() == (1,)


