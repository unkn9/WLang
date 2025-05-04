from utils.classes import Parser


class UrlParser:
    def __init__(self, parser: Parser, source_file: str):
        self.source_file = source_file
        self.method = parser.consume(source_file, "N_FUNC")
        assert self.method.value == "url"
        parser.consume(source_file, "LPAREN")
        self.url = parser.consume(source_file, "STRING")
        parser.consume(source_file, "COMMA")
        self.text = parser.consume(source_file, "STRING")
        parser.consume(source_file, "RPAREN")
        parser.consume(source_file, "SEMICOLON")

    def html(self):
        return f'<a href="{self.url.value}">{self.text.value}</a>'

    def __repr__(self):
        return f'<a href="{self.url.value}">{self.text.value}</a>'
