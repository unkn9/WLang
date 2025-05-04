import logging
from collections.abc import Iterable
from pathlib import Path
from string import Template

from utils.classes import Lexer

logger = logging.getLogger(__name__)


def scan(lexer: Lexer, sources: Iterable[Path]) -> None:
    for path in sources:
        if path.is_dir():
            for wl_file in path.rglob("*.wl"):
                _add_file_content(lexer, wl_file)
        elif path.suffix == ".wl":
            _add_file_content(lexer, path)


def _add_file_content(lexer: Lexer, file_path: Path) -> None:
    try:
        content = file_path.read_text(encoding="utf-8")
        if content.strip():
            lexer.add_source(file_path.resolve(), content)
    except Exception:
        logger.exception("Error reading %s", file_path.name)


base_template = Template("""<!DOCTYPE html>
<html lang="${lang}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    ${head}
</head>
<body>
    ${body}
</body>
${footer}
</html>""")
