class ParserError(Exception):
    """Base exception for parsing errors."""


class FunctionRedefinitionError(ParserError):
    """Raised when a function is declared multiple times."""


class UnregisteredTokenError(ParserError):
    """Raised when encountering an unrecognized token."""


class ParserValidationError(ParserError):
    """Raised when validation of AST structure fails."""


class CompilationError(Exception):
    """Base exception for compilation errors."""
