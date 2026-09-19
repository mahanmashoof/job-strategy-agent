import json
import os
from typing import Any

def ensure_dir(path: str):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

def write_json(path: str, data: Any):
    ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def write_text(path: str, text: str):
    ensure_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)