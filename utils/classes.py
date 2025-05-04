from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Token:
    type: str
    value: str
    position: tuple[int, int] = field(default=(0, 0))


class Lexer:
    def __init__(self) -> None:
        self.source_code: dict[Path, str] = {}

    def add_source(self, path: Path, content: str) -> None:
        self.source_code[path] = content


class Parser:
    def __init__(self, output_dir: Path = Path("out"), language: str = "en") -> None:
        self.positions: dict[Path, int] = {}
        self.source_tokens: dict[Path, list[Token]] = {}
        self.language: str = language
        self.output_dir: Path = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def peek(self, file: Path) -> Token | None:
        pos = self.positions.get(file, 0)
        tokens = self.source_tokens.get(file, [])
        return tokens[pos + 1] if pos + 1 < len(tokens) else None

    def current_token(self, file: Path) -> Token | None:
        pos = self.positions.get(file, 0)
        tokens = self.source_tokens.get(file, [])
        return tokens[pos] if pos < len(tokens) else None

    def consume(self, file: Path, *expected_types: str) -> Token:
        token = self.current_token(file)
        if not token:
            msg = f"Unexpected end of entry. Expected: {', '.join(expected_types)}"
            raise SyntaxError(msg)
        if token.type not in expected_types:
            msg = f"Token {token.value} (type: {token.type}) does not match expected types: {', '.join(expected_types)}"
            raise SyntaxError(msg)
        self.positions[file] = self.positions.get(file, 0) + 1
        return token
