import json, os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Settings:
    # --- Application metadata ---
    app_name: str = ""
    environment: str = "" # e.g., dev, test, prod
    debug: bool = ""

    # --- DB config ---
    database_url: str = ""
    db_pool_size: Optional[int] = None
    db_max_overflow: Optional[int] = None
    db_connect_timeout_seconds: Optional[int] = None
    db_echo: Optional[bool] = False
    require_ssl: bool = False

    @staticmethod
    def load() -> "Settings":
        with open(os.path.join("config", "app_config.json"), "r", encoding="utf-8") as f:
            cfg = json.load(f)

        return Settings(
            app_name=cfg["app_name"],
            environment=cfg["environment"],
            debug=cfg["debug"],
            database_url=os.environ.get("DATABASE_URL"),
            require_ssl=str(os.getenv("REQUIRE_SSL")).lower() == 'false',
            db_pool_size=cfg["db_pool_size"],
            db_max_overflow=cfg["db_max_overflow"],
            db_connect_timeout_seconds=cfg["db_connect_timeout_seconds"],
            db_echo=cfg["db_echo"],
        )