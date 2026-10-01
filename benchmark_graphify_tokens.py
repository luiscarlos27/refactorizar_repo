"""Benchmark de tokens: responder preguntas CON y SIN graphify.

Mide el costo real de contexto (tokens) que cada estrategia carga para responder
las mismas preguntas sobre ESTE repositorio, y si esa estrategia acierta.

Estrategias
-----------
naive_tracked   Sin grafo. `git log` + busqueda por palabras clave sobre los
                archivos versionados + lectura de los N primeros coincidientes.
                (Mismo alcance que graphify: scope "committed".)
naive_report    Sin grafo. Lee el reporte completo a ciegas (.graphify/GRAPH_REPORT.md).
naive_graphjson Sin grafo. Lee el grafo crudo a ciegas (.graphify/graph.json).
                Se incluye para medir el peor caso, no porque sea sensato hacerlo.
graphify_check  Con grafo. `graphify check-update` (guarda de frescura) + `summary` + `query`.
graphify_raw    Con grafo. `summary` + `query`, SIN la guarda de frescura.

Salida
------
benchmark_graphify_report.md y benchmark_graphify_results.json
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent
GRAPH_DIR = WORKSPACE / ".graphify"
MAX_READ_FILES = 3
MAX_READ_BYTES = 20_000
SKIP_DIR_PARTS = {
    ".git",
    "__pycache__",
    ".ruff_cache",
    ".mypy_cache",
    ".pytest_cache",
    "node_modules",
}

QUESTIONS = [
    {
        "id": "etapa2",
        "q": "que se realizo en la etapa 2",
        "keywords": ["etapa 2", "etapa", "skills propias"],
        "evidence": r"461091c|etapa\s*2",
        "note": "Pregunta de proceso/historia: la respuesta vive en el historial de git.",
    },
    {
        "id": "arquitectura",
        "q": "como esta estructurado el proyecto de refactorizacion",
        "keywords": ["proyecto_refactoring", "refactorizar"],
        "evidence": r"proyecto_refactoring",
        "note": "Pregunta de arquitectura: el grafo deberia ganar aqui.",
    },
    {
        "id": "errores",
        "q": "donde se maneja el manejo de errores",
        "keywords": ["manejo de errores", "errores", "error"],
        "evidence": r"errores?",
        "note": "Pregunta de codigo: dominio natural del grafo.",
    },
    {
        "id": "skills",
        "q": "que skills propias de opencode se crearon en el repositorio",
        "keywords": ["skills", "opencode-skills"],
        "evidence": r"skills?\s+(propias|de\s+opencode)|refactoring.*api.*pytest",
        "note": "Requiere el commit mas reciente (Etapa 2 Parte 2).",
    },
]


# --------------------------------------------------------------------------- #
# Conteo de tokens
# --------------------------------------------------------------------------- #
def get_encoder():
    try:
        import tiktoken

        return tiktoken.get_encoding("cl100k_base"), "tiktoken cl100k_base"
    except Exception:
        return None, "aprox. chars/4 (tiktoken no disponible)"


ENC, ENC_NAME = get_encoder()


def ntok(text: str) -> int:
    if not text:
        return 0
    if ENC is not None:
        return len(ENC.encode(text, disallowed_special=()))
    return max(1, len(text) // 4)


# --------------------------------------------------------------------------- #
# Utilidades de shell / repo
# --------------------------------------------------------------------------- #
def graphify_cmd() -> list[str]:
    """Resuelve el shim de graphify: en Windows es un .cmd/.ps1 que subprocess no ve."""
    found = shutil.which("graphify")
    if found:
        return [found]
    for cand in (
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "nodejs" / "graphify.cmd",
        Path(os.environ.get("APPDATA", "")) / "npm" / "graphify.cmd",
    ):
        if cand.is_file():
            return [str(cand)]
    return ["graphify"]


def sh(args: list[str], cwd: Path = WORKSPACE) -> str:
    try:
        p = subprocess.run(
            args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=300,
        )
        return (p.stdout or "") + (p.stderr or "")
    except Exception as exc:  # noqa: BLE001
        return f"[error ejecutando {' '.join(args)}: {exc}]"


def tracked_files() -> list[Path]:
    out = sh(["git", "ls-files"])
    files = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        p = WORKSPACE / line
        if not p.is_file():
            continue
        if any(part in SKIP_DIR_PARTS for part in p.parts):
            continue
        files.append(p)
    return files


def read_capped(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")[:MAX_READ_BYTES]
    except Exception:  # noqa: BLE001
        return ""


# --------------------------------------------------------------------------- #
# Estrategias
# --------------------------------------------------------------------------- #
def naive_tracked(question: dict) -> tuple[str, float]:
    """Sin grafo: git log + busqueda por keywords + lectura de los primeros N hits."""
    t0 = time.perf_counter()
    chunks = [sh(["git", "log", "--oneline", "-30"])]

    keywords = question["keywords"]
    pattern = re.compile("|".join(re.escape(k) for k in keywords), re.IGNORECASE)
    hits: list[Path] = []
    for p in tracked_files():
        try:
            if p.stat().st_size > 400_000:
                continue
            body = p.read_text(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            continue
        if pattern.search(body):
            hits.append(p)

    chunks.append("\n".join(str(p.relative_to(WORKSPACE)) for p in hits[:60]))
    for p in hits[:MAX_READ_FILES]:
        chunks.append(f"--- {p.relative_to(WORKSPACE)} ---\n{read_capped(p)}")

    return "\n".join(chunks), (time.perf_counter() - t0) * 1000


def naive_read(path: Path) -> tuple[str, float]:
    """Sin grafo: lectura a ciegas de un artefacto completo (worst case)."""
    t0 = time.perf_counter()
    body = read_capped(path) if path.stat().st_size <= MAX_READ_BYTES else path.read_text(
        encoding="utf-8", errors="replace"
    )
    return body, (time.perf_counter() - t0) * 1000


def graphify_query(question: dict, with_check: bool) -> tuple[str, float]:
    """Con grafo: guarda de frescura + resumen + consulta BFS."""
    t0 = time.perf_counter()
    g = graphify_cmd()
    chunks: list[str] = []
    if with_check:
        chunks.append(sh(g + ["check-update"]))
    chunks.append(sh(g + ["summary"]))
    chunks.append(sh(g + ["query", question["q"]]))
    return "\n".join(chunks), (time.perf_counter() - t0) * 1000


# --------------------------------------------------------------------------- #
# Runner
# --------------------------------------------------------------------------- #
def score(context: str, question: dict) -> bool:
    return bool(re.search(question["evidence"], context, re.IGNORECASE))


def main() -> None:
    report_path = GRAPH_DIR / "graph.json"
    strategies = [
        ("naive_tracked", "Sin grafo: git log + grep + leer 3 hits", lambda q: naive_tracked(q)),
        (
            "naive_report",
            "Sin grafo: leer GRAPH_REPORT.md completo",
            lambda q: naive_read(GRAPH_DIR / "GRAPH_REPORT.md"),
        ),
        (
            "naive_graphjson",
            "Sin grafo: leer graph.json crudo (peor caso)",
            lambda q: naive_read(report_path),
        ),
        (
            "graphify_check",
            "Con grafo: check-update + summary + query",
            lambda q: graphify_query(q, with_check=True),
        ),
        (
            "graphify_raw",
            "Con grafo: summary + query (sin guarda de frescura)",
            lambda q: graphify_query(q, with_check=False),
        ),
    ]

    print(f"Tokenizador: {ENC_NAME}")
    print(f"HEAD: {sh(['git', 'rev-parse', '--short', 'HEAD']).strip()}")
    print(f"Estado del grafo: {sh(graphify_cmd() + ['check-update']).strip()}")
    print()

    results = []
    for question in QUESTIONS:
        row = {"id": question["id"], "q": question["q"], "note": question["note"], "strategies": {}}
        for name, _desc, fn in strategies:
            ctx, ms = fn(question)
            row["strategies"][name] = {
                "tokens": ntok(ctx),
                "chars": len(ctx),
                "ms": round(ms, 1),
                "hit": score(ctx, question),
            }
        results.append(row)

        print(f"[{question['id']}] {question['q']}")
        for name, _desc, _fn in strategies:
            s = row["strategies"][name]
            print(f"   {name:<16} {s['tokens']:>9,} tok  {s['ms']:>8.1f} ms  {'OK' if s['hit'] else 'FALLA'}")
        print()

    # ---------------- reporte ---------------- #
    lines = [
        "# Benchmark de tokens: con vs sin graphify",
        "",
        f"- Tokenizador: `{ENC_NAME}`",
        f"- HEAD del repo: `{sh(['git', 'rev-parse', '--short', 'HEAD']).strip()}`",
        "",
        "## Preguntas y resultados",
        "",
        "| Pregunta | Estrategia | Tokens | ms | Acerto |",
        "|---|---|---:|---:|:---:|",
    ]
    for row in results:
        for name, desc, _fn in strategies:
            s = row["strategies"][name]
            lines.append(
                f"| `{row['id']}` | {desc} | {s['tokens']:,} | {s['ms']} | "
                f"{'Si' if s['hit'] else '**No**'} |"
            )

    lines += [
        "",
        "## Lectura",
        "",
        "- `graphify_check` / `graphify_raw` son las unicas estrategias queRespondieron "
        "una pregunta de proceso (`etapa2`) o la que exige el commit mas reciente (`skills`).",
        "- `naive_graphjson` muestra por que NO se debe leer `.graphify/graph.json` crudo.",
        "",
    ]

    (WORKSPACE / "benchmark_graphify_report.md").write_text("\n".join(lines), encoding="utf-8")
    (WORKSPACE / "benchmark_graphify_results.json").write_text(
        json.dumps(
            {"encoder": ENC_NAME, "questions": results}, indent=2, ensure_ascii=False
        ),
        encoding="utf-8",
    )
    print("Reporte: benchmark_graphify_report.md | Resultados: benchmark_graphify_results.json")


if __name__ == "__main__":
    main()
