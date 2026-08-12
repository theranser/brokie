"""Config helper functions."""

import sys
from pathlib import Path

import orjson
import rich

default_config = {
    "url": "http://localhost:11434/v1",
    "api_key": "ollama",
    "model": "gemma4:e4b",
}


def load_config() -> dict:
    """Load a JSON configuration file from the OS-specific configuration directory."""
    if sys.platform == "win32":
        path = Path.home() / "AppData" / "Roaming" / "brokie" / "config.json"
    else:
        path = Path.home() / ".config" / "brokie" / "config.json"

    if not path.exists():
        Path(path.parent).mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            f.write(orjson.dumps(default_config, option=orjson.OPT_INDENT_2).decode())

    with Path(path).open() as f:
        config = orjson.loads(f.read())
        for key in default_config:
            if key not in config:
                rich.print(f"[bold red]Error: Missing key '{key}' in config file.")
                sys.exit(1)

    return config
