import json
from functools import lru_cache
from pathlib import Path


CONFIG_PATH = Path(__file__).resolve().parent / "config.json"


@lru_cache(maxsize=1)
def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        return json.load(config_file)


def get_app_settings():
    app_config = load_config().get("app", {})
    return {
        "secret_key": app_config.get("secret_key"),
        "debug": bool(app_config.get("debug", False)),
        "host": app_config.get("host", "0.0.0.0"),
        "port": int(app_config.get("port", 5057)),
    }


def get_database_settings():
    database_config = load_config().get("database", {})
    return {
        "host": database_config.get("host"),
        "port": database_config.get("port"),
        "dbname": database_config.get("database"),
        "user": database_config.get("user"),
        "password": database_config.get("password"),
    }


def get_ollama_settings():
    ollama_config = load_config().get("ollama", {})
    host = str(ollama_config.get("host") or "").strip()
    port = ollama_config.get("port")

    if host and port:
        base_url = f"http://{host}:{port}"
    elif host:
        base_url = host if host.startswith("http://") or host.startswith("https://") else f"http://{host}"
    else:
        base_url = None

    return {
        "base_url": base_url,
        "model": ollama_config.get("model"),
    }
