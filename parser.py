from __future__ import annotations

import logging
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict

from exceptions import FunctionRedefinitionError, ParserError, ParserValidationError, UnregisteredTokenError
from sub_parsers.footer import FooterParser
from sub_parsers.head import HeadParser
from sub_parsers.main import MainParser
from utils.a import base_template

if TYPE_CHECKING:
    from collections.abc import Generator

    from utils.classes import Parser

logger = logging.getLogger(__name__)


class ASTSection(TypedDict):
    head: list[str]
    body: list[str]
    footer: list[str]


class TokenType(Enum):
    N_FUNC = "N_FUNC"
    OPERATOR = "OPERATOR"
    LITERAL = "LITERAL"


type HTMLContent = str
type FilePath = Path


def validate_ast(ast: ASTSection) -> None:
    required_sections = {"head", "body"}
    missing = required_sections - ast.keys()
    if missing:
        msg = f"Missing required sections: {', '.join(missing)}"
        raise ParserValidationError(msg)

    if not any(ast.values()):
        msg = "Empty AST: no content generated"
        raise ParserValidationError(msg)


def handle_function_parsing(
    parser: Parser, source: Path, parser_class: type[HeadParser | MainParser | FooterParser]
) -> Generator[str]:
    try:
        yield parser_class(parser, source).html()
    except Exception as e:
        logger.exception("Error processing function in %s", source.name)
        msg = f"Error in {source.name}"
        raise ParserError(msg) from e


def generate_html_content(ast: ASTSection, parser: Parser) -> HTMLContent:
    replacements = {
        "lang": parser.language,
        "head": "\n".join(ast["head"]),
        "body": "\n".join(ast["body"]),
        "footer": (f"<footer>\n{'\n'.join(ast['footer'])}\n</footer>" if ast["footer"] else ""),
    }

    try:
        return base_template.safe_substitute(replacements) + "\n<!-- Made with ❤️ using WLang -->"
    except KeyError as e:
        msg = f"Missing placeholder: {e}"
        logger.exception(msg)
        raise ParserValidationError(msg) from e


def parse(parser: Parser, source_file: Path) -> FilePath:
    ast: ASTSection = {"head": [], "body": [], "footer": []}
    declared_functions = set()

    try:
        logger.info("Processing file: %s", source_file.name)

        while token := parser.current_token(source_file):
            if token.type != TokenType.N_FUNC.name:
                msg = f"Unexpected token: {token.value} (type: {token.type})"
                raise UnregisteredTokenError(msg)

            match token.value:
                case "head" | "main" | "footer" as func_name:
                    if func_name in declared_functions:
                        msg = f"Function '{func_name}' already declared"
                        raise FunctionRedefinitionError(msg)
                    declared_functions.add(func_name)

                    parser_map = {
                        "head": (HeadParser, ast["head"]),
                        "main": (MainParser, ast["body"]),
                        "footer": (FooterParser, ast["footer"]),
                    }
                    parser_class, target = parser_map[func_name]
                    target.extend(handle_function_parsing(parser, source_file, parser_class))

                case _:
                    msg = f"Unrecognized function: '{token.value}'"
                    raise UnregisteredTokenError(msg)

        validate_ast(ast)

        output_path = parser.output_dir / f"{source_file.stem}.html"
        output_path.write_text(generate_html_content(ast, parser), encoding="utf-8")
        logger.debug("Generated file: %s", output_path)

    except Exception as e:
        logger.exception("Error processing %s", source_file.name)
        msg = f"Failure in {source_file.name}"
        raise ParserError(msg) from e

    else:
        return output_path
