from __future__ import annotations

import argparse
import logging
import sys
from enum import Enum, IntEnum
from pathlib import Path
from typing import TYPE_CHECKING, Final

from exceptions import CompilationError
from lexer import tokenize
from parser import parse
from utils.a import scan
from utils.classes import Lexer, Parser

if TYPE_CHECKING:
    from collections.abc import Iterable

logger = logging.getLogger(__name__)


class Command(str, Enum):
    COMPILE: Final = "compile"
    VERSION: Final = "version"
    HELP: Final = "help"


class ExitCode(IntEnum):
    SUCCESS = 0
    INPUT_ERROR = 1
    COMPILATION_ERROR = 2
    RUNTIME_ERROR = 3


def setup_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="wlang",
        description="WLang Compiler Toolkit",
        add_help=False,
        epilog="Documentation: https://github.com/Zen-kun04/WLang",
    )

    subparsers = parser.add_subparsers(title="Subcommands", dest="command", required=True, metavar="COMMAND")

    compile_parser = subparsers.add_parser(Command.COMPILE, help="Compile source files to HTML")
    compile_parser.add_argument("sources", nargs="+", type=Path, help="Source files/directories to compile")
    compile_parser.add_argument(
        "-o", "--output", type=Path, default=Path("out"), help="Output directory (default: %(default)s)"
    )
    compile_parser.add_argument(
        "-l", "--language", type=str, default="en", help="HTML lang attribute (default: %(default)s)"
    )

    subparsers.add_parser(Command.VERSION, help="Show version information")
    subparsers.add_parser(Command.HELP, help="Show help message")

    parser.add_argument(
        "-v", "--verbose", action="count", default=0, help="Increase verbosity level (use -v, -vv, -vvv)"
    )

    return parser


def get_version() -> str:
    return "1.0.0"


def handle_compilation(sources: Iterable[Path], output_dir: Path, lang: str) -> None:
    try:
        lexer = Lexer()
        parser = Parser(output_dir=output_dir, language=lang)

        logger.info("Initializing compilation...")
        scan(lexer, sources)

        if not lexer.source_code:
            logger.warning("No valid source files were found")
            return

        for source_path, content in lexer.source_code.items():
            logger.debug("Processing: %s", source_path.name)
            try:
                tokenize(content, source_path, parser)
                parse(parser, source_path)
            except CompilationError:
                logger.exception("Error in %s", source_path.name)
                raise
            except Exception as e:
                logger.exception("Unexpected error processing %s", source_path.name)
                msg = f"Failure in {source_path.name}"
                raise CompilationError(msg) from e

        logger.info("Compilation successful. Output directory: %s", output_dir.resolve())

    except KeyboardInterrupt:
        logger.info("Compilation interrupted by user")
        sys.exit(ExitCode.INPUT_ERROR)


def main() -> ExitCode:
    parser = setup_arg_parser()

    try:
        args = parser.parse_args()

        match args.command:
            case Command.VERSION:
                logger.info("WLang Compiler Toolkit v%s", get_version())
                return ExitCode.SUCCESS

            case Command.HELP:
                parser.print_help()
                return ExitCode.SUCCESS

            case Command.COMPILE:
                output_dir = args.output.resolve()
                output_dir.mkdir(parents=True, exist_ok=True)

                handle_compilation(sources=args.sources, output_dir=output_dir, lang=args.language)
                return ExitCode.SUCCESS

            case _:
                logger.error("Unrecognized command: %s", args.command)
                parser.print_help()
                return ExitCode.INPUT_ERROR

    except CompilationError:
        logger.exception("Compilation error")
        return ExitCode.COMPILATION_ERROR
    except Exception:
        logger.exception("Critical error")
        return ExitCode.RUNTIME_ERROR
    except KeyboardInterrupt:
        logger.info("Operation canceled by the user")
        return ExitCode.INPUT_ERROR


if __name__ == "__main__":
    sys.exit(main())
