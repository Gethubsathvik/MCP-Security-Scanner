from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any


def compact(value: Any, limit: int = 300) -> str:
    text = value if isinstance(value, str) else json.dumps(value, sort_keys=True, default=str)
    text = " ".join(text.split())
    return text if len(text) <= limit else f"{text[:limit - 1]}…"


def manifest_items(manifest: Any) -> Iterable[tuple[str, dict[str, Any]]]:
    for category in ("tools", "resources", "prompts"):
        for item in getattr(manifest, category):
            yield category[:-1], item


def item_text(item: dict[str, Any]) -> str:
    return " ".join(
        str(item.get(key, ""))
        for key in ("name", "title", "description", "uri", "uriTemplate")
    )


def item_name(item: dict[str, Any]) -> str:
    return str(item.get("name") or item.get("uri") or item.get("title") or "<unnamed>")