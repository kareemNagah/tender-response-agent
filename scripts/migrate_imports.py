"""One-off: rewrite old module paths to the layered layout. Delete after use."""

import re
from pathlib import Path

MOVES = {
    "app.api.v1": "app.interfaces.api.v1",
    "app.api.deps": "app.interfaces.api.deps",
    "app.api.health": "app.interfaces.api.health",
    "app.api": "app.interfaces.api",
    "app.core.logging": "app.infrastructure.observability.logging",
    "app.core.middleware": "app.interfaces.api.middleware",
    "app.core.errors": "app.interfaces.api.errors",
    "app.db.models": "app.infrastructure.persistence.orm",
    "app.db.migrations": "app.infrastructure.persistence.migrations",
    "app.db.base": "app.infrastructure.persistence.base",
    "app.db": "app.infrastructure.persistence",
    "app.main": "app.interfaces.api.main",
}
# Also cover slash forms such as alembic.ini's script_location.
MOVES |= {k.replace(".", "/"): v.replace(".", "/") for k, v in list(MOVES.items())}

# Longest keys first, so app.api.v1 wins over app.api.
keys = sorted(MOVES, key=len, reverse=True)
pattern = re.compile(r"\b(" + "|".join(re.escape(k) for k in keys) + r")\b")

files = [
    *Path("app").rglob("*.py"),
    *Path("tests").rglob("*.py"),
    *Path("scripts").rglob("*.py"),
    *Path(".github").rglob("*.yml"),
    Path("alembic.ini"),
    Path("Dockerfile"),
    Path("docker-compose.yml"),
    Path("Makefile"),
    Path("pyproject.toml"),
]
for path in files:
    if not path.exists() or path.name == "migrate_imports.py":
        continue
    text = path.read_text(encoding="utf-8")
    new = pattern.sub(lambda m: MOVES[m.group(1)], text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        print("updated", path)
